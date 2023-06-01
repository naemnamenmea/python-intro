import csv
import os
from builtins import super


class CarBase():
    def __init__(self, brand: str, photo_file_name: str, carrying: str):
        self.car_type: str = 'CarBase'
        self.photo_file_name: str = photo_file_name
        self.brand: str = brand
        self.carrying: float = float(carrying)

        self.__validate()

    @staticmethod
    def _is_valid_photo_format(ext: str):
        return ext in ['.jpg', '.jpeg', '.png', '.gif']

    def __validate(self):
        if not self._is_valid_photo_format(self.get_photo_file_ext()):
            raise ValueError
        if not self.brand:
            raise ValueError

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carrying: str, passenger_seats_count: str):
        super().__init__(brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.car_type: str = 'car'
        self.passenger_seats_count: int = int(passenger_seats_count)

        self.__validate()

    def __validate(self):
        pass


class Truck(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carrying: str, body_whl: str):
        super().__init__(brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.car_type: str = 'truck'
        try:
            sizes = list(map(float, body_whl.split('x')))
            if len(sizes) != 3:
                raise ValueError
        except:
            sizes = [0., 0., 0.]
        self.body_length: float = sizes[0]
        self.body_width: float = sizes[1]
        self.body_height: float = sizes[2]

        self.__validate()

    def __validate(self):
        pass

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carrying: str, extra: str):
        super().__init__(brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.car_type: str = 'spec_machine'
        self.extra: str = extra

        self.__validate()

    def __validate(self):
        if not self.extra:
            raise ValueError


def get_car_list(csv_filename: str):
    try:
        with open(csv_filename, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            try:
                car_list = []
                """
                                          Car Truck SpecMachine
                    car_type	            1	1	1
                    photo_file_name	        1	1	1
                    brand	                1	1	1
                    carrying	            1	1	1
                    
                    passenger_seats_count	1	0	0
                    body_width	            0	1	0
                    body_height         	0	1	0
                    body_length	            0	1	0
                    extra	                0	0	1
                """
                for line in reader:
                    try:
                        car_type = line['car_type']
                        photo_file_name = line['photo_file_name']
                        brand = line['brand']
                        carrying = line['carrying']

                        if car_type == 'car':
                            passenger_seats_count = line['passenger_seats_count']
                            car_list.append(Car(brand=brand, photo_file_name=photo_file_name, carrying=carrying,
                                                passenger_seats_count=passenger_seats_count))
                        elif car_type == 'truck':
                            body_whl = line['body_whl']
                            car_list.append(
                                Truck(brand=brand, photo_file_name=photo_file_name, carrying=carrying,
                                      body_whl=body_whl))
                        elif car_type == 'spec_machine':
                            extra = line['extra']
                            car_list.append(
                                SpecMachine(brand=brand, photo_file_name=photo_file_name, carrying=carrying,
                                            extra=extra))
                        else:
                            continue
                    except:
                        pass
                return car_list
            except csv.Error:
                raise
    except FileNotFoundError:
        raise


if __name__ == '__main__':
    car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
    print(car.car_type, car.brand, car.photo_file_name, car.carrying,
          car.passenger_seats_count, sep='\n')
    # car
    # Bugatti Veyron
    # bugatti.png
    # 0.312
    # 2
    truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
    print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length,
          truck.body_width, truck.body_height, sep='\n')
    # truck
    # Nissan
    # nissan.jpeg
    # 3.92
    # 2.09
    # 1.87
    spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
    print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying,
          spec_machine.photo_file_name, spec_machine.extra, sep='\n')
    # spec_machine
    # Komatsu-D355
    # 93.0
    # d355.jpg
    # pipelayer specs
    print(spec_machine.get_photo_file_ext())
    # '.jpg'
    cars = get_car_list('coursera_week3_cars.csv')
    print(len(cars))
    # 4
    for car in cars:
        print(type(car))
    # <class 'solution.Car'>
    # <class 'solution.Truck'>
    # <class 'solution.Truck'>
    # <class 'solution.Car'>
    """
        <class '__main__.Car'>
        <class '__main__.Truck'>
        <class '__main__.Car'>
        <class '__main__.SpecMachine'>
    """
    print(cars[0].passenger_seats_count)
    # 4
    print(cars[1].get_body_volume())
    # 60.0
