{{ config(materialized='table') }}

SELECT
    equipement_status,
    ROUND(AVG(temperature_celsius)::numeric, 2) AS moyenne_temperature,
    ROUND(MAX(vibration_hz)::numeric, 2) AS max_vibration,
    COUNT(*) AS nombre_enregistrements
FROM {{ source('postgres_silver', 'silver_telemetry') }}
GROUP BY equipement_status