import json

f = open('data.json')
data = json.load(f)
default_path = data['default_path']
f.close()

data['default_path'] = 'siema'

data['blog'] = {'URL': 'datacamp.com', 'name': 'Datacamp'}

data['lista'] = [1, 2, 3, 4]

with open('data.json', 'w') as f:
    json.dump(data, f)

print(data['blog']['URL'])

