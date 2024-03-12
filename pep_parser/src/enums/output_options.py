import enum


@enum.unique
class OutputOptions(enum.Enum):
    PRETTY = 'pretty'
    FILE = 'file'
