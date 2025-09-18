import random

devices = ["TempSensor01", "SmokeDetector02", "CO2Sensor03", "WaterLevel04"]
severities = ["Information", "Warning", "Error", "Emergency"]

def generate_event(category="ESG"):
    return {
        "category": category,
        "type": "Device",
        "metadata": {
            "deviceName": random.choice(devices),
            "deviceAddress": f"192.168.0.{random.randint(10,250)}",
            "gatewayId": f"GW{random.randint(1,5)}",
            "gatewayName": "Gateway-" + str(random.randint(1,3)),
            "subject": "AutoTest"
        },
        "severity": random.choice(severities),
        "subject": "Test Event",
        "message": "This is a simulated event",
        "status": "Unprocessed"
    }
