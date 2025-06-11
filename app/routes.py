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
        # Collect form data, add Book to db...
        # Validate and commit!
        pass
    return render_template("add_book.html")

@routes_bp.route('/login')
def login():
    return "<h1>Login Page Coming Soon</h1>"

@routes_bp.route('/logout')
def logout():
    return "<h1>Logout Coming Soon</h1>"

@routes_bp.route('/register')
def register():
    return "<h1>Register Coming Soon</h1>"
