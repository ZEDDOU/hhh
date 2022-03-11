from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from wtforms import SelectField
from forms import GreetUserForm, AddPersonalForm, AttributionForm, AffectPersonalForm
from flask import Flask, render_template, request, flash
import os
import subprocess
import sqlite3
from docxtpl import DocxTemplate
################################

from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename


######################""

def get_db_connection():
    conn = sqlite3.connect('fecc.db')
    conn.row_factory = sqlite3.Row
    crs = conn.cursor()
    return conn


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

bootstrap = Bootstrap(app)
##############################""


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fecc.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    grade = db.Column(db.String(50))

    def __repr__(self):
        return '[Choice {}]'.format(self.nom)


def choice_query():
    return Choice.query


class ChoiceForm(FlaskForm):
    nom = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='nom')

    designation = SelectField("Désignation", choices=[('Pc Portable'), ('Téléphone Portable'), ('Pc Fixe'), ('Ecran')])
    marque = StringField(label=('Marque:'), validators=[DataRequired()], render_kw={"placeholder": 'Saisir Marque'},
                         id='contentcode')

    model = StringField(label=('Modèle:'), validators=[DataRequired()], render_kw={"placeholder": 'Saisir modèle'},
                        id='contentcode')

    serial = StringField(label=('Numéro de série:'), validators=[DataRequired()],
                         render_kw={"placeholder": 'Saisir numéro de série'}, id='contentcode')
    type_attribution = SelectField("Type d'attribution", choices=[('Affectation'), ('Retour')])
    dt = DateField("Date d'attribution", format='%Y-%m-%d')
    submit = SubmitField(label=('Enregistrer'))


#########################


#  app.run(host="192.168.27.112") #host="0.0.0.0" will make the page accessable
# by going to http://[ip]:5000/ on any computer in
# the network.

# host="0.0.0.0" will make the page accessable

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


##########################
######################!!!
@app.route('/test')
def home():
    return render_template("home.html")


# {##########################               #{##########################
# {
###{[|]}################################################################################
# {
# {##########################                 #{##########################

@app.route('/', methods=('GET', 'POST'))
def formattrib():
    form = AttributionForm()

    conn = sqlite3.connect('fecc.db')
    crs = conn.cursor()

    if form.validate_on_submit():
        global designation1

        designation1 = form.designation.data
        type_mouvement = form.type_mouvement.data
        global type_mouvement1
        type_mouvement1 = type_mouvement
        if type_mouvement == 'Affectation':

            conn = get_db_connection()
            data = conn.execute('SELECT *  FROM stockinfo where  designation=? and stock=?',
                                (designation1, 'oui',)).fetchall()

            joblist = conn.execute('SELECT nom  FROM personnel ').fetchall()

            print(joblist)

            sql = crs.execute('SELECT count(designation) as nombre FROM stockinfo where  designation=? and stock=?',
                              (designation1, 'oui',))

            d2 = sql.fetchone()

            nombre = d2[0]
            if nombre == 0:
                message = "aucune disponibilté en stock"
                flash(message)
                return render_template("nn.html", form=form, messages=message)

            datas = {'designation': designation1, 'nombre': nombre}

            # my_list1 = [r for r, in my_data1]
            # t1= [(c, c) for c in my_list1]

            print(datas)
            return render_template('fin.html', datas=datas, data=data, joblist=joblist)

    return render_template('nn.html', form=form)


###############################################################################################################


@app.route('/add_personnel', methods=('GET', 'POST'))
def form_add_personnel():
    form = AddPersonalForm()
    conn = sqlite3.connect('fecc.db')
    crs = conn.cursor()
    conn.execute('SELECT * FROM personnel').fetchall()
    if form.validate_on_submit():
        nom_personnel = form.nom.data
        grade = form.grade.data
        conn = sqlite3.connect('fecc.db')

        crs = conn.cursor()

        data = [
            (nom_personnel, grade),
        ]
        # query = crs.executemany("insert into personnel values(?,?)",data)
        conn.execute('INSERT INTO personnel (nom, grade) VALUES (?, ?)',
                     (nom_personnel, grade))

        conn.execute('SELECT * FROM personnel').fetchall()
        conn.commit()
        conn.close()
        return f'''<h1> Welcome {form.nom.data}</h1>'''

    return render_template('att.html', form=form)


################------------------------------------###########################################################


##################################€~~~~~~~~~~~~######


@app.route('/attrib', methods=('GET', 'POST'))
def formh():
    form = ChoiceForm()
    a = form.nom.query = personnel.query.all()
    print(a)
    conn = sqlite3.connect('fecc.db')
    crs = conn.cursor()
    conn.execute('SELECT * FROM personnel').fetchall()

    if form.validate_on_submit():
        nom_personnel = form.nom.data
        nom = request.form.get('nom')

        print("yyyyyyyyyyy", nom)
        print("tttttttttttt", nom_personnel)

        designation = form.designation.data
        type_mouvement = form.type_attribution.data
        if type_mouvement == 'Affectation':
            print('Affectation')
        marque = form.marque.data
        print("marque", marque)
        model = form.model.data
        serial = form.serial.data
        type_mouvement = form.type_attribution.data
        date_attrib = form.dt.data.strftime('%d-%m-%Y')
        conn = sqlite3.connect('fecc.db')
        conn.row_factory = sqlite3.Row
        crs = conn.cursor()

        sql = crs.execute("select grade from personnel where id=?", (nom,))

        d1 = sql.fetchone()

        grade = d1[0]
        print(grade, "rrrrrrrr")

        sql = crs.execute("select nom from personnel where id=?", (nom,))

        d2 = sql.fetchone()

        nom_personnel = d2[0]
        print(nom_personnel, "rrrrrrrr")
        # d1=query1.fetchone()

        doc = DocxTemplate("templates/fiche2.docx")

        context = {'nom': nom_personnel,
                   'poste': grade,
                   'designation': designation,
                   'Marque': marque,
                   'Modele': model,
                   'Numero_serie': serial,
                   'mouvement': type_mouvement,
                   'Datemouvement': date_attrib
                   }

        doc.render(context)
        doc.save("output/" + nom_personnel + type_mouvement + designation + date_attrib + ".docx")
        # subprocess.call("explorer output", shell=True)

        data = [
            (nom_personnel, grade, designation, marque, model, serial, date_attrib, type_mouvement),
        ]
        query = crs.executemany("insert into affectation values(?,?,?,?,?,?,?,?)", data)
        conn.commit()

        # return f'''<h1> Welcome {form.nom.data}</h1>'''

        conn = get_db_connection()
        crs = conn.cursor()
        # rows = crs.execute('SELECT * FROM stockinfo')
        rows = crs.execute('SELECT * FROM stockinfo where stock=?', ("oui",))
        rows = rows.fetchall()

        return render_template('form11.html', rows=rows)
        # return render_template('form11.html')
        if type_mouvement == 'Retour':
            print('Retour')
            return render_template('form11.html')
    return render_template('form.html', form=form)


@app.route('/list')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM affectation').fetchall()

    return render_template('list.html', rows=rows)


@app.route('/affect', methods=['GET', 'POST'])
def affect():
    # form = ChoiceForm()
    form = AffectPersonalForm()
    option = request.form['timeoptions']
    nomp = request.form.get('comp_select')
    print(nomp)
    # option = request.form.getlist('timeoptions')

    # myVar2 = InventaireTelephonie.objects.get(id=myVar2)
    print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz", option)
    # date = request.form.get(begin).strftime('%d-%m-%Y')
    from datetime import datetime
    startdate = request.form.get('startdate')

    dt = datetime.strptime(startdate, "%Y-%m-%d").strftime("%d-%m-%Y")
    print("dttttttt", dt)

    # Connecting to sqlite
    conn = sqlite3.connect('fecc.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('SELECT * from stockinfo where idstock=?', (option,))

    grade = conn.execute('SELECT grade  FROM personnel where nom=?', (nomp,)).fetchone()
    grade = grade[0]

    print(grade)

    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for row in records:
        print("Id: ", row[0])
        print("Name: ", row[1])
        print("Email: ", row[2])
        print("JoiningDate: ", row[3])
        print("Salary: ", row[7])
        nom = nomp
        grade = grade
        designation = designation1
        marque = row[5]
        model = row[6]
        serial = row[7]
        type_mouvement = type_mouvement1
        date_attrib = dt
        print(serial)
        print("\n")

        print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        print(type_mouvement)
        doc = DocxTemplate("templates/fiche2.docx")

        context = {'nom': nom,
                   'poste': grade,
                   'designation': designation,
                   'Marque': marque,
                   'Modele': model,
                   'Numero_serie': serial,
                   'mouvement': type_mouvement,
                   'Datemouvement': date_attrib
                   }

        doc.render(context)
        doc.save("output/" + nom + type_mouvement + designation + date_attrib + ".docx")
        # subprocess.call("explorer output", shell=True)

        conn = sqlite3.connect('fecc.db')
        crs = conn.cursor()

        data = [
            (nom, grade, designation, marque, model, serial, date_attrib, type_mouvement),
        ]
        query = crs.executemany("insert into affectation values(?,?,?,?,?,?,?,?)", data)
        conn.commit()
        sql = "UPDATE stockinfo SET nom=?,stock=? WHERE serial =?"
        crs.execute(sql, (nom, 'non', serial))

        data1 = [
            (designation, nom, grade, marque, model, serial, date_attrib, "Affecté", "non", "N/A","normal"),
        ]
        #query = crs.executemany("insert into Suivi_parc_info values(?,?,?,?,?,?,?,?)", data)

        #query = crs.executemany("insert into Suivi_parc_info values(type,nom,poste,marque,modele,numero_serie,date_mouvement,type_mouvement,en_stock,etat)", data1)
        query = crs.executemany("insert into Suivi_parc_info values(?, ?, ?, ?, ?, ?, ?, ?,?,?,?)", data1)
        data2 = [
            (designation, nom, grade, marque, model, serial, date_attrib, "Sortie_Stock", "non", "N/A","normal"),
        ]
        query = crs.executemany("insert into Suivi_parc_info values(?, ?, ?, ?, ?, ?, ?, ?,?,?,?)", data2)
        conn.commit()




        print("Table updated...... ")
        return redirect(url_for('formattrib'))
        print("nnnnnnnnnnnnnnnnId: ", row[0])

    return render_template('fin.html', form=form)





