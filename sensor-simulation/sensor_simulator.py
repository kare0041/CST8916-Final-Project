import random
import time
import datetime
import json
import os
from azure.iot.device import IoTHubDeviceClient, Message

# Optional: Fix SSL certificate verification issues on macOS
# Uncomment the following lines if running into SSL issues on macOS
# import certifi
# os.environ['SSL_CERT_FILE'] = certifi.where()

# Dictionary containing connection strings for each simulated IoT device
CONNECTION_STRINGS = {
    "Dow's Lake": "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_dows_lake;SharedAccessKey=esSycMr9FxqEu5wCCaPLF4AzYlwLg7hyjugpoX9ik6Y=",
    "Fifth Avenue": "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_fifth_avenue;SharedAccessKey=d0WiV18U/x1ow+RX5+4NKP27Yyg+rWuNNmROVTjt3Ik=",
    "NAC": "HostName=danieliotcst8916.azure-devices.net;DeviceId=sensor_nac;SharedAccessKey=NglXDacC7QckPwefDzvJ5PS6SD3SsIZhy5hQwcRYP1s="
}

# Function to simulate a sensor payload with random environmental data
def generate_payload(location):
    return {
        "location": location,
        "iceThickness": random.randint(20, 40),             # Ice thickness in cm
        "surfaceTemperature": random.randint(-10, 1),       # Surface temperature in Celsius
        "snowAccumulation": random.randint(0, 20),          # Snow depth in cm
        "externalTemperature": random.randint(-15, 5),      # Ambient air temperature in Celsius
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()  # Current UTC time in ISO 8601 format
    }

def main():
    # Initialize IoT Hub clients for each sensor/location
    clients = {
        location: IoTHubDeviceClient.create_from_connection_string(conn_str)
        for location, conn_str in CONNECTION_STRINGS.items()
    }

    print("Starting IoT sensor simulation... Press Ctrl+C to stop.")

    try:
        while True:
            for location, client in clients.items():
                try:
                    # Generate and send a sensor reading
                    data = generate_payload(location)
                    message = Message(json.dumps(data))  # Convert dict to JSON message
                    client.send_message(message)
                    print(f"Sent from {location}: {data}")
                except Exception as e:
                    print(f"Error sending from {location}: {e}")
            time.sleep(10)  # Wait 10 seconds before sending the next batch
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        # Cleanly shut down all clients
        print("Shutting down clients...")
        for client in clients.values():
            client.shutdown()
        print("All clients disconnected. Goodbye!")

# Entry point for script execution
if __name__ == "__main__":
    main()
