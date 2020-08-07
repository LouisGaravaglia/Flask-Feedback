from flask import Flask, render_template, flash, redirect, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from flask_cors import CORS





app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
# app.config["TESTING"] = True
# app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def show_home():
    """Show homepage."""
    
    cupcakes = Cupcake.query.all()  

    return render_template("index.html", cupcakes=cupcakes)
        
    

    




@app.route("/api/cupcakes")
def get_all_cupcakes():
    """Get all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    

    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Show single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())
  
@app.route("/api/cupcakes", methods=["POST"])
def post_a_cupcake():
    """Show form to create a cupcake."""

        
    # if not request.json["flavor"]:
    #     return (jsonify(message="Need to add a flavor"), 404)
    # if not request.json["size"]:
    #     return (jsonify(message="Need to add a size"), 404)
    # if not request.json["rating"]:
    #     return (jsonify(message="Need to add a rating"), 404)
    
    # if request.json["image"]:
    #     cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"])
    # else:
    #     cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"])
    cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"])

    db.session.add(cupcake)
    db.session.commit()    
    response_json = jsonify(cupcake=cupcake.serialize())

    return (response_json, 201)  



@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def patch_a_cupcake(id):
    """Update an existing cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor=request.json.get("flavor", cupcake.flavor)
    cupcake.size=request.json.get("size", cupcake.size)
    cupcake.rating=request.json.get("rating", cupcake.rating)
    cupcake.image=request.json.get("image", cupcake.image)

    db.session.add(cupcake)
    db.session.commit()    
    response_json = jsonify(cupcake=cupcake.serialize())

    return response_json 


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_a_cupcake(id):
    """Delete an existing cupcake."""
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(message="Deleted cupcake"), 200)



# @app.route("/add", methods=["GET", "POST"])
# def add_pet():
#     """Pet add form; handle adding."""

#     form = AddPetForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         species = form.species.data
#         photo = form.photo.data
#         age = form.age.data
#         notes = form.notes.data
#         available = form.available.data
        
#         new_pet = Pet(name=name, species=species, photo=photo, age=age, notes=notes, available=available)
#         db.session.add(new_pet)
#         db.session.commit()
#         flash(f"Added {name} the {species}", "success")
#         return redirect("/add")

#     else:

#         return render_template(
#             "add_pet.html", form=form)


# @app.route("/edit/<int:pet_id>", methods=["GET", "POST"])
# def edit_pet(pet_id):
#     """Edit the pet listing."""
#     pet = Pet.query.get_or_404(pet_id)
#     form = AddPetForm(obj=pet)

#     if form.validate_on_submit():
#         pet.name = form.name.data
#         pet.species = form.species.data
#         pet.photo = form.photo.data
#         pet.age = form.age.data
#         pet.notes = form.notes.data
#         pet.available = form.available.data
        
#         db.session.commit()
#         flash(f"Updated {pet.name} the {pet.species}", "success")
#         return redirect(f"/edit/{pet_id}")

#     else:

#         return render_template(
#             "edit_pet.html", form=form, pet=pet)

# @app.route("/add", methods=["GET", "POST"])
# def add_snack():
#     """Snack add form; handle adding."""

#     form = AddSnackForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         price = form.price.data
#         flash(f"Added {name} at {price}")
#         return redirect("/add")

#     else:
#         return render_template(
#             "snack_add_form.html", form=form)


# @app.route("/users/<int:uid>/edit", methods=["GET", "POST"])
# def edit_user(uid):
#     """Show user edit form and handle edit."""

#     user = User.query.get_or_404(uid)
#     form = UserForm(obj=user)

#     if form.validate_on_submit():
#         user.name = form.name.data
#         user.email = form.email.data
#         db.session.commit()
#         flash(f"User {uid} updated!")
#         return redirect(f"/users/{uid}/edit")

#     else:
#         return render_template("user_form.html", form=form)
