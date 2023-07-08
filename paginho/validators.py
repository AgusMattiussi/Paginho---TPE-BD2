import re
import phonenumbers

_MAX_EMAIL_LENGTH = 254
_MAX_KEY_LENGTH = 50
_MIN_KEY_LENGTH = 5
_ARGENTINA_COUNTRY_CODE = "AR"


def validate_email(email:str):
    emailPattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(emailPattern, email) & len(email) <= _MAX_EMAIL_LENGTH

def validate_phone_number(phoneNumber:str):
    try:
        parsedPN = phonenumbers.parse(phoneNumber, _ARGENTINA_COUNTRY_CODE)
        return phonenumbers.is_valid_number(parsedPN)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

cuitRegex = r'^(20|23|27|30|33)([0-9]{9}|-[0-9]{8}-[0-9]{1})$'

def validate_cuit(cuit:str):
    cuitPattern = r'^(20|23|27|30|33)([0-9]{9}|-[0-9]{8}-[0-9]{1})$'
    return re.match(cuitPattern, cuit)


def validate_alias_key(key:str):
    aliasPattern = r'[A-Za-z\.-]{5,50}' # Key length: [5, 50]
    return re.match(aliasPattern, key)

def validate_key_selection(key:str):
    emailPattern = r'[Ee][Mm][Aa][Ii][Ll]'
    phonePattern = r'[Pp][Hh][Oo][Nn][Ee]'
    cuitPattern = r'[Cc][Uu][Ii][Tt]'
    
    return  re.match(emailPattern, key) | \
            re.match(phonePattern, key) | \
            re.match(cuitPattern, key) | \
            validate_alias_key(key)
