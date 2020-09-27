import sqlite3
from bit import PrivateKeyTestnet
import bit

DB = "wallet.db"


def create_tables():
    sql = """ CREATE TABLE IF NOT EXISTS "user" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT NOT NULL, `password` TEXT NOT NULL, `email` TEXT NOT NULL UNIQUE, `wallet_id` TEXT UNIQUE )"""
    conn = sqlite3.connect(DB)
    conn.execute(sql)
    conn.commit()
    conn.close()


def register_user(data):
    sql = ''' INSERT INTO user(name,password,email, wallet_id)
              VALUES(?,?,?,?) '''
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql, (data["name"], data["password"],
                      data["email"], create_wallet()["wallet_id"]))
    conn.commit()

    sql = """INSERT INTO wallet(name,password,email)
              VALUES(?,?,?) """


def login_user(data):
    sql = ''' SELECT * FROM user
              WHERE password=? AND email=? '''
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql, (data["password"], data["email"]))
    return cur.fetchone()


def get_user_by_email(email):
    sql = ''' SELECT name, email, wallet_id FROM user
              WHERE email=?'''
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql, (email,))
    res = cur.fetchone()

    wallet = get_wallet(res[2])

    return {"name": res[0], "email": res[1],
            "address": wallet.address,
            "balance": wallet.get_balance(currency="mbtc"),
            "wallet_id": wallet.to_wif()}


def create_wallet():
    my_key = PrivateKeyTestnet()
    print(my_key.version)
    print(my_key.to_wif())
    print(my_key.address)
    print(my_key.get_balance())
    return {"wallet_id": my_key.to_wif(), "address": my_key.address}


def get_wallet(wallet_id):
    return PrivateKeyTestnet(wif=wallet_id)


def send_btc(wallet_id, amount, receiver_address):
    my_key = PrivateKeyTestnet(wif=wallet_id)
    tx_hash = my_key.send([(receiver_address, amount, 'mbtc')])
    print(tx_hash)
    return tx_hash
