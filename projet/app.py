#Ceci est un projet scolaire pour mettre en place une base de données pour les projets de location de voitures

#importing--------------------------------------------------
from flask import Flask, render_template, request, session, redirect, url_for
from flaskext.mysql import MySQL
import pymysql




#app configurations------------------------------------------
app = Flask(__name__)

app.secret_key = 'hamza ait bourhim'
mysql = MySQL()




#MYSQL configurations----------------------------------------
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'projet'
mysql.init_app(app)




#login-------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
	#connection
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)

	if 'loggedin' in session:
		return redirect(url_for('home'))

	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		#check if account exists
		cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password))
		#fetch the account
		account = cursor.fetchone()

		#if account exists
		if account:
			#create session
			session['loggedin'] = True
			session['id'] = account['id']
			session['firstname'] = account['firstname']

			return redirect(url_for('home'))

		else:
			msg = 'Nom ou Mot de passe incorrect!'

	return render_template('login.html' , msg=msg)




#logout-------------------------------------------------------
@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('firstname', None)

	
	
	return redirect(url_for('login'))




#team-------------------------------------------------------
@app.route('/team')
def team():
	return render_template('team.html')




#home-------------------------------------------------------
@app.route('/')
def home():
	if 'loggedin' in session:
		#connection
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		#fetching tables
		cursor.execute('SELECT * FROM admins ORDER BY `id` ')
		admins = cursor.fetchall()

		cursor.execute('(SELECT * FROM vehicules INNER JOIN types_vehicules ON vehicules.idtype = types_vehicules.idtype ) ORDER BY `types_vehicules`.`idtype`')
		cars = cursor.fetchall()

		cursor.execute('SELECT * FROM types_vehicules ORDER BY `idtype` ')
		types = cursor.fetchall()

		cursor.execute('SELECT MAX(idtype) FROM types_vehicules')
		maximum = int(cursor.fetchall()[0]['MAX(idtype)'])

		cursor.execute('SELECT MIN(idtype) FROM types_vehicules')
		minimum = int(cursor.fetchall()[0]['MIN(idtype)'])

		cursor.execute('SELECT * FROM clients ')
		clients = cursor.fetchall()
		
		cursor.execute('SELECT * FROM reservations ORDER BY `dateretour` ')
		bookings = cursor.fetchall()

		cursor.execute('SELECT * FROM locations_courantes ')
		rentals = cursor.fetchall()
 
		cursor.close()
		conn.close()

		return render_template('home.html',admins = admins, cars = cars, types = types, maximum = maximum, minimum = minimum, clients = clients, bookings = bookings, rentals = rentals)

	return redirect(url_for('login'))




#admins-------------------------------------------------------

#add admin----------------------------------------------------
@app.route('/addadmin', methods = ['POST'])
def addadmin():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute('SELECT MAX(id) FROM admins')
			idmax = cursor.fetchall()

			id = int(idmax[0][0]) + 1
			username = request.form['username']
			firstname = request.form['firstname']
			lastname = request.form['lastname']
			email = request.form['email']
			password = request.form['password']

			cursor.execute("INSERT INTO `admins` (`id`, `username`, `firstname`, `lastname`, `email`, `password`) VALUES (%s, %s, %s, %s, %s, %s)", ( id, username, firstname, lastname, email, password))
			conn.commit()

		except Exception:

			msg = "changer le nom d'utilisateur"

	return redirect(url_for('home' , msg=msg))


#edit admin----------------------------------------------------
@app.route('/editadmin', methods = ['POST'])
def editadmin():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			myid = session['id']
			username = request.form['username']
			firstname = request.form['firstname']
			lastname = request.form['lastname']
			email = request.form['email']
			password = request.form['password']

			cursor.execute("UPDATE `admins` SET `id` = %s, `username` = %s, `firstname` = %s, `lastname` = %s, `email` = %s, `password` = %s WHERE `id` = %s  ", ( myid, username, firstname, lastname, email, password, myid))
			conn.commit()

		except Exception:

			msg = "il y a une erreur"

	return redirect(url_for('home' , msg=msg))


#delete admin----------------------------------------------------
@app.route('/deleteadmin', methods = ['POST'])
def deleteadmin():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			myid = session['id']

			cursor.execute(" DELETE FROM `admins` WHERE `id` = %s", ( myid))
			conn.commit()
			return redirect(url_for('logout'))

		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))




#cars---------------------------------------------------------

#add car------------------------------------------------------
@app.route('/addcar', methods = ['POST'])
def addcar():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			matricule = request.form['matricule']
			idtype = request.form['idtype']

			cursor.execute("INSERT INTO `vehicules` (`matricule`, `idtype`, `disponible`) VALUES (%s, %s, TRUE)", ( matricule, idtype))
			conn.commit()

		except Exception:

			msg = 'changer le matricule'

	return redirect(url_for('home' , msg=msg))


#delete car----------------------------------------------------
@app.route('/deletecar', methods = ['POST'])
def deletecar():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			matricule = request.form['matricule']
				
			cursor.execute(" DELETE FROM `vehicules` WHERE `matricule` = %s", (matricule))	
			conn.commit()

		except Exception:

			msg = "il y a une erreur"

	return redirect(url_for('home' , msg=msg))




#types---------------------------------------------------------

#add type------------------------------------------------------
@app.route('/addtype', methods = ['POST'])
def addtype():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute('SELECT MAX(idtype) FROM types_vehicules')
			idmax = cursor.fetchall()

			idtype = int(idmax[0][0]) + 1
			marque = request.form['marque']
			modele = request.form['modele']
			carburant = request.form['carburant']
			couleur = request.form['couleur']
			prix = request.form['prix']
			climatisation = request.form['climatisation']
			if climatisation.upper() == 'OUI':
				climatisation = 'TRUE'
			else:
				climatisation = 'FALSE'

			cursor.execute("INSERT INTO `types_vehicules` (`idtype`, `marque`, `modele`, `carburant`, `couleur`, `climatisation`, `prix`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (idtype, marque, modele, carburant, couleur, climatisation, prix))
			conn.commit()

		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#edit type------------------------------------------------------
@app.route('/edittype', methods = ['POST'])
def edittype():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			idtype = request.form['idtype']
			marque = request.form['marque']
			modele = request.form['modele']
			carburant = request.form['carburant']
			couleur = request.form['couleur']
			prix = request.form['prix']
			climatisation = request.form['climatisation']
			if climatisation.upper() == 'OUI':
				climatisation = 'TRUE'
			else:
				climatisation = 'FALSE'


			cursor.execute("UPDATE `types_vehicules` SET `marque` = %s, `modele` = %s, `carburant` = %s, `couleur` = %s, `climatisation` = %s, `prix` = %s WHERE `idtype` = %s  ", (marque, modele, carburant, couleur, climatisation, prix, idtype))
			conn.commit()

		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#delete type----------------------------------------------------
@app.route('/deletetype', methods = ['POST'])
def deletetype():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			idtype = request.form['idtype']
				
			cursor.execute(" DELETE FROM `types_vehicules` WHERE `idtype` = %s", (idtype))	
			conn.commit()

		except Exception:

			msg = "il y a une erreur"

	return redirect(url_for('home' , msg=msg))




#clients---------------------------------------------------------

#add client------------------------------------------------------
@app.route('/addclient', methods = ['POST'])
def addclient():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cin = request.form['cin']
			motdepasse = request.form['motdepasse']
			permis = request.form['permis']
			prenom = request.form['prenom']
			nom = request.form['nom']
			datenaissance = request.form['datenaissance']
			telephone = request.form['telephone']
			adresse = request.form['adresse']
			

			cursor.execute("INSERT INTO `clients` (`cin`, `motdepasse`, `permis`, `prenom`, `nom`, `datenaissance`, `telephone`, `adresse`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (cin, motdepasse, permis, prenom, nom, datenaissance, telephone, adresse))
			conn.commit()

		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#edit client------------------------------------------------------
@app.route('/editclient', methods = ['POST'])
def editclient():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cin = request.form['cin']
			motdepasse = request.form['motdepasse']
			permis = request.form['permis']
			prenom = request.form['prenom']
			nom = request.form['nom']
			datenaissance = request.form['datenaissance']
			telephone = request.form['telephone']
			adresse = request.form['adresse']


			cursor.execute("UPDATE `clients` SET `motdepasse` = %s, `permis` = %s, `prenom` = %s, `nom` = %s, `datenaissance` = %s, `telephone` = %s , `adresse` = %s WHERE `cin` = %s  ", (motdepasse, permis, prenom, nom, datenaissance, telephone, adresse, cin))
			conn.commit()

		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#delete client----------------------------------------------------
@app.route('/deleteclient', methods = ['POST'])
def deleteclient():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cin = request.form['cin']
				
			cursor.execute(" DELETE FROM `clients` WHERE `cin` = %s", (cin))	
			conn.commit()

		except Exception:

			msg = "il y a une erreur"

	return redirect(url_for('home' , msg=msg))




#bookings---------------------------------------------------------

#add booking------------------------------------------------------
@app.route('/addbooking', methods = ['POST'])
def addbooking():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute('SELECT MAX(idreservation) FROM reservations')
			idmax = cursor.fetchall()

			idreservation = int(idmax[0][0]) + 1
			cin = request.form['cin']
			idtype = request.form['idtype']
			datedepart = request.form['datedepart']
			dateretour = request.form['dateretour']
			duree = request.form['duree']
			acceptee = 'FALSE'
			vue = 'FALSE'

			cursor.execute('SELECT prix FROM types_vehicules WHERE idtype = %s',(idtype))
			prix = cursor.fetchall()


			total = int(duree) * int(prix[0][0])


			cursor.execute("INSERT INTO `reservations` (`idreservation`, `cin`, `idtype`, `datedepart`, `dateretour`, `duree`, `total`, `acceptee`, `vue`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (idreservation, cin, idtype, datedepart, dateretour, duree, total, acceptee, vue))
			conn.commit()
		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#accept booking------------------------------------------------------
@app.route('/acceptbooking', methods = ['POST'])
def acceptbooking():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			idreservation = request.form['idreservation']
			matricule = request.form['matricule']
			payee = 'FALSE'

			cursor.execute("UPDATE `reservations` SET `acceptee` = TRUE, `vue` = TRUE WHERE `idreservation` = %s  ", (idreservation))
			conn.commit()

			cursor.execute("INSERT INTO `locations_courantes` (`idreservation`, `matricule`, `payee`) VALUES (%s, %s, %s)", (idreservation, matricule, payee))
			conn.commit()

			cursor.execute("UPDATE `vehicules` SET `disponible` = FALSE WHERE `matricule` = %s  ", (matricule))
			conn.commit()


		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#refuse booking----------------------------------------------------
@app.route('/refusebooking', methods = ['POST'])
def refusebooking():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			idreservation = request.form['idreservation']
				
			cursor.execute("UPDATE `reservations` SET `vue` = TRUE WHERE `idreservation` = %s  ", (idreservation))
			conn.commit()

		except Exception:

			msg = "il y a une erreur"

	return redirect(url_for('home' , msg=msg))




#rentals---------------------------------------------------------

#paid rental------------------------------------------------------
@app.route('/paidrental', methods = ['POST'])
def paidrental():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			idreservation = request.form['idreservation']

			cursor.execute("UPDATE `locations_courantes` SET `payee` = TRUE WHERE `idreservation` = %s  ", (idreservation))
			conn.commit()
				
			
		except Exception:

			msg = 'il y a une erreur'

	return redirect(url_for('home' , msg=msg))


#delete rental----------------------------------------------------
@app.route('/deleterental', methods = ['POST'])
def deleterental():

	msg = ''
	if request.method == 'POST':

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			idreservation = request.form['idreservation']

			cursor.execute('SELECT matricule FROM locations_courantes WHERE idreservation = %s',(idreservation))
			matrcl = cursor.fetchall()
			matricule = matrcl[0][0]

			cursor.execute("UPDATE `vehicules` SET `disponible` = TRUE WHERE `matricule` = %s  ", (matricule))
			conn.commit()
				
			cursor.execute(" DELETE FROM `locations_courantes` WHERE `idreservation` = %s", (idreservation))	
			conn.commit()

		except Exception:

			msg = "il y a une erreur"

	return redirect(url_for('home' , msg=msg))


#run the app--------------------------------------------------
if __name__ == "__main__":
	app.run(debug=True)