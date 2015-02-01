import random
from collections import namedtuple

Car = namedtuple("Car", ["location",
                         "speed",
                         "max_speed",
                         "acceleration",
                         "minimum_spacing",
                         "braking_prob"])


class CrashError(RuntimeError):
    pass


def accelerate(car, amount=None):
    if amount is None:
        amount = car.acceleration
    new_speed = min(car.speed + amount, car.max_speed)
    return car._replace(speed=new_speed)


def check_braking(car, prob=None):
    if prob is None:
        prob = car.braking_prob
    if random.random() <= prob:
        # Brake by x2 b/c we check acceleration next.
        return car._replace(speed=max(0, car.speed - car.acceleration * 2))
    else:
        return car


def move(car, road_length):
    next_loc = (car.location + car.speed) % road_length
    return car._replace(location=next_loc)


def distance(car, next_car, road_length):
    car_loc = car.location
    next_car_loc = next_car.location
    if car_loc > next_car_loc and car_loc - next_car_loc > car.speed:
        next_car_loc += road_length
    return next_car_loc - car_loc


def desired_distance(car):
    """Determine the distance a car wants to be from any other cars."""
    return car.speed + 5


def too_close(car, next_car, road_length):
    dist = distance(car, next_car, road_length)

    if dist < 0:
        raise CrashError("Car at {} crashed into car at {}".format(car.location, next_car.location))

    return dist < desired_distance(car)


def adjust_speed(car, next_car, road_length):
    if too_close(car, next_car, road_length):
        new_speed = min(distance(car, next_car, road_length), car.speed, next_car.speed)  # - car.acceleration
        new_speed = max(0, new_speed)
        return car._replace(speed=new_speed)

    return car


