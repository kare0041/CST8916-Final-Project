# Rideau Canal Real-time Monitoring System

## Scenario Description
Monitoring the Rideau Canal Skateway for safe skating conditions using simulated IoT data and Azure services.

## System Architecture
![architecture-diagram](screenshots/architecture.png)

## Implementation Details

### IoT Sensor Simulation
- Sends JSON payload every 10 seconds from 3 locations.
- Payload includes ice thickness, temperature, snow accumulation, etc.

### Azure IoT Hub
- Handles ingestion of data from simulated sensors.
- Devices: `sensor-dowslake`, `sensor-fifth`, `sensor-nac`.

### Azure Stream Analytics
- Aggregates data every 5 minutes:
  - Average Ice Thickness
  - Max Snow Accumulation
- Stores results in Azure Blob Storage in JSON format.

### Azure Blob Storage
- Container: `processed-data`
- Files organized by output timestamp.

## Usage Instructions

### Run Simulation
```bash
python simulate_sensors.py
