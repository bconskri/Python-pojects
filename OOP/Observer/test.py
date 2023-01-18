"""

"""
from solution import *

def main():
    observable = ObservableEngine()
    short_printer = ShortNotificationPrinter()
    full_printer = FullNotificationPrinter()

    observable.subscribe(short_printer)
    observable.subscribe(short_printer)
    observable.subscribe(full_printer)

    observable.notify({"title": "Покоритель",
                       "text": "Дается при выполнении всех заданий в игре"})
    observable.notify({"title": "Победитель",
                       "text": "Дается при выполнении заданий в игре"})
    observable.notify({"title": "Покоритель",
                       "text": "Дается при выполнении всех заданий в игре"})
    observable.notify({"title": "Вин",
                       "text": "Дается в игре"})

    print(short_printer.achievements)
    print(full_printer.achievements)

   list().index()

if __name__ == "__main__":
    main()
