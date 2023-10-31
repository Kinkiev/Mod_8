from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    StringField,
    ReferenceField,
)
from datetime import datetime


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField()
    tags = ListField(StringField())
