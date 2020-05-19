#import sqlite3 as sql
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

#for login page
def retrieveAccount(id, password):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM Admin WHERE id = (?) and password = (?)", (id, password))
    admin = cur.fetchone()
    con.close()
    return admin

#for adding new asset to asset table
def create_newAsset(newAsset):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO Asset (asset_name, asset_type) VALUES(?,?)'''
            cur = con.cursor()
            cur.execute(sql,newAsset)
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print("couldn't add data")
    con.close()

#for adding new asset to Asset Details table
def create_newAssetDetails(newAssetDetails):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO AssetDetails (asset_id,asset_IEMI, asset_make, asset_model, 
                                                asset_pin, asset_serialNo,asset_phNo,
                                                asset_hardware,asset_tag,asset_device,asset_status,
                                                asset_purchaseDate,Notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            cur = con.cursor()
            cur.execute(sql,newAssetDetails)
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print("couldn't add data")
    con.close()

#for adding new assets to rent table
def create_newRentrecord(rent):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO Rent(user_id, asset_id) VALUES(?,?)'''
            cur = con.cursor()
            cur.execute(sql,rent)
            con.commit() #to finanlise the changes in the database
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print("couldn't add data")
    con.close()

#find user id by using email
def retrieveUserID(email):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT user_id FROM User WHERE user_email = (?)", ([email]))
    userID = cur.fetchone()
    con.close()
    return userID

#to make the new asset type appear in the dropdown list
def getAssetType():
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT assetType_name FROM AssetType")
    rows = cur.fetchall()
    con.close()

    return rows

