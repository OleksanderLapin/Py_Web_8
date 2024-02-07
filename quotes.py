import json

from models import Quote, Author

with open('files/quotes.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

    for i in data:
        Quote(
            tags=i['tags'],
            quote=i['quote'],
            author=Author.objects(fullname=i['author']).first()
        ).save()
