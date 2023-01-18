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


def custom_input(lst, message):
    # print(lst)
    std_in = input('\033[92m' + message + '\033[0m')
    if type(lst) == str:
        i = 0
        while(i < len(std_in) and std_in[i]):
            if std_in[i] not in lst:
                std_in = input('\033[91mMauvaise entree : \033[0m')
                i = 0
            else:
                i += 1
    else:
        while std_in not in lst:
            std_in = input('\033[91mMauvaise entree : \033[0m')
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
            "INSERT INTO order_dish_odh (id_ord, id_dsh) VALUES (?,?)", [*id_order, dish])
    database.commit()


def api_add_dish(dish):
    cursor.execute(
        "INSERT INTO dish_dsh (dsh_name, dsh_price) VALUES (:name, :price)", dish)
    database.commit()


def api_show_dishes():
    print("#############  MENU  #############")
    dishes = cursor.execute("SELECT * FROM dish_dsh")
    for dish in dishes:
        print("id", dish[0], " | ", dish[1], "\t| ", dish[2], "E")


def api_choose_waiter():
    waiters = cursor.execute("SELECT * FROM waiter_wtr")
    lst = []
    for waiter in waiters:
        print("id", waiter[0], " | ", waiter[1], " ", waiter[2])
        lst += [str(waiter[0])]
    return int(custom_input(lst, 'Selectionnez un id : '))


def api_show_table():
    tables = cursor.execute("SELECT * FROM table_tbl")
    table_ids = []
    for table in tables:
        table_ids += [table[0]]
    print("id tables : ", *table_ids)


def api_show_orders():

    orders = cursor.execute(
        "SELECT * FROM order_ord")
    order_ids = []
    for order in orders:
        print(order[0], '\t', order[1])
        order_ids += [str(order[0])]
    if custom_input(["y", "n"], "Afficher details (y/n) : ") == 'y':
        id_order = custom_input(order_ids, "Selectionner un id : ")
        details = cursor.execute(
            'SELECT * FROM dish_dsh INNER JOIN order_dish_odh ON dish_dsh.id_dsh=order_dish_odh.id_dsh AND order_dish_odh.id_ord=(?)', [id_order])
        for detail in details:
            print(detail[1],"\t",detail[2])


def api_show_order_by_table_id():
    api_show_table()
    tables = cursor.execute('SELECT * FROM table_tbl')
    table_ids = []
    for table in tables:
        table_ids += [str(table[0])]
    std_in = custom_input(table_ids, "Selectionner une table : ")

    orders = cursor.execute(
        "SELECT * FROM order_ord WHERE id_tbl = (?)", std_in)
    for order in orders:
        print(order[0],'\t',order[1])


def api_update_order():

    orders = cursor.execute(
        "SELECT * FROM order_ord")
    order_ids = []
    for order in orders:
        print(order[0],'\t',order[1])
        order_ids += [str(order[0])]
    id_order = custom_input(order_ids, "Selectionnez un id : ")
    orders = cursor.execute(
        "SELECT * FROM dish_dsh INNER JOIN order_dish_odh ON dish_dsh.id_dsh=order_dish_odh.id_dsh AND order_dish_odh.id_ord = (?)", [id_order])
    for order in orders:
        print(order[0],"\t",order[1],"\t",order[2])
    dish_ids = []
    dishes = cursor.execute("SELECT * FROM dish_dsh")
    for dish in dishes:
        dish_ids += [str(dish[0])]
    api_show_dishes()
    while custom_input(['y', 'n'], "Ajouter un plat (y/n) : ") == 'y':
        id_dish = custom_input(dish_ids, "Slectionnez un id : ")
        cursor.execute(
            "INSERT INTO order_dish_odh (id_ord, id_dsh) VALUES (?,?)", [id_order, id_dish])
    while custom_input(['y', 'n'], "Supprimer un plat (y/n) : ") == 'y':
        for order in orders:
            print(order[0],"\t",order[1],"\t",order[2])
        id_dish = custom_input(dish_ids, "Slectionnez un id : ")
        cursor.execute(
            'DELETE FROM order_dish_odh WHERE order_dish_odh.id_ord=(?) AND order_dish_odh.id_dsh=(?)', [id_order, id_dish])
    database.commit()
    details = cursor.execute(
            'SELECT * FROM dish_dsh INNER JOIN order_dish_odh ON dish_dsh.id_dsh=order_dish_odh.id_dsh AND order_dish_odh.id_ord=(?)', [id_order])
    for detail in details:
        print(detail[1],"\t",detail[2])


def api_delete_order_by_id():

    orders = cursor.execute(
        "SELECT * FROM order_ord")
    ids = []
    for order in orders:
        print(order[0], '\t', order[1])
        ids += [str(order[0])]
    id_order = str(custom_input(ids, "Selectionnez un id : "))
    print(id_order)
    cursor.execute(
        "DELETE FROM order_ord WHERE order_ord.id_ord = (?)", [id_order])
    database.commit()


#######################################################################################
#                        TERMINAL FUNCTIONS                                           #
#######################################################################################


def app_menu():
    print("\033[94m0 - Ajouter une commande")
    print("1 - Modifier une commande")
    print("2 - Supprimer une commande")
    print("3 - Voir les commandes")
    print("4 - Voir les commandes par table")
    print("5 - Ajouter un plat")
    print("6 - Afficher les plats")
    print("7 - Quitter\033[0m")
    return custom_input(['0', '1', '2', '3', '4', '5', '6', '7'], 'Sectionner un id de ligne : ')

#######################################################################################
#                              APP FUNCTIONS                                          #
#######################################################################################


def add_order():
    order = {}
    dishes = []

    tables = cursor.execute('SELECT * FROM table_tbl')
    table_ids = []
    for table in tables:
        table_ids += [str(table[0])]
    api_show_table()
    table_id = int(custom_input(table_ids, "Numero de table : "))
    api_show_dishes()
    dish_ids = []
    dishes_ids = cursor.execute('SELECT * FROM dish_dsh')
    for dishes_id in dishes_ids:
        dish_ids += [str(dishes_id[0])]
    while True:
        std_in = custom_input(['y', 'n'], "Ajouter un plat (y/n) : ")
        if std_in == "y":
            dish_id = int(custom_input(dish_ids, "Indiquer l'id du plat : "))
            order["table"] = table_id
            dishes += [dish_id]
        elif std_in == "n":
            return order, dishes


def add_dish():
    dish = {}

    dish["name"] = input("Nom : ")
    dish["price"] = float(custom_input("0123456789.", "Prix : "))
    return dish


def prog_exit():
    database.close()
    exit()


def main():
    os.system('clear')
    db_init()
    global WAITER
    WAITER = api_choose_waiter()
    while True:
        std_in = app_menu()
        match std_in:
            case "0":  # ajouter une commande
                os.system('clear')
                order, dishes = add_order()
                if len(dishes):
                    api_add_order(order, dishes)
            case "1":  # modifier une commande
                os.system('clear')
                api_update_order()
            case "2":  # supprimer une commande
                os.system('clear')
                api_delete_order_by_id()
            case "3":  # afficher commande
                os.system('clear')
                api_show_orders()
            case "4":  # afficher commandes par table
                os.system('clear')
                api_show_order_by_table_id()
            case "5":  # ajouter un plat
                os.system('clear')
                api_add_dish(add_dish())
            case "6":  # afficher un plat
                os.system('clear')
                api_show_dishes()
            case "7":  # quitter
                prog_exit()


main()
