import requests

def test_summarize_text_endpoint():
    url = "http://127.0.0.1:8000/summarize-text"
    payload = {
        "text": "LangChain is a framework designed to simplify the creation of applications powered by language models. It provides tools and integrations to build advanced AI-driven software."
    }

    response = requests.post(url, json=payload)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200
    assert "summary" in response.json()

if __name__ == "__main__":
    test_summarize_text_endpoint()
