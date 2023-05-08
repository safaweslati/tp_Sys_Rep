import json
import threading
import pika


from db import DBService
from Product import Product;


# QUEUE_NAME = "bo"

db_service = DBService("localhost", "root" , "root", "ho",3306)
def main():
    # UI

    start_consumer_thread()


    # channel1.start_consuming()

def start_consumer_thread():
    consumer_thread1 = threading.Thread(target=consume,args=("bo1",))
    consumer_thread2 = threading.Thread(target=consume,args=("bo2",))
    consumer_thread1.start()
    consumer_thread2.start()

def consume(QUEUE_NAME):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel1 = connection.channel()
    # channel2 = connection.channel()
    channel1.queue_declare(queue=QUEUE_NAME)
    # channel1.queue_declare(queue=QUEUE_NAME + str(2))
    print(" [*] Waiting for messages. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        received_message = body.decode('utf-8')
        print(received_message)
        p = deserialize(received_message)
        p=Product(p['id'],p['region'],p['product'],p['total'],p['date'],p['up_to_date'] ,method.routing_key)
        print(p)
        try:
            if p.up_to_date == "add":
                print(p.up_to_date)
                print(method.routing_key)
                db_service.insert_product(p.id,p.region, p.product, p.total, p.date,method.routing_key)

            elif p.up_to_date == "update":
                db_service.update_product(p.id, p.region, p.product, p.total, p.date, p.bo)

            elif p.up_to_date == "delete":
                id = db_service.get_product_id(p.region,p.product,p.total,p.date, method.routing_key)
                db_service.delete_product(id)



        except Exception as e:
            print(str(e))

    channel1.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel1.start_consuming()
def deserialize(message):
    return json.loads(message)


if __name__ == '__main__':
    main()