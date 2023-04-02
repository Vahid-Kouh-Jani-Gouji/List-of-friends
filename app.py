from flask import Flask, render_template, request, redirect ,flash ,url_for
from pymongo import MongoClient
import secrets
from bson.objectid import ObjectId

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

# Verbindung zur MongoDB-Datenbank herstellen
client = MongoClient('mongodb://root:example@localhost:27017/')
db = client['personendaten']

# Definieren der Personendaten-Kollektion
personen = db.personen
i=personen.count_documents({})
@app.route('/')
def index():
    data=personen.find()
    return render_template('index.html',friends=data,i=i)

@app.route('/add', methods=['POST'])
def add():
    # Extrahieren der Formulardaten
    global i
    i+=1
    row_id=personen.count_documents({})
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    age = int(request.form['age'])
    tell=int(request.form['tell'])
    email=request.form['email']

    # Einfügen der Daten in die Datenbank
    personen.insert_one({'firstname': firstname, 'lastname': lastname, 'age': age ,'tell':tell,'email':email ,'row-id':row_id})
    
    flash("Add is successed")
    # Weiterleitung auf die Startseite
    return redirect('/')

@app.route('/update',methods=['POST','GET'])
def update() :
    
    document_id =request.form.get('id',type=int)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = int(request.form['age'])
        tell=int(request.form['tell'])
        email=request.form['email']
        
        # query = {'row-id': row_id}
        # update = {'$set': {'firstname': firstname, 'lastname': lastname, 'age': age ,'tell':tell,'email':email}}

        # Update document in MongoDB
        personen.update_one({'row-id': document_id}, {'$set': {'firstname': firstname, 'lastname': lastname, 'age': age ,'tell':tell,'email':email}})
        flash("Edit is successed")
        # Redirect user to confirmation page
        return redirect('/update')
    return redirect('/')
        
@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    
    global i
    i-=1
    personen.delete_one({'row-id':int(id)})
    flash('Deleting is successed')
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
