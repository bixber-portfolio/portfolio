import re

import scrapy

from pep_parse.constants import REGEX_PATTERNS
from enums.pretty_settings import ColumnNamesENG
from pep_parse.items import PepParseItem
from pep_parse.constants import MAIN_PEP_DOMAIN, MAIN_PEP_URL


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = [MAIN_PEP_DOMAIN]
    start_urls = [MAIN_PEP_URL]

    def parse(self, response):
        pep_table = response.css('section#numerical-index')
        all_pep = pep_table.css('td a[href^="pep"]::attr(href)')

        for pep_link in all_pep:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        full_title = response.css('h1.page-title::text').get()
        number, name = re.search(
            REGEX_PATTERNS['find_pep_number_name'], full_title,
        ).groups()

        data = {
            ColumnNamesENG.NUMBER.value: number,
            ColumnNamesENG.NAME.value: name,
            ColumnNamesENG.STATUS.value: response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get(),
        }
        yield PepParseItem(data)
