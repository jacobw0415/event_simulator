import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

XAUTH_URL = "https://api.accelera-vs.com:8088/xauth"
EVENTS_URL = "https://api.accelera-vs.com:8088/events"

USERNAME = "admin"
PASSWORD = "admin"
GRANT_TYPE = "Password"

def get_token():
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "grantType": GRANT_TYPE
    }
    res = requests.post(XAUTH_URL, json=payload, verify=False, timeout=5)
    print("🔎 /xauth status:", res.status_code)
    print("🔎 /xauth response:", res.text)

    if res.status_code == 200:
        data = res.json()
        # 嘗試抓出可能的欄位
        for key in ["token", "access_token", "jwt", "id_token"]:
            if key in data:
                return data[key]
    return None

def test_event(token):
    headers_list = [
        ("X-Auth-Token", {"X-Auth-Token": token, "Content-Type": "application/json"}),
        ("Authorization: Bearer", {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}),
        ("Authorization (raw)", {"Authorization": token, "Content-Type": "application/json"}),
    ]

    sample_event = {
        "category": "gss",
        "type": "Device",
        "metadata": {
            "deviceName": "TestDevice",
            "deviceAddress": "192.168.0.99",
            "gatewayId": "GW-Test",
            "gatewayName": "TestGateway",
            "subject": "AutoTest"
        },
        "severity": "Warning",
        "subject": "Test Event",
        "message": "This is a test event",
        "status": "Unprocessed"
    }

    for label, headers in headers_list:
        print(f"\n===== 測試 {label} =====")
        try:
            res = requests.post(EVENTS_URL, json=sample_event, headers=headers, verify=False, timeout=5)
            print("Status:", res.status_code)
            print("Response:", res.text)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    token = get_token()
    if token:
        print("✅ 拿到 token:", token[:10] + "...")
        test_event(token)
    else:
        print("❌ 沒有拿到 token")
