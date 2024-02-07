from datetime import datetime

from mongoengine import EmbeddedDocument, Document, CASCADE
from mongoengine.fields import (BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField,
                                IntField, ReferenceField)

import connect

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    contacted = BooleanField(default=False)

class Author(Document):
    fullname = StringField(unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()