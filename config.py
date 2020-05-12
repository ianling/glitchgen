import json


class Config:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.config = json.load(file)

    @property
    def sprites_dir(self):
        return self.config['sprites_dir']
    