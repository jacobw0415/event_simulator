import random
import datetime

# === 設備對應表（根據亞灣架構） ===
GATEWAYS = [
    ("HKP01", "HighPole-01"),
    ("HKP02", "HighPole-02"),
    ("HKP03", "HighPole-03"),
    ("ST701", "Gate-70-1"),
    ("ST702", "Gate-70-2"),
    ("YMCORE", "YM-ServerRoom"),
]

DEVICES = [
    ("IW9167E", "WirelessBridge"),
    ("IE3300", "IndustrialSwitch"),
    ("IE3400", "EdgeSwitch"),
    ("IE9320", "AggregationSwitch"),
    ("C9300X", "CoreSwitch"),
    ("C9800", "WirelessController"),
    ("IC3000", "IoTGateway"),
]

SEVERITIES = ["Information", "Warning", "Error", "Emergency"]

EVENT_TEMPLATES = {
    "WirelessBridge": "Wireless link fluctuation detected on {deviceName}",
    "IndustrialSwitch": "Port utilization high on {deviceName}",
    "EdgeSwitch": "Access switch temperature warning at {gatewayName}",
    "AggregationSwitch": "Fiber uplink unstable at {gatewayName}",
    "CoreSwitch": "High CPU usage detected on {deviceName}",
    "WirelessController": "AP disconnection event on {deviceName}",
    "IoTGateway": "IoT data processing delay at {gatewayName}"
}


def generate_event(category="ESG"):
    # 隨機選擇網關與設備
    gateway_id, gateway_name = random.choice(GATEWAYS)
    device_name, device_type = random.choice(DEVICES)
    severity = random.choice(SEVERITIES)

    # 模擬事件訊息
    message = EVENT_TEMPLATES.get(device_type, "Generic device event").format(
        deviceName=device_name, gatewayName=gateway_name
    )

    event = {
        "category": category,
        "type": device_type,
        "metadata": {
            "deviceName": device_name,
            "deviceAddress": f"10.0.{random.randint(1, 14)}.{random.randint(2, 254)}",
            "gatewayId": gateway_id,
            "gatewayName": gateway_name,
            "subject": f"{device_type} Status Report",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        },
        "severity": severity,
        "subject": f"{device_type} Alert",
        "message": message,
        "status": "Unprocessed"
    }
    return event
