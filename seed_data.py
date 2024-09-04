from faker import Faker
from sqlalchemy.orm import Session
from models import User, Book, Author
from crud import create_user, create_book, create_author
from database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake = Faker()

# Seed fake data into the database
def seed_data(db: Session):
    # Seed users
    for _ in range(3):
        user = User(
            username=fake.user_name(),
            hashed_password=pwd_context.hash("password123"),
            is_active=True
        )
        db.add(user)

    # Seed authors
    authors = []
    for _ in range(5):
        author = Author(name=fake.name())
        db.add(author)
        authors.append(author)

    # Seed books
    for _ in range(10):
        book = Book(
            title=fake.catch_phrase(),
            description=fake.text(),
            author_id=fake.random_element(elements=[author.id for author in authors])
        )
        db.add(book)

    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()
    print("Database seeded successfully.")
