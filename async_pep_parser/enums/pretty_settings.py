import enum


@enum.unique
class ColumnNamesRUS(enum.Enum):
    STATUS = 'Статус'
    COUNT = 'Количество'


@enum.unique
class ColumnNamesENG(enum.Enum):
    NUMBER = 'number'
    NAME = 'name'
    STATUS = 'status'


@enum.unique
class RowNames(enum.Enum):
    TOTAL = 'Total'
