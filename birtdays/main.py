import json


class CoolError(Exception):
    def __init__(self, text):
        self.txt = text


def item_number_by_name(dir, name):
    n = len(dir)
    for i in range(n):
        if dir[i]['name'] == name:
            return i


class Birthdays:
    def __init__(self):
        with open("bd.json") as f:
            self.bd = json.load(f)
        with open("dates.json") as f:
            self.dates = json.load(f)

    def add_person(self, name, date, contact, group):
        target_dir = self.bd
        path_tokens = group.split('/')
        n = len(path_tokens)
        for i, path_token in enumerate(path_tokens):
            if path_token not in target_dir:
                if type(target_dir) != dict:
                    raise CoolError("Can't create folder in a folder with elements")
                target_dir[path_token] = [] if i == n - 1 else {}
            target_dir = target_dir[path_token]
        if type(target_dir) is not list:
            raise CoolError("Can't create element in a folder with folders")
        target_dir.append({
            'name': name,

            'date': date,
            'contact': contact
        })

        target_dir = self.dates
        path_tokens = date.split('/')[1:]
        n = len(path_tokens)
        for i, path_token in enumerate(path_tokens):
            if path_token[0] == "0":
                path_token = path_token[1]
            if path_token not in target_dir:
                if type(target_dir) != dict:
                    raise CoolError("Can't create folder in a folder with elements")
                target_dir[path_token] = [] if i == n - 1 else {}
            target_dir = target_dir[path_token]
        if type(target_dir) is not list:
            raise CoolError("Can't create element in a folder with folders")
        target_dir.append({
            'name': name,
            'group': group,
            'contact': contact
        })

    def apply(self):
        with open("bd.json", 'w') as f:
            json.dump(self.bd, f, sort_keys=True, indent=2)
        with open("dates.json", 'w') as f:
            json.dump(self.dates, f, sort_keys=True, indent=2)


def process(person):
    db = Birthdays()
    db.add_person(person['name'], person['date'], person['contact'], person['group'])
    db.apply()


while True:
    person = {'name': input("What is his/her name? (in English, please)"), "date": input("When did he/she born? (format: yyyy/mm/dd)"), "contact": input("How can I contact him/her?"), "group": input("Where can I find him/her?")}
    process(person)
