# This script is used to populate the tables in the database with the same ten records upon each session start.

from app import db
from app.models import User, Book, BookReview
from datetime import datetime, timezone

def populate_database():
    # Tables to avoid duplicates (for testing)
    BookReview.query.delete()
    Book.query.delete()
    User.query.delete()
    db.session.commit()

    # 10 users are added, user1 is only admin
    users = []
    for i in range(1, 11):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password="testpassword",  
            role="admin" if i == 1 else "regular",
            created_at=datetime.now(timezone.utc)
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # 10 books are added, initially in a dictionary then converted to book objects that are added to the database
    books_data = [
        ("The C# Player's Guide", "RB Whitaker", 2022, "9780985580131", users[0].id),
        ("PL-200 Exam Guide", "Julian Sharp", 2020, "9781803246617", users[1].id),
        ("The Pragmatic Programmer", "David Thomas", 2019, "9780135957059", users[2].id),
        ("Never Split the Difference", "Chris Voss", 2017, "9781847941497", users[3].id),
        ("Cloud Computing Basics", "Anders Lisdorf", 2021, "9781484266053", users[4].id),
        ("Python Programming Bible", "Philip Robbins", 2023, "9781800208700", users[5].id),
        ("Thinking in Systems", "Donella Meadows", 2017, "9781603580557", users[6].id),
        ("The Very Hungry Caterpillar", "Eric Carle", 2001, "9780399226908", users[7].id),
        ("The Art of Unit Testing", "Roy Osherove", 2013, "9781617290893", users[8].id),
        ("Clean Code", "Robert Martin", 2008, "9780132350884", users[1].id)
    ]
    books = []
    for title, author, year, isbn, created_by in books_data:
        book = Book(
            title=title,
            author=author,
            publication_year=year,
            isbn=isbn,
            created_by=created_by
        )
        books.append(book)
        db.session.add(book)
    db.session.commit()

    # 10 reviews are added 
    reviews_data = [
        (books[0].id, users[1].id, "Excellent intro to C#!", 9),
        (books[1].id, users[2].id, "Helped me pass the PL-200.", 7),
        (books[2].id, users[3].id, "Kinda mid tbh", 5),
        (books[3].id, users[4].id, "A bit too wishy-washy for my taste.", 3),
        (books[4].id, users[5].id, "A must for cloud beginners.", 8),
        (books[5].id, users[6].id, "Great Python coverage.", 9),
        (books[6].id, users[7].id, "A classic on systems thinking.", 8),
        (books[7].id, users[8].id, "This SUCKS!", 1),
        (books[8].id, users[9].id, "Boosted my testing skills.", 9),
        (books[9].id, users[0].id, "Should be on every developer's desk.", 10),
    ]
    for book_id, user_id, review_text, rating in reviews_data:
        review = BookReview(
            book_id=book_id,
            user_id=user_id,
            review_text=review_text,
            rating=rating
        )
        db.session.add(review)
    # Commit the changes to the database
    db.session.commit()

    print("Database populated with 10 users, 10 books, and 10 reviews!")

# This makes the script usable both as an importable function and as a standalone script for testing
if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        populate_database()
