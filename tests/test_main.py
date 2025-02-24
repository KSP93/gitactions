from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_valid_order():
    """Test creating a valid order."""
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.0
    assert data["quantity"] == 10
    assert data["order_type"] == "buy"

def test_create_order_invalid_symbol():
    """Test creating an order with an invalid symbol."""
    response = client.post("/orders", json={
        "symbol": "123",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422

def test_create_order_negative_price():
    """Test creating an order with a negative price."""
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": -10.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422

def test_create_order_invalid_order_type():
    """Test creating an order with an invalid order type."""
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "hold"  # Invalid type
    })
    assert response.status_code == 422

def test_get_orders():
    """Test retrieving the list of submitted orders."""
    response = client.get("/Submitted_Orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
