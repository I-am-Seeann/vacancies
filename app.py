import logging
import os
import secrets
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect

from cat_api import get_random_cat
from db import db
from forms import LoginForm, RegistrationForm, EditProfileForm, VacancyForm, EditVacancyForm
from models import User, Vacancy
from seed import populate_database


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'dev-key-for-testing-only'
csrf = CSRFProtect(app) # for manual forms for example: delete in profile
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacancies.db'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# This makes ALL logs go to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[logging.StreamHandler()]  # Console only for basic config
)

logger = logging.getLogger('JobBoard')
file_handler = RotatingFileHandler('logs/job_portal.log', maxBytes=10000, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s JobBoard %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger.propagate = False  # Important: don't duplicate to basic config handlers


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.init_app(app)
with app.app_context():
    db.create_all()

    # Auto-seed with sample data if database is empty
    if User.query.count() == 0:
        populate_database()

# ------------------------ROUTES------------------------

# ------------------------VACANCIES------------------------
# Home page for all the vacancies
@app.route('/')
@app.route('/page/<int:page>')
def vacancies(page=1):
    per_page = 6

    # Get filters from request args
    category_filter = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'newest')  # newest or oldest

    # Base query
    query = Vacancy.query

    # Apply category filter if not 'all'
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)

    # Apply sorting
    if sort_by == 'oldest':
        query = query.order_by(Vacancy.date_created.asc())
    else:  # newest (default)
        query = query.order_by(Vacancy.date_created.desc())

    # Paginate
    vacancies_pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Redirect to last page if page number is too high
    if page > vacancies_pagination.pages and vacancies_pagination.pages > 0:
        return redirect(url_for('vacancies', page=vacancies_pagination.pages,
                                category=category_filter, sort=sort_by))

    return render_template('index.html',
                           vacancies=vacancies_pagination,
                           current_category=category_filter,
                           current_sort=sort_by)
# Single vacancy information
@app.route('/vacancy/<int:vacancy_id>')
def vacancy_info(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    return render_template('vacancy.html', vacancy=vacancy)


# For adding new vacancy
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
        logger.info(f"User <{current_user.username}> added vacancy <{vacancy.title}>")
        flash('Vacancy posted successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('add_vacancy.html', form=vacancy_form)


# For editing a vacancy
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
        logger.info(f"Updated vacancy title: <{vacancy.title}> by <{vacancy.author.username}>")
        flash('Vacancy updated successfully!', 'success')
        return redirect(url_for('vacancy_info', vacancy_id=vacancy.id))

    return render_template('edit_vacancy.html', form=form, vacancy=vacancy)

# For deleting a vacancy
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
    logger.info(f"User <{current_user.username}> deleted vacancy <{vacancy_id}>")
    flash('Vacancy deleted successfully!', 'success')
    return redirect(url_for('profile'))


# -----------------USER AUTHENTICATION-----------------
# Registering user
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
            message = f'Profile with email: <{user_filtered_by_email.email}> already exists'
            logger.warning(message)
            flash(message, 'danger')
            register_form.email.errors.append(message)

        # check if username is already taken
        user_filtered_by_username = User.query.filter_by(username=register_form.username.data).first()
        if user_filtered_by_username:
            message = f'Username: <{register_form.username.data}> is taken'
            logger.info(message)
            flash(message, 'danger')
            register_form.username.errors.append(message)

        # Only create user if no duplicate errors
        if not register_form.email.errors and not register_form.username.errors:
            # creating new user
            user = User(username=register_form.username.data, email=register_form.email.data)
            user.password = register_form.password.data

            # add user to database
            db.session.add(user)
            db.session.commit()
            logger.info(f"User <{user.username}> registered successfully")
            flash(f"Welcome {register_form.username.data}! Your account created successfully!", 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=register_form)


# Logging in user
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
            logger.info(f"User <{username}> logged in successfully")
            flash(f'Nice to see you, {username}!', 'info')
            return redirect(url_for('profile'))
        else:
            # Add error to form instead of flash
            login_form.username.errors.append('Invalid username or password')
            logger.warning(f'Failed Login attempt by user <{username}>')

    return render_template('login.html', form=login_form)


# Loging out user
@app.route('/logout')
@login_required
def logout():
    logger.info(f"User <{current_user.username}> loging out")
    logout_user()
    flash('See you soon again!', 'secondary')
    return redirect(url_for('vacancies'))


# -----------------USER PROFILE-----------------
# Viewing logged-in user's profile page
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


# Viewing other user's profile page
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


# Editing logged-in user's profile page
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edited_form = EditProfileForm()

    if request.method == 'GET':
        edited_form.username.data = current_user.username
        edited_form.email.data = current_user.email

    if edited_form.validate_on_submit():
        # Check if email is already taken by another user
        user_filtered_by_email = User.query.filter_by(email=edited_form.email.data).first()
        if user_filtered_by_email and user_filtered_by_email.id != current_user.id:
            message = f'Profile with email: <{edited_form.email.data}> already exists'
            logger.warning(message)
            flash(message, 'danger')
            edited_form.email.errors.append(message)

        # Check if username is already taken by another user
        user_filtered_by_username = User.query.filter_by(username=edited_form.username.data).first()
        if user_filtered_by_username and user_filtered_by_username.id != current_user.id:
            message = f'Username: <{edited_form.username.data}> is taken'
            logger.info(message)
            flash(message, 'danger')
            edited_form.username.errors.append(message)

        # Only update user if no duplicate errors
        if not edited_form.email.errors and not edited_form.username.errors:
            current_user.username = edited_form.username.data
            current_user.email = edited_form.email.data

            if edited_form.image.data:
                random_hex = secrets.token_hex(8)
                _, ext = os.path.splitext(edited_form.image.data.filename)
                image_filename = f'{random_hex}{ext}'
                image_path = os.path.join(app.root_path, 'static/images', image_filename)
                edited_form.image.data.save(image_path)
                current_user.image_filename = image_filename

            db.session.commit()
            logger.info(f"User <{current_user.username}> edited profile")
            flash('Your changes have been saved!', 'success')
            return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=edited_form)


# Deleting logged-in user's profile page
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

    logger.info(f"User <{current_user.username}> deleted profile")
    logout_user()
    flash('Your account and all associated vacancies have been deleted.', 'info')
    return redirect(url_for('vacancies'))


# -----------------ABOUT PAGE-----------------
@app.route('/about')
def about():
    return render_template('about.html')


# -----------------FOR EXTERNAL API-----------------
@app.route('/cat_pics')
def cat_pics():
    cat_image_url = get_random_cat(logger)
    return render_template('cat_pics.html', cat_image_url=cat_image_url)


# -----------------ERRORS-----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@app.route('/test-500')
def test_500():
    raise Exception("This is a test 500 error!")


# -----------------FOR TESTING-----------------
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


if __name__ == '__main__':
    app.run(debug=True)