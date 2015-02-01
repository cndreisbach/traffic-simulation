import pytest
from traffic.car import *


def make_car(**kwargs):
    a_car = Car(location=0,
                speed=0,
                max_speed=35,
                acceleration=2,
                minimum_spacing=25,
                braking_prob=0.1)
    return a_car._replace(**kwargs)


def test_car_can_accelerate():
    a_car = make_car(speed=6, max_speed=10, acceleration=2)

    assert accelerate(a_car).speed == 8
    assert accelerate(a_car, 4).speed == 10


def test_car_will_not_go_past_max_speed():
    a_car = make_car(speed=6, max_speed=10, acceleration=2)
    assert accelerate(a_car, 20).speed == 10


def test_car_may_brake():
    a_car = make_car(speed=6, max_speed=10, braking_prob=1.0)
    assert check_braking(a_car).speed == 2


def test_car_will_move():
    a_car = make_car(speed=30, location=0)
    assert move(a_car, road_length=100).location == 30


def test_car_is_too_close():
    car1 = make_car(location=0, minimum_spacing=25, speed=30)
    car2 = make_car(location=20, speed=10)

    assert too_close(car1, car2, road_length=100)


def test_cars_cannot_pass():
    car1 = make_car(location=25, minimum_spacing=25, speed=30)
    car2 = make_car(location=20, speed=10)

    with pytest.raises(CrashError):
        too_close(car1, car2, road_length=100)


def test_cars_adjust_speed_to_match_next_car():
    car1 = make_car(location=0, minimum_spacing=25, speed=30)
    car2 = make_car(location=20, speed=10)

    car1 = adjust_speed(car1, car2, road_length=100)
    assert car1.speed == 10


def test_cars_do_not_increase_speed_to_match_next_car():
    car1 = make_car(location=15, minimum_spacing=25, speed=20)
    car2 = make_car(location=35, speed=30)

    car1 = adjust_speed(car1, car2, road_length=100)

    assert too_close(car1, car2, road_length=100)
    assert car1.speed == 20