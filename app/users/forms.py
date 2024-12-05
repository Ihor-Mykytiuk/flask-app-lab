from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError

from app.users.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=4, max=14),
                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                      0,
                                      'Usernames must have only letters, numbers, dots or underscores'
                                      )
                           ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=4, max=14),
                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                      0,
                                      'Usernames must have only letters, numbers, dots or underscores'
                                      )
                           ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = FileField('Update Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About Me', render_kw={"rows": 5, "cols": 40})

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already in use. Please choose a different one.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])

    submit = SubmitField('Change Password')

    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError('Old password is incorrect.')