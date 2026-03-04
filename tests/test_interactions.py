import json
from nacl.signing import SigningKey
from fastapi.testclient import TestClient
from src.main import app
from src.core.config import settings

client = TestClient(app)

def test_interactions_ping_pong_success(monkeypatch):
    # Setup: Create a test signing key and public key
    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode().hex()
    
    # Mock settings.DISCORD_PUBLIC_KEY
    monkeypatch.setattr(settings, "DISCORD_PUBLIC_KEY", public_key)
    
    # Interaction payload (PING)
    payload = {"type": 1}
    body = json.dumps(payload).encode()
    timestamp = "1234567890"
    
    # Generate signature
    message = timestamp.encode() + body
    signature = signing_key.sign(message).signature.hex()
    
    # Execute request
    response = client.post(
        "/interactions",
        content=body,
        headers={
            "X-Signature-Ed25519": signature,
            "X-Signature-Timestamp": timestamp,
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {"type": 1}

def test_interactions_slash_command_ping_success(monkeypatch):
    # Setup: Create a test signing key and public key
    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode().hex()
    
    # Mock settings.DISCORD_PUBLIC_KEY
    monkeypatch.setattr(settings, "DISCORD_PUBLIC_KEY", public_key)
    
    # Interaction payload (APPLICATION_COMMAND: ping)
    payload = {
        "type": 2,
        "data": {
            "name": "ping",
            "type": 1
        }
    }
    body = json.dumps(payload).encode()
    timestamp = "1234567890"
    
    # Generate signature
    message = timestamp.encode() + body
    signature = signing_key.sign(message).signature.hex()
    
    # Execute request
    response = client.post(
        "/interactions",
        content=body,
        headers={
            "X-Signature-Ed25519": signature,
            "X-Signature-Timestamp": timestamp,
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "type": 4,
        "data": {"content": "Pong!"}
    }

def test_interactions_invalid_signature():
    response = client.post(
        "/interactions",
        json={"type": 1},
        headers={
            "X-Signature-Ed25519": "invalid_signature",
            "X-Signature-Timestamp": "1234567890",
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid request signature"}
