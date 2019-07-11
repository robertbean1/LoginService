from Extended import ExtendedDictionary

class BaseLoginService:
    def __init__(self):
        self.user_table = ExtendedDictionary(hash_type='SHA512')

    def new_user(self, username, password):
        if not username in self.user_table:
            self.user_table[username] = password
            return True
        else:
            return False

    def login(self, username, password):
        if username in self.user_table:
            if self.user_table[username] == self.user_table._hash(password):
                return True
            else:
                return False
        else:
            return False

    def save(self, file_path):
        with open(file_path, 'w+') as file:
            file.write(self.user_table.json_digest())

    def load(self, file_path):
        with open(file_path, 'r') as file:
            self.user_table.load_json(file.read())

class SaltLoginService:
    def __init__(self):
        self.user_table = ExtendedDictionary(hash_type='SHA512')

    def new_user(self, username, password):
        if not username in self.user_table:
            self.user_table[username] = self.user_table._hash(username) + password
            return True
        else:
            return False

    def login(self, username, password):
        if username in self.user_table:
            if self.user_table[username] == self.user_table._hash(self.user_table._hash(username) + password):
                return True
            else:
                return False
        else:
            return False

    def save(self, file_path):
        with open(file_path, 'w+') as file:
            file.write(self.user_table.json_digest())

    def load(self, file_path):
        with open(file_path, 'r') as file:
            self.user_table.load_json(file.read())















