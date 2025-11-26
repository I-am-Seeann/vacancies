import pytest
from app import app, db
from models import User, Vacancy


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create two test users
            user1 = User(username='user1', email='user1@test.com')
            user1.password = 'password123'

            user2 = User(username='user2', email='user2@test.com')
            user2.password = 'password123'

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            # Create a vacancy for user1
            vacancy = Vacancy(
                title='User1 Vacancy',
                category='it',
                author_id=user1.id,
                short_description='Test',
                full_description='Test',
                company='Test',
                salary='$50,000',
                location='Remote'
            )
            db.session.add(vacancy)
            db.session.commit()

            yield client
            db.drop_all()


def test_user_cannot_edit_others_vacancies(client):
    """Test that users cannot edit other users' vacancies"""
    # Login as user2
    client.post('/login', data={
        'username': 'user2',
        'password': 'password123'
    })

    # Try to access edit page for user1's vacancy (vacancy ID 1)
    response = client.get('/edit_vacancy/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'You can only edit your own vacancies' in response.data


def test_user_cannot_delete_others_vacancies(client):
    """Test that users cannot delete other users' vacancies"""
    # Login as user2
    client.post('/login', data={
        'username': 'user2',
        'password': 'password123'
    })

    # Try to delete user1's vacancy
    response = client.post('/delete_vacancy/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'You can only delete your own vacancies' in response.data


def test_user_can_edit_own_vacancies(client):
    """Test that users can edit their own vacancies"""
    # Login as user1
    client.post('/login', data={
        'username': 'user1',
        'password': 'password123'
    })

    # Access own vacancy edit page
    response = client.get('/edit_vacancy/1')

    assert response.status_code == 200
    assert b'Edit Vacancy' in response.data