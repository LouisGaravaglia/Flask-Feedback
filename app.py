from flask import Flask, render_template, flash, redirect, render_template, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from flask_cors import CORS
from forms import AddUserForm, AddFeedbackForm
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


    
@app.route("/users/<username>")
def show_secret(username):
    """Show the users info."""
    
    if session["username"] != username:
        flash("You do not have permission to view this content.")
        return redirect("/")
    else:
        user = User.query.filter_by(username=username).first()
        feedbacks = Feedback.query.filter_by(username=username).all()
        return render_template("user.html", user=user, feedbacks=feedbacks)
    
    
    
@app.route("/logout")
def logout():
    """Log out the user."""
    session.pop("username")

    return redirect("/")


# GET /users/<username>/feedback/add
#     Display a form to add feedback Make sure that only 
#     the user who is logged in can see this form
# POST /users/<username>/feedback/add
#     Add a new piece of feedback and redirect to /users/<username> — 
#     Make sure that only the user who is logged in can successfully add feedback

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def show_add_feedback(username):
    """Show a form to add feedback. Handle the posting of that feedback."""

    if "username" not in session or username != session['username']:
        return redirect("/")
    else:
        form = AddFeedbackForm()
        
    
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        
        post = Feedback(title=title, content=content, username=username)
        db.session.add(post)
        db.session.commit()
        flash(f"Feedback Posted!", "success")
        return redirect(f"/users/{username}")
        
    else:
    
        return render_template(
            "add_feedback.html", form=form)
