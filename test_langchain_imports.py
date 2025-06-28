from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_summarize_text_endpoint():
    # Petición JSON actualizada
    payload = {
        "text": "LangChain is a framework that simplifies the creation of LLM-powered applications in a modular and flexible way."
    }

    response = client.post("/summarize-text", json=payload)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert len(data["summary"]) > 0

if __name__ == "__main__":
    test_summarize_text_endpoint()
