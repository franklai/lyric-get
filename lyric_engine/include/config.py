# coding: utf-8

class Config:
    def __init__(self):
        self.config = {
            'joysound': {
                'id': 'nocbanba@gmail.com',
                'password': 'pfg1103'
            }
        }

    def get(self, module, key):
        if module not in self.config:
            return None

        if key not in self.config[module]:
            return None

        return self.config[module][key]
