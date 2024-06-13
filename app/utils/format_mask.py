@staticmethod
def format_cpf(cpf):
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    else:
        return cpf

@staticmethod
def format_phone_number(phone_number):
    if len(phone_number) == 11:
        return f"({phone_number[:2]}) {phone_number[2:7]}-{phone_number[7:]}"
    return phone_number
