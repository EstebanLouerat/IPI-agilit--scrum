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
#                                     UTLS                                             #
########################################################################################

def  custom_input(list, message):
    print(list)
    std_in = input('\033[92m'+ message + '\033[0m')
    while std_in not in list:
        std_in = input("Mauvaise entree : ")
    return std_in


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
    curs = cursor.execute(
        "SELECT id_ord FROM order_ord ORDER BY id_ord DESC LIMIT 1")
    id_order = [cur[0] for cur in curs]
    for dish in dishes:
        cursor.execute(
            "INSERT INTO order_dish_odh (id_ord, id_dsh) VALUES (?,?)", [id_order,dish])
    database.commit()


def api_add_dish(dish):
    cursor.execute(
        "INSERT INTO dish_dsh (dsh_name, dsh_price) VALUES (:name, :price)", dish)
    database.commit()


def api_show_dishes():
    dishes = cursor.execute("SELECT * FROM dish_dsh")
    for dish in dishes:
        print("id", dish[0], " | ", dish[1], "\t| ", dish[2], "E")


def api_choose_waiter():
    os.system('clear')
    waiters = cursor.execute("SELECT * FROM waiter_wtr")
    lst = []
    for waiter in waiters:
        print("id", waiter[0], " | ", waiter[1], " ", waiter[2])
        lst += [str(waiter[0])]
    return custom_input(lst, 'Selectionnez un id : ')


def api_show_table():
    os.system('clear')
    tables = cursor.execute("SELECT * FROM table_tbl")
    for table in tables:
        print("id", table[0])


def api_show_orders():
    os.system('clear')
    orders = cursor.execute(
        "SELECT * FROM order_ord")
    for order in orders:
        print(order[0], '-', order[1])
    if custom_input(["y","n"],"Afficher details (y/n) : ") == 'y':
        id_order = input("Selectionner un id : ")
        details = cursor.execute(
            '''SELECT * FROM dish_dsh 
                INNER JOIN order_dish_odh 
                ON dish_dsh.id_dsh=order_dish_odh.id_dsh 
                AND order_dish_odh.id_ord=(?)''', id_order)
        for detail in details:
            print(detail[1]+"\t"+str(detail[2]))


def api_show_order_by_table_id():
    api_show_table()
    std_in = input("Selectionner une table : ")
    os.system('clear')
    orders = cursor.execute(
        "SELECT * FROM order_ord WHERE id_tbl = (?)", std_in)
    for order in orders:
        print(order[0], order[1])


def api_update_order():
    os.system('clear')
    orders = cursor.execute(
        "SELECT * FROM order_ord")
    for order in orders:
        print(order[0], '-', order[1])
    id_order = input("Selectionnez un id : ")
    orders = cursor.execute(
        "SELECT * FROM dish_dsh INNER JOIN order_dish_odh ON dish_dsh.id_dsh=order_dish_odh.id_dsh AND order_dish_odh.id_ord = (?)", id_order)
    for order in orders:
        print(order)
    while input("Ajouter un plat (y/n) : ") == 'y':
        api_show_dishes()
        id_dish = input("Slectionnez un id : ")
        cursor.execute(
            "INSERT INTO order_dish_odh (id_ord, id_dsh) VALUES (?,?)", [id_order, id_dish])
    while input("Supprimer un plat (y/n)") == 'y':
        for order in orders:
            print(order)
        id_dish = input("Slectionnez un id : ")
        cursor.execute(
            '''DELETE FROM order_dish_odh 
                WHERE order_dish_odh.id_ord=(
                    SELECT order_dish_odh.id_ord 
                    FROM order_dish_odh 
                    WHERE order_dish_odh.id_ord=(?) 
                    AND order_dish_odh.id_dsh=(?)
                    LIMIT 1
                )''', [id_order, id_dish])
    database.commit()


def api_delete_order_by_id():
    os.system('clear')
    orders = cursor.execute(
        "SELECT * FROM order_ord")
    for order in orders:
        print(order[0], '-', order[1])
    id_order = input("Selectionnez un id : ")
    cursor.execute(
        "DELETE FROM order_ord WHERE order_ord.id_ord = (?)", id_order)
    database.commit()


#######################################################################################
#                        TERMINAL FUNCTIONS                                           #
#######################################################################################


def app_menu() -> str:
    print("0 - Ajouter une commande")
    print("1 - Modifier une commande")
    print("2 - Supprimer une commande")
    print("3 - Voir les commandes")
    print("4 - Voir les commandes par table")
    print("5 - Ajouter un plat")
    print("6 - Afficher les plats")
    print("7 - Quitter")
    return custom_input('01234567', 'Sectionner une commande : ')

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
        std_in = input("Ajouter un plat (y/n) : ")
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
    WAITER = api_choose_waiter()
    
    # [str(*data) for data in cursor.execute("SELECT id_tbl FROM table_tbl")]

    # WAITER = int(input("Selectionner un id : "))
    while True:
        std_in = app_menu()
        match std_in:
            case "0":  # ajouter une commande
                order, dishes = add_order()
                api_add_order(order, dishes)
            case "1":  # modifier une commande
                api_update_order()
            case "2":  # supprimer une commande
                api_delete_order_by_id()
            case "3":  # afficher commande
                api_show_orders()
            case "4":  # afficher commandes par table
                api_show_order_by_table_id()
            case "5":  # ajouter un plat
                api_add_dish(add_dish())
            case "6":  # afficher un plat
                api_show_dishes()
            case "7":  # quitter
                prog_exit()


main()
