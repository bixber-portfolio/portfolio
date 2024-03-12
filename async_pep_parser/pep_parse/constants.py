import re

TIMESTAMP = "%Y-%m-%d_%H-%M-%S"

MAIN_PEP_URL = 'https://peps.python.org/'
MAIN_PEP_DOMAIN = 'peps.python.org'

REGEX_PATTERNS = {
    'find_pep_number_name': re.compile(r'PEP (?P<number>\d+) – (?P<name>.*)'),
}
