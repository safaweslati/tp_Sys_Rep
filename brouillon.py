import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import BOTH, END, LEFT
from my_connect import my_conn  # database connection
from sqlalchemy.exc import SQLAlchemyError

font1 = ('Times', 14, 'normal')
font2 = ('Times', 32, 'bold')
my_w = tk.Tk()
my_w.geometry("1000x800")

my_w.columnconfigure(0, weight=4)
my_w.columnconfigure(1, weight=2)
my_w.rowconfigure(0, weight=1)
my_w.rowconfigure(1, weight=6)  # change weight to 4
my_w.rowconfigure(2, weight=2)

frame_top = tk.Frame(my_w, bg='white')
frame_bottom = tk.Frame(my_w, bg='white')

frame_m_right = tk.Frame(my_w, bg='#f8fab4')
frame_m_left = tk.Frame(my_w, bg='#284474')

# placing in grid
frame_top.grid(row=0, column=0, sticky='WENS', columnspan=2)
frame_m_left.grid(row=1, column=0, sticky='WENS')
frame_m_right.grid(row=1, column=1, sticky='WENS')
frame_bottom.grid(row=2, column=0, sticky='WENS', columnspan=2)
# Layout is over , placing components
trv = ttk.Treeview(frame_m_left, selectmode='browse')
trv.grid(row=0, column=0, columnspan=2, padx=3, pady=2)

# column identifiers
trv["columns"] = ("1", "2", "3", "4", "5")
trv.column("#0", width=40, anchor='w')  # p_id
trv.column("1", width=150, anchor='w')  # p_name
trv.column("2", width=100, anchor='w')  # unit
trv.column("3", width=50, anchor='w')  # price
trv.column("4", width=50, anchor='w')  # category
trv.column("5", width=80, anchor='w')  # available

# Headings
# respective columns
trv.heading("#0", text="id", anchor='w')
trv.heading("1", text="name", anchor='w')
trv.heading("2", text="Unit", anchor='w')
trv.heading("3", text="Price", anchor='w')
trv.heading("4", text="Category", anchor='w')
trv.heading("5", text="Available", anchor='w')

path_image = "G:\\My Drive\\testing\\plus2_restaurant_v1\\images\\"
img_top = tk.PhotoImage(file=path_image + "restaurant-3.png")
img_l1 = tk.Label(frame_top, image=img_top)
img_l1.grid(row=0, column=0, sticky='nw', pady=1)

# Right side layout to display product details for Edit
lr1 = tk.Label(frame_m_right, text='P Name', font=font1)
lr1.grid(row=0, column=0, sticky='nw')
p_name = tk.StringVar()  # string variable for product name
e_p_name = tk.Entry(frame_m_right, textvariable=p_name, font=font1)
e_p_name.grid(row=0, column=1, columnspan=2)
unit = tk.StringVar()  # string variable for unit
lr2 = tk.Label(frame_m_right, text='Unit', font=font1)
lr2.grid(row=1, column=0, sticky='nw')
e_unit = tk.Entry(frame_m_right, textvariable=unit, font=font1)
e_unit.grid(row=1, column=1, columnspan=2)
price = tk.DoubleVar()  # double variable for price
lr3 = tk.Label(frame_m_right, text='Price', font=font1)
lr3.grid(row=2, column=0, sticky='nw')
e_price = tk.Entry(frame_m_right, textvariable=price, font=font1)
e_price.grid(row=2, column=1, columnspan=2)

my_cats = {1: 'Breakfast', 2: 'Lunch', 3: 'Dinner'}  # mataching product category
category = list(my_cats.values())  # list to show as options

p_cat = tk.IntVar()
p_cat_sel = tk.StringVar()


def my_upd(*args):  # collect the selected option of combobox
    for i, j in my_cats.items():
        if (j == p_cat_sel.get()):  # selected option
            p_cat.set(i)  # category number


p_cat_sel.trace('w', my_upd)  # trigger the changes in combobox

lr2 = tk.Label(frame_m_right, text='Category', font=font1)
lr2.grid(row=3, column=0, sticky='nw')
e_p_cat = ttk.Combobox(frame_m_right, values=category,
                       textvariable=p_cat_sel, width=10, font=font1)
e_p_cat.grid(row=3, column=1, columnspan=2)

available = tk.IntVar()  # available , Yes or No
lr2 = tk.Label(frame_m_right, text='Available', font=font1)
lr2.grid(row=4, column=0, sticky='nw')
r1 = tk.Radiobutton(frame_m_right, text='Yes', variable=available, value=1, font=font1)
r1.grid(row=4, column=1, padx=1, pady=1)
r1 = tk.Radiobutton(frame_m_right, text='No', variable=available, value=0, font=font1)
r1.grid(row=4, column=2, padx=1, pady=1)

b_update = tk.Button(frame_m_right, text='Update')
b_update.grid(row=5, column=1)
l_error = tk.Label(frame_m_right, text='Message here', font=font1)
l_error.grid(row=6, column=0, columnspan=3)


def show_items(cat):  # Populating the treeview with records
    for item in trv.get_children():  # loop all child items
        trv.delete(item)  # delete them
    query = "SELECT * FROM plus2_products WHERE p_cat=%s"
    r_set = my_conn.execute(query, cat)  # get the record set from table
    for dt in r_set:  # add data to treeview
        trv.insert("", 'end', iid=dt[0], text=dt[0],
                   values=(dt[1], dt[2], dt[3], dt[4], dt[5]))


def data_collect(self):  # collect data to display for edit
    selected = trv.focus()  # gets the product id or p_id
    if (selected != None):
        query = "SELECT * from plus2_products WHERE p_id=%s"
        row = my_conn.execute(query, selected)
        s = row.fetchone()  # row details as tuple
        if (s != None):
            p_name.set(s[1])
            unit.set(s[2])
            price.set(s[3])
            e_p_cat.set(my_cats[s[4]])  # set the category value
            available.set(s[5])
            b_update.config(state='normal')
            b_update.config(command=lambda: my_update(selected))
    else:
        b_update.config(state='disabled')


def my_update(p_id):  # receives the p_id on button click to update
    try:
        data = (p_name.get(), unit.get(), price.get(), p_cat.get(), available.get(), p_id)
        id = my_conn.execute("UPDATE plus2_products SET p_name=%s,unit=%s,\
            price=%s,p_cat=%s, available=%s WHERE p_id=%s", data)
        # print(data)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        msg_display = error
        show_msg(msg_display, 'error')  # send error message
    except tk.TclError as e:
        msg_display = e.args[0]
        show_msg(msg_display, 'error')  # send error message
    else:
        msg_display = "Number of records updated: " + str(id.rowcount)
        show_msg(msg_display, 'normal')  # success message
        p_name.set('')  # remove the product name
        unit.set('')
        price.set(0)
        e_p_cat.set('')  # set the category value
        available.set(5)
        r1_v.set(data[3])
        show_items(data[3])  # refresh the treeview with fresh data


def show_msg(msg_display, type):  # to show message to user
    if (type == 'normal'):  # updated or normal message
        l_error.config(text=msg_display, fg='green')
    else:  # error message
        l_error.config(text=msg_display, fg='red')
    my_w.after(3000, lambda: l_error.config(text=''))  # hide message after delay


show_items(1)  # populate treeview with one category of product

r1_v = tk.IntVar(value=1)  # We used integer variable here
r1 = tk.Radiobutton(frame_bottom, text='Breakfast', variable=r1_v, value=1, command=lambda: show_items(1))
r1.grid(row=0, column=0)

r2 = tk.Radiobutton(frame_bottom, text='Lunch', variable=r1_v, value=2, command=lambda: show_items(2))
r2.grid(row=0, column=1)

r3 = tk.Radiobutton(frame_bottom, text='Dinner', variable=r1_v, value=3, command=lambda: show_items(3))
r3.grid(row=0, column=2)

trv.bind("<<TreeviewSelect>>", data_collect)

my_w.mainloop()