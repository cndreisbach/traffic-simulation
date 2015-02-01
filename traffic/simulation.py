import traffic.car as simcar
import numpy as np
import matplotlib as plt
import seaborn as sea

def make_car(**kwargs):
    car_params = {"speed": 0,
                  "max_speed": 34,
                  "acceleration": 2,
                  "minimum_spacing": 25,
                  "braking_prob": 0.1}
    car_params.update(kwargs)
    return simcar.Car(**car_params)

def rotate(cars):
    return cars[1:] + cars[:1]


def run_trials(trials=100, verbose=False, **kwargs):
    means = []
    update_n = int(trials / 20)
    for n in range(1, trials + 1):
        if n % update_n == 0 and verbose:
            print("Running trial {}...".format(n))
        results = Simulation(**kwargs).run()
        results = np.array(results)
        mean = results[:,:,0].mean()
        means.append(mean)

    return np.array(means)


class Simulation:
    def __init__(self, road_length=1000, seconds=60, cars_per_km=30, **kwargs):
        self.car_params = kwargs
        self.road_length = road_length
        self.cars_per_km = cars_per_km
        self.seconds = seconds

    def tick(self, cars):
        cars = [simcar.check_braking(car) for car in cars]
        cars = [simcar.accelerate(car) for car in cars]
        car_pairs = list(zip(cars, rotate(cars)))
        cars = [simcar.adjust_speed(car1, car2, road_length=self.road_length) for car1, car2 in car_pairs]
        cars = [simcar.move(car, road_length=self.road_length) for car in cars]
        return cars

    def run(self):
        snapshots = []
        cars = []

        starting_locations = np.linspace(0, self.road_length - 1, (self.road_length / 1000 * self.cars_per_km))
        for loc in starting_locations:
            cars.append(make_car(location=int(loc), **self.car_params))

        # Run for one minute before collecting data in order to seed the highway.
        for i in range(60):
            cars = self.tick(cars)

        for i in range(self.seconds):
            cars = self.tick(cars)
            snapshots.append([[car.speed, car.location] for car in cars])

        return snapshots

