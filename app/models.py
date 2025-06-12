# This file holds the database models, including related tables for users, books and book reviews 
from . import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

# User model, including fields for username, email, password, created_at and role
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships to link users with books and reviews
    books = relationship("Book", back_populates="user")
    reviews = relationship("BookReview", back_populates="user")
    
    # String representation of the User model
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

# Book model, has a title, author, publication year, isbn, and a created_by column with a foreign key to the User model
class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    publication_year = Column(Integer, nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)

    #relationships to link books with their reviews and the user who created them
    user = relationship("User", back_populates="books")
    reviews = relationship("BookReview", back_populates="book")
    
    # String representation of the Book model
    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', publication_year='{self.publication_year}')>"

# BookReview model, has a review text, rating (1-10), it's primary key is a composite of book_id and user_id, and it has foreign keys to both the Book and User models
class BookReview(db.Model):
    __tablename__ = 'book_reviews'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    review_text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    #restraint to ensure rating is between 1 and 10
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 10', name='check_rating_range'),
    )
    
    # relationships to link reviews with the book and user
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")   
    
    # String representation of the BookReview model
    def __repr__(self):
        return f"<BookReview(book_id='{self.book_id}', user_id='{self.user_id}', rating='{self.rating}')>"
