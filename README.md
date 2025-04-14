# Real-time Monitoring System for Rideau Canal Skateway

## Scenario Description

The Rideau Canal Skateway, a historic and world-renowned attraction in Ottawa, requires constant monitoring to ensure skater safety. This project implements a real-time data streaming system that simulates three IoT sensors to monitor ice conditions and weather factors along the canal, processes the incoming sensor data to detect unsafe conditions in real-time, and stores the results in Azure Blob Storage for further analysis.

## System Architecture

The system architecture is illustrated below:

![System Architecture](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-14%20at%2016.55.05.png)
1.  **Simulated IoT Sensors:** Python scripts simulate sensors at three locations (Dow's Lake, Fifth Avenue, NAC), generating ice conditions and weather data.
2.  **Azure IoT Hub:** Ingests the simulated sensor data.
3.  **Azure Stream Analytics:** Processes the data in real-time, aggregating it over 5-minute windows to calculate average ice thickness and maximum snow accumulation.
4.  **Azure Blob Storage:** Stores the processed data for further analysis and historical records.

## Implementation Details

### IoT Sensor Simulation

The `sensor-simulation/sensor_simulator.py` script simulates IoT sensors at three key locations on the Rideau Canal.

#### Script Details

-   **Locations:** Dow's Lake, Fifth Avenue, NAC
-   **Data Generated (every 10 seconds):**
    -   Ice Thickness (cm)
    -   Surface Temperature (°C)
    -   Snow Accumulation (cm)
    -   External Temperature (°C)
    -   Timestamp (ISO 8601 format)
-   **Technology:** Python 3.x
-    The script uses the Azure IoT Hub Device SDK to send data to Azure IoT Hub.

#### JSON Payload Example:

```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2024-11-23T12:00:00Z"
}
```
Code: The IoT Sensor Simulator is available at (sensor-simulation/sensor_simulator.py)

## Azure IoT Hub Configuration

An Azure IoT Hub instance is used to receive data from the simulated sensors.

- Device identities are created for each simulated sensor:
  - `sensor_dows_lake`
  - `sensor_fifth_avenue`
  - `sensor_nac`
- Device connection strings are used by the Python script to authenticate and send data.
  
![Azure IoT Hub creation](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2015.10.34.png)
![Azure IoT Hub devices](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2015.24.43.png)

---

## Azure Stream Analytics Job

A Stream Analytics job processes the incoming data in real-time.

![Azure Stream Analytics creation](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2015.10.34.png)

- **Input**: Azure IoT Hub is configured as the input source.
 ![Azure Stream Analytics Input](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2018.24.29.png)
- **Output**: Azure Blob Storage is configured as the output sink.

![Azure Stream Analytics Output](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2018.26.47.png)

- **Query**: The following SQL-like query aggregates data over a 5-minute tumbling window:

```sql
SELECT
    IoTHub.ConnectionDeviceId AS DeviceId,
    location,
    AVG(iceThickness) AS avgIceThickness,
    MAX(snowAccumulation) AS maxSnowAccumulation,
    System.Timestamp AS EventTime

INTO
    [output]
FROM
    [input]
GROUP BY
    IoTHub.ConnectionDeviceId, TumblingWindow(minute, 5), location
```

This query calculates the average ice thickness and maximum snow accumulation for each location over a 5-minute window.
![Azure Stream Analytics Query](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2020.22.33.png)


---

## Azure Blob Storage

Processed data from Azure Stream Analytics is stored in Azure Blob Storage.

- Data is stored in **JSON format**.

![Blob Storage Output](screenshots/blob_storage_output.png)

---

## Usage Instructions

### Running the IoT Sensor Simulation

**Prerequisites**:
- Python 3.x
- Azure IoT Hub Device SDK for Python:
  ```bash
  pip install azure-iot-device
  ```
- Azure IoT Hub device connection strings for:
  - `sensor_dows_lake`
  - `sensor_fifth_avenue`
  - `sensor_nac`

**Steps**:
1. **Clone the Repository**: Clone the GitHub repository containing the `sensor-simulation/simulate_sensors.py` script.
2. **Navigate to the Directory**:
   ```bash
   cd sensor-simulation/
   ```
3. **Configure Connection Strings**:
   - Open `simulate_sensors.py`
   - Replace the placeholder values in the `CONNECTION_STRINGS` dictionary with your actual device connection strings.
4. **Run the Script**:
   ```bash
   python simulate_sensors.py
   ```
   - The script will send simulated sensor data to Azure IoT Hub every 10 seconds.
   - Press `Ctrl+C` to stop.

---

### Configuring Azure Services

#### Azure IoT Hub:
- Create an Azure IoT Hub instance in the Azure portal.
- Create three device identities:
  - `sensor_dows_lake`
  - `sensor_fifth_avenue`
  - `sensor_nac`
- Retrieve the device connection strings.

#### Azure Stream Analytics:
- Create a Stream Analytics job in the Azure portal.
- Configure Azure IoT Hub as the **input source**, specifying the consumer group.
- Configure Azure Blob Storage as the **output sink**, providing storage account and container details.
- Write the SQL query (provided above) to **aggregate the data**.
- Start the Azure Stream Analytics job

![Start the Azure Stream Analytics Job](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2020.41.56.png)
![Azure Stream Analytics Job running](https://github.com/kare0041/CST8916-Final-Project/blob/main/screenshots/Screenshot%202025-04-13%20at%2020.43.41.png)

#### Azure Blob Storage:
- Create a **Storage Account** and a **container** to store the processed data.

---

## Accessing Stored Data

- The processed data is stored in **Azure Blob Storage** as JSON files.
- You can access the data using:
  - Azure Portal
  - Azure Storage Explorer
  - Azure CLI

---

## Results

The system successfully:
- Simulates IoT sensors
- Processes data in real-time using Azure Stream Analytics
- Stores aggregated results in Azure Blob Storage

The Stream Analytics job calculates:
- **Average ice thickness**
- **Maximum snow accumulation**
- For each location, **every 5 minutes**

### Sample of the data stored in Blob Storage:

```json
{"DeviceId":"sensor_nac","location":"NAC","avgIceThickness":30.586206896551722,"maxSnowAccumulation":20.0,"EventTime":"2025-04-14T00:50:00.0000000Z"}
{"DeviceId":"sensor_dows_lake","location":"Dow's Lake","avgIceThickness":31.448275862068964,"maxSnowAccumulation":20.0,"EventTime":"2025-04-14T00:50:00.0000000Z"}
{"DeviceId":"sensor_fifth_avenue","location":"Fifth Avenue","avgIceThickness":31.275862068965516,"maxSnowAccumulation":20.0,"EventTime":"2025-04-14T00:50:00.0000000Z"}

```

## Reflection
When running the sensor_simulator script for the first time, I faced a TLS certificate verification issue (SSLCertVerificationError), which usually happens on macOS, when the system's certificate store is not available to python. 

In order to fix this issue, I ran the "install certificates" script for Python and included a fix to this issue in the sensor_simulator script; which can be uncommented if the simulator is being run on macOs system.
