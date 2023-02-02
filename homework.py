from typing import ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # Тип тренировки
    duration: float     # Продолжительность, часы
    distance: float     # Дистанция, киллометры
    speed: float        # Скорость, км/ч
    calories: float     # Затрачено энергии, килокалории

    def get_message(self):
        """Отформатировать и вернуть готовое сообщение"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65    # Шаг, метров
    M_IN_KM: ClassVar[float] = 1000     # Метров в км
    MIN_IN_HOUR: ClassVar[float] = 60   # Минут в часы

    action: int         # Количество движений
    duration: float     # Продолжительность, час
    weight: float       # Вес

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    # Коэффициент для формулы
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    # Коэффициент формулы
    K1: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Расчитать колличество затраченных калорий при беге"""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.K1)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_WALK: ClassVar[float] = 0.035     # Коэффициент формулы
    K_WALK2: ClassVar[float] = 0.029    # Коэффициент для формулы
    KM_H_M_S: ClassVar[float] = 0.278   # Коэфициент перевода км/ч в м/сек
    MM_TO_M: ClassVar[int] = 100        # Миллиметров в метре

    height: float  # Рост в мм

    def get_spent_calories(self) -> float:
        """Расчитать колличество затраченных калорий при ходьбе"""
        return ((self.K_WALK * self.weight + ((self.get_mean_speed()
                * self.KM_H_M_S) ** 2 / (self.height / self.MM_TO_M))
                * self.K_WALK2 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38    # "Шаг" в плавании
    K_SWM: ClassVar[float] = 1.1        # Коэффициент формулы
    K_SWM2: ClassVar[float] = 2         # Коэффициент формулы

    length_pool: float    # Длина бассейна, метры
    count_pool: float     # Количество дорожек

    def get_mean_speed(self) -> float:
        """Расчитать среднюю скорость вплавь"""
        return (self.count_pool * self.length_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расчитать колличество затраченных калорий вплавь"""
        return ((self.get_mean_speed() + self.K_SWM)
                * self.K_SWM2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    option_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in option_training:
        return option_training[workout_type](*data)
    raise KeyError(f'Неверный код тренировки: {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
