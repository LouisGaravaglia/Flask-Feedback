from flask import Flask, render_template, flash, redirect, render_template, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from flask_cors import CORS
from forms import AddUserForm
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
# app.config["TESTING"] = True
# app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

debug = DebugToolbarExtension(app)

connect_db(app)


# GET /
#     Redirect to /register.
# GET /register

#     Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name.

#     Make sure you are using WTForms and that your password input hides the characters that the user is typing!
# POST /register
#     Process the registration form by adding a new user. Then redirect to /secret
# GET /login

#     Show a form that when submitted will login a user. This form should accept a username and a password.

#     Make sure you are using WTForms and that your password input hides the characters that the user is typing!
# POST /login
#     Process the login form, ensuring the user is authenticated and going to /secret if so.
# GET /secret
#     Return the text “You made it!” (don’t worry, we’ll get rid of this soon) 
    
    
@app.route("/")
def show_home():
    """Show homepage."""
    

    return render_template(
            "index.html")
        
    
@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Show register user form; handle adding user."""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        flash(f"{username} is now registered!", "success")
        return redirect("/secret")

    else:

        return render_template(
            "register.html", form=form)

    
@app.route("/secret")
def show_secret():
    """Show the secret."""
    if "user_id" not in session:
        flash(f"You do not have permission to view this content. Please login first", "error")
        return redirect("/login")
    else:
        return render_template("secret.html")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Show login user form; handle logging in user."""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        
        if user:
            flash(f"Welcome back {username}!", "success")
            session["user_id"] = user.id
            return redirect("/secret")
        
        else:
            form.username.errors = ["Invalid Username/Password"]

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Log out the user."""
    session.pop("user_id")

    return redirect("/")

# @app.route("/api/cupcakes")
# def get_all_cupcakes():
#     """Get all cupcakes."""
#     all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    

#     return jsonify(cupcakes=all_cupcakes)

# @app.route("/api/cupcakes/<int:id>")
# def get_cupcake(id):
#     """Show single cupcake."""
#     cupcake = Cupcake.query.get_or_404(id)
#     return jsonify(cupcake=cupcake.serialize())
  
# @app.route("/api/cupcakes", methods=["POST"])
# def post_a_cupcake():
#     """Show form to create a cupcake."""

        
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
#     cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"])

#     db.session.add(cupcake)
#     db.session.commit()    
#     response_json = jsonify(cupcake=cupcake.serialize())

#     return (response_json, 201)  



# @app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
# def patch_a_cupcake(id):
#     """Update an existing cupcake."""
#     cupcake = Cupcake.query.get_or_404(id)
#     cupcake.flavor=request.json.get("flavor", cupcake.flavor)
#     cupcake.size=request.json.get("size", cupcake.size)
#     cupcake.rating=request.json.get("rating", cupcake.rating)
#     cupcake.image=request.json.get("image", cupcake.image)

#     db.session.add(cupcake)
#     db.session.commit()    
#     response_json = jsonify(cupcake=cupcake.serialize())

#     return response_json 


# @app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
# def delete_a_cupcake(id):
#     """Delete an existing cupcake."""
#     cupcake = Cupcake.query.get_or_404(id)

#     db.session.delete(cupcake)
#     db.session.commit()

#     return (jsonify(message="Deleted cupcake"), 200)



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
