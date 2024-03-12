import re
import logging

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin

from constants import (
    BASE_DIR, MAIN_DOC_URL, MAIN_PEP_URL, EXPECTED_STATUS,
    UNMATCHED_STATUSES_MSG, ABSENCE_STATUS_MSG, SOUP_PARSER, REGEX_PATTERNS,
)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag
from exceptions import ParserFindTagException
from enums.pretty_settings import ColumnNames


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)

    soup = BeautifulSoup(response.text, features=SOUP_PARSER)

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    section_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [(
        ColumnNames.ARTICLE_LINK.value,
        ColumnNames.TITLE.value,
        ColumnNames.REVIEWER.value,
    )]
    for section in tqdm(section_by_python, desc='Парсинг Python-версий'):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)

        response = get_response(session, version_link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, SOUP_PARSER)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')

        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)

    soup = BeautifulSoup(response.text, SOUP_PARSER)

    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException('Ничего не нашлось')

    results = [(
        ColumnNames.DOC_LINK.value,
        ColumnNames.VERSION.value,
        ColumnNames.STATUS.value,
    )]

    for a_tag in a_tags:
        link = a_tag['href']
        found_strings = re.search(
            REGEX_PATTERNS['find_python_features'], a_tag.text,
        )
        if found_strings is not None:
            version, status = found_strings.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)

    soup = BeautifulSoup(response.text, features=SOUP_PARSER)

    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})

    pdf_a4_tag = find_tag(
        table_tag, 'a', attrs={'href': REGEX_PATTERNS['fing_pdf_a4_zip']},
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)

    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, MAIN_PEP_URL)
    soup = BeautifulSoup(response.text, SOUP_PARSER)

    pep_table = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    pep_table_content = find_tag(pep_table, 'tbody')
    pep_tables_rows = pep_table_content.find_all('tr')
    pep_status_count = {}

    for row in tqdm(pep_tables_rows, desc='Парсинг PEP-документаций'):
        relative_link = find_tag(row, 'a')['href']
        pep_link = urljoin(MAIN_PEP_URL, relative_link)

        response = get_response(session, pep_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, SOUP_PARSER)
        pep_content = find_tag(soup, 'section', attrs={'id': 'pep-content'})
        pep_features = find_tag(pep_content, 'dl')
        pep_real_status = pep_features.find(
            string='Status',
        ).find_parent().find_next_sibling().text

        pep_status_count.setdefault(pep_real_status, 0)
        pep_status_count[pep_real_status] += 1

        type_status_str = row.td.text[1:]
        expected_status = EXPECTED_STATUS.get(type_status_str)
        if expected_status is None:
            logging.info(ABSENCE_STATUS_MSG.format(
                pep_link,
                list((EXPECTED_STATUS.get(type_status_str))),
                ))
        if pep_real_status not in expected_status:
            logging.info(UNMATCHED_STATUSES_MSG.format(
                pep_link, pep_real_status, list(expected_status)
                ))
    results = [(ColumnNames.STATUS.value, ColumnNames.COUNT.value)]
    results.extend(pep_status_count.items())
    results.append(('Total', len(pep_tables_rows)))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
