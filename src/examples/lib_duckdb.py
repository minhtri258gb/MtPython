import duckdb

r1 = duckdb.sql("SELECT 42 AS i")
duckdb.sql("SELECT i * 2 AS k FROM r1").show()

# duckdb.sql("SELECT 42").show()
# a = duckdb.sql("SELECT 42")
# print(type(a))
# a.show()

# duckdb.sql("""
# 	SELECT station, count(*) AS num_services
# 	FROM train_services
# 	GROUP BY ALL
# 	ORDER BY num_services DESC
# 	LIMIT 3;
# 	""")
