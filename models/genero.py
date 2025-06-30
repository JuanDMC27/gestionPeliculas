from mongoengine import *

class Genero(Document):
    nombre = StringField(max_length=50, unique= True, required=True)