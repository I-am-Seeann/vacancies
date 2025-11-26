import pytest
from app import app, db
from models import User, Vacancy


@pytest.fixture
def client():
    """Create a test client with a temporary database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user and vacancy
            user = User(username='testuser', email='test@test.com')
            user.password = 'password123'
            db.session.add(user)

            vacancy = Vacancy(
                title='Test Vacancy',
                category='it',
                author_id=1,
                short_description='Short desc',
                full_description='Full desc',
                company='Test Co',
                salary='$50,000',
                location='Remote'
            )
            db.session.add(vacancy)
            db.session.commit()
            yield client
            db.drop_all()


def test_home_page(client):
    """Test that home page loads with vacancies"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Available Job Vacancies' in response.data
    assert b'Test Vacancy' in response.data


def test_home_page_pagination(client):
    """Test home page pagination"""
    response = client.get('/page/1')
    assert response.status_code == 200
    assert b'Available Job Vacancies' in response.data


def test_about_page(client):
    """Test about page loads"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data


def test_vacancy_detail_page(client):
    """Test individual vacancy page"""
    response = client.get('/vacancy/1')
    assert response.status_code == 200
    assert b'Test Vacancy' in response.data
    assert b'Full desc' in response.data


def test_vacancy_detail_nonexistent(client):
    """Test non-existent vacancy returns 404"""
    response = client.get('/vacancy/999')
    assert response.status_code == 404


def test_user_profile_page(client):
    """Test user profile page"""
    response = client.get('/user/testuser')
    assert response.status_code == 200
    assert b"testuser's Profile" in response.data


def test_user_profile_nonexistent(client):
    """Test non-existent user profile returns 404"""
    response = client.get('/user/nonexistent')
    assert response.status_code == 404


def test_cat_pics_page(client):
    """Test cat pics page loads"""
    response = client.get('/cat_pics')
    assert response.status_code == 200
    assert b'random cat pic' in response.data


def test_add_vacancy_requires_login(client):
    """Test that add vacancy page requires login"""
    response = client.get('/add_vacancy', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login Form' in response.data


def test_edit_vacancy_requires_login(client):
    """Test that edit vacancy page requires login"""
    response = client.get('/edit_vacancy/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login Form' in response.data


def test_profile_requires_login(client):
    """Test that profile page requires login"""
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login Form' in response.data


def test_edit_profile_requires_login(client):
    """Test that edit profile page requires login"""
    response = client.get('/edit_profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login Form' in response.data


def test_logout_requires_login(client):
    """Test that logout requires login"""
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login Form' in response.data


def test_vacancy_filtering(client):
    """Test category filtering on home page"""
    response = client.get('/?category=it')
    assert response.status_code == 200
    assert b'Test Vacancy' in response.data

    response = client.get('/?category=design')
    assert response.status_code == 200
    # Should not show IT vacancies when filtered for design


def test_vacancy_sorting(client):
    """Test sorting on home page"""
    response = client.get('/?sort=newest')
    assert response.status_code == 200

    response = client.get('/?sort=oldest')
    assert response.status_code == 200


def test_error_pages(client):
    """Test custom error pages"""
    # Test 404 page
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data


def test_test_db_route(client):
    """Test the test database route"""
    response = client.get('/test-db')
    assert response.status_code == 200
    assert b'Database tables created successfully' in response.data


def test_users_route(client):
    """Test the users list route"""
    response = client.get('/users')
    assert response.status_code == 200
    assert b'testuser' in response.data


def test_test_relationship_route(client):
    """Test the relationship test route"""
    response = client.get('/test-relationship')
    assert response.status_code == 200
    assert b'Relationship works' in response.data





def test_test_500_route(client):
    """Test the 500 error test route"""
    response = client.get('/test-500')
    assert response.status_code == 500


# Test authenticated routes
def test_authenticated_routes(client):
    """Test routes that require authentication work when logged in"""
    # Login first
    client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    })

    # Test profile page
    response = client.get('/profile')
    assert response.status_code == 200
    assert b'My Vacancies' in response.data

    # Test add vacancy page
    response = client.get('/add_vacancy')
    assert response.status_code == 200
    assert b'Post a New Job Vacancy' in response.data

    # Test edit profile page
    response = client.get('/edit_profile')
    assert response.status_code == 200
    assert b'Edit Your Profile' in response.data

    # Test logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'See you soon again' in response.data