from pyspark.sql import SparkSession
from config import configuration
from pyspark.sql.types import StructType as StrucType, StructField as structField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.functions import from_json, col
from pyspark.sql.dataframe import DataFrame

def main():
 
  
    spark = SparkSession.builder \
    .appName("Spark City Streaming") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.hadoop.fs.s3a.access.key", configuration["AWS_ACCESS_KEY"]) \
    .config("spark.hadoop.fs.s3a.secret.key", configuration["AWS_SECRET_KEY"]) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.fast.upload", "true") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.executor.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true") \
    .config("spark.driver.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true") \
    .getOrCreate()
    # .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
            # "org.apache.hadoop:hadoop-aws:3.3.1,""com.amazonaws:aws-java-sdk:1.11.469") \
    



    # # ✅ Test S3 write before starting streaming
    # testDF = spark.createDataFrame([(1, "ok")], ["id", "msg"])
    # testDF.write.mode("overwrite").parquet("s3a://smartcity-spark-streaming-data-01/test")
    # print("✅ Test write to S3 successful!")
    
    #adjust log level to reduce the console output
    spark.sparkContext.setLogLevel("WARN")

    #vehicle schema
    vehicleSchema = StrucType([
        structField("id", StringType(), True),
        structField("device_id", StringType(), True),
        structField("timestamp", TimestampType(), True),
        structField("location", StringType(), True),  
        structField("speed", DoubleType(), True),
        structField("direction", StringType(), True),
        structField("make", StringType(), True),
        structField("model", StringType(), True),
        structField("year", IntegerType(), True),
        structField("fuelType", StringType(), True)
    ])

    #gps schema
    gpsSchema = StrucType([
        structField("id", StringType(), True),
        structField("device_id", StringType(), True),
        structField("timestamp", TimestampType(), True),  
        structField('speed', DoubleType(), True),
        structField('direction', StringType(), True),
        structField('vehicle_type', StringType(), True),
    ])

    #traffic camera schema
    trafficSchema = StrucType([
        structField("id", StringType(), True),
        structField("device_id", StringType(), True),
        structField("camera_id", StringType(), True),
        structField('location', StringType(), True),
        structField("timestamp", TimestampType(), True),  
        structField('snapshot', StringType(), True),
        structField('traffic_density', StringType(), True),
        structField('average_speed', DoubleType(), True),
    ])

    #weather schema
    weatherSchema = StrucType([
        structField("id", StringType(), True),
        structField("device_id", StringType(), True),
        structField("location", StringType(), True),
        structField("timestamp", TimestampType(), True),
        structField('temperature', DoubleType(), True),
        structField('weatherConditions', StringType(), True),
        structField('precipitation', DoubleType(), True),
        structField('windSpeed', DoubleType(), True),
        structField('humidity', DoubleType(), True),
        structField('airQualityIndex', IntegerType(), True),
    ])

    #emergency incident schema
    emergencySchema = StrucType([
        structField("id", StringType(), True),
        structField("device_id", StringType(), True),
        structField("incident_id", StringType(), True),
        structField("type", StringType(), True),
        structField("timestamp", TimestampType(), True),  
        structField('location', StringType(), True),
        structField('status', StringType(), True),
        structField('description', StringType(), True),
    ])

    def read_kafka_topic(topic, schema):
        return spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "broker:29092") \
            .option("subscribe", topic) \
            .option("startingOffsets", "earliest") \
            .load() \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), schema).alias("data")) \
            .select("data.*") \
            .withWatermark("timestamp", "2 minute")
    
    def stream_writer(input: DataFrame, checkpointFolder, output):
        return(
            input.writeStream \
            .format("parquet") \
            .option("checkpointLocation", checkpointFolder) \
            .option("path", output) \
            .outputMode("append") \
            .start()
        )


    vehicleDF = read_kafka_topic('vehicle_data', vehicleSchema).alias('vehicle')
    gpsDF = read_kafka_topic('gps_data', gpsSchema).alias('gps')
    trafficDF = read_kafka_topic('traffic_data', trafficSchema).alias('traffic')
    weatherDF = read_kafka_topic('weather_data', weatherSchema).alias('weather')
    emergencyDF = read_kafka_topic('emergency_data', emergencySchema).alias('emergency')

    #join all the dfs with the id and timestamp

    query1 = stream_writer(vehicleDF, "s3a://smartcity-spark-streaming-data-01/checkpoints/vehicle_data", 
                  "s3a://smartcity-spark-streaming-data-01/data/vehicle_data")
    query2 = stream_writer(gpsDF, "s3a://smartcity-spark-streaming-data-01/checkpoints/gps_data", 
                  "s3a://smartcity-spark-streaming-data-01/data/gps_data")
    query3 = stream_writer(trafficDF, "s3a://smartcity-spark-streaming-data-01/checkpoints/traffic_data", 
                  "s3a://smartcity-spark-streaming-data-01/data/traffic_data")
    query4 = stream_writer(weatherDF, "s3a://smartcity-spark-streaming-data-01/checkpoints/weather_data", 
                  "s3a://smartcity-spark-streaming-data-01/data/weather_data")
    query5 = stream_writer(emergencyDF, "s3a://smartcity-spark-streaming-data-01/checkpoints/emergency_data", 
                  "s3a://smartcity-spark-streaming-data-01/data/emergency_data")
    query5.awaitTermination()
    

if __name__ == "__main__":
    main()