import phonenumbers

_ARGENTINA_COUNTRY_CODE = "AR"

def normalizePhoneNumber(phoneNumber: str):
    return phonenumbers.format_number(phonenumbers.parse(phoneNumber, _ARGENTINA_COUNTRY_CODE), phonenumbers.PhoneNumberFormat.INTERNATIONAL)

#TODO: Sacarlo de un archivo
BANK_SERVERS = {
    "000": {"127.0.0.1", "8001"},
    "001": {"127.0.0.1", "8002"}
}