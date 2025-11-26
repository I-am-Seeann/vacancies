import os
import secrets
from datetime import datetime

from flask import Flask, render_template, url_for, redirect, flash, request
from flask_wtf import CSRFProtect

from models import User, Vacancy
from forms import LoginForm, RegistrationForm, EditProfileForm, VacancyForm, EditVacancyForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import db
app = Flask(__name__)

import os


app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'dev-key-for-testing-only'
csrf = CSRFProtect(app) # for manual forms for example: delete in profile
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacancies.db'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
        full_description='We are looking for a skilled software developer...',
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
@app.route('/page/<int:page>')  # Add this route
def vacancies(page=1):  # Default to page 1
    per_page = 6  # Show 6 vacancies per page
    vacancies_pagination = Vacancy.query.order_by(Vacancy.date_created.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Redirect to last page if page number is too high
    if page > vacancies_pagination.pages > 0:
        return redirect(url_for('vacancies', page=vacancies_pagination.pages))


    return render_template('index.html', vacancies=vacancies_pagination)


@app.route('/vacancy/<int:vacancy_id>')
def vacancy_info(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    return render_template('vacancy.html', vacancy=vacancy)


@app.route('/edit_vacancy/<int:vacancy_id>', methods=['GET', 'POST'])
@login_required
def edit_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)

    # Check if current user is the author
    if vacancy.author != current_user:
        flash('You can only edit your own vacancies!', 'danger')
        return redirect(url_for('vacancies'))

    form = EditVacancyForm()

    # Pre-populate form with current data on GET request
    if request.method == 'GET':
        form.title.data = vacancy.title
        form.category.data = vacancy.category
        form.short_description.data = vacancy.short_description
        form.full_description.data = vacancy.full_description
        form.company.data = vacancy.company
        form.salary.data = vacancy.salary
        form.location.data = vacancy.location

    if form.validate_on_submit():
        vacancy.title = form.title.data
        vacancy.category = form.category.data
        vacancy.short_description = form.short_description.data
        vacancy.full_description = form.full_description.data
        vacancy.company = form.company.data
        vacancy.salary = form.salary.data
        vacancy.location = form.location.data

        db.session.commit()
        flash('Vacancy updated successfully!', 'success')
        return redirect(url_for('vacancy_info', vacancy_id=vacancy.id))

    return render_template('edit_vacancy.html', form=form, vacancy=vacancy)


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
@app.route('/profile/page/<int:page>')
@login_required
def profile(page=1):
    per_page = 3
    vacancies_pagination = Vacancy.query.filter_by(author_id=current_user.id) \
        .order_by(Vacancy.date_created.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    # Redirect to last page if page number is too high
    if page > vacancies_pagination.pages > 0:
        return redirect(url_for('profile', page=vacancies_pagination.pages))

    return render_template('profile.html', user=current_user, vacancies=vacancies_pagination)


@app.route('/user/<string:username>')
@app.route('/user/<string:username>/page/<int:page>')
def user_profile(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    per_page = 3
    vacancies_pagination = Vacancy.query.filter_by(author_id=user.id) \
        .order_by(Vacancy.date_created.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    # Redirect to last page if page number is too high
    if page > vacancies_pagination.pages > 0:
        return redirect(url_for('user_profile', username=username, page=vacancies_pagination.pages))

    return render_template('profile.html', user=user, vacancies=vacancies_pagination)



@app.route('/add_vacancy', methods=['GET', 'POST'])
@login_required
def add_vacancy():
    vacancy_form = VacancyForm()
    if vacancy_form.validate_on_submit():
        vacancy = Vacancy(
            title=vacancy_form.title.data,
            category=vacancy_form.category.data,
            short_description=vacancy_form.short_description.data,
            full_description=vacancy_form.full_description.data,
            company=vacancy_form.company.data,
            salary=vacancy_form.salary.data,
            location=vacancy_form.location.data,
            author_id=current_user.id
        )
        db.session.add(vacancy)
        db.session.commit()
        flash('Vacancy posted successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('add_vacancy.html', form=vacancy_form)


@app.route('/delete_vacancy/<int:vacancy_id>', methods=['POST'])
@login_required
def delete_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)

    # Check if current user is the author
    if vacancy.author != current_user:
        flash('You can only delete your own vacancies!', 'danger')
        return redirect(url_for('vacancies'))

    db.session.delete(vacancy)
    db.session.commit()
    flash('Vacancy deleted successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edited_form = EditProfileForm()

    if request.method == 'GET':
        edited_form.username.data = current_user.username
        edited_form.email.data = current_user.email

    if edited_form.validate_on_submit():
        current_user.username = edited_form.username.data
        current_user.email = edited_form.email.data

        if edited_form.image.data:
            random_hex = secrets.token_hex(8)
            _, ext = os.path.splitext(edited_form.image.data.filename)
            image_file = f'{random_hex}{ext}'
            image_path = os.path.join(app.root_path, 'static/images', image_file)
            edited_form.image.data.save(image_path)
            current_user.image_file = image_file

        db.session.commit()
        flash('Your changes have been saved!', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=edited_form)


@app.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    # Get current user's vacancies and delete them first
    vacancies = Vacancy.query.filter_by(author_id=current_user.id).all()
    for vacancy in vacancies:
        db.session.delete(vacancy)

    # Delete the user
    db.session.delete(current_user)
    db.session.commit()

    logout_user()
    flash('Your account and all associated vacancies have been deleted.', 'info')
    return redirect(url_for('vacancies'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@app.route('/test-500')
def test_500():
    raise Exception("This is a test 500 error!")


@app.route('/generate-test-data')
def generate_test_data():
    """Generate test users and vacancies (run once only!)"""
    import random

    # Don't run if data already exists
    if User.query.count() > 1:  # More than just the default test user
        flash('Test data already exists!', 'warning')
        return redirect(url_for('vacancies'))

    # Sample data
    companies = ['TechCorp', 'WebSolutions', 'DataDrive', 'CloudSystems', 'InnovateLabs',
                 'SoftWorks', 'DigitalCraft', 'CodeMasters', 'AppFactory', 'NetSolutions']

    locations = ['Tbilisi', 'Batumi', 'Kutaisi', 'Remote', 'Hybrid', 'New York', 'London', 'Berlin']

    job_titles = [
        'Software Developer', 'Frontend Engineer', 'Backend Developer', 'Full Stack Developer',
        'Data Scientist', 'DevOps Engineer', 'UI/UX Designer', 'Product Manager',
        'Marketing Specialist', 'Sales Manager', 'Project Coordinator', 'System Administrator'
    ]

    # Create 10 test users
    users = []
    for i in range(1, 11):
        user = User(
            username=f't{i}',
            email=f't{i}@example.com',
            image_file='default.png'
        )
        user.password = f't{i}'
        users.append(user)
        db.session.add(user)

    db.session.commit()
    flash(f'Created {len(users)} test users', 'success')

    # Create 20 test vacancies
    vacancies = []
    for i in range(20):
        # Randomly assign to any of the test users
        author = random.choice(users)

        vacancy = Vacancy(
            title=random.choice(job_titles),
            category=random.choice(['it', 'design', 'marketing', 'sales', 'other']),
            author_id=author.id,
            short_description=f'This is a test vacancy #{i + 1} with exciting opportunities.',
            full_description=f'This is a detailed description for test vacancy #{i + 1}. ' * 5,
            company=random.choice(companies),
            salary=f'${random.randint(30000, 100000)}',
            location=random.choice(locations)
        )
        vacancies.append(vacancy)
        db.session.add(vacancy)

    db.session.commit()
    flash(f'Created {len(vacancies)} test vacancies', 'success')
    flash('Test data generation complete!', 'info')

    return redirect(url_for('vacancies'))


if __name__ == '__main__':
    app.run(debug=True)