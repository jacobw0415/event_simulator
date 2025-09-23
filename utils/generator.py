import random
import datetime

DEVICES = [
    ("TempSensor01", "Temperature"),
    ("CO2Sensor03", "CO2"),
    ("SmokeDetector02", "Smoke"),
    ("WaterLevel04", "WaterLevel"),
    ("HumiditySensor05", "Humidity"),
    ("VibrationSensor06", "Vibration"),
    ("PowerMeter07", "Power"),
    ("GasDetector08", "GasLeak"),
]

GATEWAYS = [
    ("GW1", "Gateway-1"),
    ("GW2", "Gateway-2"),
    ("GW3", "Gateway-3"),
]

SEVERITIES = ["Information", "Warning", "Error", "Emergency"]

LOCATIONS = [
    "Warehouse-A",
    "Dock-3",
    "Control-Room",
    "Pump-Station",
    "Office-Building",
    "Generator-Room",
]


def generate_event(category="GSS"):
    device_name, device_type = random.choice(DEVICES)
    gateway_id, gateway_name = random.choice(GATEWAYS)
    severity = random.choice(SEVERITIES)
    location = random.choice(LOCATIONS)

    # 產生隨機數值
    if device_type == "Temperature":
        value = round(random.uniform(20, 90), 1)  # 攝氏度
        unit = "°C"
        message = f"Temperature reading {value}{unit} at {location}"
    elif device_type == "CO2":
        value = random.randint(300, 2000)  # ppm
        unit = "ppm"
        message = f"CO2 level {value}{unit} detected at {location}"
    elif device_type == "Smoke":
        value = random.randint(0, 10)  # 煙霧強度等級
        unit = "scale"
        message = f"Smoke intensity {value} detected at {location}"
    elif device_type == "WaterLevel":
        value = round(random.uniform(0.1, 5.0), 2)  # 公尺
        unit = "m"
        message = f"Water level {value}{unit} detected at {location}"
    else:
        value = None
        unit = ""
        message = f"{device_type} event detected at {location}"

    event = {
        "category": category,
        "type": device_type,
        "metadata": {
            "deviceName": device_name,
            "deviceAddress": f"192.168.0.{random.randint(2, 254)}",
            "gatewayId": gateway_id,
            "gatewayName": gateway_name,
            "subject": "AutoTest",
            "location": location,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "value": value,
            "unit": unit
        },
        "severity": severity,
        "subject": f"{device_type} Alert",
        "message": message,
        "status": "Unprocessed"
    }
    return event
