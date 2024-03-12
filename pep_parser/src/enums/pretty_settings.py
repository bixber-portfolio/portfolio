import enum


@enum.unique
class ColumnNames(enum.Enum):
    ARTICLE_LINK = 'Ссылка на статью'
    TITLE = 'Заголовок'
    REVIEWER = 'Редактор, Автор'
    DOC_LINK = 'Ссылка на документацию'
    VERSION = 'Версия'
    STATUS = 'Статус'
    COUNT = 'Количество'
