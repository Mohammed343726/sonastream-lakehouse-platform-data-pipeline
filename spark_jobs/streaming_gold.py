import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg, sum as spark_sum, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Configuration dyal Windows (Java & Hadoop)
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17" 
os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

def start_gold_streaming():
    print("🚀 Démarrage du job PySpark : Couche Gold (KPIs & Agrégation)...")

    spark = SparkSession.builder \
        .appName("SonaStream_Gold_Layer") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Schéma dyal l-Couche Silver
    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("sensor_id", StringType(), True),
        StructField("temperature_celsius", DoubleType(), True),
        StructField("vibration_hz", DoubleType(), True),
        StructField("current_amps", DoubleType(), True),
        StructField("ingestion_timestamp", TimestampType(), True),
        StructField("equipement_status", StringType(), True)
    ])

    print("⏳ Spark kay-qra mn l-Couche Silver...")

    # Qra mn Silver
    df_silver = spark.readStream \
        .format("parquet") \
        .schema(schema) \
        .load("s3a://silver/eaf_cleaned_data")

    # ---------------------------------------------------------
    # LA LOGIQUE GOLD : L-7ssab dyal les KPIs kola 30 Taniya
    # ---------------------------------------------------------
    df_gold = df_silver \
        .withWatermark("ingestion_timestamp", "10 seconds") \
        .groupBy(window(col("ingestion_timestamp"), "30 seconds")) \
        .agg(
            avg("temperature_celsius").alias("avg_temperature"),
            avg("vibration_hz").alias("avg_vibration"),
            avg("current_amps").alias("avg_current"),
            # X7al mn warning wqe3 f had 30 taniya?
            spark_sum(when(col("equipement_status") == "WARNING", 1).otherwise(0)).alias("total_warnings")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "avg_temperature",
            "avg_vibration",
            "avg_current",
            "total_warnings"
        )

    print("🚀 La Couche Gold kat-7seb w kat-lo7 l-Moulakhas f MinIO (Bucket Gold)...")

    # Kteb f Gold (Append mode m3a l-Watermark)
    query = df_gold.writeStream \
        .format("parquet") \
        .outputMode("append") \
        .option("checkpointLocation", "s3a://gold/checkpoints/eaf_kpis") \
        .option("path", "s3a://gold/eaf_kpis") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    start_gold_streaming()