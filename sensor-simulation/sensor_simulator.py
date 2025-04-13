import random, time, datetime, json
# from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRINGS = ["Your IoT Device Connection String", "Your IoT Device Connection String","Your IoT Device Connection String"]

LOCATIONS = ["Dow's Lake", "Fifth Avenue", "NAC"]

def generate_payload(location):
    return {
        "location": location,
        "iceThickness": random.randint(20, 40),
        "surfaceTemperature": random.randint(-10, 1),
        "snowAccumulation": random.randint(0, 20),
        "externalTemperature": random.randint(-15, 5),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
def main():
    # clients = {
    #     "Dow's Lake": IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRINGS[0]),
    #     "Fifth Avenue": IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRINGS[1]),
    #     "NAC": IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRINGS[2])
    # }
    try:
        while True:
            for location in LOCATIONS:
                data = generate_payload(location)
                # message = Message(json.dumps(data))
                print(f"Sending: {data}")
                # clients[location].send_message(message)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        # client.shutdown()
        print("Client shutdown.")

if __name__ == "__main__":
    main()
