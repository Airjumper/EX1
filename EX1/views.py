"""
Routes and views for the flask application.
"""

from datetime import datetime
from datetime import date
from flask import render_template
from EX1 import app
from EX1 import models as dbHandler
from flask import request, redirect, url_for, session, jsonify
from io import TextIOWrapper
import csv

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_connection(r"diona.db")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('welcome.html',
                            title='Home Page',
                            year=datetime.now().year,)

@app.route('/login')
def login():
     """Renders the login page."""
     return render_template('login.html',
                             title='Login',
                             year=datetime.now().year,
                             message='Login Page',
                             msg='')


@app.route('/login_success')
def login_success():

     if 'loggedin' in session:
         #"""Renders the login page."""
         return render_template('admin_main.html',
                                 username=session['id'],
                                 title='Login',
                                 year=datetime.now().year,
                                 message='Main page')
     return render_template('login.html')



@app.route('/login_request', methods=['POST', 'GET'])
def login_request():
    # error = None
     if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']
        account = dbHandler.retrieveAccount(id, password)
        # If the account exists in Admin table in the database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account
            #session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('login_success'))
            #return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password! Please try again!'
        
        # Show the login form with message (if any)
        return render_template('login.html',
                                title='Login',
                                year=datetime.now().year,
                                message='Login Page',
                                error=True,
                                msg=msg)
     else:
         return render_template('login.html',
                                title='Login',
                                year=datetime.now().year,
                                message='Login Page',
                                error=True,
                                msg='')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('loggedin', None)
    session.pop('id', None)
    return redirect(url_for('home'))



@app.route('/adminview')
def adminview():  
    # Check if user is loggedin
    if 'loggedin' in session:
        
        types = dbHandler.getAllAssetType()
   
        return render_template('adminview.html', 
                                username=session['id'],   
                                title='Admin View',
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

    
@app.route('/adminview/mobile')
def admin_mobile():

    # Check if user is loggedin
    if 'loggedin' in session:
        types = dbHandler.getAllAssetType()
        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_id, a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]

        for x in range(len(rows)):
            results[x] = rows[x][3].split(',')      
        # Get key_name rows

        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_id, a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")

        return render_template('admin_mobile.html',
                                username=session['id'],
                                title='Admin View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][2].split(','),
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/adminview/tablet')
def admin_tablet():

    if 'loggedin' in session:
        types = dbHandler.getAllAssetType()
        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_id, a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]

        for x in range(len(rows)):
            results[x] = rows[x][3].split(',')      
        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_id, a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")

        #"""Renders the user page."""
        return render_template('admin_tablet.html',
                                username=session['id'],
                                title='Admin View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][2].split(','),
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  

@app.route('/adminview/laptop')
def admin_laptop():

    if 'loggedin' in session:
        types = dbHandler.getAllAssetType()
        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_id, a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
        rows = name_types.fetchall()

        results = [0 for x in range(len(rows))]

        for x in range(len(rows)):
            results[x] = rows[x][3].split(',')      
        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_id, a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")

        # """Renders the user page."""
        return render_template('admin_laptop.html',
                                title='Admin View',
                                username=session['id'],
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][2].split(','),
                                type = types,
                                year=datetime.now().year)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/userview')
def userview():

    types = dbHandler.getAllAssetType() 
   
    # """Renders the user page."""
    return render_template('userview.html',
                            title='User View',
                            type = types,
                            year=datetime.now().year)

@app.route('/userview/mobile')
def mobile():
        types = dbHandler.getAllAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_id")

        
        return render_template('userview_mobile.html', 
                                title='User View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)


@app.route('/userview/tablet')
def tablet():
        types = dbHandler.getAllAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_id")
       
    # """Renders the user page."""
        return render_template('userview_tablet.html',
                                title='User View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)

@app.route('/userview/laptop')
def laptop():
        types = dbHandler.getAllAssetType()

        conn = sqlite3.connect(r"diona.db")
        # Get name and type of an asset, and get key_value store as results
        cur = conn.cursor() 
        name_types = cur.execute("SELECT a.asset_name , t.assetType_name, GROUP_CONCAT(d.key_value) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
        rows = name_types.fetchall()
        results = [0 for x in range(len(rows))]
        for x in range(len(rows)):
            results[x] = rows[x][2].split(',')      

        # Get key_name rows
        cur2 = conn.cursor() 
        details_keys = cur2.execute("SELECT a.asset_name, GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_id")
    # """Renders the user page."""
        return render_template('userview_laptop.html',
                                title='User View',
                                rows = rows,
                                res = results,
                                keys = details_keys.fetchall()[0][1].split(','),
                                type = types,
                                year=datetime.now().year)



@app.route('/import')
def import_main():
        templates = ["mobile_template.csv","laptop_template.csv","tablet_template.csv"]
        msg = ''

        return render_template('import_and_templates.html', 
                                username=session['id'],   
                                title='Import/Export',  
                                files = templates,
                                msg = msg,
                                year=datetime.now().year)
  

@app.route('/import_request', methods=['POST', 'GET'])
def import_request():

     if request.method == 'POST':
       
        new_asset = ''
        asset_id = ''
       
        file = request.files['upload_file']

        csvf = TextIOWrapper(file, encoding='utf-8')
        csv_reader = csv.reader(csvf, delimiter=',')
        headers = next(csv_reader, None)
 
        for row in csv_reader:

            # get name and type of input asset
            name = row[0]
            type = row[1]
            assetType_id = dbHandler.retrieveAssetTypeID(type)
            
            #create new row in Asset table
            if assetType_id:
                new_asset = (assetType_id[0],name)
            if new_asset:
                asset_id = dbHandler.create_newAsset(new_asset)

            #insert details of new asset
            if asset_id:
                data = row[2:]
                keys = headers[2:]
                new_dict = dict(zip(keys,data))

                for key, value in new_dict.items():
                    new_assetDetails = (asset_id, key, value, date.today(), date.today())    
                    dbHandler.create_newAssetDetails(new_assetDetails)

                msg = 'Successfully insert...'
            else:
                # Table doesnt exist.
                msg = 'Error inserting into database.'

        return render_template('import_and_templates_confirm.html',
                               username=session['id'],
                               msg = msg,
                               year=datetime.now().year)
       


@app.route('/new_assets')
def new_assets():
    """Renders the New Assets page."""
    menu = dbHandler.getAllAssetType()
   
    return render_template('new_assets.html',
                            username=session['id'],
                            title='New Assets',
                            year=datetime.now().year,
                            message='New assets',
                            menu = menu)


@app.route('/add_asset', methods=['POST', 'GET'])
def add_asset():
    #if the form is submittied, declare the variable of new_asset, asset_id and user_id
    if request.method == 'POST':
        new_asset = ''
        asset_id = ''
        user_id = ''
        #get the asset type from the form to get assetTypeID    
        if request.form['assetType']:
            assetType_id = dbHandler.retrieveAssetTypeID(request.form['assetType'])
        else:
            msg = 'Enter all details'
        
        #prepare new asset from form data, to get the asset record (name and type) first
        if request.form['Name']:
            if assetType_id:
                new_asset = (assetType_id[0], request.form['Name'])
            else:
                #add to assess type and continue creating asset
                #print(request.form['assetType'])
                assetType_id = dbHandler.create_newAssetType(request.form['assetType'])
                new_asset = (assetType_id, request.form['Name'])
        else:
            msg = 'Enter all details'        
        
        #create new asset and get asset id
        if new_asset:
            asset_id = dbHandler.create_newAsset(new_asset)
        else:
            msg = 'Error! Cannot create new asset.'
        
        #get the email from the form to get userID
        user_id = dbHandler.retrieveUserID(request.form['assetAssigned'])

        if user_id: 
            if asset_id:
                if user_id:
                    rent = (user_id[0],asset_id,date.today())
                    dbHandler.create_newRentrecord(rent)
        else:
            #create new user
            user_id = dbHandler.createnewUser(request.form['assetAssigned'])
            if asset_id:
                if user_id:
                    rent = (user_id,asset_id,date.today())
                    dbHandler.create_newRentrecord(rent)
            
        #Continue adding into Asset Details if asset is added in Asset table
        if asset_id:
            #convert form data into dictionary
            data = request.form.to_dict()
            #remove type and name before adding to asset details table
            data.pop('assetType', None)
            data.pop('assetName', None)
            data.pop('assetAssigned', None)
            
            
            #add all details in data dictionary to asset details table
            for key, value in data.items():
                new_assetDetails = (asset_id, key, value, date.today(), date.today())    
                dbHandler.create_newAssetDetails(new_assetDetails)
 
            msg = "Inserted data successfully"
        else:
            # Table doesnt exist.
            msg = 'Error inserting into database.'
        #print(user_id)
        pageName = page_name(request.form['assetType'])

        menu = dbHandler.getAllAssetType()

        # Show the form with message (if any)
        return render_template( pageName,
                                title='New Assets',
                                year=datetime.now().year,
                                message='New Assets',
                                menu = menu,
                                msg=msg)
    else:
        return render_template('new_assets.html',
                                title='New Assets',
                                year=datetime.now().year,
                                message='New Assets',
                                menu = menu,
                                error=True,
                                msg=''
                                )


def page_name(x):
            return {
                'Mobile Phone': 'new_assetsMobile.html',
                'Tablet': 'new_assetsTablet.html',
                'Laptop': 'new_assetsLaptop.html'
            }.get(x, 'admin_main.html')


@app.route('/newAsset_Default.html')
def new_assetDefault():
    """Renders the New Assets Default page."""
    #to make all the asset types appear on the page
    menu = dbHandler.getAllAssetType()
    return render_template('new_assetsDefault.html',
                            title='New Assets for Mobile',
                            year=datetime.now().year,
                            message='New assets Mobile',
                            menu = menu)


@app.route('/newAsset_Mobile')
def new_assetsMobile():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    return render_template('new_assetsMobile.html',
                            title='New Assets for Mobile',
                            year=datetime.now().year,
                            message='New assets Mobile',
                            menu = menu)

@app.route('/newAsset_Tablet')
def new_assetsTablet():
    """Renders the New Assets Tablet page."""
    menu = dbHandler.getAllAssetType()
    return render_template('new_assetsTablet.html',
                            title='New Assets for Tablet',
                            year=datetime.now().year,
                            message='New assets Tablet',
                            menu = menu)

@app.route('/newAsset_Laptop')
def new_assetsLaptop():
    """Renders the New Assets Laptop page."""
    menu = dbHandler.getAllAssetType()
    return render_template('new_assetsLaptop.html',
                            title='New Assets for Laptop',
                            year=datetime.now().year,
                            message='New assets Laptop',
                            menu = menu)


@app.route('/view_users')
def view_users():
    """Renders the View Users page."""

    if 'loggedin' in session:

        conn = sqlite3.connect(r"diona.db")
        cur = conn.cursor() 

        # Get all user details from user table
        query = cur.execute("SELECT * FROM User")

        rows = query.fetchall()

        return render_template('view_users.html',
                                username=session['id'],
                                title='Admin View',
                                rows = rows,
                                year=datetime.now().year)



@app.route('/add_users')
def add_users():
    """Renders the Add Users page."""

    user_details = ''
    submit_url = ''

    #if asset is passed in URL parameter, use it to fetch its details and populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        user_details = dbHandler.getUserDetails(request.args.get('id'))
        submit_url = "submit_update_user"
    else:
        submit_url = 'submit_add_users'

    return render_template('new_user_details.html',
                            title='Add Users',
                            user = user_details,
                            submit_url = submit_url,
                            year=datetime.now().year,
                            message='Add Users page. Nice.')

@app.route('/update_users')
def update_users():
    """Renders the Add Users page."""

    user_details = ''
    submit_url = ''

    #if asset is passed in URL parameter, use it to fetch its details and populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        user_details = dbHandler.getUserDetails(request.args.get('id'))
        submit_url = "submit_update_user"
    else:
        submit_url = 'submit_add_users'

    return render_template('update_user.html',
                            title='Add Users',
                            user = user_details,
                            submit_url = submit_url,
                            year=datetime.now().year)


@app.route('/submit_update_user', methods=['POST', 'GET'])
def submit_update_user():
    #if the form is submittied, declare the variable of new_users and user_id 
    if request.method == 'POST':
        user = (request.form['userName'],request.form['userEmail'],request.form['userPhone'],request.form['user_id'])
        user_id = dbHandler.updateUser(user)

        if user_id:
            # Show the form with message (if any)
            msg = 'user table has been updated'
        else:
            msg = 'Error'


    types = dbHandler.getAllAssetType()

    conn = sqlite3.connect(r"diona.db")
        
        # Get name and type of an asset, and get key_value store as results

    cur = conn.cursor() 

    query = cur.execute("SELECT * FROM User")

    rows = query.fetchall()

    return render_template('view_users.html',
                            username=session['id'],
                            title='View users',
                            rows = rows,
                            msg = msg,
                            year=datetime.now().year)


@app.route('/submit_add_users', methods=['POST', 'GET'])
def submit_add_users():
    #if the form is submittied, declare the variable of new_users and user_id 
    if request.method == 'POST':
        new_users = (request.form['userName'],request.form['userEmail'],request.form['userPhone'])
        user_id = dbHandler.create_newUsers(new_users)

        if user_id:
            # Show the form with message (if any)
            msg = 'new user is created successfully'
        else:
            msg = 'Error'

        return render_template('new_user_details.html',
                                title='Add Users',
                                year=datetime.now().year,
                                message='Add Users',
                                msg=msg)




@app.route('/history')
def view_history():
    if 'loggedin' in session:
       
        conn = sqlite3.connect(r"diona.db")

        conn.row_factory = sqlite3.Row
            # Get name and type of an asset, and get key_value store as results
        rows = conn.execute("SELECT u.user_name AS Username, a.asset_Name AS Asset, r.date_rental AS Start, r.date_return AS Return FROM Rent r, Asset a INNER JOIN User u on u.user_id = r.user_id AND a.asset_id = r.asset_id ")
        col_names = rows.fetchone()
        headers = col_names.keys()

        cur2 = conn.cursor() 
        results = cur2.execute("SELECT u.user_name, a.asset_Name, r.date_rental, r.date_return FROM Rent r, Asset a INNER JOIN User u on u.user_id = r.user_id AND a.asset_id = r.asset_id ")


    return render_template('view_history.html',
                            username=session['id'],
                            title = 'User History',
                            header = headers,
                            list = results.fetchall(),
                            year = datetime.now().year,)


@app.route('/asset_type')
def asset_type():
    """Renders the Asset Type page."""
    return render_template('new_asset_type.html',
                            username=session['id'],
                            title='Asset Type',
                            year=datetime.now().year,
                            message='Asset type')

@app.route('/site_info')
def site_default():
    """Renders the Site Details page."""
    return render_template('site_default.html',
                            username=session['id'],
                            title='Site Details',
                            year=datetime.now().year,
                            message='Site Details')

@app.route('/site_details')
def site_all_details():

    # Check if user is loggedin
    if 'loggedin' in session:
        conn = sqlite3.connect(r"diona.db")

        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM Site")
        col_names = rows.fetchone()
        headers = col_names.keys()

        
        cur2 = conn.cursor() 
        results = cur2.execute("SELECT * FROM Site")

        """Renders the Site Details page."""
        return render_template('site_all_details.html',
                            username=session['id'],
                            title='Site Details',
                            year=datetime.now().year,
                            message='Site Details',
                            header = headers,
                            rows = results.fetchall())
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



    
@app.route('/submit_site_details', methods=['POST', 'GET'])
def submit_site_details():
    #if the form is submittied, declare the variable of new_siteDetails and
    #site_id
    if request.method == 'POST':
        new_siteDetails = (request.form['siteLocation'],request.form['siteAddress'],request.form['siteDevice'],request.form['siteDeviceName'],request.form['siteDeviceSerial'],request.form['siteIpAddress'],request.form['siteMobileNo'],request.form['siteMobileSim'],request.form['siteComputer'],request.form['sitePcUsername'],request.form['sitePcPassword'],request.form['sitePrinter'],request.form['siteProjectMgr'])
        site_id = dbHandler.create_newSite(new_siteDetails)

        if site_id:
            # Show the form with message (if any)
            msg = 'Site details are saved successfully'
        else:
            msg = 'Error'

        return render_template('site_details.html',
                                title='Site Details',
                                year=datetime.now().year,
                                message='Site Details',
                                msg=msg)



#handle update asset POST request
@app.route('/update_asset', methods=['POST', 'GET'])
def update_asset():
    #if the form is submittied, declare the variable of new_asset, asset_id and user_id
    if request.method == 'POST':
        new_asset = ''
        asset_id = ''
        user_id = ''
        type = ''
        page_name = ''
        data = request.form.to_dict()
        dateTimeObj = datetime.now()

        #prepare asset from form data
        if request.form['assetID']:
            asset_id = request.form['assetID']

            type = dbHandler.getAssetType(request.form['assetID'])
            #update asset name
            dbHandler.updateAssetName((request.form['assetName'],request.form['assetID']))

            #get current user email that has selected asset
            current_user_email = dbHandler.retrieveUserEmailByAssetID(request.form['assetID'])
            #print("Current user id " + current_user_email)

            #handle email comparison
            if request.form['assetAssigned']:
                if current_user_email != request.form['assetAssigned']:
                    #add return date on current rent record and create with new user details
                    print("update user")
                    
                    timestampStr = dateTimeObj.strftime("%Y-%m-%d")
                    print(timestampStr)
                    record = (timestampStr,request.form['assetID'])
                    dbHandler.updateRentRecord(record)
                    user_id = dbHandler.retrieveUserID(request.form['assetAssigned'])
                    if asset_id:
                        if user_id:
                            rent = (user_id[0],asset_id,date.today())
                            dbHandler.create_newRentrecord(rent)

                elif current_user_email == request.form['assetAssigned']:
                    print("same user, don't do anything")
            else:
                #user is removed from current asset, adding return date on rent table
                timestampStr = dateTimeObj.strftime("%Y-%m-%d")
                print(timestampStr)
                record = (timestampStr,request.form['assetID'])
                dbHandler.updateRentRecord(record)
            
            #remove unnecessary key names
            
            data.pop('assetType', None)
            data.pop('assetName', None)
            data.pop('assetID', None)
            data.pop('assetAssigned', None)
            
            #loop through form data and update each asset values
            for key, value in data.items():
                new_assetDetails = (value, datetime.today(), asset_id, key)
                dbHandler.updateAssetDetails(new_assetDetails)
                msg = "Asset details are updated successfully."
        else:
            msg = 'Enter all details'
        
        menu = dbHandler.getAllAssetType()
        
        if (type[0] == 'Tablet'):
            page_name = 'admin_tablet'
        elif (type[0] == 'Mobile Phone'):
            page_name = 'admin_mobile'
        elif (type[0] == 'Laptop'):
            page_name = 'admin_laptop'
        else:
            page_name = 'admin_view'

        return redirect(url_for(page_name))

        # Show the form with message (if any)
        # url = 'admin_mobile.html'
        # return render_template(url,
        #         title='Admin Mobile View',
        #         year=datetime.now().year,
        #         menu = menu,
        #         msg = msg)
    else:
        return render_template('admin_mobile.html',
                                title='Admin Mobile View',
                                year=datetime.now().year,
                                message='',
                                menu = menu
                                )

@app.route('/mobile_update')
def update_assetsMobile():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    header = 'Update Asset - Mobile Phone'
    title = 'Update Asset for Mobile'
    submitURL = 'update_asset'
    asset_details = ''
    key_names = ''
    key_values = ''
    newdict = {}

    #if asset is passed in URL parameter, use it to fetch its details and
    #populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        keys = dbHandler.getAssetKeys(request.args.get('id'))
        key_names = [0 for x in range(len(keys))]
        for x in range(len(keys)):
            key_names[x] = keys[x][0].split(',')

        #get asset key values and add into key_values list
        asset_details = dbHandler.getAssetValues(request.args.get('id'))
        key_values = [0 for x in range(len(asset_details))]
        for x in range(len(asset_details)):
            key_values[x] = asset_details[x][2].split(',')
        

        #output = [0 for x in range(len(key_names))]
        #combine key name and key value into key-value dictionary before
        #sending back to form
        asset_kv_pair = {}
        asset_kv_pair = dict(zip(key_names[0], key_values[0]))

    else:
        header = 'Asset id is required.'

    return render_template('update_mobile.html',
                            username=session['id'],
                            title=title,
                            header=header,
                            year=datetime.now().year,
                            #message='New assets Mobile',
                            menu = menu,
                            submit_url = submitURL,
                            asset_details = asset_details,
                            asset_kv_pair = asset_kv_pair)


@app.route('/laptop_update')
def update_assetsLaptop():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    header = 'Update Asset - Laptop'
    title = 'Update Asset for Laptop'
    submitURL = 'update_asset'
    asset_details = ''
    key_names = ''
    key_values = ''
    newdict = {}

    #if asset is passed in URL parameter, use it to fetch its details and
    #populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        keys = dbHandler.getAssetKeys(request.args.get('id'))
        key_names = [0 for x in range(len(keys))]
        for x in range(len(keys)):
            key_names[x] = keys[x][0].split(',')

        #get asset key values and add into key_values list
        asset_details = dbHandler.getAssetValues(request.args.get('id'))
        key_values = [0 for x in range(len(asset_details))]
        for x in range(len(asset_details)):
            key_values[x] = asset_details[x][2].split(',')
        

        #output = [0 for x in range(len(key_names))]
        #combine key name and key value into key-value dictionary before
        #sending back to form
        asset_kv_pair = {}
        asset_kv_pair = dict(zip(key_names[0], key_values[0]))

    else:
        header = 'Asset id is required.'

    return render_template('update_laptop.html',
                            username=session['id'],
                            title=title,
                            header=header,
                            year=datetime.now().year,
                            #message='New assets Mobile',
                            menu = menu,
                            submit_url = submitURL,
                            asset_details = asset_details,
                            asset_kv_pair = asset_kv_pair)

@app.route('/tablet_update')
def update_assetsTablet():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    header = 'Update Asset - Tablet'
    title = 'Update Asset for Tablet'
    submitURL = 'update_asset'
    asset_details = ''
    key_names = ''
    key_values = ''
    newdict = {}

    #if asset is passed in URL parameter, use it to fetch its details and
    #populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        keys = dbHandler.getAssetKeys(request.args.get('id'))
        key_names = [0 for x in range(len(keys))]
        for x in range(len(keys)):
            key_names[x] = keys[x][0].split(',')

        #get asset key values and add into key_values list
        asset_details = dbHandler.getAssetValues(request.args.get('id'))
        key_values = [0 for x in range(len(asset_details))]
        for x in range(len(asset_details)):
            key_values[x] = asset_details[x][2].split(',')
        

        #output = [0 for x in range(len(key_names))]
        #combine key name and key value into key-value dictionary before
        #sending back to form
        asset_kv_pair = {}
        asset_kv_pair = dict(zip(key_names[0], key_values[0]))

    else:
        header = 'Asset id is required.'

    return render_template('update_tablet.html',
                            username=session['id'],
                            title=title,
                            header=header,
                            year=datetime.now().year,
                            #message='New assets Mobile',
                            menu = menu,
                            submit_url = submitURL,
                            asset_details = asset_details,
                            asset_kv_pair = asset_kv_pair)



#handle update asset POST request
@app.route('/delete_asset', methods=['POST', 'GET'])
def delete_asset():
    #if the form is submittied, declare the variable of new_asset, asset_id and
    #user_id
    if request.method == 'POST':
        new_asset = ''
        asset_id = ''
        user_id = ''
        data = request.form.to_dict()


        type = dbHandler.getAssetType(request.form['assetID'])
        
        #prepare asset from form data
        if request.form['assetID']:
            
            #remove unnecessary key names
            asset_id = request.form['assetID']
            data.pop('assetType', None)
            data.pop('assetName', None)
            data.pop('assetID', None)
            data.pop('assetAssigned', None)
            
            #loop through form data and delete each asset values

            
            dbHandler.deleteAssetDetails(asset_id)  

            #delete asset from Asset table 
            dbHandler.deleteAsset(asset_id)
            msg = "Asset details are updated successfully."
        else:
            msg = 'Enter all details'        

        menu = dbHandler.getAllAssetType()
        
        if (type[0] == 'Tablet'):
            page_name = 'admin_tablet'
        elif (type[0] == 'Mobile Phone'):
            page_name = 'admin_mobile'
        elif (type[0] == 'Laptop'):
            page_name = 'admin_laptop'
        else:
            page_name = 'admin_view'

        return redirect(url_for(page_name))

        # Show the form with message (if any)
        # url = 'admin_mobile.html'
        # return render_template(url,
        #         title='Admin Mobile View',
        #         year=datetime.now().year,
        #         menu = menu,
        #         msg = msg)
    else:
        return render_template('adminview.html',
                                username=session['id'],
                                title='Admin View',
                                year=datetime.now().year,
                                message='',
                                menu = menu)




@app.route('/delete_mobile')
def delete_mobile():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    header = 'Delete Asset - Mobile Phone'
    title = 'Delete Asset for Mobile'
    submitURL = 'delete_asset'
    asset_details = ''
    key_names = ''
    key_values = ''
    newdict = {}

    #if asset is passed in URL parameter, use it to fetch its details and
    #populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        keys = dbHandler.getAssetKeys(request.args.get('id'))
        key_names = [0 for x in range(len(keys))]
        for x in range(len(keys)):
            key_names[x] = keys[x][0].split(',')

        #get asset key values and add into key_values list
        asset_details = dbHandler.getAssetValues(request.args.get('id'))
        key_values = [0 for x in range(len(asset_details))]
        for x in range(len(asset_details)):
            key_values[x] = asset_details[x][2].split(',')
        

        #output = [0 for x in range(len(key_names))]
        #combine key name and key value into key-value dictionary before
        #sending back to form
        asset_kv_pair = {}
        asset_kv_pair = dict(zip(key_names[0], key_values[0]))

    else:
        header = 'Asset id is required.'

    return render_template('delete_mobile.html',
                            username=session['id'],
                            title=title,
                            header=header,
                            year=datetime.now().year,
                            #message='New assets Mobile',
                            menu = menu,
                            submit_url = submitURL,
                            asset_details = asset_details,
                            asset_kv_pair = asset_kv_pair)

@app.route('/delete_laptop')
def delete_laptop():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    header = 'Delete Asset - Laptop'
    title = 'Delete Asset for Laptop'
    submitURL = 'delete_asset'
    asset_details = ''
    key_names = ''
    key_values = ''
    newdict = {}

    #if asset is passed in URL parameter, use it to fetch its details and
    #populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        keys = dbHandler.getAssetKeys(request.args.get('id'))
        key_names = [0 for x in range(len(keys))]
        for x in range(len(keys)):
            key_names[x] = keys[x][0].split(',')

        #get asset key values and add into key_values list
        asset_details = dbHandler.getAssetValues(request.args.get('id'))
        key_values = [0 for x in range(len(asset_details))]
        for x in range(len(asset_details)):
            key_values[x] = asset_details[x][2].split(',')
        

        #output = [0 for x in range(len(key_names))]
        #combine key name and key value into key-value dictionary before
        #sending back to form
        asset_kv_pair = {}
        asset_kv_pair = dict(zip(key_names[0], key_values[0]))

    else:
        header = 'Asset id is required.'

    return render_template('delete_laptop.html',
                            username=session['id'],
                            title=title,
                            header=header,
                            year=datetime.now().year,
                            #message='New assets Mobile',
                            menu = menu,
                            submit_url = submitURL,
                            asset_details = asset_details,
                            asset_kv_pair = asset_kv_pair)

@app.route('/delete_tablet')
def delete_tablet():
    """Renders the New Assets Mobile page."""
    menu = dbHandler.getAllAssetType()
    header = 'Delete Asset - Tablet'
    title = 'Delete Asset for Tablet'
    submitURL = 'delete_asset'
    asset_details = ''
    key_names = ''
    key_values = ''
    newdict = {}

    #if asset is passed in URL parameter, use it to fetch its details and
    #populate form data
    if(request.args.get('id')):
        #get asset key names and add into key_names list
        keys = dbHandler.getAssetKeys(request.args.get('id'))
        key_names = [0 for x in range(len(keys))]
        for x in range(len(keys)):
            key_names[x] = keys[x][0].split(',')

        #get asset key values and add into key_values list
        asset_details = dbHandler.getAssetValues(request.args.get('id'))
        key_values = [0 for x in range(len(asset_details))]
        for x in range(len(asset_details)):
            key_values[x] = asset_details[x][2].split(',')
        

        #output = [0 for x in range(len(key_names))]
        #combine key name and key value into key-value dictionary before
        #sending back to form
        asset_kv_pair = {}
        asset_kv_pair = dict(zip(key_names[0], key_values[0]))

    else:
        header = 'Asset id is required.'

    return render_template('delete_tablet.html',
                            username=session['id'],
                            title=title,
                            header=header,
                            year=datetime.now().year,
                            #message='New assets Mobile',
                            menu = menu,
                            submit_url = submitURL,
                            asset_details = asset_details,
                            asset_kv_pair = asset_kv_pair)





@app.route('/delete_user_request', methods=['POST', 'GET'])
def delete_user_request():


 
    if request.method == 'POST':
        user_id = request.form['user_id']
        dbHandler.deleteUser(user_id)

    
    types = dbHandler.getAllAssetType()

    conn = sqlite3.connect(r"diona.db")
    cur = conn.cursor() 

    query = cur.execute("SELECT * FROM User")

    rows = query.fetchall()


    return render_template('view_users.html',
                            username=session['id'],
                            title='View users',
                            rows = rows,
                            year=datetime.now().year)



@app.route('/delete_user')
def delete_users():
    #if the form is submittied, declare the variable of new_asset, asset_id and
    #user_id
   if(request.args.get('id')):
        #get asset key names and add into key_names list
        user_details = dbHandler.getUserDetails(request.args.get('id'))
    
 
   return render_template('delete_user.html',
                           username=session['id'],
                           title='View users',
                           user = user_details,
                           year=datetime.now().year)



