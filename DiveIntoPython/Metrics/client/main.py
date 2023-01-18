"""

"""
from solution import Client

def main():

     print(client = Client("127.0.0.1", 8888, timeout=15))

     print(client.put("palm.cpu", 0.5, timestamp=1150864247))

     print(client.put("palm.cpu", 2.0, timestamp=1150864248))

     print(client.put("palm.cpu", 0.5, timestamp=1150864248))

     print(client.put("eardrum.cpu", 3, timestamp=1150864250))

     print(client.put("eardrum.cpu", 4, timestamp=1150864251))

     print(client.put("eardrum.memory", 4200000))

     print(client.get("*"))


if __name__ == "__main__":
    main()
