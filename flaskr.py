#!/usr/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
# from test import ret_d
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response, json
from functools import wraps
reload(sys)
sys.setdefaultencoding("utf-8")
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

if __name__ == '__main__':
    app.run( host='192.168.1.72', port=80,debug=True)

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
    if session.get('logged_in'):
        db= get_db()
        c= db.execute('select * from shiping where id_usr= ? ', [session['usr_id']])
        sales = c.fetchall()
        return render_template('logon.html',sales=sales)
    else:
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
@app.route('/single', methods=['GET', 'POST'])
def single_item():
    db= get_db()
    c= db.execute('select * from products where id = ? ', [request.form['id']])
    prod = c.fetchone()
    return render_template("single.html", prod = prod)
    
@app.route('/men', methods=['GET', 'POST'])
def men_store():
    db = get_db()
    ranges = [(0,2500),
                (2500,10000),
                (10000,25000),
                (5000,99999999)]
    tot_range = []
    for k in ranges:
        tot_range += str(db.execute('select count(*) as n from products where price between ? and ?',k).fetchone()['n'])     
    if request.method == 'POST':
        categorias = db.execute('select catego, count(catego) as count from products group by catego').fetchall()

        try:
            entries = db.execute('select * from products where catego = ?', [request.form['catego']] ).fetchall()
            return render_template("men.html", entries=entries, categos=categorias,ranges=tot_range)
        except Exception, e:
            # return "oli fallo"
            if not session.get('logged_in'):
                db.execute('insert into searches values ( ?, ? )', [999999,request.form['search']])
                db.commit()
            else:
                db.execute('insert into searches values ( ?, ? )', [session['usr_id'],request.form['search']])
                db.commit()
            entries = db.execute('select * from products p where name like ? or catego like ? or description like ?',["%"+request.form['search']+"%", "%"+request.form['search']+"%", "%"+request.form['search']+"%"] ).fetchall()
            return render_template("men.html", entries=entries, categos=categorias,ranges=tot_range)
    else:
        db = get_db()
        cur = db.execute('select * from products order by id desc')
        entries= cur.fetchall()
        cur = db.execute('select catego, count(catego) as count from products group by catego')
        categorias=cur.fetchall()
        return render_template("men.html", entries=entries, categos=categorias,ranges=tot_range)

@app.route('/checkout.php', methods=['POST','GET'])
def checkout():
    if request.method == 'POST':
        json_data = json.loads(request.form['json_data'])
        db = get_db()
        cur = db.execute('select * from products order by id desc  ')
        entries= cur.fetchall()
        return render_template("checkout.html", entries=entries)
    else:
        return render_template("checkout.html")
    return ""

@app.route('/get_details', methods = ['POST', 'GET'])
def get_Detalis():
    if request.method != 'POST':
        return "no post"
    else:
        # return "no post"
        try:
            db = get_db()
            cur = db.execute('select s.id_ship, s.id_prod, p.name, p.img_file,  s.qty, s.price, s.total from sales s,products p where p.id=s.id_prod and s.id_ship=?',[request.form['id_ship']])
            details = cur.fetchall()
            strinch="["
            for k in details:
                diction= dict(price=k['price'],total=k['total'],qty=k['qty'], id_prod = k['id_prod'], id_ship = k['id_ship'], img_file=k['img_file'] ) 
                # diction= dict(price= 
                strinch+=json.dumps(diction)+','
            strinch= strinch[0:len(strinch)-1] + "]"
            # return json.jsonify(total=details[0]['total'],price=details[0]['price'], qty=details[0]['qty'] )
            return strinch
            # return Response(strinch,  mimetype='application/json')
        except Exception, e:
            return "oli"
        
@app.route('/contacto')
def contacto():
    return render_template("contact.html")

@app.route('/single.html')
def single():
    return render_template("single.html")


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
            ' <div class="close2" onclick="cerrar($(this))"> </div>\n'\
            '  <div class="cart-sec simpleCart_shelfItem">\n'\
            '        <div class="cart-item cyc">\n'\
            '             <img src="/static/images/'+str(row[3])+'" class="img-responsive" alt="">\n'\
            '        </div>\n'\
            '       <div class="cart-item-info">\n'\
            '        <h3><a href="#">'+str(row[1])+'</a><span class="mod-id" >Modelo #:'+str(row[0])+'</span></h3>\n'\
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


@app.route('/sale', methods=['POST', 'GET'])
def sale():
    if request.method== 'POST':
        try:
            db = get_db()
            session['usr_id']

            db.execute('insert into shiping ( id_usr, country, edo, mun, cp, fracc, calle, nume, tel) values ('+str(session['usr_id'])+', ?, ?, ?, ?, ?, ?, ?, ?)',
                         [request.form['country'], request.form['edo'], request.form['mun'], request.form['cp'], request.form['fracc'], request.form['calle'], request.form['num'], request.form['tel'] ])
            db.commit()
            
            id_ship = db.execute('select max(id) from shiping').fetchone()[0]
            jsondat=json.loads( request.form['json'])
            flach=""
            for item in jsondat:
                flach='insert into sales (id_ship, id_prod, qty, price) values ('+str(id_ship)+', ' + str(item['id_prod'])+ ', ' +str(item['qty'])+ ', '+str(item['price'])+ ')'
                db.execute(flach)
                db.commit()
            flash('Compra realizada con exito')
        except Exception, e:
            flash('Bad data not uploaded')#insert into shiping ( id_usr, country, edo, mun, cp, fracc, calle, nume, tel) values ('+str(session['usr_id'])+', '+request.form['country']+', '+request.form['edo']+', '+request.form['mun']+', '+request.form['cp']+', '+request.form['fracc']+', '+request.form['calle']+', '+request.form['num']+','+request.form['tel']+')')
        return render_template('payment.html')
    else:
        return str(session['usr_id'])#render_template('payment.html')



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


@app.route('/login', methods=['POST', 'GET'])
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
                return render_template('logon.html', error)
            else:
                if data['admin'] == True:
                    session['admin'] = True
                session['logged_in'] = True
                session['name'] = data['name'] 
                session['usr_id'] = data['id'] 
                error = None
                return redirect(url_for('show_entries'))
            
    except Exception, e:
        error ="Identificacion no valida, intenta de nuevo "
        flash(error)
        return render_template('logon.html')
        # return render_template('login.html', error=error)
@app.route('/contacto')
def contact():
    return render_template('contact.html')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Necesitas iniciar sesion")
            return redirect(url_for('secret_page'))
    return wrap

def admin_required(f):
    @wraps(f)
    def admin_wrap(*args, **kwargs):
        if 'logged_in' in session and session['admin'] == True:
            return f(*args, **kwargs)
        else:
            flash("Necesitas permisos de administrador")
            return redirect(url_for('men_store'))
    return admin_wrap

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

@app.route('/topVentas')
def top_ventas(methods = ['POST', 'GET']):
    db = get_db()
    cur = db.execute('select count(s.id_prod) as qty, p.name, "#"||hex(randomblob(1))||hex(randomblob(1))||hex(randomblob(1)) as color from sales s,products p where s.id_prod = p.id group by s.id_prod limit 10')
    data = cur.fetchall()
    json_str="["

    for fila in data:
        json_str += "{"
        json_str += '"visits":' + str(fila['qty'])+ ','+'"country":"' + fila['name'] + '",'+'"color":"' + fila['color']+ '"'
        json_str += "},"
    json_str = json_str[:len(json_str)-1]+ "]"
    return json_str

@app.route('/ventas_edos')
def ventas_edos(methods = ['POST', 'GET']):
    db = get_db()
    cur = db.execute('select edo, round(cast(count() as float)*100/(select count() from shiping), 2) as percent from shiping group by edo')
    data = cur.fetchall()
    json_str="["
    for fila in data:
        json_str += "{"
        json_str += '"estado":"' + str(fila['edo'])+ '",'+'"value":' + str(fila['percent'])
        json_str += "},"
    json_str = json_str[:len(json_str)-1]+ "]"
    return json_str


    


@app.route('/admin')
# @admin_required
def dashboards():
    return render_template("dash.html")

# views secc: http://flask.pocoo.org/docs/0.11/tutorial/templates/#tutorial-templates
# *************   END View functions ***********************

