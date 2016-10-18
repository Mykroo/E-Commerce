#!/usr/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
# from test import ret_d
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response, json
from functools import wraps

#creacion de la aplicacion
app= Flask(__name__)
app.config.from_object(__name__)

#Loads the default config and override it from enviroment variable

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
	))
app.config.from_envvar('FLASKR_SETTINGS', silent= True)

# *************   Database functions ***********************
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# *************   END of Database functions ***********************
# *************   View functions ***********************


@app.route('/logon.aspx')
def secret_page():
    return render_template('logon.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries= cur.fetchall()
    cur = db.execute('select name, lastname, mail  from users order by id desc')
    users = cur.fetchall()
    
    return render_template("index.html")
    # return render_template('show_entries.html', entries=entries, users=users)

@app.route('/men')
def men_store():
    db = get_db()
    cur = db.execute('select * from products order by id desc')
    entries= cur.fetchall()
    cur = db.execute('select catego, count(catego) as count from products group by catego')
    categorias=cur.fetchall()
    return render_template("men.html", entries=entries, categos=categorias)

@app.route('/checkout.php', methods=['POST','GET'])
def checkout():
    if request.method == 'POST':
        json_data = json.loads(request.form['json_data'])
        db = get_db()
        cur = db.execute('select * from products order by id desc')
        entries= cur.fetchall()
        return render_template("checkout.html", entries=entries)
    else:
        return render_template("checkout.html")
    return ""

@app.route('/ret_cart',methods=['POST','GET'])
def ret_cart():
    if request.method == 'POST':
        db = get_db()
        ids = request.form['ids']
        qty = request.form.getlist('qty')[0].split(',')
        DATOS= (1)
        cur = db.execute('select * from products where id in ('+ids+')')
        res = cur.fetchall()
        # aux = "["
        # for  row in res:
            # aux+="{"
            # aux += '"id":'+str(row[0])+',"name": "'+str(row[1])+'","img_file":"'+str(row[3])+'","price":"'+str(row[4])+'","qty":"'+str(row[6])+'"'
            # aux+="},"
        # aux=aux[:len(aux)-1]+"]"
        aux=""
        i=0
        for  row in res:
            
            aux+='<div class="cart-header2" id="itemCart_'+str(i)+'">\n'\
            ' <div class="close2" onclick=" '\
            '   $(this).parent().fadeOut(\'slow\', function(c){{\n'\
            '       json_cart=JSON.parse(localStorage.simpleCart_items);\n'   \
            '       props = Object.getOwnPropertyNames ( json_cart )\n'   \
            '       delete json_cart[props['+str(i)+']]\n'   \
            '       localStorage.simpleCart_items=JSON.stringify(json_cart)\n'   \
            '       window.location.reload()\n'   \
            '                                                                \n'   \
            '                                                                \n'   \
            '   }});"> </div>\n'\
            '  <div class="cart-sec simpleCart_shelfItem">\n'\
            '        <div class="cart-item cyc">\n'\
            '             <img src="/static/images/'+str(row[3])+'" class="img-responsive" alt="">\n'\
            '        </div>\n'\
            '       <div class="cart-item-info">\n'\
            '        <h3><a href="#">'+str(row[1])+'</a><span>Modelo #: '+str(row[0])+'</span></h3>\n'\
            '        <ul class="qty">\n'\
            '            <li><p>Precio : $'+str(row[4])+'.00</p></li>\n'\
            '            <li><p>Cantidad Restante: '+str(row[6])+' </p></li>\n'\
            '        </ul>\n'\
            '             <div class="delivery">\n'\
            '             <p>Cargos de servicio: $100.00</p>\n'\
            '             <span>Envió de 2 a 3 días hábiles</span>\n'\
            '             <div class="clearfix"></div>\n'\
            '        </div>  \n'\
            '       </div>\n'\
            '       <div class="clearfix"></div>\n'\
            '  </div>\n'\
            '</div>'
            # aux += '"id":'+str(row[0])+',"name": "'+str(row[1])+'","img_file":"'+str(row[3])+'","price":"'+str(row[4])+'","qty":"'+str(row[6])+'"'
            i+=1
        # aux=aux[:len(aux)-1]+"]"
        #aux+='<script>$(document).ready(function(c) {'\
        #     '       $(".close2").on("click", function(c){'\
        #     '                   // c.remove()'\
        #     '               // console.log(c.id())'\
        #     '               // $(".cart-header2").fadeOut("slow", function(c){'\
        #     '               $(this).parent().fadeOut("slow", function(c){'\
        #     '                   // $(".cart-header2").remove();'\
        #     '       });'\
        #     '       });   '\
        #     '       });'\
        #     '</script>'
        return str(aux)
    else:
        db = get_db()
        cur = db.execute('select * from products ')
        res = cur.fetchall()
        aux = "["
        for  row in res:
            aux+="{"
            aux += '"id":'+str(row[0])+',"name": "'+str(row[1])+'","img_file":"'+str(row[3])+'","price":"'+str(row[4])+'","qty":"'+str(row[6])+'"'
            aux+="},"
        aux=aux[:len(aux)-1]+"]"
        return "str(aux)"

@app.route('/sale', methods=['POST'])
def sale():
    if request.method== 'POST':
        try:
            db = get_db()
            db.execute('insert into shiping (id_venta, country, edo, mun, cp, fracc, calle, nume, tel) values (55, ?, ?, ?, ?, ?, ?, ?, ?)',
                         [request.form['country'], request.form['edo'], request.form['mun'], request.form['cp'], request.form['fracc'], request.form['calle'], request.form['num'], request.form['tel'] ])
            db.commit()
            flash('New entry was successfully posted')
        except Exception, e:
            flash("Not valid")
        return render_template('payment.html')
    else:
        return render_template('payment.html')



@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/add_usr', methods=['POST','GET'])
def add_usr():
    # if not session.get('logged_in'):
        # abort(401)
    db = get_db()
    db.execute('insert into users (name, lastname, mail, password) values (?, ?, ?, ?)',
                 [request.form['name'], request.form['lastname'], request.form['mail'], request.form['password']])
    db.commit()
    flash('Usuario registrado puedes iniciar sesión')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    try:
        db = get_db()
        cur = db.execute('select * from users where mail=?', [request.form['username']])
        data = cur.fetchone()
        # error = data['password']
        if request.method == 'POST':
            if request.form['password'] != data['password']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['name'] = data['name'] 
                session['usr_id'] = data['id'] 
                return redirect(url_for('login'))
            return render_template('login.html', error=error)
    except Exception, e:
        error ="Identificacion no valida, intenta de nuevo "
        return redirect(url_for('show_entries'))
        # return render_template('login.html', error=error)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Necesitas iniciar sesion")
            return redirect(url_for('login'))
        
    return wrap

@app.route('/logout/')
@login_required
def logout():
    # session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('show_entries'))

@app.route('/payment.jsp')
@login_required
def payment():
    return render_template("payment.html")
    

# views secc: http://flask.pocoo.org/docs/0.11/tutorial/templates/#tutorial-templates
# *************   END View functions ***********************

