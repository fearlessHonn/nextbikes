from data.city import City
from time import sleep


karlsruhe = City('Karlsruhe')

i = 0
while True:
    karlsruhe.refresh()
    i += 1
    print(i)
    sleep(10)
