import os
from confluent_kafka import Producer  # Changed to regular Producer
import json
from datetime import datetime, timedelta
import random, uuid
import time 

LONDON_COORDINATES = {'latitude': 51.5074,'longitude': -0.1278}
BIRMINGHAM_COORDINATES = {'latitude': 52.4862,'longitude': -1.8904}

LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude']) / 100

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

random.seed(42)
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()

def get_next_time():
    global start_time 
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def generate_gps_data(vehicle_id, timestamp, vehicle_type='private'):
    return {
        'id': str(uuid.uuid4()),
        'device_id': vehicle_id,
        'timestamp': timestamp,
        'vehicle_type': vehicle_type,
        'speed': random.uniform(0, 40),
        'direction': 'North-East',
    }

def generate_traffic_camera_data(vehicle_id, timestamp, location, camera_id):
    return {
        'id': str(uuid.uuid4()),
        'device_id': vehicle_id,
        'timestamp': timestamp,
        'camera_id': camera_id,
        'location': location,
        'snapshot': 'Base64EncodedImageString',
        'traffic_density': random.choice(['Low', 'Medium', 'High']),
        'average_speed': random.uniform(20, 60),
    }

def generate_weather_data(vehicle_id, timestamp, location):
    return {
        'id': str(uuid.uuid4()),
        'device_id': vehicle_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(-5, 26),
        'weatherConditions': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
        'precipitation': random.uniform(0, 25),
        'windSpeed': random.uniform(0, 100),
        'humidity': float(random.randint(0, 100)),  # Convert to float
        'airQualityIndex': random.randint(0, 500),
    }

def generate_emergency_incident_data(vehicle_id, timestamp, location):
    return {
        'id': str(uuid.uuid4()),
        'device_id': vehicle_id,
        'incident_id': str(uuid.uuid4()),
        'type': random.choice(['Accident', 'Roadblock', 'Medical Emergency', 'Police', 'None']),
        'timestamp': timestamp,
        'location': location,
        'status': random.choice(['Active', 'Resolved']),
        'description': 'description of the incident',
    }

def simulate_vehicle_movement():
    global start_location
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)
    return start_location

def generate_vehicle_data(vehicle_id):
    location = simulate_vehicle_movement()
    return {
        'id': str(uuid.uuid4()),  # FIXED: Convert to string
        'device_id': vehicle_id,
        'timestamp': get_next_time().isoformat(),
        'location': f"{location['latitude']},{location['longitude']}",
        'speed': random.uniform(10, 40),
        'direction': 'North-East',
        'make': 'BMW',
        'model': 'C500',
        'year': 2025,
        'fuelType': 'Hybrid',
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()}")

def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic=topic,
        key=str(data['id']),
        value=json.dumps(data).encode('utf-8'),
        on_delivery=delivery_report
    )
    producer.flush()

def simulate_journey(producer, vehicle_id):
    while True:
        vehicle_data = generate_vehicle_data(vehicle_id)
        gps_data = generate_gps_data(vehicle_id, vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(
            vehicle_id, vehicle_data['timestamp'], vehicle_data['location'], camera_id='Camera_123'
        )
        weather_data = generate_weather_data(vehicle_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(
            vehicle_id, vehicle_data['timestamp'], vehicle_data['location']
        )
      
        lat, lon = map(float, vehicle_data['location'].split(','))
        if (lat >= BIRMINGHAM_COORDINATES['latitude'] and lon <= BIRMINGHAM_COORDINATES['longitude']):
            print("Vehicle has reached Birmingham. Ending journey simulation...")
            break
            
        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)
        
        time.sleep(5)

if __name__ == "__main__":
    producer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    }
    producer = Producer(producer_conf)

    try:
        simulate_journey(producer, 'Vehicle_Maxi_01')
    except KeyboardInterrupt:
        print("Journey simulation ended by the user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")