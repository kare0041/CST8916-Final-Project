import random
import time
import datetime
import json
import os
from azure.iot.device import IoTHubDeviceClient, Message

# Optional: Fix SSL cert verification issue on macOS (uncomment if needed)
# import certifi
# os.environ['SSL_CERT_FILE'] = certifi.where()

# Define device connection strings
CONNECTION_STRINGS = {
    "Dow's Lake": "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_dows_lake;SharedAccessKey=esSycMr9FxqEu5wCCaPLF4AzYlwLg7hyjugpoX9ik6Y=",
    "Fifth Avenue": "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_fifth_avenue;SharedAccessKey=d0WiV18U/x1ow+RX5+4NKP27Yyg+rWuNNmROVTjt3Ik=",
    "NAC": "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_nac;SharedAccessKey=NglXDacC7QckPwefDzvJ5PS6SD3SsIZhy5hQwcRYP1s="
}

# Generate a simulated payload
def generate_payload(location):
    return {
        "location": location,
        "iceThickness": random.randint(20, 40),
        "surfaceTemperature": random.randint(-10, 1),
        "snowAccumulation": random.randint(0, 20),
        "externalTemperature": random.randint(-15, 5),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

def main():
    # Create IoT clients for each device/location
    clients = {location: IoTHubDeviceClient.create_from_connection_string(conn_str)
               for location, conn_str in CONNECTION_STRINGS.items()}

    print("Starting IoT sensor simulation... Press Ctrl+C to stop.")

    try:
        while True:
            for location, client in clients.items():
                try:
                    data = generate_payload(location)
                    message = Message(json.dumps(data))
                    client.send_message(message)
                    print(f"Sent from {location}: {data}")
                except Exception as e:
                    print(f"Error sending from {location}: {e}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        print("Shutting down clients...")
        for client in clients.values():
            client.shutdown()
        print("All clients disconnected. Goodbye!")

if __name__ == "__main__":
    main()
