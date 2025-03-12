from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from sqlalchemy.exc import SQLAlchemyError

from src.db import Session, Base, engine
from src.models.book import Book
from src.models.category import Category
from src.models.review import Review

console = Console()

def main():
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Using a dictionary for menu options with function references
    menu_options = {
        '1': ('Manage Books', handle_books_menu),
        '2': ('Manage Categories', handle_categories_menu),
        '3': ('Manage Reviews', handle_reviews_menu),
        '4': ('Exit', None)
    }

    console.print(Panel.fit("Welcome to CLIbrary - Your Command Line Library Manager",
                           style="bold green"))

    while True:
        console.print("\n[bold blue]Main Menu[/bold blue]")

        # Using dictionary items for menu display
        for key, (label, _) in menu_options.items():
            console.print(f"  {key}. {label}")

        choice = Prompt.ask("Select an option", choices=list(menu_options.keys()))

        if choice == '4':
            console.print("[yellow]Thank you for using CLIbrary![/yellow]")
            break

        # Call the appropriate handler function
        menu_options[choice][1]()

def handle_books_menu():
    session = Session()

    # Using a tuple for menu options (immutable sequence)
    options = (
        ("List all books", lambda: list_books(session)),
        ("Add a new book", lambda: add_book(session)),
        ("Update a book", lambda: update_book(session)),
        ("Delete a book", lambda: delete_book(session)),
        ("Return to main menu", None)
    )

    while True:
        console.print("\n[bold blue]Books Menu[/bold blue]")

        for i, (label, _) in enumerate(options, 1):
            console.print(f"  {i}. {label}")

        choice = IntPrompt.ask("Select an option", choices=[str(i) for i in range(1, len(options) + 1)])

        if choice == len(options):
            break

        options[choice - 1][1]()

    session.close()

def handle_categories_menu():
    session = Session()

    options = [
        ("List all categories", lambda: list_categories(session)),
        ("Add a new category", lambda: add_category(session)),
        ("Update a category", lambda: update_category(session)),
        ("Delete a category", lambda: delete_category(session)),
        ("Return to main menu", None)
    ]

    while True:
        console.print("\n[bold blue]Categories Menu[/bold blue]")

        for i, (label, _) in enumerate(options, 1):
            console.print(f"  {i}. {label}")

        choice = IntPrompt.ask("Select an option", choices=[str(i) for i in range(1, len(options) + 1)])

        if choice == len(options):
            break

        options[choice - 1][1]()

    session.close()

def handle_reviews_menu():
    session = Session()

    options = {
        1: ("List all reviews", lambda: list_reviews(session)),
        2: ("Add a new review", lambda: add_review(session)),
        3: ("Update a review", lambda: update_review(session)),
        4: ("Delete a review", lambda: delete_review(session)),
        5: ("Return to main menu", None)
    }

    while True:
        console.print("\n[bold blue]Reviews Menu[/bold blue]")

        for key in sorted(options.keys()):
            console.print(f"  {key}. {options[key][0]}")

        choice = IntPrompt.ask("Select an option", choices=[str(i) for i in range(1, len(options) + 1)])

        if choice == 5:
            break

        options[choice][1]()

    session.close()

# Book CRUD operations
def list_books(session):
    books = session.query(Book).all()

    if not books:
        console.print("[yellow]No books found in the library.[/yellow]")
        return

    # Convert SQLAlchemy objects to dictionaries for easier data manipulation
    book_data = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category.name if book.category else "Uncategorized"
        }
        for book in books
    ]

    table = Table(title="Books in Library")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="green")
    table.add_column("Author", style="blue")
    table.add_column("Category", style="magenta")

    # Using the list of dictionaries to populate the table
    for book in book_data:
        table.add_row(str(book["id"]), book["title"], book["author"], book["category"])

    console.print(table)

def add_book(session):
    console.print("[bold]Add a New Book[/bold]")

    # Get all categories for selection
    categories = session.query(Category).all()

    if not categories:
        console.print("[yellow]No categories available. Please create a category first.[/yellow]")
        return

    # Display categories
    console.print("\nAvailable Categories:")
    for i, category in enumerate(categories, 1):
        console.print(f"  {i}. {category.name}")

    title = Prompt.ask("Enter book title")
    author = Prompt.ask("Enter author name")

    # Category selection
    category_choice = IntPrompt.ask(
        "Select category number",
        choices=[str(i) for i in range(1, len(categories) + 1)]
    )
    selected_category = categories[category_choice - 1]

    try:
        new_book = Book(title=title, author=author, category_id=selected_category.id)
        session.add(new_book)
        session.commit()
        console.print(f"[green]Book '{title}' added successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error adding book: {str(e)}[/red]")

def update_book(session):
    list_books(session)

    books = session.query(Book).all()
    if not books:
        return

    book_id = IntPrompt.ask("Enter the ID of the book to update")
    book = session.query(Book).filter_by(id=book_id).first()

    if not book:
        console.print("[red]Book not found![/red]")
        return

    console.print(f"Updating book: [bold]{book.title}[/bold] by {book.author}")

    title = Prompt.ask("Enter new title", default=book.title)
    author = Prompt.ask("Enter new author", default=book.author)

    # Category selection
    categories = session.query(Category).all()
    console.print("\nAvailable Categories:")
    for i, category in enumerate(categories, 1):
        console.print(f"  {i}. {category.name}")

    category_choice = IntPrompt.ask(
        "Select new category number",
        choices=[str(i) for i in range(1, len(categories) + 1)]
    )
    selected_category = categories[category_choice - 1]

    try:
        book.title = title
        book.author = author
        book.category_id = selected_category.id
        session.commit()
        console.print(f"[green]Book updated successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error updating book: {str(e)}[/red]")

def delete_book(session):
    list_books(session)

    books = session.query(Book).all()
    if not books:
        return

    book_id = IntPrompt.ask("Enter the ID of the book to delete")
    book = session.query(Book).filter_by(id=book_id).first()

    if not book:
        console.print("[red]Book not found![/red]")
        return

    confirm = Confirm.ask(f"Are you sure you want to delete '{book.title}'?")
    if not confirm:
        console.print("Deletion cancelled.")
        return

    try:
        session.delete(book)
        session.commit()
        console.print(f"[green]Book '{book.title}' deleted successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error deleting book: {str(e)}[/red]")

# Category CRUD operations
def list_categories(session):
    categories = session.query(Category).all()

    if not categories:
        console.print("[yellow]No categories found.[/yellow]")
        return

    table = Table(title="Book Categories")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Book Count", style="blue")

    for category in categories:
        book_count = len(category.books)
        table.add_row(str(category.id), category.name, str(book_count))

    console.print(table)

def add_category(session):
    console.print("[bold]Add a New Category[/bold]")

    name = Prompt.ask("Enter category name")

    # Using a dictionary for the new category data
    category_data = {"name": name}

    try:
        new_category = Category(**category_data)
        session.add(new_category)
        session.commit()
        console.print(f"[green]Category '{name}' added successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error adding category: {str(e)}[/red]")

def update_category(session):
    list_categories(session)

    categories = session.query(Category).all()
    if not categories:
        return

    category_id = IntPrompt.ask("Enter the ID of the category to update")
    category = session.query(Category).filter_by(id=category_id).first()

    if not category:
        console.print("[red]Category not found![/red]")
        return

    console.print(f"Updating category: [bold]{category.name}[/bold]")

    name = Prompt.ask("Enter new name", default=category.name)

    try:
        category.name = name
        session.commit()
        console.print(f"[green]Category updated successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error updating category: {str(e)}[/red]")

def delete_category(session):
    list_categories(session)

    categories = session.query(Category).all()
    if not categories:
        return

    category_id = IntPrompt.ask("Enter the ID of the category to delete")
    category = session.query(Category).filter_by(id=category_id).first()

    if not category:
        console.print("[red]Category not found![/red]")
        return

    # Check if category has books
    if category.books:
        console.print(f"[yellow]Warning: This category has {len(category.books)} books.[/yellow]")

    confirm = Confirm.ask(f"Are you sure you want to delete '{category.name}'?")
    if not confirm:
        console.print("Deletion cancelled.")
        return

    try:
        session.delete(category)
        session.commit()
        console.print(f"[green]Category '{category.name}' deleted successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error deleting category: {str(e)}[/red]")

# Review CRUD operations
def list_reviews(session):
    reviews = session.query(Review).all()

    if not reviews:
        console.print("[yellow]No reviews found.[/yellow]")
        return

    table = Table(title="Book Reviews")
    table.add_column("ID", style="dim")
    table.add_column("Book", style="green")
    table.add_column("Rating", style="blue")
    table.add_column("Comment", style="magenta")

    for review in reviews:
        book_title = review.book.title if review.book else "Unknown Book"
        table.add_row(str(review.id), book_title, str(review.rating), review.comment or "")

    console.print(table)

def add_review(session):
    console.print("[bold]Add a New Review[/bold]")

    # Get all books for selection
    books = session.query(Book).all()

    if not books:
        console.print("[yellow]No books available. Please add a book first.[/yellow]")
        return

    # Display books
    console.print("\nAvailable Books:")
    for i, book in enumerate(books, 1):
        console.print(f"  {i}. {book.title} by {book.author}")

    # Book selection
    book_choice = IntPrompt.ask(
        "Select book number",
        choices=[str(i) for i in range(1, len(books) + 1)]
    )
    selected_book = books[book_choice - 1]

    # Get review details
    rating = IntPrompt.ask("Enter rating (1-5)", choices=["1", "2", "3", "4", "5"])
    comment = Prompt.ask("Enter comment (optional)", default="")

    try:
        new_review = Review(rating=rating, comment=comment, book_id=selected_book.id)
        session.add(new_review)
        session.commit()
        console.print(f"[green]Review for '{selected_book.title}' added successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error adding review: {str(e)}[/red]")

def update_review(session):
    list_reviews(session)

    reviews = session.query(Review).all()
    if not reviews:
        return

    review_id = IntPrompt.ask("Enter the ID of the review to update")
    review = session.query(Review).filter_by(id=review_id).first()

    if not review:
        console.print("[red]Review not found![/red]")
        return

    book_title = review.book.title if review.book else "Unknown Book"
    console.print(f"Updating review for: [bold]{book_title}[/bold]")

    rating = IntPrompt.ask(
        "Enter new rating (1-5)",
        default=str(review.rating),
        choices=["1", "2", "3", "4", "5"]
    )
    comment = Prompt.ask("Enter new comment", default=review.comment or "")

    try:
        review.rating = rating
        review.comment = comment
        session.commit()
        console.print(f"[green]Review updated successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error updating review: {str(e)}[/red]")

def delete_review(session):
    list_reviews(session)

    reviews = session.query(Review).all()
    if not reviews:
        return

    review_id = IntPrompt.ask("Enter the ID of the review to delete")
    review = session.query(Review).filter_by(id=review_id).first()

    if not review:
        console.print("[red]Review not found![/red]")
        return

    book_title = review.book.title if review.book else "Unknown Book"
    confirm = Confirm.ask(f"Are you sure you want to delete review for '{book_title}'?")
    if not confirm:
        console.print("Deletion cancelled.")
        return

    try:
        session.delete(review)
        session.commit()
        console.print(f"[green]Review deleted successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error deleting review: {str(e)}[/red]")

if __name__ == "__main__":
    main()