{{ config(materialized='table') }}

SELECT 
    equipement_status,
    AVG(temperature_celsius) as moyenne_temperature,
    MAX(vibration_hz) as max_vibration,
    COUNT(*) as nombre_enregistrements
FROM public.silver_telemetry
GROUP BY equipement_status
