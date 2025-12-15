import random

from app import db
from mock_data import job_data, usernames
from models import User, Vacancy


def populate_database():
    users = []
    # Adding Users
    for username in usernames:
        user = User(
            username=username,
            email=f'{username}@gmail.com',
            image_filename='default.png'
        )
        user.password = '11111111'
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Adding Vacancies
    for _ in range(20):
        author = random.choice(users)
        job = random.choice(job_data)
        vacancy = Vacancy(
            title=job[0],
            category=job[3],
            author_id=author.id,
            short_description=job[1],
            full_description=job[2],
            company=job[4],
            salary=job[5],
            location=job[6],
            date_created=job[7]
        )
        db.session.add(vacancy)
    db.session.commit()

