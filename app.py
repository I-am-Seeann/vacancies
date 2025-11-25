from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import CSRFProtect
from models import User, Vacancy
from forms import LoginForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import db
app = Flask(__name__)

#TODO secret key shesacvlelia!
app.config["SECRET_KEY"] = "very secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacancies.db'
# csrf = CSRFProtect(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if @login_required fails

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/test-db')
def test_db():
    try:
        db.create_all()
        return "Database tables created successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/users')
def show_users():
    users = User.query.all()
    return f"Total users: {len(users)}<br>" + "<br>".join([f"User: {user.username} - {user.email}" for user in users])

@app.route('/add-test-user')
def add_test_user():
    user = User(username='testuser', email='test@test.com')
    user.password = 'password123'
    db.session.add(user)
    db.session.commit()
    return "Test user added!"

@app.route('/test-relationship')
def test_relationship():
    # Clear any existing data
    Vacancy.query.delete()
    User.query.delete()
    db.session.commit()

    # Create a test user
    user = User(username='testuser', email='test@test.com')
    user.password = 'password123'
    db.session.add(user)
    db.session.commit()

    # Create a vacancy for that user
    vacancy = Vacancy(
        title='Software Developer',
        category='IT',
        author_id=user.id,
        short_description='Develop amazing software',
        long_description='We are looking for a skilled software developer...',
        company='Tech Corp',
        salary='$80,000',
        location='Remote'
    )
    db.session.add(vacancy)
    db.session.commit()

    # Test the relationship - get user's vacancies
    user_vacancies = user.vacancies
    vacancy_author = vacancy.author

    return f"""
    User: {user.username}<br>
    User's vacancies: {len(user_vacancies)}<br>
    First vacancy title: {user_vacancies[0].title if user_vacancies else 'None'}<br>
    Vacancy author: {vacancy_author.username}<br>
    Relationship works! 
    """

@app.route('/')
def vacancies():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, redirect to profile
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        # find user by username
        user = User.query.filter_by(username=username).first()

        # check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            flash(f'Nice to see you, {username}!', 'info')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('See you soon again!', 'secondary')
    return redirect(url_for('vacancies'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is already logged in, redirect to profile
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        # check if user with same mail already exists
        user_filtered_by_email = User.query.filter_by(email=register_form.email.data).first()
        if user_filtered_by_email:
            flash(f'Account with email: "{register_form.email.data}" already exists', 'danger')
            return redirect(url_for('register'))

        # check if username is already taken
        user_filtered_by_username = User.query.filter_by(username=register_form.username.data).first()
        if user_filtered_by_username:
            flash(f'Username: "{register_form.username.data}" is taken', 'danger')
            return redirect(url_for('register'))

        # creating new user
        user = User(username=register_form.username.data, email=register_form.email.data)
        user.password = register_form.password.data

        # add user to database
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {register_form.username.data}! Your account created successfully!", 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=register_form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/add_vacancy')
@login_required
def add_vacancy():
    return render_template('add_vacancy.html')

if __name__ == '__main__':
    app.run(debug=True)