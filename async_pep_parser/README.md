# ASYNC_PEP_PARSER
## 🔍 Описание:

**Проект ASYNC_PEP_PARSER\*** - это учебный проект на Python, написанный для освоение навыков парсинга при помощи фреймворка Scrapy. Благодаря нему Вы сможете загрузить
статистику по всем PEP-соглашениям (Python Enhancement Proposals).
![logotype](https://repository-images.githubusercontent.com/529502/dab2bd00-0ed2-11eb-8588-5e10679ace4d)

---

## 💡 Как начать пользоваться проектом:

1. **Склонировать проект к себе на компьютер:**
```bash
# HTTPS протокол
git clone https://github.com/BIXBER/scrapy_parser_pep.git
# SSH протокол
git clone git@github.com:BIXBER/scrapy_parser_pep.git
```

2. **Создать и активировать виртуальное окружение:**

```bash
python -m venv venv
source venv/Scripts/activate
```

3. **Обновить пакетный менеджер *pip*:**
```bash
python -m pip install --upgrade pip
```

4. **Установить зависимости из файла requirements.txt:**

```bash
pip install -r requirements.txt
```

---

## ▶️ Примеры использования:
> Перед запуском ознакомьтесь с условиями, описанные ниже в [примечании⬇️](#примечание)...
1. **Загрузить все PEP-соглашения и сводную статику:**
Вы можете узнать, что было добавлено в каждой версии Python, перейдя по ссылке в⬆ списке, а также вывести автора такого обновления:
    ```bash
    scrapy crawl pep
    ```

---

### Примечание:
> **В данном руководстве приведены все возможные варианты использования проекта.**

---

### Стек используемых технологий:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)


> Перечислено в порядке приоритета использования.