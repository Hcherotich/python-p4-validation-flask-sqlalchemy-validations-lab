from server import create_app, db
from server.models import Author, Post
from faker import Faker

app = create_app()
fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    for _ in range(10):
        author = Author(name=fake.name(), phone_number=fake.msisdn()[:10])
        db.session.add(author)

    db.session.commit()

    authors = Author.query.all()

    for author in authors:
        for _ in range(5):
            post = Post(
                title=fake.sentence(nb_words=6),
                content=fake.text(max_nb_chars=300),
                summary=fake.text(max_nb_chars=250),
                category='Fiction'
            )
            post.author_id = author.id
            db.session.add(post)

    db.session.commit()
