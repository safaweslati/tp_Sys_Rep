db_host = "localhost"
db_user = "root"
db_pass="root"
db_name = "bo1"
import mysql.connector

mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    database=db_name,
    password=db_pass,
    port= "3306"
)
mycursor = mydb.cursor()
create_query = '''CREATE TABLE IF NOT EXISTS product (
        id INT NOT NULL AUTO_INCREMENT,
        region VARCHAR(30) ,
        product VARCHAR(30),
        total int,
        date DATE,
        up_to_date VARCHAR(30) DEFAULT 'add',
        PRIMARY KEY (ID)
    ) ;'''
mycursor.execute(create_query)