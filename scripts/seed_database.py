"""
Script to seed the database with sample data.
"""

from faker import Faker

from app.core.logging_config import get_logger, setup_logging
from app.core.security import get_password_hash
from app.db.database import SessionLocal
from app.models import Author, Book, User

setup_logging()
logger = get_logger(__name__)

fake = Faker()


def seed_data():
    """Seed the database with sample data."""
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            logger.info("Database already contains data. Skipping seed.")
            return

        logger.info("Starting database seeding...")

        # Create sample users
        logger.info("Creating sample users...")
        users = []
        for i in range(3):
            user = User(
                username=f"user{i+1}",
                hashed_password=get_password_hash("password123"),
                is_active=True,
            )
            db.add(user)
            users.append(user)

        # Create admin user
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
        )
        db.add(admin_user)
        users.append(admin_user)

        db.commit()
        logger.info(f"Created {len(users)} users")

        # Create sample authors
        logger.info("Creating sample authors...")
        authors = []
        for _ in range(10):
            author = Author(name=fake.name())
            db.add(author)
            db.commit()  # Commit to get the ID
            db.refresh(author)
            authors.append(author)

        logger.info(f"Created {len(authors)} authors")

        # Create sample books
        logger.info("Creating sample books...")
        books = []
        for _ in range(30):
            book = Book(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                author_id=fake.random_element(elements=[author.id for author in authors]),
            )
            db.add(book)
            books.append(book)

        db.commit()
        logger.info(f"Created {len(books)} books")

        logger.info("Database seeding completed successfully!")
        logger.info("\nDefault credentials:")
        logger.info("  Username: admin | Password: admin123")
        logger.info("  Username: user1 | Password: password123")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
