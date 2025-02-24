
import uuid
import psycopg2
from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketDisconnect, Query
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Trade Orders API",
    description="API for submitting and listing trade orders using PostgreSQL for data storage."
)

class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

clients: List[WebSocket] = []

async def broadcast_message(message: str):
    for client in clients.copy():
        try:
            await client.send_text(message)
        except Exception:
            clients.remove(client)

def get_connection():
    return psycopg2.connect(
        host="3.94.10.52",
        database="Orders",
        user="postgres",
        password="Blockhouse",
        port=5432
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            symbol TEXT,
            price REAL,
            quantity INTEGER,
            order_type TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

@app.post("/orders", summary="Submit a new trade order")
def create_order(
    symbol: str = Query(..., description="Order symbol"),
    price: float = Query(..., description="Order price"),
    quantity: int = Query(..., description="Order quantity"),
    order_type: str = Query(..., description="Order type"), 
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    order = Order(symbol=symbol, price=price, quantity=quantity, order_type=order_type)
    order_id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (id, symbol, price, quantity, order_type)
        VALUES (%s, %s, %s, %s, %s)
    """, (order_id, order.symbol, order.price, order.quantity, order.order_type))
    conn.commit()
    cursor.close()
    conn.close()
    background_tasks.add_task(
        broadcast_message, f"New order created: {order_id} for {order.symbol}"
    )
    return {"id": order_id, **order.dict()}

@app.get("/Submitted_Orders", summary="List all submitted orders", response_model=List[dict])
def list_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symbol, price, quantity, order_type FROM orders")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    orders = [
        {"id": row[0], "symbol": row[1], "price": row[2], "quantity": row[3], "order_type": row[4]}
        for row in rows
    ]
    return orders


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)