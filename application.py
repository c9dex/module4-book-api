from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request

app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

# Connect Flask to SQLAlchemy
db = SQLAlchemy(app)

# Define our Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    return "Book API is running!"
# GET all books from the database
@app.route("/books", methods=["GET"])
def get_books():
    books = db.session.execute(db.select(Book)).scalars().all()

    output = []

    for book in books:
        book_data = {
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "publisher": book.publisher
        }

        output.append(book_data)

    return {"books": output}

# POST - Add a new book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    if not data or not all(
        data.get(field) for field in ("book_name", "author", "publisher")
    ):
        return {"error": "Missing book information"}, 400

    new_book = Book(
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )

    db.session.add(new_book)
    db.session.commit()

    return {"message": "Book added successfully!", "id": new_book.id}, 201

# PUT - Update an existing book
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = db.get_or_404(Book, id)
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not all(
        data.get(field) for field in ("book_name", "author", "publisher")
    ):
        return {"error": "Missing book information"}, 400

    book.book_name = data["book_name"]
    book.author = data["author"]
    book.publisher = data["publisher"]

    db.session.commit()

    return {"message": "Book updated successfully!", "id": book.id}

# DELETE - Remove a book
@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = db.get_or_404(Book, id)

    db.session.delete(book)
    db.session.commit()

    return {"message": "Book deleted successfully!"}