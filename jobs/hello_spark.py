"""Premier exercice PySpark : créer et agréger des lignes en mémoire."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as sum_

spark = SparkSession.builder.appName("simple-bigdata-bi-intro").getOrCreate()

sales = [
    ("Paris", "livre", 3, 12.50),
    ("Paris", "cahier", 5, 4.00),
    ("Lyon", "livre", 2, 12.50),
]

df = spark.createDataFrame(
    sales,
    ["ville", "produit", "quantite", "prix_unitaire"],
)

result = (
    df.withColumn("montant", df.quantite * df.prix_unitaire)
    .groupBy("ville")
    .agg(sum_("montant").alias("chiffre_affaires"))
    .orderBy("ville")
)

result.show()
spark.stop()
