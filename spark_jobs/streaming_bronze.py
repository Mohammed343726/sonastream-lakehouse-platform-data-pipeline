from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def start_bronze_streaming():
    print("🚀 Démarrage du job PySpark : Ingestion vers Bronze Layer...")

    # 1. Configuration de Spark avec les connecteurs Kafka et S3 (MinIO)
    spark = SparkSession.builder \
        .appName("SonaStream_Bronze_Ingestion") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.4") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

    # N-nqqiw l-Terminal mn l-hdera bzaf dyal Spark (Logs)
    spark.sparkContext.setLogLevel("WARN")

    # 2. Définition du Schéma de la Télémétrie (M-tabeq m3a l-Cahier des Charges)
    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("sensor_id", StringType(), True),
        StructField("temperature_celsius", DoubleType(), True),
        StructField("vibration_hz", DoubleType(), True),
        StructField("current_amps", DoubleType(), True)
    ])

    # 3. Lecture du flux en temps réel depuis Kafka
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "eaf_telemetry") \
        .option("startingOffsets", "earliest") \
        .load()

    # 4. Transformation : Décoder le JSON et ajouter l'heure d'ingestion
    parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("ingestion_timestamp", current_timestamp())

    # 5. Écriture dans le Data Lake (MinIO) en format Parquet
    query = parsed_df.writeStream \
        .format("parquet") \
        .option("checkpointLocation", "s3a://bronze/checkpoints/eaf_telemetry") \
        .option("path", "s3a://bronze/eaf_telemetry") \
        .outputMode("append") \
        .start()

    print("✅ Le flux Streaming est ouvert ! Spark écoute Kafka et écrit dans MinIO (Bucket Bronze)...")
    
    # Khelli l-moteur khddam dima
    query.awaitTermination()

if __name__ == "__main__":
    start_bronze_streaming()