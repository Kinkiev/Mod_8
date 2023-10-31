from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    full_name = StringField()
    email = StringField()
    message_sent = BooleanField(default=False)
