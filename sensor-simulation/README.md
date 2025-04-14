# Sensor Simulation for Rideau Canal Skateway Monitoring

This directory contains the Python script used to simulate IoT sensors for the Rideau Canal Skateway monitoring system. The script generates synthetic sensor data for three key locations along the canal and sends this data to Azure IoT Hub.

## Overview

The `simulate_sensors.py` script simulates the behavior of IoT sensors deployed at Dow's Lake, Fifth Avenue, and NAC on the Rideau Canal Skateway. It generates data points for ice thickness, surface temperature, snow accumulation, and external temperature at a regular interval (every 10 seconds) and transmits this data as JSON payloads to Azure IoT Hub.

## Files

-   `simulate_sensors.py`: The Python script responsible for simulating sensor data and sending it to Azure IoT Hub.
-   `README.md`: This file, providing information about the sensor simulation script.

## Prerequisites

Before running the script, ensure you have the following:

1.  **Python 3.x** installed on your system.
2.  **Azure IoT Hub Device SDK for Python** installed. You can install it using pip:

    ```bash
    pip install azure-iot-device
    ```

3.  **Azure IoT Hub:**
    * You need an Azure IoT Hub instance.
    * You need to create three device identities within your IoT Hub: `sensor_dows_lake`, `sensor_fifth_avenue`, and `sensor_nac`.
    * You need the **device connection strings** for each of these devices.

## Configuration

1.  **Download the Script:** Download the `simulate_sensors.py` file to your local machine.
2.  **Update Connection Strings:** Open the `simulate_sensors.py` file in a text editor. Locate the `CONNECTION_STRINGS` dictionary:

    ```python
    CONNECTION_STRINGS = {
        "Dow's Lake": "YOUR_DOWS_LAKE_DEVICE_CONNECTION_STRING",
        "Fifth Avenue": "YOUR_FIFTH_AVENUE_DEVICE_CONNECTION_STRING",
        "NAC": "YOUR_NAC_DEVICE_CONNECTION_STRING"
    }
    ```

    Replace `"YOUR_DOWS_LAKE_DEVICE_CONNECTION_STRING"`, `"YOUR_FIFTH_AVENUE_DEVICE_CONNECTION_STRING"`, and `"YOUR_NAC_DEVICE_CONNECTION_STRING"` with the actual device connection strings for the corresponding devices you created in your Azure IoT Hub.  **Important:** Ensure the device names in the dictionary match the Device IDs in your IoT Hub.

## Running the Script

1.  **Open a Terminal or Command Prompt:** Navigate to the directory where you saved the `simulate_sensors.py` file.
2.  **Execute the Script:** Run the script using the Python interpreter:

    ```bash
    python simulate_sensors.py
    ```

3.  **Observe Output:** The script will start generating and sending sensor data to Azure IoT Hub every 10 seconds. You should see output in the console indicating which location's data is being sent, along with the data payload.  Any errors during sending will also be printed to the console.

## Script Details

The `simulate_sensors.py` script performs the following actions:

1.  **Imports Libraries:** Imports necessary Python libraries: `random` for generating random data, `time` for controlling the sending interval, `datetime` for handling timestamps, `json` for formatting data, `os`, and `azure.iot.device`.
2.  **Defines Connection Strings:** Stores the device connection strings for each simulated sensor in the `CONNECTION_STRINGS` dictionary.  The keys of the dictionary (`"Dow's Lake"`, `"Fifth Avenue"`, `"NAC"`) correspond to the sensor locations and should match the Device IDs in Azure IoT Hub.
3.  **`generate_payload(location)` Function:**
    * Takes the `location` (string) as input.
    * Generates random values within a reasonable range for:
        * `iceThickness`: (20 to 40 cm)
        * `surfaceTemperature`: (-10 to 1 °C)
        * `snowAccumulation`: (0 to 20 cm)
        * `externalTemperature`: (-15 to 5 °C)
    * Gets the current timestamp in UTC format using `datetime.datetime.now(datetime.timezone.utc).isoformat()`.
    * Constructs a JSON payload containing the location, sensor data, and timestamp.
    * Returns the JSON payload as a Python dictionary.
4.  **`main()` Function:**
    * Creates an `IoTHubDeviceClient` for each device/location using the connection strings from the `CONNECTION_STRINGS` dictionary.  These clients are stored in the `clients` dictionary.
    * Enters a `try...except...finally` block to handle the main loop and ensure proper shutdown of the IoT Hub clients.
    * Enters an infinite loop (`while True`):
        * Iterates through each location and its corresponding client in the `clients` dictionary.
        * Calls `generate_payload(location)` to get the sensor data.
        * Creates an `azure.iot.device.Message` object from the JSON data (converted to a string).
        * Sends the message to Azure IoT Hub using `client.send_message(message)`.
        * Prints a success message to the console, including the location and the data sent.
        * Includes error handling within the loop: if sending a message fails, it catches the exception, prints an error message with the location and the error details, and continues to the next location.
        * Pauses for 10 seconds using `time.sleep(10)` before sending the next set of messages.
    * Handles `KeyboardInterrupt`: If the user presses Ctrl+C, the loop breaks, and the `except` block is executed.
    * In the `finally` block:
        * Iterates through the `clients` dictionary and calls `client.shutdown()` for each client to gracefully disconnect from Azure IoT Hub.
        * Prints a message indicating that the clients have been shut down.
5.  **Entry Point:** The `if __name__ == "__main__":` block ensures that the `main()` function is called when the script is executed.

## Important Notes

-   Ensure that the device IDs in your Azure IoT Hub match the keys used in the `CONNECTION_STRINGS` dictionary in the script (e.g., `"Dow's Lake"`, `"Fifth Avenue"`, `"NAC"`).
-   The random data generation is for simulation purposes. In a real-world scenario, this data would come from actual IoT sensors.
-   Keep the script running to continuously feed data to your Azure IoT Hub for the Stream Analytics job to process. You can stop the script by pressing `Ctrl + C` in the terminal.
-   The script includes basic error handling for sending messages to IoT Hub.  If an error occurs, it will print a message to the console but continue to try sending data from other simulated sensors.
