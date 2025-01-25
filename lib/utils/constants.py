from enum import Enum

class ColumnDataType(Enum):
    FLOATING = "floating"
    INTEGER = "integer"
    DATETIME = "datatime"
    DATE = "date"
    STRING = "string"