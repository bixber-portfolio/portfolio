import csv
from datetime import datetime
import os
from collections import Counter

from enums.pretty_settings import ColumnNamesRUS, ColumnNamesENG, RowNames
from .constants import TIMESTAMP
from .settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = Counter()
        self.total_count = 0

    def process_item(self, item, spider):
        status = item[ColumnNamesENG.STATUS.value]
        self.status_counter[status] += 1
        self.total_count += 1
        return item

    def close_spider(self, spider):
        os.makedirs(BASE_DIR, exist_ok=True)
        current_datetime = datetime.utcnow().strftime(TIMESTAMP)
        file_name = f'status_summary_{current_datetime}.csv'
        file_path = f'{BASE_DIR}/{file_name}'
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([ColumnNamesRUS.STATUS.value,
                             ColumnNamesRUS.COUNT.value])
            for status, count in self.status_counter.items():
                writer.writerow([status, count])
            writer.writerow([RowNames.TOTAL.value, self.total_count])
