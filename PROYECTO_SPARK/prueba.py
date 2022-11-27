# For running Spark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Spark").getOrCreate()
# For running Pandas on top of Spark
import pyspark.pandas as ps

a=ps.DataFrame()