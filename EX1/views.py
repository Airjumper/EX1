"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from EX1 import app
from EX1 import models as dbHandler
from flask import request, redirect, url_for, session



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
    return render_template(
        'welcome.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/login')
def login():
     """Renders the login page."""
     return render_template(
         'login.html',
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
        
        conn = sqlite3.connect(r"diona.db")
        types = conn.execute("SELECT * FROM Asset") 
   
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
        
        conn = sqlite3.connect(r"diona.db")
        types = conn.execute("SELECT * FROM Asset") 
        details = conn.execute("SELECT A.asset_name, D.asset_IEMI, D.asset_pin,D.asset_model, D.Notes FROM AssetDetails D, Asset A WHERE A.asset_type = 'Mobile' AND A.asset_id = D.asset_id")
        colNames = details.description
     
   
        return render_template('admin_mobile.html', 
                                username=session['id'],   
                                title='Admin View',
                                tableRows = details,
                                headers = colNames,
                                type = types,
                                year=datetime.now().year  
                                )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))





@app.route('/adminview/tablet')
def admin_tablet():
    if 'loggedin' in session:
        
        conn = sqlite3.connect(r"diona.db")
        types = conn.execute("SELECT * FROM Asset") 
        details = conn.execute("SELECT A.asset_name, D.asset_IEMI, D.asset_pin, D.asset_make , D.asset_tag, D.asset_serialNo, D.asset_device,D.asset_model, D.Notes FROM AssetDetails D, Asset A WHERE A.asset_type = 'Tablet' AND A.asset_id = D.asset_id")
        colNames = details.description
    
    
    # """Renders the user page."""
        return render_template('admin_tablet.html',
                                username=session['id'],
                                title='Admin View',
                                tableRows = details,
                                headers = colNames,
                                type = types,
                                year=datetime.now().year       
                            )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
   

@app.route('/adminview/laptop')
def admin_laptop():
    if 'loggedin' in session:
        
        conn = sqlite3.connect(r"diona.db")
        types = conn.execute("SELECT * FROM Asset") 
        details = conn.execute("SELECT A.asset_name, D.asset_make , D.asset_tag,D.asset_hardware,D.asset_serialNo,D.asset_device,D.Notes  FROM AssetDetails D, Asset A WHERE A.asset_type = 'Laptop' AND A.asset_id = D.asset_id")
        colNames = details.description
    
    # """Renders the user page."""
        return render_template('admin_laptop.html',
                                title='Admin View',
                                username=session['id'],
                                tableRows = details,
                                headers = colNames,
                                type = types,
                                year=datetime.now().year       
                            )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    

    

@app.route('/userview')
def userview():
    conn = sqlite3.connect(r"diona.db")
    types = conn.execute("SELECT * FROM Asset") 
   
    # """Renders the user page."""
    return render_template(
        'userview.html',
        title='User View',
        type = types,
        year=datetime.now().year      
    )

@app.route('/userview/mobile')
def mobile():
    conn = sqlite3.connect(r"diona.db")
    types = conn.execute("SELECT * FROM Asset") 
    details = conn.execute("SELECT A.asset_name,D.asset_IEMI, D.asset_pin, D.asset_model, D.asset_make, D.Notes  FROM AssetDetails D, Asset A WHERE A.asset_type = 'Mobile' AND A.asset_id = D.asset_id")
    colNames = details.description
    
    
    # """Renders the user page."""
    return render_template(
        'userview_mobile.html',
        title='User View',
        tableRows = details,
        headers = colNames,
        type = types,
        year=datetime.now().year       
    )

@app.route('/userview/tablet')
def tablet():
    conn = sqlite3.connect(r"diona.db")
    types = conn.execute("SELECT * FROM Asset") 
    details = conn.execute("SELECT A.asset_name, D.asset_IEMI, D.asset_pin, D.asset_make , D.asset_tag, D.asset_serialNo, D.asset_device,D.asset_model, D.Notes FROM AssetDetails D, Asset A WHERE A.asset_type = 'Tablet' AND A.asset_id = D.asset_id")
    colNames = details.description
    
    
    # """Renders the user page."""
    return render_template(
        'userview_tablet.html',
        title='User View',
        tableRows = details,
        headers = colNames,
        type = types,
        year=datetime.now().year       
    )

@app.route('/userview/laptop')
def laptop():
    conn = sqlite3.connect(r"diona.db")
    types = conn.execute("SELECT * FROM Asset") 
    details = conn.execute("SELECT A.asset_name, D.asset_make , D.asset_tag,D.asset_hardware,D.asset_serialNo,D.asset_device,D.Notes  FROM AssetDetails D, Asset A WHERE A.asset_type = 'Laptop' AND A.asset_id = D.asset_id")
    colNames = details.description
    
    # """Renders the user page."""
    return render_template(
        'userview_laptop.html',
        title='User View',
        tableRows = details,
        headers = colNames,
        type = types,
        year=datetime.now().year       
    )



@app.route('/import_export')
def i_or_o_main():
     # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('i_or_o_main.html', 
                                username=session['id'],   
                                title='Import/Export',
                                year=datetime.now().year  
                                )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
