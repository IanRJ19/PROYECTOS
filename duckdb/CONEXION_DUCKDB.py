import duckdb

# Create DB (embedded DBMS)
conn = duckdb.connect('BASE_DATOS.duckdb')
c = conn.cursor()

c.execute("SELECT * FROM usuarios")

# Fetch all rows from the result set
result = c.fetchall()

# Process the result as needed
for row in result:
    print(row)

# Close the cursor and the connection
c.close()
conn.close()
