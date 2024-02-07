import connect
from models import Author, Quote


def find_quote_by_tags(tags_list):
    quotes = Quote.objects(tags__in=tags_list)
    result = {}
    for q in quotes:
        print(q.quote)
        if tags_list in q.tags:
            result[q.author]= [q.quote]
    return result

def find_by_author(author: str):
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def find_by_text(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


def app_work():
    print(f"Use next sample - command: value\nlist of comands: name,text,tags,exit\ntags:life,live")
    while True:
        command = input ("Please enter command >")
        if command == 'exit':
            print("Have a good day!")
            break
        else:
            try:
                arg, value = command.split(':')
                match arg:
                    case 'name':
                        print(find_by_author(value))
                    case 'text':
                        print(find_by_text(value))
                    case 'tags':
                        tag = value.split(',')
                        print(tag)
                        find_quote_by_tags(tag)
                    case _:
                        print("Enter correct command")
            except ValueError:
                print('Incorrect input')



if __name__ == '__main__':
    app_work()
