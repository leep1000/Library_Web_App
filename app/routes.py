# This file holds the routes for the Flask application, including user registration, login, book management, and review submission
from .validators import BookForm

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import current_app as app
from functools import wraps
from . import db
from .models import User, Book, BookReview

# decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if user is an admin, this is used to ensure that only users with admin privileges can access delete route
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('routes.list_books'))
        return f(*args, **kwargs)
    return decorated_function

# Create a blueprint for the routes
routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/")
def home():
    return render_template("home.html")

@routes_bp.route("/books")
@login_required
def list_books():
    books = Book.query.all()
    return render_template("books.html", books=books)

@routes_bp.route("/books/add", methods=["GET", "POST"])
@login_required
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
                isbn=form.isbn.data,
                created_by=session["user_id"]
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
@login_required
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"Book '{book.title}' has been deleted.", "success")
    return redirect(url_for("routes.list_books"))

@routes_bp.route("/books/<int:book_id>/edit", methods=["POST"])
@login_required
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
            session["role"] = user.role
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("routes.list_books"))
        else:
            flash("Invalid username or password, please try again.", "danger")
            
    return render_template("login.html")

@routes_bp.route('/logout')
def logout():
    session.clear() 
    flash("You have been logged out.", "success")
    return redirect(url_for("routes.login"))

@routes_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "regular")

        # Validation
        if not username or not password:
            flash("Both username and password are required.", "danger")
            return render_template("register.html")
        if len(username) > 50:
            flash("Username must be less than 50 characters.", "danger")
            return render_template("register.html")
        if len(password) > 50:
            flash("Password must be less than 50 characters.", "danger")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template("register.html")

        # All checks passed and create user
        new_user = User(
            username=username,
            password=password,
            role=role,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("routes.login"))
    
    return render_template("register.html")
