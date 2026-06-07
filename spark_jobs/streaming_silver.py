import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17" 
os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

# --- L-Fonction dyal Postgres (B-Radar) ---
def write_to_postgres(df, epoch_id):
    print(f"\n--- 🔄 Micro-Batch ID: {epoch_id} ---")
    if not df.isEmpty():
        print(f"📦 La data wslat! Lqit {df.count()} stoura. Ghadi n-kteb f Postgres...")
        try:
            df.write \
                .format("jdbc") \
                .option("url", "jdbc:postgresql://127.0.0.1:5432/sonastream") \
                .option("driver", "org.postgresql.Driver") \
                .option("dbtable", "silver_telemetry") \
                .option("user", "postgres") \
                .option("password", "postgres") \
                .mode("append") \
                .save()
            print("✅ T-ktbat f Postgres B-Naja7!")
        except Exception as e:
            print(f"❌ ERREUR f Postgres: {e}")
    else:
        print("📭 Batch khawi, ma-kayn ma n-kteb.")

def start_silver_streaming():
    print("🚀 Démarrage du job PySpark : Couche Silver...")

    spark = SparkSession.builder \
        .appName("SonaStream_Silver_Layer") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,org.postgresql:postgresql:42.6.0") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR") # nqessna l-blabla dyal Spark bax n-xofou l-erreurs d-bessa7

    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("sensor_id", StringType(), True),
        StructField("temperature_celsius", DoubleType(), True),
        StructField("vibration_hz", DoubleType(), True),
        StructField("current_amps", DoubleType(), True),
        StructField("ingestion_timestamp", TimestampType(), True)
    ])

    df_bronze = spark.readStream \
        .format("parquet") \
        .schema(schema) \
        .load("s3a://bronze/eaf_telemetry")

    df_silver = df_bronze \
        .filter(col("temperature_celsius").isNotNull()) \
        .filter(col("temperature_celsius") > 0) \
        .filter(col("vibration_hz") > 0) \
        .withColumn("equipement_status", 
                    when((col("temperature_celsius") > 1500) | (col("vibration_hz") > 50), "WARNING")
                    .otherwise("NORMAL"))

    print("🚀 La Couche Silver kat-tsenna la data mn Bronze...")

    query_postgres = df_silver.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .option("checkpointLocation", "s3a://silver/checkpoints/postgres_telemetry") \
        .start()

    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    start_silver_streaming()