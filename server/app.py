from . import create_app, db
from .models import Author, Post

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
