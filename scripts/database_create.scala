// Spark Shell is here: /mnt/c/spark-2.4.3-bin-hadoop2.7/bin/spark-shell
// to run scala files with the spark shell run spark-shell -i "path"":
// /mnt/c/spark-2.4.3-bin-hadoop2.7/bin/spark-shell -i /mnt/c/Github/DotA2-Exploration/scripts/database_create.scala

val spark = SparkSession
      .builder()
      .appName("SparkSQL")
      .master("local[*]")
      .getOrCreate()

import spark.implicits._

val path = "/mnt/e/DataSets/versions_test/7.21/4385181848.json"
val df = spark.read.json(path)

df.printSchema()

df.createOrReplaceTempView("match")

spark.sql("select version from match").show()

System.exit(0)
