"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from EX1 import app
from EX1 import models as dbHandler
from flask import request, redirect, url_for, session
from io import StringIO
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
                            year=datetime.now().year,
                        )

@app.route('/login')
def login():
     """Renders the login page."""
     return render_template('login.html',
                             title='Login',
                             year=datetime.now().year,
                             message='Login Page',
                             msg=''
                         )

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
            return redirect(url_for('adminview'))
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
                                msg=''
                                )



@app.route('/adminview')
def adminview():  
    # Check if user is loggedin
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()
   
        return render_template('adminview.html', 
                                username=session['id'],   
                                title='Admin View',
                                type = types,
                                year=datetime.now().year  
                                )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

    
@app.route('/adminview/mobile')
def admin_mobile():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")     
        details = conn.execute("SELECT a.asset_name AS AssetName , t.assetType_name AS AssetType, GROUP_CONCAT(d.key_value), GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_name")
        
        return render_template('admin_mobile.html', 
                                username=session['id'],   
                                title='Admin View',
                                tableRows = details,
                                type = types,
                                year=datetime.now().year  
                                )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/adminview/tablet')
def admin_tablet():
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()
        conn= sqlite3.connect(r"diona.db")
        details = conn.execute("SELECT a.asset_name AS AssetName , t.assetType_name AS AssetType, GROUP_CONCAT(d.key_value), GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_name")
       
    # """Renders the user page."""
        return render_template('admin_tablet.html',
                                username=session['id'],
                                title='Admin View',
                                tableRows = details,
                                type = types,
                                year=datetime.now().year       
                            )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  

@app.route('/adminview/laptop')
def admin_laptop():
    if 'loggedin' in session:
        
        types = dbHandler.getAssetType()
        conn= sqlite3.connect(r"diona.db")
        details = conn.execute("SELECT a.asset_name AS AssetName , t.assetType_name AS AssetType, GROUP_CONCAT(d.key_value), GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_name")
                                      
    # """Renders the user page."""
        return render_template('admin_laptop.html',
                                title='Admin View',
                                username=session['id'],
                                tableRows = details,
                                type = types,
                                year=datetime.now().year       
                            )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
  

@app.route('/userview')
def userview():

    types = dbHandler.getAssetType() 
   
    # """Renders the user page."""
    return render_template('userview.html',
                            title='User View',
                            type = types,
                            year=datetime.now().year      
                        )

@app.route('/userview/mobile')
def mobile():
        types = dbHandler.getAssetType()

        conn = sqlite3.connect(r"diona.db")     
        details = conn.execute("SELECT a.asset_name AS AssetName , t.assetType_name AS AssetType, GROUP_CONCAT(d.key_value), GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Mobile Phone' GROUP BY a.asset_name")
        
        return render_template('userview_mobile.html', 
                                username=session['id'],   
                                title='User View',
                                tableRows = details,
                                type = types,
                                year=datetime.now().year  
                                )


@app.route('/userview/tablet')
def tablet():
        types = dbHandler.getAssetType()
        conn= sqlite3.connect(r"diona.db")
        details = conn.execute("SELECT a.asset_name AS AssetName , t.assetType_name AS AssetType, GROUP_CONCAT(d.key_value), GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Tablet' GROUP BY a.asset_name")
       
    # """Renders the user page."""
        return render_template('userview_tablet.html',
                                username=session['id'],
                                title='User View',
                                tableRows = details,
                                type = types,
                                year=datetime.now().year       
                            )

@app.route('/userview/laptop')
def laptop():
        types = dbHandler.getAssetType()
        conn= sqlite3.connect(r"diona.db")
        details = conn.execute("SELECT a.asset_name AS AssetName , t.assetType_name AS AssetType, GROUP_CONCAT(d.key_value), GROUP_CONCAT(d.key_name) FROM AssetDetails d, AssetType t INNER JOIN Asset a on a.asset_id = d.asset_id AND a.assetType_id = t.assetType_id WHERE t.assetType_name = 'Laptop' GROUP BY a.asset_name")
                                      
    # """Renders the user page."""
        return render_template('userview_laptop.html',
                                title='User View',
                                username=session['id'],
                                tableRows = details,
                                type = types,
                                year=datetime.now().year       
                            )



@app.route('/import')
def i_or_o_main():
   
        conn = sqlite3.connect(r"diona.db")
        types = conn.execute("SELECT DISTINCT assetType_name FROM AssetType") 

        return render_template('i_or_o_main.html', 
                                username=session['id'],   
                                title='Import/Export',
                                type = types,
                                year=datetime.now().year  
                                )
  


@app.route('/import_request', methods=['POST', 'GET'])
def import_main():
     if request.method == 'POST':
        
        file = request.files['upload_file']
        
        csvf = StringIO(file.read().decode('utf8'))
      
        contents = csv.reader(csvf, delimiter=',')
      

        return render_template('i_or_o_main.html',
                                header = contents,
                                year=datetime.now().year
                                )
       

       

@app.route('/new_asset')
def new_assets():
    """Renders the New Assets page."""
    return render_template('new_assets.html',
                            title='New Assets',
                            year=datetime.now().year,
                            message='New assets'
                        )

@app.route('/new_asset_default')
def new_assetDefault():
    """Renders the New Assets Default page."""
    #to appear all the asset types on the page
    #menu = dbHandler.getAssetType()
    return render_template( 'new_asset(Default).html',
                            title='New Assets Default',
                            year=datetime.now().year
                        )


@app.route('/new_asset',methods=['POST', 'GET'])
def add_asset():
    if request.method == 'POST':
        new_asset = ''
        asset_id = ''
        user_id = ''
        #prepare new asset from form data
        if request.form['assetName']:
            if request.form['assetType']:
                new_asset = (request.form['assetName'], request.form['assetType'])
            else:
                msg = 'Enter all details'
        else:
            msg = 'Enter all details'
        
        #create new asset and get asset id
        if new_asset:
            asset_id = dbHandler.create_newAsset(new_asset)
        else:
            msg = 'Error! Cannot create new asset.'
            
        user_id = dbHandler.retrieveUserID(request.form['assetAssigned'])
        
        #Continue adding into Asset Details if asset is added in Asset table
        if asset_id:
            #convert form data into dictionary
            data = request.form.to_dict()

            #remove type and name before adding to asset details table
            data.pop('assetType', None)
            data.pop('assetName', None)
            data.pop('assetAssigned', None)
            
            #empty dictionary for formatting
            empty_dict = {'assetID':asset_id,'assetIEMI': '', 'assetMake':'', 'assetModel':'',
                            'assetPin':'','assetSerial':'','assetMobileNo':'',
                            'assetHardware':'','assetTag':'','assetDevice':'',
                            'assetStatus':'','assetDate':'','assetNotes':''}

            #combine dictionaries
            combined_dict = {**empty_dict, **data}
            
            #create new list to append value from combined dictionary
            new_list = list()

            #append dictionary values into list
            for key, value in combined_dict.items():
                new_list.append(value)
            
            #convert list to dictionary before inserting into database
            AssetDetails = tuple(new_list)
            
            assetdetail_id = dbHandler.create_newAssetDetails(AssetDetails)
            
            if asset_id:
                if user_id:
                    rent = (user_id[0],asset_id)
                    dbHandler.create_newRentrecord(rent)
                    msg = "Inserted data successfully"
                else:
                    msg = 'Error! Cannt create new asset'
            else:
                msg = 'Error! Cannt create new asset'
        else:
            # Table doesnt exist.
            msg = 'Error inserting into database.'
        
        #pageName = page_name(request.form['assetType'])

        # Show the form with message (if any)
        return render_template('new_asset(Default).html',
                                title='New Assets',
                                year=datetime.now().year,
                                message='New Assets',
                                msg=msg)
    else:
        return render_template('new_assets.html',
                                title='New Assets',
                                year=datetime.now().year,
                                message='New Assets',
                                error=True,
                                msg=''
                                )



#hello
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
                            title='Contact',
                            year=datetime.now().year,
                            message='hello aidan.'
                        )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
                            title='About',
                            year=datetime.now().year,
                            message='Your application description page.'
                        )
