import json
import threading

import mysql.connector
import pika
import schedule
import time


from ho.Product import Product
from ho.db import DBService


def getAllProducts(mycursor):
    select_all_query="select * from product"
    products=[]
    mycursor.execute(select_all_query)
    rows=mycursor.fetchall()
    for row in rows: 
        id,region,product,total,date,up_to_date,bo= row
        p=Product(id,region,product,total,date,up_to_date,bo)
        products.append(p)

    return products



def get_products_to_send(mycursor):
    select_to_send=f"select * from product where up_to_date <> 'ok'  "
    products=[]
    mycursor.execute(select_to_send)
    rows=mycursor.fetchall()
    for row in rows: 
        id,region,product,total,date,up_to_date,bo= row
        p=Product(id,region,product,total,date,up_to_date,bo)
        products.append(p)
        print(p)
    return products



db= DBService("bo1")

#conncet to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='bo1')



#polling function
def polling_func():
    db=DBService("bo1")

    print("polling function running...")
    mycursor=db.cursor
    ps=get_products_to_send(db.cursor)
    for p in ps:
        json_date = p.get_date().strftime('%Y-%m-%d')
        p.set_date(json_date)
        channel.basic_publish(exchange='', routing_key='bo1', body=json.dumps(p.__dict__))
        print(f'product of id { p.get_id()} sent ')
        p.set_up_to_date('ok')
        mycursor.execute(f"UPDATE product SET up_to_date ='ok'  where id= '{ p.get_id()}' " )
        db.conn.commit()




def poll():
    while True:
        polling_func()
        time.sleep(10)




poll_thread = threading.Thread(target=poll)
poll_thread.start()
db.RenderTable("bo1")

