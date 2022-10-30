from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    RESULT = ('Тип тренировки: {training_type}; '
              'Длительность: {duration:.3f} ч.; '
              'Дистанция: {distance:.3f} км; '
              'Ср. скорость: {speed:.3f} км/ч; '
              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.RESULT.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight_kg
                    / self.M_IN_KM * self.duration_h * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        calories = (self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
                    + (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height_cm / self.CM_IN_M)
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight_kg) * self.duration_h * self.MIN_IN_H
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        length_count_pool = self.length_pool_m * self.count_pool
        return length_count_pool / self.M_IN_KM / self.duration_h

    def get_spent_calories(self) -> float:
        cal = self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
        calories = cal * self.CALORIES_WEIGHT_MULTIPLIER
        full_calories = calories * self.weight_kg * self.duration_h
        return full_calories


def read_package(workout_type: str, data: list[int]) -> Type[Training]:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, str] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}
    if workout_type not in training_types:
        raise ValueError('Не верно указан тип тренировки')
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
