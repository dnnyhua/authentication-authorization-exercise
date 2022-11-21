from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, NumberRange


class RegisterForm(FlaskForm):
    """ Form to register new users """

    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=50)])
    email = StringField("Email", validators=[InputRequired(), 
                                                Length(max=50),
                                                Email()])
    first_name = StringField("First Name",  validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=30)])

class LoginForm(FlaskForm):
    """ Login Form """
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])



class FeedbackForm(FlaskForm):
    """ Form to add feedback """

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
    