from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    SubmitField,
    FileField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

class UserForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Length(max=120), Email()]
    )
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=25)]
    )

class RegistrationForm(UserForm):
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class EditProfileForm(UserForm):
    image = FileField(
        "Change profile picture",
        validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    submit = SubmitField("Apply Changes")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    submit = SubmitField("Login")


class VacancyForm(FlaskForm):
    title = StringField(
        "Job Title",
        validators=[DataRequired(), Length(max=100)]
    )
    short_description = TextAreaField(
        "Short Description",
        validators=[DataRequired(), Length(max=200)]
    )
    full_description = TextAreaField(
        "Full Description",
        validators=[DataRequired()]
    )
    company = StringField(
        "Company",
        validators=[DataRequired(), Length(max=50)]
    )
    salary = StringField(
        "Salary",
        validators=[DataRequired(), Length(max=50)]
    )
    location = StringField(
        "Location",
        validators=[DataRequired(), Length(max=50)]
    )
    category = SelectField(
        "Category",
        choices=[
            ("it", "IT"),
            ("design", "Design"),
            ("marketing", "Marketing"),
            ("sales", "Sales"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Post Vacancy")


class EditVacancyForm(VacancyForm):
    submit = SubmitField("Update Vacancy")
