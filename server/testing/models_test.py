import pytest
from sqlalchemy.exc import IntegrityError
from server import create_app, db
from server.models import Author, Post
import logging
from faker import Faker

LOGGER = logging.getLogger(__name__)
app = create_app()
fake = Faker()

class TestAuthor:
    '''Class Author in models.py'''

    def test_requires_name(self):
        '''requires each record to have a name.'''
        with app.app_context():
            # valid name
            author1 = Author(name=fake.name(), phone_number='1234567890')
            db.session.add(author1)
            db.session.commit()

            # missing name
            with pytest.raises(ValueError):
                author2 = Author(name='', phone_number='1234567890')
                db.session.add(author2)
                db.session.commit()

    def test_requires_unique_name(self):
        '''requires each record to have a unique name.'''
        with app.app_context():
            db.session.query(Author).delete()
            db.session.commit()

            author_a = Author(name='Ben', phone_number='1234567890')
            db.session.add(author_a)
            db.session.commit()

            author_b = Author(name='Ben', phone_number='1234567890')
            db.session.add(author_b)

            with pytest.raises(IntegrityError):
                db.session.commit()

            db.session.rollback()

    def test_requires_ten_digit_phone_number(self):
        '''requires each phone number to be exactly ten digits.'''
        with app.app_context():
            with pytest.raises(ValueError):
                LOGGER.info('testing short phone number')
                author = Author(name="Jane Author", phone_number="1234")
                db.session.add(author)
                db.session.commit()

            with pytest.raises(ValueError):
                LOGGER.info("testing long phone number")
                author2 = Author(name="Jane Author", phone_number="123456789012345")
                db.session.add(author2)
                db.session.commit()
                
            with pytest.raises(ValueError):
                LOGGER.info("testing non-digit")
                author3 = Author(name="Jane Author", phone_number="123456789!")
                db.session.add(author3)
                db.session.commit()

class TestPost:
    '''Class Post in models.py'''

    def test_requires_title(self):
        '''requires each post to have a title.'''
        with app.app_context():
            with pytest.raises(ValueError):
                content_string = "HI" * 126
                post = Post(title='', content=content_string, category='Non-Fiction')
                db.session.add(post)
                db.session.commit()

    def test_content_length(self):
        '''Content too short test. Less than 250 chars.'''
        with app.app_context():
            # valid content length
            content_string1 = 'A' * 250
            post1 = Post(title='Secret Why I love programming.', content=content_string1, category='Non-Fiction')
            db.session.add(post1)
            db.session.commit()
            
            with pytest.raises(ValueError):
                # too short
                content_string2 = 'A' * 249
                post2 = Post(title='Guess Why I love programming.', content=content_string2, category='Non-Fiction')
                db.session.add(post2)
                db.session.commit()

    def test_summary_length(self):
        '''Summary too long test. More than 250 chars.'''
        with app.app_context():
            content_string = "A" * 250
            
            # valid summary string
            summary_string1 = "T" * 250
            post1 = Post(title="You Won't Believe Why I love programming.", content=content_string, summary=summary_string1, category='Non-Fiction')
            db.session.add(post1)
            db.session.commit()
            
            # too long
            summary_string2 = "T" * 251
            with pytest.raises(ValueError):
                post2 = Post(title="Top Reasons Why I love programming.", content=content_string, summary=summary_string2, category='Non-Fiction')
                db.session.add(post2)
                db.session.commit()
