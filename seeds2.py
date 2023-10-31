import json
from models2 import Author, Quote
import connect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Завантаження даних з authors.json
logger.info("Завантаження даних з authors.json...")
with open("authors.json", "r") as file:
    authors_data = json.load(file)
    for author_data in authors_data:
        author = Author(
            fullname=author_data["fullname"],
            born_date=author_data["date_born"],
            born_location=author_data["location_born"],
            description=author_data["bio"],
        )
        author.save()
        logger.info(f"Завантажено автора: {author.fullname}")

# Завантаження даних з quotes.json з посиланням на авторів
logger.info("Завантаження даних з quotes.json з посиланням на авторів...")
with open("quotes.json", "r") as file:
    quotes_data = json.load(file)
    for quote_data in quotes_data:
        author_fullname = quote_data["author"]
        author = Author.objects(
            fullname=author_fullname
        ).first()  # Знаходимо автора в колекції "authors"
        if author:
            keywords = quote_data.get("keywords", [])  # Отримуємо список ключових слів
            quote = Quote(
                author=author,
                quote=quote_data["quote"],
                tags=keywords,  # Зберігаємо ключові слова як теги
            )
            quote.save()
            logger.info(f"Завантажено цитату для автора: {author.fullname}")

logger.info("Завантаження завершено.")
