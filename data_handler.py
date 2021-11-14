import json

class Room:
    def __init__(self, name, description, image, position, can_go_to, objects, conditions):
        self.name = name
        self.description = description
        self.image = image
        self.position = position
        self.can_go_to = can_go_to
        self.objects = objects
        self.conditions = conditions

def load_data():
    data = json.loads(open('data.json', 'r', encoding='utf-8').read())
    rooms = []
    for element in data:
        rooms.append(Room(element['name'], element['description'], element['sprite'], element['position'], element['can_go_to'], element['objects'], element['conditions']))
    return rooms

def load_config():
    return json.loads(open('config.json', 'r', encoding='utf-8').read())
