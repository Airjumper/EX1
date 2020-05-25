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
            sql = '''INSERT INTO Asset (assetType_id, asset_name) VALUES(?,?)'''
            cur = con.cursor()
            cur.execute(sql,newAsset)
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

#for adding new asset to Asset Details table
def create_newAssetDetails(newAssetDetails):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO AssetDetails (asset_id,key_name, key_value, created_date, 
                                                modified_date) VALUES(?,?,?,?,?)'''
            cur = con.cursor()
            cur.execute(sql,newAssetDetails)
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

#for adding new assets to rent table
def create_newRentrecord(rent):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO Rent(user_id, asset_id,date_rental) VALUES(?,?,?)'''
            cur = con.cursor()
            cur.execute(sql,rent)
            con.commit() #to finanlise the changes in the database
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

#find user id by using email
def retrieveUserID(email):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT user_id FROM User WHERE user_email = (?)", ([email]))
    userID = cur.fetchone()
    con.close()
    return userID

#find asset type id by using asset type name
def retrieveAssetTypeID(assetTypeName):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT assetType_id FROM AssetType WHERE assetType_name = (?)", ([assetTypeName]))
    assetTypeID = cur.fetchone()
    print('winter is coming')
    print(assetTypeID)
    con.close()
    return assetTypeID
    

#to make the new asset type appear in the dropdown list
def getAssetType():
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT assetType_name FROM AssetType")
    rows = cur.fetchall()
    con.close()
    return rows

#to store the new asset type in the database
def create_newAssetType(assetType):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO AssetType(assetType_name) VALUES(?)'''
            cur = con.cursor()
            cur.execute(sql,[assetType])
            con.commit() #to finanlise the changes in the database
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

#for adding new site details to Site table
def create_newSite(newSite):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO Site (site_location, site_address, site_device, device_name, serial, ip_address, mobile_no, sim, computer, PC_username, PC_password, printer, projectManager) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            cur = con.cursor()
            cur.execute(sql,newSite)
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()


def getAssetValues(id):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT a.asset_id, a.asset_name , GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE a.asset_id = (?)", ([id]))
            rows = cur.fetchall()
            return rows
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()



def getAssetKeys(id):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE a.asset_id = (?)", ([id]))
            rows = cur.fetchall()
            return rows
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()


def updateAssetName(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("UPDATE Asset SET asset_name = ? WHERE asset_id = ?", (asset))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()

def updateAssetDetails(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("UPDATE AssetDetails SET key_value = ?, modified_date = ? WHERE asset_id = ? AND key_name = ?", (asset))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()

def deleteAsset(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Asset WHERE asset_id = ?", (asset))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()

def deleteAssetDetails(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM AssetDetails WHERE asset_id = ?",(asset))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()