import re

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_cpf(cpf):
    cpf_regex = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
    return re.match(cpf_regex, cpf)
