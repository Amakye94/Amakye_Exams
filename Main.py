from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# Routes
@app.route('/')
def home():
    return "Welcome to the Book Management System"

@app.route('/books')
def books():
    with app.app_context():
        all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        new_book = Book(title=title, author=author, publication_year=publication_year)
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('books'))
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
