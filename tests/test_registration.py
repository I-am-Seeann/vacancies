import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    """Create a test client with a temporary database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_registration_page_loads(client):
    """Test that the registration page loads successfully"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Registration Form' in response.data


def test_successful_registration(client):
    """Test successful user registration"""
    response = client.post('/register', data={
        'email': 'newuser@test.com',
        'username': 'newuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'account created successfully' in response.data

    # Check if user was created in database
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.email == 'newuser@test.com'


def test_registration_duplicate_email(client):
    """Test registration with already existing email"""
    # First registration
    client.post('/register', data={
        'email': 'test@test.com',
        'username': 'user1',
        'password': 'password123',
        'confirm_password': 'password123'
    })

    # Try to register with same email but different username
    response = client.post('/register', data={
        'email': 'test@test.com',
        'username': 'user2',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert b'already exists' in response.data


def test_registration_duplicate_username(client):
    """Test registration with already existing username"""
    # First registration
    client.post('/register', data={
        'email': 'user1@test.com',
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    })

    # Try to register with same username but different email
    response = client.post('/register', data={
        'email': 'user2@test.com',
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert b'is taken' in response.data


def test_registration_password_mismatch(client):
    """Test registration with non-matching passwords"""
    response = client.post('/register', data={
        'email': 'test@test.com',
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'differentpassword'
    })

    assert response.status_code == 200
    assert b'Registration Form' in response.data  # Should stay on registration page