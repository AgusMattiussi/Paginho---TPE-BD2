from sqlalchemy.orm import Session
from pgDatabase import FinancialEntity
from fastapi import status, HTTPException

import crud
import requests

#TODO: Sacarlo de un archivo
_BANK_SERVERS = {
    "000": ["127.0.0.1", "8001"],
    "001": ["127.0.0.1", "8002"]
}

_HTTP_PROTOCOL = "http://"

class UnregisteredEntityException(Exception):
    """Raised when the entity's server is not registered"""
    pass

def _generate_payload(cbuFrom: str, cbuTo: str, amount: float):
    return {
        "cbuFrom": cbuFrom,
        "cbuTo": cbuTo,
        "amount": amount
    }

def _single_bank_transaction(entity: FinancialEntity, cbuFrom: str, cbuTo: str, amount: float):
    if entity.id not in _BANK_SERVERS:
        raise UnregisteredEntityException()
    
    host = _BANK_SERVERS[entity.id][0]
    port = _BANK_SERVERS[entity.id][1]
    url = _HTTP_PROTOCOL + host + ":" + port + "/transactions"
    payload = _generate_payload(cbuFrom, cbuTo, amount)

    result = requests.post(url, json=payload, timeout=10000)
    
    try:
        result.raise_for_status()
    except Exception:
        raise HTTPException(result.status_code)

    return result.status_code == status.HTTP_201_CREATED or result.status_code == status.HTTP_200_OK


def _multiple_bank_transaction(entityFrom: FinancialEntity, entityTo: FinancialEntity, cbuFrom: str, cbuTo: str, amount: float):
    try:
        _single_bank_transaction(entityFrom, cbuFrom, cbuTo, amount)
    except Exception:
        raise
    
    try:
        _single_bank_transaction(entityTo, cbuFrom, cbuTo, amount)
    except Exception:
        # Rollback first transaction
        _single_bank_transaction(entityFrom, cbuTo, cbuFrom, amount)
        raise
    


def bank_transaction(db: Session, cbuFrom: str, cbuTo: str, amount: float):
    entityFrom = crud.get_financial_entity_from_cbu(db, cbuFrom)
    entityTo = crud.get_financial_entity_from_cbu(db, cbuTo)

    if entityFrom.id == entityTo.id:
        try:
            _single_bank_transaction(entityFrom, cbuFrom, cbuTo, amount)
        except Exception:
            raise
    else:
        try:
            _multiple_bank_transaction(entityFrom, entityTo, cbuFrom, cbuTo, amount)
        except Exception:
            raise
    