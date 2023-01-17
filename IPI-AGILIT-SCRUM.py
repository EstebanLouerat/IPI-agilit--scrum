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

########################################################################################
#                                     INIT                                             #
########################################################################################

def db_init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS table_tbl (
                    	id_tbl INTEGER PRIMARY KEY AUTOINCREMENT,
                    	tbl_num INTEGER);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_ord(
                        id_ord INTEGER PRIMARY KEY AUTOINCREMENT,
                        ord_ref VARCHAR,
                        ord_hour DATE,
                        fk_ord_tbl INTEGER,
                        FOREIGN KEY(fk_ord_tbl) REFERENCES table_tbl(id_tbl));''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS dish_dsh(
                        id_dsh INTEGER PRIMARY KEY AUTOINCREMENT,
                        dsh_name VARCHAR,
                        dsh_price FLOAT,
                        fk_dsh_ord INTEGER,
                        FOREIGN KEY(fk_dsh_ord) REFERENCES order_tbl(dish_dsh));''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_ord (
	                    tbl_id INTEGER,
	                    ord_id INTEGER,
	                    PRIMARY KEY(tbl_id, ord_id));''')

########################################################################################
#                                     API FUNCTIONS                                    #
########################################################################################

def api_add_order(order):
    order["ref"] = "ref-" + str(random.randint(100000, 999999))
    order["date"] = date.today()
    cursor.execute(
        "INSERT INTO order_ord (ord_ref, ord_hour) VALUES (:ref, :date)", order)
    database.commit()

def api_show_orders():
    os.system('clear')
    orders = cursor.execute(
        "SELECT * FROM order_ord INNER JOIN dish_dsh ON dish_dsh.fk_dsh_ord=order_ord.id_ord")
    orders = list(orders)
    objs = []
    for order in orders:
        if [order[1]] not in objs:
            objs += [[order[1]]]
    for obj in objs:
        for order in orders:
            if order[1] in obj:
                obj += [order[5], order[6]]
    for i, obj in enumerate(objs):
        print("Commande n", i, obj)


def api_add_dish(dish):
    cursor.execute(
        "INSERT INTO dish_dsh (dsh_name, dsh_price) VALUES (:name, :price)", dish)
    database.commit()


def api_show_dishes():
    os.system('clear')
    dishes = cursor.execute("SELECT * FROM dish_dsh")
    for dish in dishes:
        print("id", dish[0], " | ", dish[1], "\t| ", dish[2], "E")

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
    price = [10, 3, 14, 8]
    order = {}
    order["order"] = []
    os.system('clear')
    table_id = int(input("Numero de table : "))
    os.system('clear')
    api_show_dishes()
    while True:
        std_in = input("Ajouter un plat (y/n)")
        if std_in == "y" or std_in == "":
            dish_id = int(input("Indiquer l'id du plat : "))
            order["table"] = table_id
            order["order"] += [{"dish": dish_id, "price": price[dish_id]}]
        elif std_in == "n":
            return order


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
    while True:
        std_in = app_menu()
        match std_in:
            case "0":
                api_add_order(add_order())
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
