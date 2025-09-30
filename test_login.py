import requests

BASE_URL = "http://127.0.0.1:5000/api"

def test_login():
    url = f"{BASE_URL}/login"
    payload = {
        "email": "tester@test.com",
        "password": "1234"
    }
    response = requests.post(url, json=payload)
    print("📌 Login status:", response.status_code)
    print("📌 Login raw text:", response.text)  # 👈 Para ver la respuesta real
    try:
        print("📌 Login JSON:", response.json())
    except Exception as e:
        print("❌ Error parseando JSON:", e)
