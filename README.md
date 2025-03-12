# CLIbrary - Command Line Library Manager

CLIbrary is a command-line application for managing a personal book library. It allows you to track books, categorize them, and add reviews, all through an intuitive terminal interface.

## Features

- Manage books with title and author information
- Organize books into categories
- Add, update, and delete reviews for books
- User-friendly command-line interface with color formatting
- SQLite database for persistent storage

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- pipenv (Python virtual environment manager)

## Installation

1. Clone the repository to your local machine:

```bash
git clone <repository-url>
cd p3-project-CLIbrary
```

2. Set up the virtual environment and install dependencies:

```bash
pipenv install
```

This will install all required packages including:
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- Rich (Terminal formatting)

## Database Setup

1. Initialize the database with Alembic:

```bash
pipenv run alembic upgrade head
```

This command will create the SQLite database file and set up all required tables.

## Running the Application

Start the application with:

```bash
pipenv run python main.py
```

## Usage Guide

### Main Menu

The application presents a main menu with the following options:
1. Manage Books
2. Manage Categories
3. Manage Reviews
4. Exit

### Managing Books

In the Books menu, you can:
- List all books in your library
- Add a new book with title, author, and category
- Update existing book information
- Delete books from your library

### Managing Categories

In the Categories menu, you can:
- List all categories with book counts
- Add ne categories
- Update category names
- Delete categories (with warning if books are assigned)

### Managing Reviews

In the Reviews menu, you can:
- List all reviews
- Add new reviews with ratings (1-5) and optional comments
- Update existing reviews
- Delete reviews

## Project Structure

```
p3-project-CLIbrary/
├── alembic/                  # Database migration files
│   ├── versions/             # Migration version files
│   └── env.py                # Alembic environment configuration
├── src/                      # Source code
│   ├── models/               # SQLAlchemy models
│   │   ├── book.py           # Book model
│   │   ├── category.py       # Category model
│   │   └── review.py         # Review model
│   ├── db.py                 # Database connection setup
│   └── cli.py                # CLI interface implementation
├── main.py                   # Application entry point
├── alembic.ini               # Alembic configuration
├── Pipfile                   # Pipenv dependencies
└── Pipfile.lock              # Locked dependencies
```

## Troubleshooting

### Database Issues

If you encounter database errors:

1. Reset the database:
```bash
rm p3-project-CLIbrary/library.db
pipenv run alembic upgrade head
```

2. If migration issues occur:
```bash
pipenv run alembic revision --autogenerate -m "Reset database"
pipenv run alembic upgrade head
```

### Dependency Issues

If you have issues with dependencies:

```bash
pipenv --rm
pipenv install
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.