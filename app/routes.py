# This file holds the routes for the Flask application, including user registration, login, book management, and review submission
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .models import User, Book, BookReview
from flask import current_app as app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/books")
def list_books():
    books = Book.query.all()
    return render_template("books.html", books=books)

@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        # Collect form data, add Book to db...
        # Validate and commit!
        pass
    return render_template("add_book.html")
