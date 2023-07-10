import re, phonenumbers

_MAX_EMAIL_LENGTH = 254
_MAX_KEY_LENGTH = 50
_MIN_KEY_LENGTH = 5
_ARGENTINA_COUNTRY_CODE = "AR"


def validate_email(email:str):
    emailPattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(emailPattern, email)) and len(email) <= _MAX_EMAIL_LENGTH

def validate_phone_number(phoneNumber:str):
    try:
        parsedPN = phonenumbers.parse(phoneNumber, _ARGENTINA_COUNTRY_CODE)
        return phonenumbers.is_valid_number(parsedPN)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def validate_cuit(cuit:str):
    cuitPattern = r'^(20|23|27|30|33)-[0-9]{8}-[0-9]{1}$'
    return bool(re.match(cuitPattern, cuit))

#TODO: Agregar validador de CBU
def validate_cbu(cbu:str):
    # Expresión regular para validar el formato del CBU
    cbuPattern = r'^\d{22}$'
    return bool(re.match(cbuPattern, cbu))


def validate_amount(amount:str):
    floatAmount = 0.0
    try:  
        floatAmount = float(amount)
    except:
        return False

    if '.' in amount:
        return floatAmount > 0 and len(amount.split('.')[1]) <= 2
    else:
        return floatAmount > 0
    
def validate_alias_key(key:str):
    aliasPattern = r'^[A-Za-z\.-]{5,50}$' # Key length: [5, 50]
    return bool(re.match(aliasPattern, key))

def validate_key_selection(key:str):
    emailPattern = r'^[Ee][Mm][Aa][Ii][Ll]$'
    phonePattern = r'^[Pp][Hh][Oo][Nn][Ee]$'
    cuitPattern = r'^[Cc][Uu][Ii][Tt]$'
    
    return  bool(re.match(emailPattern, key)) or \
            bool(re.match(phonePattern, key)) or \
            bool(re.match(cuitPattern, key)) or \
            validate_alias_key(key)

def validate_password(password:str):
    return len(password) >= 5 and len(password) <= 50

def validate_name(name:str):
    return len(name) >= 3 and len(name) <= 255