with open('data.txt') as f:
    data = f.read()


data = data.replace('True', 'true').replace('False', 'false').replace('None', 'null')

with open('data.txt', 'w') as f:
    f.write(data)