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
        pass
    return render_template("add_book.html")

@routes_bp.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"Book '{book.title}' has been deleted.", "success")
    return redirect(url_for("routes.list_books"))

@routes_bp.route("/books/<int:book_id>/edit", methods=["POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    new_title = request.form.get("title")
    if new_title:
        book.title = new_title
        db.session.commit()
        flash(f"Book '{book.title}' updated.", "success")
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
