from models2 import Quote, Author
import connect
from mongoengine import Q

while True:
    user_input = input("Команда: ")

    if user_input == "exit":
        break
    elif user_input.startswith("name:"):
        # Пошук цитат за ім'ям автора
        author_name = user_input.split("name: ")[1]
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print(f"Автор {author_name} не знайдений.")
    elif user_input.startswith("tag:"):
        # Пошук  цитат за тегом
        tag = user_input.split("tag: ")[1]
        quotes = Quote.objects(tags__contains=tag)
        for quote in quotes:
            print(quote.quote)
    elif user_input.startswith("tags:"):
        # Пошук цитат за набором тегів
        tags = user_input.split("tags: ")[1].split(",")
        query = Q()
        for tag in tags:
            query |= Q(tags=tag)
        quotes = Quote.objects(query)
        for quote in quotes:
            print(quote.quote)

    elif user_input.startswith(
        "nametag:"
    ):  # команда щоб отримати теги за цитатою конкретного автора
        author_name = user_input.split("nametag: ")[1]
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            tags = set()  # Використовуємо множину для унікальних тегів
            for quote in quotes:
                tags.update(quote.tags)
            print(f"Теги автора {author_name}: {', '.join(tags)}")
        else:
            print(f"Автор {author_name} не знайдений.")

    else:
        print("Невідома команда. Спробуйте ще раз.")
