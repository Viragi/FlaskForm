from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from pet_form import PetForm, PetEditForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

generic_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSHVICVCReNZlA53kqdCbVnFCOD9nYIi9jFCIGXNL61lCSKPp7"


class Pet(db.Model):
    __tablename__ = "pet_details"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def getphotourl(self):
        if len(self.photo_url) > 0:
            return self.photo_url
        return generic_image


db.create_all()

# def get_petfinder_info():
#     r=requests.get(PETFINDER_RANDOM_PET_URL,{
#         "key":petfinder_api_key,
#         "format":"jason",
#         "output":"basics"
#     })
#     info =r.json()['petfinder']['pet']
#     name=info['name']['$t']
#     return {}


@app.route("/adopt", methods=['GET'])
def adopt():
    pet_list = Pet.query.all()

    return render_template('welcome.html', pets=pet_list)


@app.route("/adopt/add", methods=['GET'])
def add_pet_form():
    return render_template('pet_form.html', form=PetForm())


@app.route("/adopt/add", methods=['POST'])
def add_pet():
    form = PetForm(request.form)
    if form.validate():
        new_pet = Pet(form.data['name'], form.data['species'],
                      form.data['age'])
        new_pet.photo_url = form.data['photo_url']
        new_pet.available = form.data['available']
        new_pet.notes = form.data['notes']
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/adopt")
    return render_template('pet_form.html', form=form)


@app.route("/adopt/<int:id>/delete", methods=['POST'])
def del_pet(id):
    pet_found = Pet.query.get(id)
    db.session.delete(pet_found)
    db.session.commit()
    return redirect("/adopt")


@app.route("/adopt/<int:id>/edit", methods=['GET'])
def edit_form(id):
    found_pet = Pet.query.get(id)
    form = PetEditForm(obj=found_pet)
    return render_template("/pet_edit_form.html", pet=found_pet, form=form)


@app.route("/adopt/<int:id>/edit", methods=['POST'])
def edit_pet(id):
    found_pet = Pet.query.get(id)
    form = PetEditForm(request.form)
    if form.validate():
        print("\n\n\ndebug this is the form data\n", form.data, "\n\n\n")
        found_pet.age = form.data['age']
        found_pet.photo_url = form.data['photo_url']
        found_pet.available = form.data['available']
        db.session.commit()
        return redirect(url_for('adopt'))
    return render_template("pet_edit_form.html", form=form, id=found_pet.id)


@app.route("/api/pets/<int:id>", methods=['GET'])
def api_call(id):
    b = Pet.query.get_or_404(id)
    bb = {
        "name": b.name,
        "species": b.species,
        "photo_url": b.photo_url,
        "age": b.age,
        "notes": b.notes,
        "available": b.available
    }
    return jsonify(bb)
