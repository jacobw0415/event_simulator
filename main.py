import time
import requests
import urllib3
import signal
import sys
import os
import logging
import threading
from logging.handlers import RotatingFileHandler
from requests.adapters import HTTPAdapter, Retry

from config import API_URL, XAUTH_URL, USERNAME, PASSWORD, GRANT_TYPE, INTERVAL, CATEGORY
from utils.generator import generate_event

# === SSL 驗證控制 (環境變數) ===
SSL_VERIFY = os.getenv("SSL_VERIFY", "False").lower() == "true"
if not SSL_VERIFY:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === Debug 模式控制 ===
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# === Logging 設定 ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "event_simulator.log")

logger = logging.getLogger("event_simulator")
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

# 避免重複加入 handler
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# === HTTP Session with Retry ===
session = requests.Session()
retries = Retry(
    total=3, backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["POST"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# === Global Stop Event ===
stop_event = threading.Event()


# === Step 1. 取得 X-Token ===
def get_token():
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "grantType": GRANT_TYPE
    }
    try:
        res = session.post(XAUTH_URL, json=payload, verify=SSL_VERIFY, timeout=5)
        if res.status_code == 200:
            data = res.json()
            token = data.get("token")
            if token:
                logger.info(f"✅ Got X-Token: {token[:10]}...")
                return token
            else:
                logger.error(f"❌ Token not found in response: {res.text}")
        else:
            logger.error(f"❌ Failed to get token: {res.status_code} {res.text}")
    except Exception:
        logger.exception("❌ Token request failed")
    return None


# === Step 2. 發送事件 ===
def send_event(event, token):
    headers = {
        "X-Token": token,
        "Content-Type": "application/json"
    }

    if DEBUG:
        safe_token = token[:10] + "..." if token else "(none)"
        logger.debug(f"🔎 Debug -> URL: {API_URL}")
        logger.debug(f"🔎 Debug -> Headers: {{'X-Token': '{safe_token}'}}")

    try:
        res = session.post(API_URL, json=event, headers=headers, verify=SSL_VERIFY, timeout=5)
        return res
    except requests.RequestException:
        logger.exception("❌ Network error while sending event")
        return None


# === Step 3. Graceful Shutdown Handler ===
def shutdown_handler(sig, frame):
    logger.info("🛑 Graceful Shutdown: Stopping event simulator...")
    stop_event.set()


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# === Main Loop ===
if __name__ == "__main__":
    token = get_token()
    if not token:
        logger.error("❌ No token, exiting.")
        sys.exit(1)

    logger.info(f"🚀 Event simulator started, sending to {API_URL} every {INTERVAL}s (SSL_VERIFY={SSL_VERIFY})")

    while not stop_event.is_set():
        event = generate_event(CATEGORY)
        try:
            res = send_event(event, token)
            if res is None:
                logger.error("❌ No response from server.")
            elif res.status_code == 401:
                logger.warning("⚠️ Token expired or invalid, refreshing...")
                token = get_token()
                if not token:
                    logger.error("❌ Failed to refresh token, exiting.")
                    break
                else:
                    res = send_event(event, token)

            if res is not None:
                logger.info(f"[OK] {event['metadata']['deviceName']} | {event['severity']} | Status {res.status_code}")
                if res.status_code >= 400:
                    logger.error(f"Response: {res.text}")

        except Exception:
            logger.exception("❌ Failed to send event")

        # 可中斷的 sleep
        stop_event.wait(INTERVAL)

    logger.info("✅ Event simulator stopped cleanly.")
