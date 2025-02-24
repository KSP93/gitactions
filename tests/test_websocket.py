import asyncio
import websockets
import pytest

@pytest.mark.asyncio
async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Test message")
        response = await websocket.recv()
        assert response == "Echo: Test message"
