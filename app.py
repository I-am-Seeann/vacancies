from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import CSRFProtect
from models import db, Users
from forms import LoginForm, RegistrationForm

app = Flask(__name__)

#TODO secret key shesacvlelia!
app.config["SECRET_KEY"] = "very secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacancies.db'
# csrf = CSRFProtect(app)


db.init_app(app)

@app.route('/test-db')
def test_db():
    try:
        db.create_all()
        return "Database tables created successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/users')
def show_users():
    users = Users.query.all()
    return f"Total users: {len(users)}<br>" + "<br>".join([f"User: {user.username} - {user.email}" for user in users])

@app.route('/')
def vacancies():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        return render_template('profile.html')
    return render_template('login.html', form=login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        flash(f"{username}'s account created successfully!", 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=register_form)

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)