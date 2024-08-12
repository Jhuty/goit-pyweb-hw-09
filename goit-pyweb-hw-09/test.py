from mongoengine import connect
from models import Author, Quote

# Подключение к базе данных
uri = "mongodb+srv://Boris:ytunymuny@cluster0.nsntelu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connect(host=uri)

# Проверка авторов
authors = Author.objects()
for author in authors:
    print(f"Author: {author.fullname}, Born Date: {author.born_date}, Born Location: {author.born_location}")

# Проверка цитат
quotes = Quote.objects()
for quote in quotes:
    print(f"Quote: {quote.text}, Author: {quote.author.fullname}, Tags: {', '.join(quote.tags)}")
