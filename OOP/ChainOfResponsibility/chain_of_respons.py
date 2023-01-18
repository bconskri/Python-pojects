"""
Вам дан объект класса SomeObject, содержащего три поля: integer_field, float_field и string_field:

12345
class SomeObject:    def __init__(self):        self.integer_field = 0        self.float_field = 0.0        self.string_field = ""

Необходимо реализовать поведение:

EventGet(<type>) создаёт событие получения данных соответствующего типа
EventSet(<value>) создаёт событие изменения поля типа type(<value>)
Необходимо реализовать классы NullHandler, IntHandler, FloatHandler, StrHandler так, чтобы можно было создать цепочку:

1
chain = IntHandler(FloatHandler(StrHandler(NullHandler)))

Описание работы цепочки:

chain.handle(obj, EventGet(int)) — вернуть значение obj.integer_field
chain.handle(obj, EventGet(str)) — вернуть значение obj.string_field
chain.handle(obj, EventGet(float)) — вернуть значение obj.float_field
chain.handle(obj, EventSet(1)) — установить значение obj.integer_field =1
chain.handle(obj, EventSet(1.1)) — установить значение obj.float_field = 1.1
chain.handle(obj, EventSet("str")) — установить значение obj.string_field = "str"
"""
GET_EVENT, SET_EVENT = 1, 0

class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""

class EventSet:

    def __init__(self, value):
        self.kind = SET_EVENT
        self.type = type(value)
        self.value = value

class EventGet:

    def __init__(self, type):
        self.kind = GET_EVENT
        self.type = type

class NullHandler(object):

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):

    def handle(self, obj, event):
        if event.type == int:
            if event.kind == SET_EVENT:
                obj.integer_field = event.value
            elif event.kind == GET_EVENT:
                return obj.integer_field
        else:
            print("int: Передаю обработку дальше")
            return super().handle(obj, event)

class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if event.type == float:
            if event.kind == SET_EVENT:
                obj.float_field = event.value
            elif event.kind == GET_EVENT:
                return obj.float_field
        else:
            print("float: Передаю обработку дальше")
            return super().handle(obj, event)

class StrHandler(NullHandler):

    def handle(self, obj, event):
        if event.type == str:
            if event.kind == SET_EVENT:
                obj.string_field = event.value
            elif event.kind == GET_EVENT:
                return obj.string_field
        else:
            print("str: Передаю обработку дальше")
            return super().handle(obj, event)

def main():
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(obj, EventGet(int)))
    #42
    print(chain.handle(obj, EventGet(float)))
    #3.14
    print(chain.handle(obj, EventGet(str)))
    #'some text'
    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))
    # 100
    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))
    #0.5
    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))
    #'new text'


if __name__ == "__main__":
    main()
