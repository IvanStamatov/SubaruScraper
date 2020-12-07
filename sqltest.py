import sqlite3

#create the actual db file
connection = sqlite3.connect('subarus.db')

# creating a variable via which to issue commands
cursor = connection.cursor()

# """ """ are used so no special symbols need to be used
# cursor.execute("""CREATE TABLE subarus(
#         model text,
#         year integer
#         )""")



# cursor.execute("INSERT INTO subarus VALUES ('Impreza', 2005)")

cursor.execute("SELECT * FROM subarus WHERE year='2005'")

# gets the next row in our results and only return that row. 
print(cursor.fetchone())

# commits the current transaction
connection.commit()

# closes the connection
connection.close()