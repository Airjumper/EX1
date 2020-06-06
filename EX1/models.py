#import sqlite3 as sql
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date

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

#for updating user details 
def updateUser(user):
    con = create_connection("diona.db")
    
    try:
        with con:
            cur = con.cursor()
            cur.execute("UPDATE User SET user_name = ?, user_email = ?, user_phone = ? WHERE user_id = ?", (user))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

def getUserDetails(id):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE user_id = (?)", ([id]))
    userID = cur.fetchone()
    con.close()
    return userID

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

#for adding new assets to rent table
def createnewUser(email):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO User(user_email) VALUES(?)'''
            cur = con.cursor()
            cur.execute(sql,[email])
            con.commit() #to finanlise the changes in the database
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

#find user id by using asset ID
def retrieveUserEmailByAssetID(id):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT user_email FROM User u, Rent r WHERE r.user_id = u.user_id AND (r.date_return = '' or r.date_return IS NULL) AND r.asset_id = (?)", ([id]))
    userEmail = cur.fetchone()
    #userEmail = retrieveUserEmail(user_id)
    con.close()
    if userEmail:
        return userEmail[0]

#add End date on Rent record
def updateRentRecord(asset):
    con = create_connection("diona.db")
    
    try:
        with con:
            cur = con.cursor()
            cur.execute("UPDATE Rent SET date_return = ? WHERE asset_id = ?", (asset))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

#find asset type id by using asset type name
def retrieveAssetTypeID(assetTypeName):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT assetType_id FROM AssetType WHERE assetType_name = (?)", ([assetTypeName]))
    assetTypeID = cur.fetchone()
    con.close()
    return assetTypeID
    
#add End date on Rent record
def getAssetType(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT AssetType.assetType_name from AssetType, Asset where Asset.assetType_id = AssetType.assetType_id AND Asset.asset_id = ?", ([asset]))
            assetType = cur.fetchone()
    
    except sqlite3.IntegrityError:
        print ("couldn't add data")

    con.close()
    return assetType
    

#to make the new asset type appear in the dropdown list
def getAllAssetType():
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT DISTINCT assetType_name FROM AssetType")
            rows = cur.fetchall()
            return rows
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()

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

#for adding new users to User table
def create_newUsers(new_users):
    con = create_connection("diona.db")
    try:
        with con:
            sql = '''INSERT INTO User (user_name, user_email, user_phone) VALUES(?,?,?)'''
            cur = con.cursor()
            cur.execute(sql,new_users)
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
            #rows = cur.fetchall()
            #return rows
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
            #rows = cur.fetchall()
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()

def getSiteDetails(id):
    con = create_connection("diona.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Site WHERE site_id = (?)", ([id]))
    siteID = cur.fetchone()
    con.close()
    return siteID

def updateSite(site):
    con = create_connection("diona.db")
    print("updating site")
    try:
        with con:
            cur = con.cursor()
            cur.execute("UPDATE Site SET site_location = ?, site_address = ?, site_device = ?, device_name = ?, serial = ?, ip_address = ?, mobile_no = ?, sim = ?, computer = ?, PC_username = ?, PC_password = ?, printer = ?, projectManager = ? WHERE site_id = ?", (site))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    con.close()


def deleteAsset(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Asset WHERE asset_id = ?", (asset,))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()



def deleteUser(user):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM User WHERE user_id = ?", (user,))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()


def deleteSite(site):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Site WHERE site_id = ?", (site,))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()


def deleteAssetDetails(asset):
    con = create_connection("diona.db")
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM AssetDetails WHERE asset_id = ?",(asset,))
            return True
    except sqlite3.IntegrityError:
        print ("couldn't add data")
    
    con.close()