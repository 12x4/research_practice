class FakeDB:
    def __init__(self):
        self.db = {}

    def insert(self, person):
        self.db[person.name] = person

    def get(self, name):
        return self.db[name]

    def delete(self, name):
        if name in self.db:
            del self.db[name]
    
    ...  # другие методы работы базой данной
