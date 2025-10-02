def test_login():
    url = f"{BASE_URL}/login"
    payload = {
        "email": "tester@test.com",
        "password": "1234"
    }
    response = requests.post(url, json=payload)

    # Imprimimos la respuesta tal cual venga
    print("📌 Login status:", response.status_code)
    print("📌 Login raw text:", response.text)  # 👈 aquí veremos si es HTML, JSON o vacío

    try:
        print("📌 Login JSON:", response.json())
    except Exception as e:
        print("❌ Error parseando JSON:", e)
