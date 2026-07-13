import sys
import os

# adiciona a pasta raiz (D:\MOD32) ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello_world():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"Hello": " World!"}