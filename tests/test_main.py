from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_order():
    response = client.post(
        "/orders?symbol=AAPL&price=150.0&quantity=10&order_type=buy"
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.0
    assert data["quantity"] == 10
    assert data["order_type"] == "buy"

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)