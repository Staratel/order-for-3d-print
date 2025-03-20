import sqlite3
from math import ceil



def create_table():
    conn = sqlite3.connect('plastic.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS FDM_plastic (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    weight REAL NOT NULL,
    cost REAL NOT NULL,
    price_per_gram REAL NOT NULL
    )""")

    conn.commit()
    conn.close()

def add_plastic():
    plastic = {}

    plastic["name"] = input("Название пластика: ")
    plastic["date"] = input("Дата покупки в формате ГГГГ-ММ-ДД: ")
    plastic["weight"] = float(input("Вес: "))
    plastic["cost"] = float(input("Стоимость: "))
    plastic["price_per_gram"] = ceil(float((plastic["cost"] / plastic["weight"]) * 1000 )) / 1000

    return plastic

def create_plastic(plastic):
    conn = sqlite3.connect('plastic.db')
    cur = conn.cursor()

    cur.execute("""INSERT INTO FDM_plastic (name, date, weight, cost, price_per_gram) VALUES (?, ?, ?, ?, ?)""",
                (plastic["name"], plastic["date"], plastic["weight"], plastic["cost"], plastic["price_per_gram"]))

    conn.commit()
    conn.close()