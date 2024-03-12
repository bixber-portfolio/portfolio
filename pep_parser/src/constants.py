import re
from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
LOGGING_DIR = BASE_DIR / 'logs'
LOGGING_FILE = LOGGING_DIR / 'parser.log'

SOUP_PARSER = 'lxml'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

REGEX_PATTERNS = {
    # Поиск тега <a> с архивом документации актуальной версии Python
    'fing_pdf_a4_zip': re.compile(r'.+pdf-a4\.zip$'),
    # Поиск версии и статуса разработки Python в теге <a>
    'find_python_features': re.compile(
        r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    ),
}

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

UNMATCHED_STATUSES_MSG = """
Несовпадающие статусы:
{}
Статус в карточке: {}
Ожидаемые статусы: {}
"""

ABSENCE_STATUS_MSG = """
{}
Статус в карточке: Some unknown status
Ожидаемые статусы: {}
"""
