import logging
import os
import secrets
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect

from cat_api import get_random_cat
from db import db
from forms import LoginForm, RegistrationForm, EditProfileForm, VacancyForm, EditVacancyForm, UserForm
from models import User, Vacancy
from seed import populate_database

#TODO make logs uniform
load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'dev-key-for-testing-only'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacancies.db'

csrf = CSRFProtect(app) # for manual forms for example: delete in profile

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.login_view = 'login'

# This makes ALL logs go to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[logging.StreamHandler()]  # Console only for basic config
)

logger = logging.getLogger('JobBoard')
file_handler = RotatingFileHandler(filename='logs/job_portal.log', maxBytes=10_000, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s JobBoard %(message)s'))
logger.addHandler(hdlr=file_handler)
logger.setLevel(level=logging.INFO)
logger.propagate = False  # Important: don't duplicate to basic config handlers


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(ident=int(user_id))


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
def vacancies():
    per_page = 6  # Max number of vacancies on one page

    # Get filters and page number from request args
    category_filter = request.args.get(key='category', default='all')
    sort_by = request.args.get(key='sort', default='newest')
    page = request.args.get(key='page', default=1, type=int)

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
    if page > vacancies_pagination.pages > 0:
        return redirect(url_for(endpoint='vacancies',
                                page=vacancies_pagination.pages,
                                category=category_filter,
                                sort=sort_by))

    return render_template(template_name_or_list='index.html',
                           vacancies=vacancies_pagination,
                           current_category=category_filter,
                           current_sort=sort_by)

# Single vacancy information
@app.route('/vacancy/<int:vacancy_id>')
def vacancy_info(vacancy_id):
    vacancy = Vacancy.query.get_or_404(ident=int(vacancy_id))
    return render_template(template_name_or_list='vacancy.html', vacancy=vacancy)

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
        logger.info(f"UserID: <{current_user.id}> with username: <{current_user.username}> \
                    added vacancy <{vacancy.id}> with title <{vacancy.title}>")
        flash(message='Vacancy posted successfully!', category='success')
        return redirect(url_for(endpoint='vacancy_info', vacancy_id=vacancy.id))

    return render_template(template_name_or_list='add_vacancy.html', form=vacancy_form)

def invalid_author(action = None, author = None):
    if author != current_user:
        flash(message=f'You can only {action} your own vacancies!', category='danger')
        return True
    return False

# For editing a vacancy
@app.route('/edit_vacancy/<int:vacancy_id>', methods=['GET', 'POST'])
@login_required
def edit_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)

    # Check if current user is the author
    if invalid_author(action='edit', author=vacancy.author):
        return redirect(url_for(endpoint='vacancies'))

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
        logger.info(f"Updated vacancy <{vacancy.id}> with title: <{vacancy.title}> \
                    by UserID <{current_user.id}> with username <{vacancy.author.username}>")
        flash(message='Vacancy updated successfully!', category='success')
        return redirect(url_for(endpoint='vacancy_info', vacancy_id=vacancy.id))

    return render_template(template_name_or_list='edit_vacancy.html', form=form, vacancy=vacancy)

# For deleting a vacancy
@app.route('/delete_vacancy/<int:vacancy_id>', methods=['POST'])
@login_required
def delete_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)

    # Check if current user is the author
    if invalid_author(action='delete', author=vacancy.author):
        return redirect(url_for(endpoint='vacancies'))

    db.session.delete(vacancy)
    db.session.commit()
    logger.info("User <{current_user.username}> deleted vacancy <{vacancy_id}>")
    flash(message='Vacancy deleted successfully!', category='success')
    return redirect(url_for(endpoint='profile'))

# -----------------USER AUTHENTICATION-----------------
def email_already_exists(form: UserForm) -> bool:
     existing_email = User.query.filter_by(email=form.email.data).first()
     if existing_email:
         message = f'Profile with email: <{form.email.data}> already exists'
         logger.warning(message)
         flash(message, 'danger')
         form.email.errors.append(message)
         return True
     return False

def username_already_exists(form: UserForm) -> bool:
    existing_username = User.query.filter_by(username=form.username.data).first()
    if existing_username:
        message = f'Profile with username: <{form.username.data}> already exists'
        logger.warning(message)
        flash(message, 'danger')
        form.username.errors.append(message)
        return True
    return False

# Registering user
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is already logged in, redirect to profile
    if current_user.is_authenticated:
        return redirect(url_for(endpoint='profile'))

    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        if not email_already_exists(form=register_form) and not username_already_exists(form=register_form):
            # creating new user
            user = User(username=register_form.username.data, email=register_form.email.data)
            user.password = register_form.password.data

            # add user to database
            db.session.add(user)
            db.session.commit()
            logger.info(f"User <{user.username}> registered successfully")
            flash(message="Welcome {register_form.username.data}! Your account created successfully!", category='success')
            return redirect(url_for(endpoint='login'))

    return render_template(template_name_or_list='register.html', form=register_form)


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
            flash(message='Nice to see you, {username}!', category='info')
            return redirect(url_for('profile'))
        else:
            # Add error to form instead of flash
            login_form.username.errors.append('Invalid username or password')
            logger.warning(f'Failed Login attempt by user <{username}>')

    return render_template(template_name_or_list='login.html', form=login_form)


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
def show_user_profile(user: User, endpoint: str):
    per_page = 3
    page = request.args.get(key='page', default=1, type=int)
    vacancies_pagination = Vacancy.query.filter_by(author_id=user.id) \
        .order_by(Vacancy.date_created.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)
    # Redirect to last page if page number is too high
    if page > vacancies_pagination.pages > 0:
        return redirect(url_for(endpoint=endpoint, username=user.username, page=vacancies_pagination.pages))

    return render_template(template_name_or_list='profile.html', user=user, vacancies=vacancies_pagination)

@app.route('/profile')
@login_required
def profile():
    return show_user_profile(user=current_user, endpoint='profile')

# Viewing other user's profile page
@app.route('/user/<string:username>')
def user_profile(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    return show_user_profile(user=user, endpoint='user_profile')

# Editing logged-in user's profile page
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edited_form = EditProfileForm()

    if request.method == 'GET':
        edited_form.username.data = current_user.username
        edited_form.email.data = current_user.email

        # Only update user if no duplicate errors
        if not email_already_exists(form=edited_form) and not username_already_exists(form=edited_form):
            current_user.username = edited_form.username.data
            current_user.email = edited_form.email.data

            if edited_form.image.data:
                random_hex = secrets.token_hex(nbytes=8)
                _, ext = os.path.splitext(p=edited_form.image.data.filename)
                image_filename = f'{random_hex}{ext}'
                image_path = os.path.join(app.root_path, 'static', 'images', image_filename)
                edited_form.image.data.save(image_path)
                current_user.image_filename = image_filename

            db.session.commit()
            logger.info(f"User <{current_user.username}> edited profile")
            flash(message='Your changes have been saved!', category='success')
            return redirect(url_for(endpoint='profile'))

    return render_template(template_name_or_list='edit_profile.html', form=edited_form)


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
    flash(message='Your account and all associated vacancies have been deleted.', category='info')
    return redirect(url_for(endpoint='vacancies'))


# -----------------ABOUT PAGE-----------------
@app.route('/about')
def about():
    return render_template(template_name_or_list='about.html')


# -----------------FOR EXTERNAL API-----------------
@app.route('/cat_pics')
def cat_pics():
    cat_image_url = get_random_cat()
    return render_template(template_name_or_list='cat_pics.html', cat_image_url=cat_image_url)


# -----------------ERRORS-----------------
@app.errorhandler(404)
def page_not_found(e):
    logger.error(f'Page not found: {e}')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f'Internal server error: {e}')
    return render_template('errors/500.html'), 500

@app.route('/test-500')
def test_500():
    raise Exception("This is a test 500 error!")