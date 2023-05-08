import time

import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from ho.Product import Product



class DBService:
    def __init__(self, database, host="localhost", user="root", password="root", port="3306"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.conn.cursor()

    def create_product_table(self):
        create_query = '''CREATE TABLE IF NOT EXISTS product (
            id INT NOT NULL AUTO_INCREMENT,
            region VARCHAR(30) ,
            product VARCHAR(30),
            total int,
            date DATE,
            PRIMARY KEY (ID)
        ) ;'''
        self.cursor.execute(create_query)
        self.conn.commit()
        print("Product table created successfully")

    def insert_product(self, id,region, product, total, date,bo):
        insert_query = "INSERT INTO product (id,region, product, total, date ,bo) VALUES (%s, %s, %s, %s, %s,%s)"
        values = (id,region, product, total, date ,bo)
        self.cursor.execute(insert_query, values)
        self.conn.commit()
        print("Product inserted successfully")


    def update_product(self, id, region, product, total, date, bo):
        update_query = f"UPDATE `product` SET `region` = '{region}', `product` = '{product}', `total` = '{total}', `date` = '{date}' WHERE `product`.`id` ='{id}' and `product`.`bo` = '{bo}' ;"
        print(update_query)
        self.cursor.execute(update_query)
        self.conn.commit()
        print("Product updated successfully")

    def update_product_up_to_date(self, id):
        update_query = f"UPDATE `product` SET `up_to_date` = 'delete' WHERE `product`.`id` ='{id}' ;"
        print(update_query)
        self.cursor.execute(update_query)
        self.conn.commit()
        print("Product up_to_date updated successfully")

    def get_product_id(self, region, product, total, date):
        self.cursor.execute("SELECT id FROM product WHERE region = %s AND product = %s AND total = %s AND date = %s",
                            (region, product, total, date))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def delete_product(self, id):
        delete_query = "DELETE FROM product WHERE id = %s"
        values = (id,)
        self.cursor.execute(delete_query, values)
        self.conn.commit()
        print("Product deleted successfully")

    def getAllProducts(self):
        select_all_query = "SELECT * FROM product"
        products = []
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        for row in rows:
            id, region, product, total, date, bo, up_to_date = row
            p = Product(id, region, product, total, date, up_to_date, bo)
            products.append(p)

        return products

    def RenderTable(self, type):
        font1 = ('Times', 14, 'normal')
        font2 = ('Times', 32, 'bold')
        my_w = tk.Tk()
        my_w.geometry("1000x400")

        my_w.columnconfigure(0, weight=4)
        my_w.columnconfigure(1, weight=2)
        my_w.rowconfigure(0, weight=1)
        my_w.rowconfigure(1, weight=6)
        my_w.rowconfigure(2, weight=2)

        frame_top = tk.Frame(my_w, bg='white')
        frame_bottom = tk.Frame(my_w, bg='white')

        frame_m_right = tk.Frame(my_w, bg='#f8fab4')
        frame_m_right.columnconfigure(0, weight=1)
        frame_m_right.columnconfigure(1, weight=1)
        frame_m_right.columnconfigure(2, weight=1)
        frame_m_right.rowconfigure(0, weight=1)
        frame_m_right.rowconfigure(1, weight=1)
        frame_m_right.rowconfigure(2, weight=1)
        frame_m_right.rowconfigure(3, weight=1)
        frame_m_right.rowconfigure(4, weight=1)
        frame_m_right.rowconfigure(5, weight=1)

        frame_m_left = tk.Frame(my_w, bg='#284474')

        # placing in grid
        frame_top.grid(row=0, column=0, sticky='WENS', columnspan=2)
        frame_m_left.grid(row=1, column=0, sticky='WENS')
        frame_m_right.grid(row=1, column=1, sticky='WENS')
        frame_bottom.grid(row=2, column=0, sticky='WENS', columnspan=2)

        # Layout is over, placing components
        table = ttk.Treeview(frame_m_left, selectmode='browse')
        table.grid(row=0, column=0, columnspan=2, padx=3, pady=2)
        table["columns"] = ("id", "region", "product", "total", "date", "BO")

        table.column("#0", width=0, stretch=tk.NO)
        table.column("id", width=50)
        table.column("region", width=100)
        table.column("product", width=100)
        table.column("total", width=50)
        table.column("date", width=100)
        table.column("BO", width=50)

        table.heading("id", text="id")
        table.heading("region", text="Region")
        table.heading("product", text="Product")
        table.heading("total", text="Total")
        table.heading("date", text="Date")
        table.heading("BO", text="BO")

        if "ho" in type:
            my_w.title('Head Office')
        elif "bo" in type:
            my_w.title("Branch Office " + type[-1])
            lr1 = tk.Label(frame_m_right, text='Region', font=font1)
            lr1.grid(row=0, column=0, sticky='nw')
            region = tk.StringVar()  # string variable for region
            e_region = tk.Entry(frame_m_right, textvariable=region, font=font1)
            e_region.grid(row=0, column=1, columnspan=2)

            product = tk.StringVar()  # string variable for product
            lr2 = tk.Label(frame_m_right, text='Product', font=font1)
            lr2.grid(row=1, column=0, sticky='nw')
            e_product = tk.Entry(frame_m_right, textvariable=product, font=font1)
            e_product.grid(row=1, column=1, columnspan=2)

            total = tk.DoubleVar()  # double variable for price
            lr3 = tk.Label(frame_m_right, text='Total', font=font1)
            lr3.grid(row=2, column=0, sticky='nw')
            e_total = tk.Entry(frame_m_right, textvariable=total, font=font1)
            e_total.grid(row=2, column=1, columnspan=2)

            date = tk.StringVar()  # string variable for product
            lr4 = tk.Label(frame_m_right, text='Date', font=font1)
            lr4.grid(row=3, column=0, sticky='nw')
            e_date = DateEntry(frame_m_right, width=12, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                               textvariable=date)
            e_date.grid(row=3, column=1, columnspan=2)
            insert_button = tk.Button(frame_m_right, text="Insert", font=font1,
                                      command=lambda: self.insertButtonClicked(region.get(), product.get(), total.get(),
                                                                               date.get(),type))
            insert_button.grid(row=4, column=0, padx=20, pady=10)
            update_button = tk.Button(frame_m_right, text="Update", font=font1,
                                      command=lambda: self.updateButtonClicked(region.get(), product.get(), total.get(),
                                                                               date.get(), type))
            update_button.grid(row=4, column=1, padx=20, pady=10)

            # Delete button
            delete_button = tk.Button(frame_m_right, text="Delete", font=font1,
                                      command=lambda: self.deleteButtonClicked(table))

            delete_button.grid(row=4, column=2, padx=20, pady=10)
        tk.mainloop()

    def insertButtonClicked(self,region, product, total, date, type):
        id = len(self.getAllProducts())+10
        self.insert_product(id,region,product,total,date,type)

    def updateButtonClicked(self, region, product, total,date, type):
        id = self.get_product_id(region,product,total,date)
        self.update_product(id,region,product,total,date,type)

    def deleteButtonClicked(self, region, product, total,date):
        id = self.get_product_id(region,product,total,date)
        self.update_product_up_to_date(id)
        time.sleep(10)
        self.delete_product(id)


