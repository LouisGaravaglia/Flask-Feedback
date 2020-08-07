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


    
@app.route("/")
def show_home():
    """Show homepage."""
    
    if "username" not in session:
        return render_template(
            "index.html")
    else:
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        return render_template(
            "index.html", user=user)
        
    
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
        session["username"] = username
        flash(f"{username} is now registered!", "success")
        return redirect(f"/users/{username}")

    else:

        return render_template(
            "register.html", form=form)

    
@app.route("/users/<username>")
def show_secret(username):
    """Show the users info."""
    user = User.query.filter_by(username=username).first()
    if session["username"] != username:
        flash("You do not have permission to view this content.")
        return redirect("/")
    else:
        return render_template("user.html", user=user)


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
            session["username"] = username
            return redirect(f"/users/{username}")
        
        else:
            form.username.errors = ["Invalid Username/Password"]

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Log out the user."""
    session.pop("username")

    return redirect("/")
