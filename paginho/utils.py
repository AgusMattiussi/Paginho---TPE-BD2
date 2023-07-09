import phonenumbers

_ARGENTINA_COUNTRY_CODE = "AR"

def normalizePhoneNumber(phoneNumber: str):
    return phonenumbers.format_number(phonenumbers.parse(phoneNumber, _ARGENTINA_COUNTRY_CODE), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
