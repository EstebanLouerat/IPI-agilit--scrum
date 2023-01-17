import random
import os
import sqlite3
from sqlite3 import Cursor, Connection
from datetime import date

########################################################################################
#                                     GLOBAL                                           #
########################################################################################

database: Connection = sqlite3.connect('restaurant.db')
cursor: Cursor = database.cursor()
WAITER = 0

########################################################################################
#                                     INIT                                             #
########################################################################################


def db_init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS table_tbl (
    	id_tbl INTEGER PRIMARY KEY AUTOINCREMENT,
    	tbl_num INTEGER
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS waiter_wtr (
    	id_wtr INTEGER PRIMARY KEY AUTOINCREMENT,
    	wtr_firstname VARCHAR,
    	wtr_lastname VARCHAR
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_ord (
    	id_ord INTEGER PRIMARY KEY AUTOINCREMENT,
    	ord_ref VARCHAR, 
    	ord_hour DATE,
    	id_wtr INTEGER ,
    	id_tbl INTEGER,
    	FOREIGN KEY (id_wtr) REFERENCES id_wtr(waiter_wtr),
    	FOREIGN KEY (id_tbl) REFERENCES id_tbl(table_tbl)
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS dish_dsh (
    	id_dsh INTEGER PRIMARY KEY AUTOINCREMENT,
    	dsh_name VARCHAR,
    	dsh_price FLOAT
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_dish_odh (
    	id_odh INTEGER PRIMARY KEY AUTOINCREMENT,
    	id_dsh INTEGER,
    	id_ord INTEGER,
    	FOREIGN KEY (id_dsh) REFERENCES id_dsh(dish_dsh),
    	FOREIGN KEY (id_ord) REFERENCES id_ord(order_ord)
    );''')

########################################################################################
#                                     API FUNCTIONS                                    #
########################################################################################


def api_add_order(order, dishes):
    order["ref"] = "ref-" + str(random.randint(100000, 999999))
    order["date"] = date.today()
    order["waiter"] = WAITER

    cursor.execute(
        "INSERT INTO order_ord (ord_ref, ord_hour, id_wtr, id_tbl ) VALUES (:ref, :date, :waiter, :table)", order)
    database.commit()
    rqs = cursor.execute("SELECT id_ord FROM order_ord ORDER BY id_ord DESC LIMIT 1")
    id_order = 0
    for rq in rqs:
        id_order = rq[0]
    objs = []
    for dish in dishes:
        objs += [[id_order,dish]]
    for obj in objs:
        cursor.execute(
            "INSERT INTO order_dish_odh (id_ord, id_dsh) VALUES (?,?)", obj)
    database.commit()

def api_show_orders():
    os.system('clear')
    orders = cursor.execute(
        "SELECT * FROM order_ord")
    for order in orders:
        print(order[0],'-',order[1])


def api_add_dish(dish):
    cursor.execute(
        "INSERT INTO dish_dsh (dsh_name, dsh_price) VALUES (:name, :price)", dish)
    database.commit()


def api_show_dishes():
    os.system('clear')
    dishes = cursor.execute("SELECT * FROM dish_dsh")
    for dish in dishes:
        print("id", dish[0], " | ", dish[1], "\t| ", dish[2], "E")

def api_show_waiter():
    os.system('clear')
    waiters = cursor.execute("SELECT * FROM waiter_wtr")
    for waiter in waiters:
        print("id", waiter[0], " | ", waiter[1], " ", waiter[2])

#######################################################################################
#                        TERMINAL FUNCTIONS                                           #
#######################################################################################


def app_menu() -> str:
    print("0 - Ajouter une commande")
    print("1 - Supprimer une commande par id")
    print("2 - Voir les commandes")
    print("3 - Voir une commande par id")
    print("4 - Prix total des commandes")
    print("5 - Ajouter un plat")
    print("6 - Afficher les plats")
    print("7 - Quitter")
    return input()

#######################################################################################
#                              APP FUNCTIONS                                          #
#######################################################################################


def add_order():
    order = {}
    dishes = []
    os.system('clear')
    table_id = int(input("Numero de table : "))
    os.system('clear')
    api_show_dishes()
    while True:
        std_in = input("Ajouter un plat (y/n)")
        if std_in == "y" or std_in == "":
            dish_id = int(input("Indiquer l'id du plat : "))
            order["table"] = table_id
            dishes += [dish_id]
        elif std_in == "n":
            return order, dishes


def add_dish():
    dish = {}
    os.system('clear')
    dish["name"] = input("Nom : ")
    dish["price"] = float(input("Prix : "))
    return dish


def prog_exit():
    database.close()
    exit()

    

def main():
    db_init()
    api_show_waiter()
    WAITER = int(input("Selectionner un id : "))
    while True:
        std_in = app_menu()
        match std_in:
            case "0":
                a,b = add_order()
                api_add_order(a,b)
            case "1":
                print("Supprimer une commande")
            case "2":
                api_show_orders()
            case "3":
                print("Voir une commande pa id")
            case "4":
                print("Prix total des commandes")
            case "5":
                api_add_dish(add_dish())
            case "6":
                api_show_dishes()
            case "7":
                prog_exit()


main()
