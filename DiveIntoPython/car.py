import os
import csv


class CarBase:

    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        try:
            self.carrying = float(carrying)
        except:
            self.carrying = float()

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]


class Car(CarBase):

    def __init__(self, brand, photo_file_name, carrying,
                 passanger_seats_count):
        super().__init__('car', brand, photo_file_name, carrying)
        try:
            self.passenger_seats_count = int(passanger_seats_count)
        except:
            self.passenger_seats_count = int()


class Truck(CarBase):

    def __init__(self, brand, photo_file_name, carrying,
                 body_length=0, body_width=0, body_height=0):
        super().__init__('truck', brand, photo_file_name, carrying)
        try:
            self.body_length = float(body_length)
            self.body_width = float(body_width)
            self.body_height = float(body_height)
        except:
            whl = parse_whl(body_length)
            self.body_length = whl[0]
            self.body_width = whl[1]
            self.body_height = whl[2]

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__('spec_machine', brand, photo_file_name, carrying)
        self.extra = extra


def parse_whl(whl):
    try:
        if len(whl.split('x')) > 3:
            raise ValueError

        return [float(x) for x in whl.split('x')]
    except Exception:
        return [float(), float(), float()]


def get_car_list(csv_filepath):
    car_list = []
    with open(csv_filepath) as csv_f:
        reader = csv.reader(csv_f, delimiter=';')
        next(reader)
        for row in reader:
            try:
                brand = row[1]
                if not brand:
                    raise ValueError("incorrect brand")
                photo_file_name = row[3]
                if os.path.splitext(photo_file_name)[-1] not in [".jpg", ".jpeg", ".png", ".gif"]:
                    raise ValueError("incorrect photo_file_name")
                carrying = float(row[5])
                if row[0] == 'car':
                    passanger_seats_count = int(row[2])
                    car_list.append(Car(brand, photo_file_name, carrying,
                                        passanger_seats_count))
                elif row[0] == 'truck':
                    whl = parse_whl(row[4])
                    car_list.append(Truck(brand, photo_file_name, carrying,
                                          *whl))
                elif row[0] == 'spec_machine':
                    extra = row[6]
                    if extra:
                        car_list.append(SpecMachine(brand, photo_file_name,
                                                    carrying, extra))
                else:
                    raise ValueError("incorrect car_type")
            except Exception as err:
                # print(err)
                continue
    return car_list


if __name__ == '__main__':
    car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
    print(car.car_type, car.brand, car.photo_file_name, car.carrying,
    car.passenger_seats_count, sep = '\n')

    truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3x4x5x6')
    print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length,
    truck.body_width, truck.body_height, sep = '\n')

    spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
    print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying,
    spec_machine.photo_file_name, spec_machine.extra, sep = '\n')

    print(spec_machine.get_photo_file_ext())

    cars = get_car_list('cars.csv')
    print(len(cars))
    4
    for car in cars:
        print(type(car))

    print(cars[0].passenger_seats_count)
    print(cars[1].get_body_volume())