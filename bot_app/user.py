from os.path import join, isfile
from json import load, dump
from os import getcwd


class User:
    DIR = join(getcwd(), 'Users')

    def __init__(self, _id):
        self.id = _id
        self.file = f'{_id}.json'
        self.user_path = join(self.DIR, self.file)

        self.navigate()

    def navigate(self):
        if isfile(self.user_path):
            self.load_user()
        else:
            self.save_user()

    def save_user(self):
        data = {
            'id': self.id
        }

        with open(self.user_path, 'w', encoding='utf-8') as file:
            dump(data, file)

    def load_user(self):
        with open(self.user_path, 'r', encoding='utf-8') as file:
            data = load(file)

        self.id = data['id']