import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    """Create a test client with a temporary database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user for login tests
            user = User(username='testuser', email='test@test.com')
            user.password = 'password123'
            db.session.add(user)
            db.session.commit()
            yield client
            db.drop_all()


def test_login_page_loads(client):
    """Test that the login page loads successfully"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login Form' in response.data


def test_successful_login(client):
    """Test successful user login with correct credentials"""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'My Vacancies' in response.data  # Should redirect to profile
    assert b'Nice to see you' in response.data  # Success message


def test_login_wrong_password(client):
    """Test login with incorrect password"""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
    assert b'Login Form' in response.data  # Should stay on login page


def test_login_nonexistent_user(client):
    """Test login with username that doesn't exist"""
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data


def test_login_empty_credentials(client):
    """Test login with empty username and password"""
    response = client.post('/login', data={
        'username': '',
        'password': ''
    })

    assert response.status_code == 200
    # Should show validation errors (WTForms should handle this)


def test_redirect_if_already_logged_in(client):
    """Test that logged-in users are redirected from login page"""
    # First login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    })

    # Try to access login page again
    response = client.get('/login', follow_redirects=True)

    assert response.status_code == 200
    assert b'My Vacancies' in response.data  # Should redirect to profile


def test_logout_functionality(client):
    """Test that logout works correctly"""
    # First login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    })

    # Then logout
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'See you soon again' in response.data  # Logout message
    assert b'Available Job Vacancies' in response.data  # Should redirect to home page


def test_protected_route_access(client):
    """Test that protected routes redirect to login when not authenticated"""
    response = client.get('/profile', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login Form' in response.data  # Should redirect to login
    assert b'Please log in to access this page' in response.data  # Flask-Login message