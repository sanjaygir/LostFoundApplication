# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from werkzeug.security import generate_password_hash, check_password_hash

from contextlib import closing

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = "AynGXn^J$3>65'KOQ6x_,]i/Pi8#t+"


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])



@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()




@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        g.db.execute('insert into passwords (username, password) values (?, ?)', [username, password_hash])
        g.db.commit()
        flash('New account created')
    return render_template('register.html', error=error)


	
	
	


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #password_hash = generate_password_hash(password)
        
        cur = g.db.execute('select username, password from passwords order by id')
        entries = [dict(username=row[0], password = row[1]) for row in cur.fetchall()]

        found = False

        for e in entries:
          if e['username'] == username and check_password_hash(e['password'], password):
            found = True


        if found == False:
            error = 'Invalid username/password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
	
	
	
@app.route('/lost', methods=['GET', 'POST'])
def lost():
    error = None
    if request.method == 'POST':
        if request.form['item'] =='':
		  error = 'Item cannot be empty'
        else:		
          g.db.execute('insert into lost (name, item, description, number, email) values (?, ?, ?, ?, ?)',
                 [request.form['name'], request.form['item'], request.form['description'], request.form['number'], request.form['email'] ])
          g.db.commit()
          flash('New entry was successfully posted')
    return render_template('lost.html', error=error)

	
@app.route('/found', methods=['GET', 'POST'])
def found():
    error = None
    if request.method == 'POST':
        if request.form['item'] == '':
          error = 'Item cannot be empty'
        else:
          g.db.execute('insert into found (name, item, description, number, email) values (?, ?, ?, ?, ?)',
                 [request.form['name'], request.form['item'], request.form['description'], request.form['number'], request.form['email'] ])
          g.db.commit()
          flash('New entry was successfully posted')
    return render_template('found.html', error=error)



@app.route('/show_lost_one', methods=['GET', 'POST'])
def show_lost_one():
    id = request.args.get('id') 

    cur = g.db.execute('select id, name, item, description, number, email from lost where id = ? order by id', id)
    entries = [dict(id = row[0], name=row[1], item=row[2], description=row[3], number=row[4], email=row[5]) for row in cur.fetchall()]
    return render_template('show_lost_one.html', entries=entries)



@app.route('/show_lost_all')
def show_lost_all():
    cur = g.db.execute('select id, name, item, description, number, email from lost order by id desc')
    entries = [dict(id = row[0], name=row[1], item=row[2], description=row[3], number=row[4], email=row[5]) for row in cur.fetchall()]
    return render_template('show_lost_all.html', entries=entries)



@app.route('/show_found_one', methods=['GET', 'POST'])
def show_found_one():
    id = request.args.get('id') 

    cur = g.db.execute('select id, name, item, description, number, email from found where id = ? order by id', id)
    entries = [dict(id = row[0], name=row[1], item=row[2], description=row[3], number=row[4], email=row[5]) for row in cur.fetchall()]
    return render_template('show_found_one.html', entries=entries)



@app.route('/show_found_all')
def show_found_all():
    cur = g.db.execute('select id, name, item, description, number, email from found order by id desc')
    entries = [dict(id = row[0], name=row[1], item=row[2], description=row[3], number=row[4], email=row[5]) for row in cur.fetchall()]
    return render_template('show_found_all.html', entries=entries)




@app.route('/')
def show_entries():
    #cur = g.db.execute('select id, title, text from entries order by id desc')
    #entries = [dict(id = row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('index.html')




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run()


