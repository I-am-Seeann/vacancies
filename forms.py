from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

#TODO ar dagaviwydes parolis sigrdzis 8-mde gazrda!
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 20
MAX_USERNAME_LENGTH = 25

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    username = StringField('Username',
                          validators=[DataRequired(), Length(max=MAX_USERNAME_LENGTH)])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class EditProfileForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    username = StringField('Username',
                          validators=[DataRequired(), Length(max=MAX_USERNAME_LENGTH)])
    image = FileField('Change profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Apply Changes')


class LoginForm(FlaskForm):
    username = StringField('Username',
                          validators=[DataRequired()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    submit = SubmitField('Login')

class VacancyForm(FlaskForm):
    title = StringField('Job Title',
                       validators=[DataRequired(), Length(max=100)])
    short_description = TextAreaField('Short Description',
                                     validators=[DataRequired(), Length(max=200)])
    full_description = TextAreaField('Full Description',
                                    validators=[DataRequired()])
    company = StringField('Company',
                         validators=[DataRequired(), Length(max=50)])
    salary = StringField('Salary',
                        validators=[Length(max=20)])
    location = StringField('Location',
                          validators=[DataRequired(), Length(max=50)])
    category = SelectField('Category',
                          choices=[
                              ('it', 'IT'),
                              ('design', 'Design'),
                              ('marketing', 'Marketing'),
                              ('sales', 'Sales'),
                              ('other', 'Other')
                          ],
                          validators=[DataRequired()])
    submit = SubmitField('Post Vacancy')