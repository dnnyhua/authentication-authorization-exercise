from flask import Flask, request, jsonify, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

# This is so that we can handle integrityerror and not have the app break
from sqlalchemy.exc import IntegrityError 
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SECRET"
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)



@app.route('/home')
def homepage():
    
    if "username" not in session:
        flash("Please log in or register to view this page", "danger")
        return redirect('/login')
    
    feedbacks = Feedback.query.all()
    return render_template('home.html', feedbacks=feedbacks)


@app.route('/register', methods=['GET','POST'])
def register_user():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        # need to add try except to handle error for duplicate username
        db.session.commit()

        session['username'] = new_user.username
        flash(f"Hi {new_user.username}, your account was successfully created!", "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form) 


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """ The user will delete their profile along with all feedbacks they created """

    if "username" not in session or session['username'] != username:
        flash("Please login!", "danger")
        return redirect(f'/users/{user.username}')

    user = User.query.get(username)
    db.session.delete(user)        
    db.session.commit()
    session.pop('username')
    return redirect('/')
    

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # class method authenticate will return the user instance or False
        user = User.authenticate(username,password)
        if user:
            flash(f'Welcome back, {user.username}', "primary")
            session['username'] = user.username # To keep user logged in
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Incorrect Username or Password was entered']

    return render_template('login.html', form=form)



@app.route("/users/<username>")
def user_profile(username):
    """ User's profile when logged in """

    if 'username' not in session or username != session['username']:
        # Can use raise Unauthorized or redirect and flash message
        # raise Unauthorized()
        flash('Please login to view page', "danger")
        return redirect('/login')
       
    user = User.query.get(username)
    feedbacks = Feedback.query.filter_by(username=username)
    return render_template('user_profile.html', user=user, feedbacks=feedbacks)


@app.route('/logout')
def logout():
    
    flash(f"See you later {session['username']}", "info")
    session.pop("username")
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_form(username):
    """ Displays a form for feedback. Only logged in users can see the form """
    if 'username' not in session or username != session['username']:
        flash('Please login to add feedbacks', 'danger')
        return redirect('/')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    
    return render_template('feedback_form.html', form=form)

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """ Delete feedback created by the user """

    if 'username' not in session: 
        return Unauthorized()

    feedback = Feedback.query.get_or_404(id)

    # Make sure only the user who create the feedback can delete it
    if feedback.username != session['username']:
        flash("You are not authorized to access this page.", "danger")
        return redirect('/login')
    
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback Deleted", "info")
    return redirect(f'/users/{feedback.username}')


@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def update_feedback(id):
    """ update a feedback the user created"""

    feedback = Feedback.query.get_or_404(id)
    if 'username' not in session or session['username'] != feedback.username:
        return redirect(f'/users/{feedback.username}')
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    
    return render_template('update_feedback.html', form=form, feedback=feedback)



        
