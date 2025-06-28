# test_write_poem.py
import requests

def test_write_poem():
    todo_id = 13  # Usa el ID correcto
    url = f"http://127.0.0.1:8000/write-poem/{todo_id}"

    response = requests.post(url)

    print("STATUS:", response.status_code)

    try:
        json_response = response.json()
        print("RESPONSE:", json_response)
        assert response.status_code == 200
        assert 'poem' in json_response
        print("✅ Test passed")
    except Exception as e:
        print("❌ Error ejecutando el test:", e)

if __name__ == "__main__":
    test_write_poem()
