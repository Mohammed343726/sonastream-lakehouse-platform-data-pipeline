import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer

# 1. Configuration dyal Kafka (Fin ghadi n-lo7ou la data)
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'eaf_telemetry'

conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': 'sonasid-eaf-sensor'
}

producer = Producer(conf)

# 2. Fonction bax t-générer m3loumat dyal l-Four (Vibration, Température)
def generate_eaf_data():
    return {
        "sensor_id": "EAF-01",
        "timestamp": datetime.utcnow().isoformat(),
        "temperature_celsius": round(random.uniform(1500.0, 1650.0), 2),
        "vibration_hz": round(random.uniform(45.0, 60.0), 2), # Foq 55Hz ra kayna anomalie
        "current_amps": round(random.uniform(50000, 60000), 2)
    }

# 3. L-Moteur li kay-bqa y-دور w y-lo7 l-Kafka
def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Erreur dyal l-irssal : {err}")
    else:
        print(f"✅ Data mchat l-Kafka -> Topic: {msg.topic()} | Partition: {msg.partition()}")

print(f"🚀 Démarrage du Simulateur EAF vers Kafka ({KAFKA_BROKER})...")

try:
    while True:
        data = generate_eaf_data()
        # Kan-reddou la data l-format JSON bax Kafka y-fhemha
        producer.produce(TOPIC_NAME, key=data["sensor_id"], value=json.dumps(data), callback=delivery_report)
        producer.poll(0)
        time.sleep(1) # Kan-lo7ou message kol taniya (Temps Réel)
except KeyboardInterrupt:
    print("\n🛑 L-Simulateur 7bess.")
finally:
    producer.flush()