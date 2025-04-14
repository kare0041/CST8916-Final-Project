import random, time, datetime, json
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_fifth_avenue;SharedAccessKey=d0WiV18U/x1ow+RX5+4NKP27Yyg+rWuNNmROVTjt3Ik="

location = "Fifth Avenue"

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
    client =  IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    
    try:
        while True:
            data = generate_payload(location)
            message = Message(json.dumps(data))
            print(f"Sending: {data}")
            client.send_message(message)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.shutdown()
        print("Client shutdown.")

if __name__ == "__main__":
    main()