import time
import requests
import urllib3
import signal
import sys
from config import API_URL, XAUTH_URL, USERNAME, PASSWORD, GRANT_TYPE, INTERVAL, CATEGORY
from utils.generator import generate_event

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DEBUG = True  

# === Global Flag ===
running = True

# === Step 1. 取得 X-Token ===
def get_token():
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "grantType": GRANT_TYPE
    }
    try:
        res = requests.post(XAUTH_URL, json=payload, verify=False, timeout=5)
        if res.status_code == 200:
            data = res.json()
            token = data.get("token")
            if token:
                print("✅ Got X-Token:", token[:10] + "...")
                return token
            else:
                print("❌ Token not found in response:", res.text)
        else:
            print("❌ Failed to get token:", res.status_code, res.text)
    except Exception as e:
        print("[ERROR] Token request failed:", e)
    return None

# === Step 2. 發送事件 ===
def send_event(event, token):
    headers = {
        "X-Token": token,
        "Content-Type": "application/json"
    }

    if DEBUG:
        safe_token = token[:10] + "..." if token else "(none)"
        print(f"🔎 Debug -> URL: {API_URL}")
        print(f"🔎 Debug -> Headers: {{'X-Token': '{safe_token}'}}")

    res = requests.post(
        API_URL,
        json=event,
        headers=headers,
        verify=False,
        timeout=5
    )
    return res

# === Step 3. Graceful Shutdown Handler ===
def shutdown_handler(sig, frame):
    global running
    print("\n🛑 Graceful Shutdown: Stopping event simulator...")
    running = False

# 綁定 SIGINT (Ctrl+C) 和 SIGTERM
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# === Main Loop ===
if __name__ == "__main__":
    token = get_token()
    if not token:
        print("❌ No token, exiting.")
        sys.exit(1)

    print(f"🚀 Event simulator started, sending to {API_URL} every {INTERVAL}s")

    while running:
        event = generate_event(CATEGORY)
        try:
            res = send_event(event, token)
            if res.status_code == 401:
                print("⚠️  Token expired or invalid, refreshing...")
                token = get_token()
                if not token:
                    print("❌ Failed to refresh token, exiting.")
                    break
                else:
                    res = send_event(event, token)

            print(f"[OK] {event['metadata']['deviceName']} | {event['severity']} | Status {res.status_code}")
            if res.status_code >= 400:
                print("Response:", res.text)

        except Exception as e:
            print("[ERROR] Failed to send event:", e)

        # loop 間隔
        time.sleep(INTERVAL)

    print("✅ Event simulator stopped cleanly.")
