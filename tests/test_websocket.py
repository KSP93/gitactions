import asyncio
import websockets
import pytest

@pytest.mark.asyncio
async def test_websocket():
    """Test WebSocket connection and message transmission."""
    uri = "ws://localhost:8080/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            message = "Test message"
            await websocket.send(message)
            response = await websocket.recv()
            assert response == f"Echo: {message}"
    except Exception as e:
        pytest.fail(f"WebSocket connection failed: {e}")
