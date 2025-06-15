# Library Web App

This Flask application manages a small library of books and user reviews using SQLite.
The database is automatically created and populated with sample data when you start the app.

## Running Locally

1. **Create and activate a virtual environment (recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the development server:**

   ```bash
   python run.py
   ```

4. Open localhost in your browser.

An `library.db` file will be created in the project directory the first time you run the app, and it will be populated with ten users, ten books, and ten reviews.
