from .validators import BookForm

# This file holds the routes for the Flask application, including user registration, login, book management, and review submission
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .models import User, Book, BookReview
from flask import current_app as app

# Create a blueprint for the routes
routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/")
def home():
    return render_template("home.html")

@routes_bp.route("/books")
def list_books():
    books = Book.query.all()
    return render_template("books.html", books=books)

@routes_bp.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        form = BookForm(request.form)
        isbn_conflict = Book.query.filter_by(isbn=form.isbn.data).first()
        if isbn_conflict:
            form.isbn.errors.append("A book with this ISBN already exists.")

        if form.validate() and not form.isbn.errors:
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                publication_year=form.publication_year.data,
                isbn=form.isbn.data
            )
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully!", "success")
            return redirect(url_for("routes.list_books"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.capitalize()}: {error}", "danger")
    return render_template("add_book.html")

@routes_bp.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"Book '{book.title}' has been deleted.", "success")
    return redirect(url_for("routes.list_books"))

from .validators import BookForm

@routes_bp.route("/books/<int:book_id>/edit", methods=["POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(request.form)
    isbn_conflict = Book.query.filter(Book.isbn == form.isbn.data, Book.id != book_id).first()
    if isbn_conflict:
        form.isbn.errors.append("A different book already has this ISBN.")

    if form.validate() and not form.isbn.errors:
        book.title = form.title.data
        book.author = form.author.data
        book.publication_year = form.publication_year.data
        book.isbn = form.isbn.data
        db.session.commit()
        flash("Book updated successfully!", "success")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", "danger")
    return redirect(url_for("routes.list_books"))


@routes_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("routes.list_books"))
        else:
            flash("Invalid username or password, please try again.", "danger")
            
    return render_template("login.html")

@routes_bp.route('/logout')
def logout():
    return "<h1>Logout Coming Soon</h1>"

@routes_bp.route('/register')
def register():
    return "<h1>Register Coming Soon</h1>"
