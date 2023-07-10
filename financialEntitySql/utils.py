from enum import Enum

class TransactionTypes(Enum):
    INTERNAL = 0
    SUBSTRACT_FUNDS = 1
    ADD_FUNDS = 2