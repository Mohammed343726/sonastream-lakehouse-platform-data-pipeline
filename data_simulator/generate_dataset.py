import csv
import random
from datetime import datetime, timedelta

# Configuration
FILENAME = 'eaf_historical_data.csv'
NUM_ROWS = 5000
START_TIME = datetime(2026, 5, 26, 8, 0, 0)

# 7iydna l-emojis w les accents bax Windows ma-y-t-blokax
print(f"Generation de {NUM_ROWS} lignes de donnees industrielles...")

# Zidna encoding='utf-8' hna bax la data t-t-stocka n9iya
with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # L-Sass dyal l-CSV (Header)
    writer.writerow(['timestamp', 'sensor_id', 'temperature_celsius', 'vibration_hz', 'current_amps'])

    for i in range(NUM_ROWS):
        current_time = START_TIME + timedelta(seconds=i)
        
        # 5% dyal l-waqt ghadi n-saybou "Anomalie" bax n-testiw Spark mn b3d
        if random.random() < 0.05:
            temp = round(random.uniform(1600.0, 1750.0), 2)  # 7arara tal3a bzaf
            vib = round(random.uniform(60.0, 80.0), 2)       # Vibration khatira
            amp = round(random.uniform(60000, 65000), 2)
        else:
            # Data 3adiya w m-zyana
            temp = round(random.uniform(1500.0, 1550.0), 2)
            vib = round(random.uniform(40.0, 50.0), 2)
            amp = round(random.uniform(50000, 55000), 2)

        writer.writerow([current_time.strftime('%Y-%m-%dT%H:%M:%SZ'), 'EAF-01', temp, vib, amp])

print(f"Nadi! Le fichier '{FILENAME}' est pret et contient {NUM_ROWS} lignes.")