from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_valid_order():
    """Test creating a valid order using query parameters."""
    response = client.post("/orders", params={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })

    assert response.status_code == 200, f"Expected 200, got {response.status_code} with response {response.json()}"
    response_data = response.json()
    
    assert "id" in response_data
    assert response_data["symbol"] == "AAPL"
    assert response_data["price"] == 150.0
    assert response_data["quantity"] == 10
    assert response_data["order_type"] == "buy"

def test_create_order_invalid_symbol():
    """Test creating an order with an invalid symbol (numeric instead of uppercase letters)."""
    response = client.post("/orders", params={
        "symbol": "1234",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422, f"Expected 422, got {response.status_code} with response {response.json()}"

def test_create_order_negative_price():
    """Test creating an order with a negative price."""
    response = client.post("/orders", params={
        "symbol": "AAPL",
        "price": -10.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422, f"Expected 422, got {response.status_code} with response {response.json()}"

def test_create_order_invalid_order_type():
    """Test creating an order with an invalid order type."""
    response = client.post("/orders", params={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "hold"  # Invalid order type
    })
    assert response.status_code == 422, f"Expected 422, got {response.status_code} with response {response.json()}"

def test_create_order_missing_parameters():
    """Test creating an order with missing required parameters."""
    response = client.post("/orders", params={
        "symbol": "AAPL",
        "price": 150.0  # Missing 'quantity' and 'order_type'
    })
    assert response.status_code == 422, f"Expected 422, got {response.status_code} with response {response.json()}"

def test_get_orders():
    """Test retrieving the list of submitted orders."""
    response = client.get("/Submitted_Orders")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert isinstance(response.json(), list), "Expected a list of orders"
