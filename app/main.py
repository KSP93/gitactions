
import uuid
import psycopg2
from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketDisconnect, Query , HTTPException
from pydantic import BaseModel, Field, constr, confloat, conint, ValidationError
from typing import List

app = FastAPI(
    title="Trade Orders API",
    description="API for submitting and listing trade orders using PostgreSQL for data storage."
)
# Order schema
from pydantic import BaseModel, Field

class Order(BaseModel):
    symbol: constr(min_length=1, max_length=10, pattern="^[A-Z]+$") = Field(..., description="Stock symbol (e.g., AAPL)")
    price: confloat(gt=0) = Field(..., description="Price must be greater than zero")
    quantity: conint(gt=0) = Field(..., description="Quantity must be greater than zero")
    order_type: constr(pattern="^(buy|sell)$") = Field(..., description="Order type must be 'buy' or 'sell'")

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
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    price: float = Query(..., gt=0, description="Price must be greater than 0"),
    quantity: int = Query(..., gt=0, description="Quantity must be greater than 0"),
    order_type: str = Query(..., pattern="^(buy|sell)$", description="Order type must be 'buy' or 'sell'"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Creates a trade order using query parameters instead of JSON."""
    try:
        # Validate input with Pydantic
        validated_order = Order(symbol=symbol, price=price, quantity=quantity, order_type=order_type)

        order_id = str(uuid.uuid4())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (id, symbol, price, quantity, order_type)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, validated_order.symbol, validated_order.price, validated_order.quantity, validated_order.order_type))
        conn.commit()
        cursor.close()
        conn.close()

        # Notify clients via WebSocket
        background_tasks.add_task(
            broadcast_message, f"New order created: {order_id} for {validated_order.symbol}"
        )

        return {
            "id": order_id,
            "symbol": validated_order.symbol,
            "price": validated_order.price,
            "quantity": validated_order.quantity,
            "order_type": validated_order.order_type
        }

    except ValidationError as e:
        # Explicitly return 422 if validation fails
        raise HTTPException(status_code=422, detail=e.errors())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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
