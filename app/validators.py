#This file will hold the validators for the Flask application, including user registration and book management
from wtforms import Form, StringField, PasswordField, IntegerField, validators

class UserRegistrationForm(Form):
    username = StringField('Username', [
        validators.DataRequired(message="Username is required."),
        validators.Length(min=3, max=50, message="Username must be between 3 and 50 characters.")
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message="Password is required."),
        validators.Length(min=6, message="Password must be at least 6 characters long.")
    ])
    role = StringField('Role', [
        validators.DataRequired(message="Role is required."),
        validators.Length(min=3, max=10, message="Role must be between 3 and 10 characters.")
    ])
    
class BookForm(Form):
    title = StringField('Title', [
        validators.DataRequired(message="Title is required."),
        validators.Length(max=200, message="Title must be less than 200 characters.")
    ])
    author = StringField('Author', [
        validators.DataRequired(message="Author is required."),
        validators.Length(max=100, message="Author must be less than 100 characters.")
    ])
    publication_year = IntegerField('Publication Year', [
        validators.DataRequired(message="Publication year is required."),
        validators.NumberRange(min=1600, max=2025, message="Publication year must be between 1600 and 2025.")
    ])
    isbn = StringField('ISBN', [
        validators.DataRequired(message="ISBN is required."),
        validators.Length(min=10, max=20, message="ISBN must be between 10 and 20 characters.")
    ])
    