from flask import Flask, redirect, render_template, request
from datetime import date, timedelta
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
  select_sql("CREATE TABLE IF NOT EXISTS Users (\
    user_ID INTEGER PRIMARY KEY AUTOINCREMENT, \
    username TEXT NOT NULL, \
    password TEXT NOT NULL)")

  select_sql("CREATE TABLE IF NOT EXISTS Admins (\
  admin_ID INTEGER PRIMARY KEY AUTOINCREMENT, \
  username TEXT NOT NULL, \
  password TEXT NOT NULL)")

  select_sql("CREATE TABLE IF NOT EXISTS Vitamins (\
    vitamin_id INTEGER PRIMARY KEY AUTOINCREMENT, \
    name TEXT NOT NULL, \
    price TEXT NOT NULL, \
    sale TEXT NOT NULL, \
    final_price TEXT NOT NULL, \
    ISBN INTEGER NOT NULL UNIQUE, \
    reserved BOOLEAN DEFAULT 0)")

  select_sql("CREATE TABLE IF NOT EXISTS CodePass (\
  code_id INTEGER PRIMARY KEY AUTOINCREMENT, \
  code TEXT NOT NULL )")

  select_sql(
      "INSERT OR REPLACE INTO CodePass (code) "
      "SELECT 'aptieka' "
      "WHERE NOT EXISTS (SELECT 1 FROM CodePass WHERE code = 'aptieka!')"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('JONAX STRESS CONTROL kapsulas, 30 gab.', '6,78 €', '60 %', '2,71 €', '9780061120084', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('ELITE Collagen Complex paciņas, 30 gab.', '47,99 €', '60 %', '19,28 €', '9780451524935', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('BIOFARMACIJA Skin MAXfiller kolagēns, 28 gab.', '73,39 €', '60 %', '29,36 €', '9780743273565', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('GORELAX DAY kapsulas, 20 gab.', '13,59 €', '50 %', '6.80 €', '9780141439518', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('ACORUS BALANCE Fiber Sugar Balance pulveris, 220 g', '16,99 €', '50 %', '8,50 €', '9780156907392', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('RFF Beauty Shots 25 ml pudelītes, 7 gab.', '20,49 ', '50 %', '10.25 €', '9780316769488', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('MOLLERS Dobbel Immunity kapsulas, 90 gab.', '22,49 €', '50 %', '11.25 €', '9780060850524', 0)"
  )
  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('MOCARD Atero kapsulas, 120 gab.', '43,99 €', '50 %', '22.00 €', '9780544003415', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('KARDIOVITAL balzams, 250 ml', '11,59 €', '50 %', '5.80 €', '9780747532743', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('JONAX Glikozamīns tabletes, 60 gab.', '14,99 €', '50 %', '7.50 €', '9780064404990', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('ICONFIT Beauty Collagen ar Apelsīnu garšu pulveris, 300 g', '15,99 €', '50 %', '8.00 €', '9780553381689', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('PAYOT Pate Grise Stop Pimple Original pasta, 15 ml', '26,99 €', '40 %', '16.19 €', '9780385504201', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('JONAX Mellene Max tabletes, 60 gab.', '5,99 €', '30 %', '4.19 €', '9780062315007', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('JONAX Medus - Intensīvas Darbības lūpu balzams, 4.5 g', '2,90 €', '40 %', '1.74 €', '9780307269751', 0)"
  )

  select_sql(
      "INSERT OR REPLACE INTO Vitamins (name, price, sale, final_price, ISBN, reserved) "
      "VALUES ('JONAX A + E vitamīni kapsulas, 30 gab.', '3,99 €', '40 %', '2.39 €', '9780307588364', 0)"
  )



  select_sql("CREATE TABLE IF NOT EXISTS Reservations (\
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, \
    vitamin_id INTEGER, \
    startingDate DATE, \
    endingDate DATE, \
    FOREIGN KEY (vitamin_id) REFERENCES Vitamins(vitamin_id) \
  )")

  return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
  return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
  return render_template('register.html')


@app.route('/registerAdmin', methods=["GET", "POST"])
def registerAdmin():
  return render_template('registerAdmin.html')


@app.route('/clinic')
def clinic():
  return render_template('clinic.html')

@app.route('/clinicAdmin')
def clinicAdmin():
  global user_names
  global vitamin_names  
  vitamin_names = select_sql("SELECT vitamin_id, name FROM Vitamins")
  user_names = select_sql("SELECT user_id, username FROM Users")
  return render_template('clinicAdmin.html', vitamin_names=vitamin_names, user_names=user_names)


@app.route('/code')
def code():
  return render_template('code.html')


info = []
error = []
search = None
ending_date = None
vitamin_names = None
user_names = None

@app.route('/codeVerify', methods=["GET", "POST"])
def codeVerify():
  data = select_sql("SELECT code FROM CodePass")
  if request.method == "POST":
    code = data[0][0]
    password = request.form["password"]
    if code == password:
      return redirect('/registerAdmin')
  error_message = "The submited code is wrong!"
  return render_template("code.html", error_message=error_message)

@app.route('/registerDataAdmin', methods=["GET", "POST"])
def registerDataAdmin():
  jaunsLietotajsDati = {}
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    insert_sql("INSERT INTO Admins(username, password) VALUES(?, ?)",
               (username, password))
    jaunsLietotajsDati["username"] = username
    jaunsLietotajsDati["password"] = password
    return redirect("/")
  return redirect("/")


@app.route('/searchVitaminUser', methods=["GET", "POST"])
def searchVitaminUser():
  global ending_date
  global info
  global error
  global search
  if request.method == "POST":
    search = request.form["vitamin"]
    vitamin_info = select_sql("SELECT vitamin_id FROM Vitamins WHERE name=? OR ISBN=?", (search, search))
    if vitamin_info:
      vitamin_id = vitamin_info[0][0]
      reservations_data = select_sql("SELECT vitamin_id, startingDate, endingDate FROM Reservations WHERE vitamin_id = ?", (vitamin_id,))
      if reservations_data:
        ending_date = reservations_data[0][2]
    choiceType = request.form["choice"]
    data = select_sql("SELECT name, price, sale, final_price, ISBN, reserved FROM Vitamins")
    if search and choiceType == "name":
      info = []
      error = []
      for i in data:
        if search in i[0]:
          info.append({
              'name': i[0],
              'price': i[1],
              'sale': i[2],
              'final_price': i[3],
              'ISBN': i[4],
              'reserved': i[5]
          })
          error.append({'error': ''})
      if len(info) == 0:
        error.append({'error': 'No vitamin is found('})
    elif search and choiceType == "isbn":
      info = []
      error = []
      for i in data:
        if search in str(i[4]):
          info.append({
              'name': i[0],
              'price': i[1],
              'sale': i[2],
              'final_price': i[3],
              'ISBN': i[4],
              'reserved': i[5]
          })
          error.append({'error': ''})
      if len(info) == 0:
        error.append({'error': 'No vitamin is found('})

  if not search:
    info = []
    error = []
    error.append({'error': 'Please enter a vitamin name or ISBN'})

  return render_template('clinic.html', info=info, error=error, ending_date= ending_date)

@app.route('/searchVitaminAdmin', methods=["GET", "POST"])
def searchVitaminAdmin():
  global vitamin_names
  global user_names
  vitamin_names = select_sql("SELECT vitamin_id, name FROM Vitamins")
  user_names = select_sql("SELECT user_id, username FROM Users")
  global ending_date
  global info
  global error
  global search
  if request.method == "POST":
    search = request.form["vitamin"]
    vitamin_info = select_sql("SELECT vitamin_id FROM Vitamins WHERE name=? OR ISBN=?", (search, search))
    if vitamin_info:
      vitamin_id = vitamin_info[0][0]
      reservations_data = select_sql("SELECT vitamin_id, startingDate, endingDate FROM Reservations WHERE vitamin_id = ?", (vitamin_id,))
      if reservations_data:
        ending_date = reservations_data[0][2]
    choiceType = request.form["choice"]
    data = select_sql("SELECT name, price, sale, final_price, ISBN, reserved FROM Vitamins")
    if search and choiceType == "name":
      info = []
      error = []
      for i in data:
        if search in i[0]:
          info.append({
              'name': i[0],
              'price': i[1],
              'sale': i[2],
              'final_price': i[3],
              'ISBN': i[4],
              'reserved': i[5]
          })
          error.append({'error': ''})
      if len(info) == 0:
        error.append({'error': 'No vitamin is found('})
    elif search and choiceType == "isbn":
      info = []
      error = []
      for i in data:
        if search in str(i[4]):
          info.append({
              'name': i[0],
              'price': i[1],
              'sale': i[2],
              'final_price': i[3],
              'ISBN': i[4],
              'reserved': i[5]
          })
          error.append({'error': ''})
      if len(info) == 0:
        error.append({'error': 'No vitamin is found('})

  if not search:
    info = []
    error = []
    error.append({'error': 'Please enter a vitamin name or ISBN'})

  return render_template('clinicAdmin.html', info=info, error=error, ending_date=ending_date, vitamin_names=vitamin_names, user_names=user_names)


@app.route('/reserveVitaminUsers', methods=["GET", "POST"])
def reserveVitaminUsers():
  global search
  global ending_date
  if request.method == "POST":
    update_sql("UPDATE Vitamins SET reserved=1 WHERE name=? OR ISBN=?", (search, search))

    vitamin_info = select_sql("SELECT vitamin_id FROM Vitamins WHERE name=? OR ISBN=?", (search, search))
    if vitamin_info:
        vitamin_id = vitamin_info[0][0]

        
        today = date.today()
        thirty_days_ahead = today + timedelta(days=30)
        insert_sql("INSERT INTO Reservations (vitamin_id, startingDate, endingDate) VALUES (?, ?, ?)",
                   (vitamin_id, today, thirty_days_ahead))
        reservations_data = select_sql("SELECT vitamin_id, startingDate, endingDate FROM Reservations WHERE vitamin_id = ?", (vitamin_id,))
        if reservations_data:
          ending_date = reservations_data[0][2]

    
  return render_template('clinic.html', ending_date=ending_date)

@app.route('/reserveVitaminAdmins', methods=["GET", "POST"])
def reserveVitaminAdmins():
  global search
  global thirty_days_ahead
  if request.method == "POST":
    update_sql("UPDATE Vitamins SET reserved=1 WHERE name=? OR ISBN=?", (search, search))

    vitamin_info = select_sql("SELECT vitamin_id FROM Vitamins WHERE name=? OR ISBN=?", (search, search))
    if vitamin_info:
        vitamin_id = vitamin_info[0][0]


        today = date.today()
        thirty_days_ahead = today + timedelta(days=30)
        insert_sql("INSERT INTO Reservations (vitamin_id, startingDate, endingDate) VALUES (?, ?, ?)",
                   (vitamin_id, today, thirty_days_ahead))


  return render_template('clinicAdmin.html', thirty_days_ahead=thirty_days_ahead)


@app.route('/deleteVitamins', methods=["GET", "POST"])
def deleteVitamins():
  global user_names
  global vitamin_names
  vitamin_names = select_sql("SELECT vitamin_id, name FROM Vitamins")
  if request.method == "POST":
    vitamin_id = request.form["vitamin_id"]
    delete_sql("DELETE FROM Vitamins WHERE vitamin_id=?", (vitamin_id,))
  return render_template('clinicAdmin.html', vitamin_names=vitamin_names, user_names=user_names)

@app.route('/deleteUsers', methods=["GET", "POST"])
def deleteUsers():
  global vitamin_names
  global user_names
  user_names = select_sql("SELECT user_id, username FROM Users")
  if request.method == "POST":
    user_id = request.form["user_id"]
    delete_sql("DELETE FROM Users WHERE user_id=?", (user_id,))
  return render_template('clinicAdmin.html', user_names=user_names, vitamin_names=vitamin_names)

@app.route('/loginData', methods=["GET", "POST"])
def loginData():
  formTips = request.form.get("form")
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    registerData = select_sql("SELECT username, password FROM Users")
    for data in registerData:
      if username == data[0] and password == data[1]:
        return redirect("/clinic")
    registerDataAdmin = select_sql("SELECT username, password FROM Admins")
    for data in registerDataAdmin:
      if username == data[0] and password == data[1]:
        return redirect("/clinicAdmin")
  error_message = "Wrong username and/or password!"
  return render_template("login.html", error_message=error_message)

@app.route('/editUser', methods=["GET", "POST"])
def editUser():
  global vitamin_names
  global user_names
  if request.method == "POST":
    user_id = request.form["user_id"]
    new_username = request.form["new_username"]
    new_password = request.form["new_password"]

    if new_username:
        update_sql("UPDATE Users SET username=? WHERE user_id=?",
                   (new_username, user_id))
    if new_password:
        update_sql("UPDATE Users SET password=? WHERE user_id=?",
                   (new_password, user_id))
    user_names = select_sql("SELECT user_id, username FROM Users")
  return render_template('clinicAdmin.html', user_names=user_names, vitamin_names=vitamin_names)


@app.route('/addVitamin', methods=["GET", "POST"])
def addVitamin():
  global vitamin_names
  global user_names
  if request.method == "POST":
    name = request.form["name"]
    price = request.form["price"]
    sale = request.form["sale"]
    final_price = request.form["final_price"]
    isbn = request.form["isbn"]

    insert_sql("INSERT INTO Vitamins (name, price, sale, final_price, ISBN, reserved) VALUES (?, ?, ?, ?, ?, 0)",
               (name, price, sale, final_price, isbn))
    vitamin_names = select_sql("SELECT vitamin_id, name FROM Vitamins")
  return render_template('clinicAdmin.html', user_names=user_names, vitamin_names=vitamin_names)
  
@app.route('/registerData', methods=["GET", "POST"])
def registerData():
  jaunsLietotajsDati = {}
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    insert_sql("INSERT INTO Users(username, password) VALUES(?, ?)",
               (username, password))
    jaunsLietotajsDati["username"] = username
    jaunsLietotajsDati["password"] = password
    return redirect("/")
  return redirect("/")


def delete_sql(cmd, vals=None):
  conn = sqlite3.connect('flask.db')
  c = conn.cursor()

  if vals is not None:
    res = c.execute(cmd, vals).fetchall()
  else:
    res = c.execute(cmd).fetchall()

  conn.commit()
  conn.close()
  return res


def insert_sql(cmd, vals=None):
  conn = sqlite3.connect('flask.db')
  c = conn.cursor()

  if vals is not None:
    res = c.execute(cmd, vals).fetchall()
  else:
    res = c.execute(cmd).fetchall()

  conn.commit()
  conn.close()
  return res


def select_sql(cmd, vals=None):
  conn = sqlite3.connect('flask.db')
  c = conn.cursor()

  if vals is not None:
      res = c.execute(cmd, vals).fetchall()
  else:
      res = c.execute(cmd).fetchall()

  conn.commit()
  conn.close()
  return res

def update_sql(cmd, vals=None):
  conn = sqlite3.connect('flask.db')
  c = conn.cursor()

  if vals is not None:
      c.execute(cmd, vals)
  else:
      c.execute(cmd)

  conn.commit()
  conn.close()


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
