import requests
import time

# URL base
BASE_URL = "http://IP_DE_TU_VM:8080/api/data/"

# Credenciales inválidas
INVALID_HEADERS = {
    "X-Username": "fake_user",
    "X-API-Key": "fake_key"
}

# Credenciales válidas
VALID_HEADERS = {
    "X-Username": "valid_user",
    "X-API-Key": "valid_api_key"
}

def test_invalid_credentials():
    print("Probando con credenciales inválidas...")
    try:
        r = requests.put(BASE_URL, headers=INVALID_HEADERS, json={"data": "test"})
        print(f"Respuesta: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_ip_blocked():
    print("\nVerificando si la IP está bloqueada...")
    try:
        r = requests.get(BASE_URL, headers=VALID_HEADERS)
        print(f"Respuesta: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_invalid_credentials()
    
    time.sleep(2)
    
    test_ip_blocked()