from abc import ABC, abstractmethod
from enum import Enum

# Кастомное исключение недоступности зоны
class ZoneUnavailableException(Exception):
    pass

# Перечисление типов залов
class ZoneType(Enum):
    GYM = "Тренажёрный зал"
    YOGA = "Зал йоги"
    POOL = "Бассейн"

# Перечисление статусов залов
class ZoneStatus(Enum):
    OPEN = "открыт"
    CLEANING = "на уборке"

# Перечисление мпециализаций тренеров
class Specializations(Enum):
    POWERLIFTING = "Силовые тренировки"
    YOGA = "Йога"
    SWIMMING = "Плавание"

"""Интерфейс Cleanable, обязывающий реализовать метод clean_zone"""
class Cleanable(ABC):
    @abstractmethod
    def clean_zone():
        pass

# Абстрактный класс
class FitnessZone(ABC):
    # Статический атрибут для хранения существующих идентификаторов зон
    _existing_zone_ids = set()
    def __init__(self, zone_id, zone_type, capacity, status):
        # protected поля:
        self._zone_id = zone_id # Идентификатор зоны
        self._type = zone_type # Тип зоны
        self._capacity = capacity # Вместимость зоны в людях
        self._status = status # Статус зоны

    # Свойства для доступа к атрибутам:
    @property
    def zone_id(self):
        return self._zone_id
    @zone_id.setter
    def zone_id(self, value):
        self._zone_id = value

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value

    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

    # Абстрактный метод для подготовки зоны
    @abstractmethod
    def prepare_zone(self):
        # pass позволяет не реализовывать метод
        pass

    # Переопределение магического метода __str__()
    def __str__(self):
        return f"ID зоны: {self.zone_id}, Тип зоны: {self.type}, Вместимость зоны: {self.capacity}, Статус зоны: {self.status}"
        
    # Переопределение магического метода __new__()
    def __new__(cls, zone_id, *args, **kwargs):
        # Запрещаем создание объекта с существующим идентификатором
        if zone_id in FitnessZone._existing_zone_ids:
            raise ValueError(f"Зона с идентификатором {zone_id} уже существует.")
        return super().__new__(cls)
    
class GymZone(FitnessZone, Cleanable):
    def __init__(self, zone_id, capacity, status, machines_count : int, ventilation: bool):
        super().__init__(zone_id, ZoneType.GYM, capacity, status)
        self.__machines_count = machines_count
        self.__ventilation = ventilation

    # Свойства для доступа к атрибутам:
    @property
    def machines_count(self):
        return self.__machines_count
    @machines_count.setter
    def machines_count(self, value):
        self.__machines_count = value

    @property
    def ventilation(self):
        return self.__ventilation
    @ventilation.setter
    def ventilation(self, value):
        self.__ventilation = value

    # Переопределение абстрактного метода подготовки зоны
    def prepare_zone(self):
        self.status = ZoneStatus.CLEANING
    # Реализация метода clean_zone интерфейса Cleanable
    def clean_zone(self):
        self.status = ZoneStatus.OPEN
    
class YogaZona(FitnessZone):
    def __init__(self, zone_id, capacity, status, zone_square, carpet_type):
        super().__init__(zone_id, ZoneType.YOGA, capacity, status)
        self.__zone_square = zone_square
        self.__carpet_type = carpet_type

    # Свойства для доступа к атрибутам:
    @property
    def zone_square(self):
        return self.__zone_square
    @zone_square.setter
    def zone_square(self, value):
        self.__zone_square = value

    @property
    def carpet_type(self):
        return self.__carpet_type
    @carpet_type.setter
    def carpet_type(self, value):
        self.__carpet_type = value

    # Переопределение абстрактного метода подготовки зоны
    def prepare_zone(self):
        self.status = ZoneStatus.CLEANING
    # Реализация метода clean_zone интерфейса Cleanable
    def clean_zone(self):
        self.status = ZoneStatus.OPEN
    
class PoolZone(FitnessZone):
    def __init__(self, zone_id, capacity, status, pool_len, pool_depth):
        super().__init__(zone_id, ZoneType.POOL, capacity, status)
        self.__pool_len = pool_len
        self.__pool_depth = pool_depth

    # Свойства для доступа к атрибутам:
    @property
    def pool_len(self):
        return self.__pool_len
    @pool_len.setter
    def pool_len(self, value):
        self.__pool_len = value

    @property
    def pool_depth(self):
        return self.__pool_depth
    @pool_depth.setter 
    def pool_depth (self, value):
        self.__pool_depth = value

    # Переопределение абстрактного метода подготовки зоны
    def prepare_zone(self):
        self.status = ZoneStatus.CLEANING
    # Реализация метода clean_zone интерфейса Cleanable
    def clean_zone(self):
        self.status = ZoneStatus.OPEN

class Trainer():
    def __init__(self, full_name, specialization, experience):
        self.__full_name = full_name
        self.__specialization = specialization
        self.__experience = experience

    # Свойства для доступа к атрибутам:
    @property
    def full_name(self):
        return self.__full_name
    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    @property
    def specialization(self):
        return self.__specialization
    @specialization.setter
    def specialization(self, value):
        self.__specialization = value

    @property
    def experience(self):
        return self.__experience
    @experience.setter
    def experience(self, value):
        self.__experience = value

    # Методы:
    def work_in_zone(self, fitness_zone: FitnessZone):
        if fitness_zone.status == ZoneStatus.CLEANING:
            raise ZoneUnavailableException(f"Зона {fitness_zone.zone_id} находится на уборке.")
        
        return f"Тренер {self.full_name} вышел на смену в зоне {fitness_zone.zone_id}"

class FitnessCenter():
    def __init__(self, zones=None, trainers=None):
        self.__zones = zones if zones is not None else []
        self.__trainers = trainers if trainers is not None else []

    # Свойства для доступа к атрибутам:
    @property
    def zones(self):
        return self.__zones
    @zones.setter
    def zones(self, value):
        self.__zones = value

    @property
    def trainers(self):
        return self.__trainers
    @trainers.setter
    def trainers(self, value):
        self.__trainers = value

    # Методы
    def add_zone(self, zone: FitnessZone):
        if zone.zone_id in [z.zone_id for z in self.zones]:
            raise ValueError(f"Зона с идентификатором {zone.zone_id} уже существует в фитнес-центре.")
        self.zones.append(zone)

    def remove_zone(self, zone: FitnessZone):
        if zone.zone_id not in [z.zone_id for z in self.zones]:
            raise ValueError(f"Зона с идентификатором {zone.zone_id} не найдена в фитнес-центре.")    
        self.zones.remove(zone)
        
    def get_available_zones(self):
        return [zone for zone in self.zones if zone.status == ZoneStatus.OPEN]

class TrainingSession():
    __existing_session_ids = set()
    def __init__(self, session_id, date_time, members_count):
        self.__session_id = session_id
        self.__date_time = date_time
        self.__members_count = members_count

    # Свойства для доступа к атрибутам:
    @property
    def session_id(self):
        return self.__session_id
    @session_id.setter
    def session_id(self, value):
        self.__session_id = value

    @property
    def date_time(self):
        return self.__date_time
    @date_time.setter
    def date_time(self, value):
        self.__date_time = value

    @property
    def members_count(self):
        return self.__members_count
    @members_count.setter
    def members_count(self, value):
        self.__members_count = value

    # Методы:
    def get_session_info(self):
        return f"Номер тренировки: {self.session_id}, дата и время: {self.date_time}, количество участников: {self.members_count}" 

    # Переопределение магического метода __new()
    def new(cls, session_id, *args, **kwargs):
        # Запрещаем создание объекта с существующим идентификатором
        if session_id in TrainingSession.__existing_session_ids:
            raise ValueError(f"Тренировка с идентификатором {session_id} уже существует.")
        return super().__new__(cls)
    
class FitnessNetwork():
    def __init__(self, centers=None):
        self.__centers = centers if centers is not None else []
        self.__zone_sessions = {} # Словарь для хранения назначенных тренировок зонам

    # Свойства для доступа к атрибутам:
    @property
    def centers(self):
        return self.__centers 
    @centers.setter
    def centers(self, value):
        self.__centers = value

    @property
    def zone_sessions(self):
        return self.__zone_sessions
    @zone_sessions.setter
    def zone_sessions(self, value):
        self.__zone_sessions = value

    # Методы:
    def add_center(self, center: FitnessCenter):
        self.centers.append(center)

    def remove_center(self, center: FitnessCenter):
        self.centers.remove(center)
    
    def assign_session_to_zone(self, session: TrainingSession, zone: FitnessZone):
        if zone.status == ZoneStatus.CLEANING:
            raise ZoneUnavailableException(f"Зона {zone.zone_id} находится на уборке.")

        self.zone_sessions[zone.zone_id] = session
        return (f"Тренировка {session.session_id} назначена зоне {zone.zone_id}")
        
    def get_session_for_zone(self, zone: FitnessZone):
        return self.zone_sessions.get(zone.zone_id, None)

    def assign_trainer(self, trainer: Trainer, zone: FitnessZone):
        # Проверяем, что зона существует хотя бы в одном из центров
        zone_exists = False
        for center in self.centers:
            if zone in center.zones:
                zone_exists = True
                break
        
        if not zone_exists:
            raise ValueError(f"Зона с идентификатором {zone.zone_id} не найдена ни в одном из фитнес-центров сети.")
        
        # Проверяем специализацию тренера и тип зоны
        if zone.type == ZoneType.GYM and trainer.specialization != Specializations.POWERLIFTING:
            raise ValueError(f"Предупреждение: Тренер {trainer.full_name} не специализируется на силовых тренировках.")
        elif zone.type == ZoneType.YOGA and trainer.specialization != Specializations.YOGA:
            raise ValueError(f"Предупреждение: Тренер {trainer.full_name} не специализируется на йоге.")
        elif zone.type == ZoneType.POOL and trainer.specialization != Specializations.SWIMMING:
            raise ValueError(f"Предупреждение: Тренер {trainer.full_name} не специализируется на плавании.")
        
        return trainer.work_in_zone(zone)

class FitnessPolicies:
    @staticmethod
    def get_fitness_rules():
        rules = [
                "1. Соблюдайте правила гигиены: используйте полотенце на тренажерах и протирайте их после использования.",
                "2. Возвращайте спортивный инвентарь на место после использования.",
                "3. Не оставляйте личные вещи в зонах тренировок.",
                "4. Используйте подходящую спортивную одежду и обувь.",
                "5. Уважайте других посетителей зала и не создавайте шум.",
                "6. Соблюдайте инструкции тренеров и персонала.",
                "7. Не занимайтесь самолечением и проконсультируйтесь с врачом перед началом тренировок.",
                "8. При возникновении травм или недомоганий немедленно обратитесь к персоналу.",
                "9. Не допускается посещение зала в состоянии алкогольного или наркотического опьянения.",
                "10. Соблюдайте правила техники безопасности при работе с тренажерами."
            ]
        return rules
    
def main():
    # Создание зон
    try:
        gym_zone1 = GymZone(zone_id="GYM001", capacity=30, status=ZoneStatus.OPEN, machines_count=20, ventilation=True)
        yoga_zone1 = YogaZona(zone_id="YOGA001", capacity=15, status=ZoneStatus.OPEN, zone_square=50, carpet_type="Джут")
        pool_zone1 = PoolZone(zone_id="POOL001", capacity=20, status=ZoneStatus.OPEN, pool_len=25, pool_depth=1.5)
    except ValueError as e:
        print(f"Ошибка при создании зоны: {e}")
        return

    # Создание тренеров
    trainer1 = Trainer(full_name="Иван Иванов", specialization=Specializations.POWERLIFTING, experience=5)
    trainer2 = Trainer(full_name="Мария Смирнова", specialization=Specializations.YOGA, experience=3)
    trainer3 = Trainer(full_name="Петр Петров", specialization=Specializations.SWIMMING, experience=7)

    # Создание фитнес-центра
    fitness_center1 = FitnessCenter(zones=[gym_zone1, yoga_zone1, pool_zone1], trainers=[trainer1, trainer2, trainer3])

    # Создание фитнес-сети
    fitness_network = FitnessNetwork(centers=[fitness_center1])

    # Проверка добавления и удаления зоны
    try:
        gym_zone2 = GymZone(zone_id="GYM002", capacity=25, status=ZoneStatus.OPEN, machines_count=15, ventilation=False)
        fitness_center1.add_zone(gym_zone2)
        print("Зона успешно добавлена.")
    except ValueError as e:
        print(f"Ошибка при добавлении зоны: {e}")

    try:
        fitness_center1.remove_zone(gym_zone2)
        print("Зона успешно удалена.")
    except ValueError as e:
        print(f"Ошибка при удалении зоны: {e}")

    # Проверка получения доступных зон
    available_zones = fitness_center1.get_available_zones()
    print("Доступные зоны:")
    for zone in available_zones:
        print(zone)

    # Проверка работы тренера в зоне
    try:
        # gym_zone1.prepare_zone()
        print(trainer1.work_in_zone(gym_zone1))
    except ZoneUnavailableException as e:
        print(f"Ошибка: {e}")

    # Проверка назначения тренировки зоне
    try:
        session1 = TrainingSession(session_id="SES001", date_time="2024-01-20 10:00", members_count=10)
        print(fitness_network.assign_session_to_zone(session1, gym_zone1))
    except ZoneUnavailableException as e:
        print(f"Ошибка: {e}")

    # Проверка получения тренировки для зоны
    session_for_zone = fitness_network.get_session_for_zone(gym_zone1)
    if session_for_zone:
        print(f"Назначенная тренировка для зоны {gym_zone1.zone_id}: {session_for_zone.get_session_info()}")
    else:
        print(f"Для зоны {gym_zone1.zone_id} не назначено тренировок.")

    # Проверка назначения тренера зоне (с проверкой специализации)
    try:
        print(fitness_network.assign_trainer(trainer1, gym_zone1))
    except Exception as e:
        print(f"Ошибка при назначении тренера: {e}")

    # Попытка создания зоны с существующим ID
    try:
        gym_zone_duplicate = GymZone(zone_id="GYM001", capacity=20, status=ZoneStatus.OPEN, machines_count=10, ventilation=True)  # Пытаемся создать зону с тем же ID
        print("Ошибка: Зона с существующим ID была создана.")
    except ValueError as e:
        print(f"Ожидаемое исключение: {e}")

    # Демонстрация политик фитнес-центра
    print("\nПравила фитнес-центра:")
    for rule in FitnessPolicies.get_fitness_rules():
        print(rule)

    # Демонстрация подготовки и уборки зоны
    print(f"\nСтатус зоны {gym_zone1.zone_id}: {gym_zone1.status.value}")
    gym_zone1.prepare_zone()
    print(f"Статус зоны {gym_zone1.zone_id} после подготовки: {gym_zone1.status.value}")
    gym_zone1.clean_zone()
    print(f"Статус зоны {gym_zone1.zone_id} после уборки: {gym_zone1.status.value}")

if __name__ == "__main__":
    main()

    