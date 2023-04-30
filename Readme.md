# Everyday bot

Данный бот парсит сайт с погодой, собирает данные, а дальше рассылает их пользователям в мессенджерах (VK).

- [Everyday bot](#everyday-bot)
    - [Запуск бота](#запуск-бота)
        - [Клонирование репозитория](#клонирование-репозитория)
        - [Передача токена](#передача-токена)
        - [Если у вас есть docker](#если-у-вас-есть-docker)
        - [Установка зависимостей](#установка-зависимостей)
        - [Запуск бота VK](#запуск-бота-vk)
    - [Для разработчиков](#для-разработчиков)
        - [Запуск `pre-commit`](#запуск-pre-commit)
        - [Запуск форматировщиков](#запуск-форматировщиков)
        - [Запуск тестов](#запуск-тестов)
            - [Локальные тесты](#локальные-тесты)
            - [Docker тесты](#docker-тесты)
        - [Запуск линтеров](#запуск-линтеров)

## Запуск бота

### Клонирование репозитория

Чтобы клонировать данный репозиторий воспользуйтесь командой:

```shell
git clone https://github.com/Allozo/everyday_bot.git
```

### Передача токена

Чтобы подключить бота к сообществу VK, надо сохранить токен этой группы. Сделать это можно, создав файл `.env` и записав в переменную `VK_BOT_TOKEN` токен.

Пример файла `.env`:

```.env
VK_BOT_TOKEN=your_secret_token
```

### Если у вас есть docker

Если у вас установлен Docker, то всего одной командой можно запустить приложение:

```
make docker-up
```

Если же программы `make` у вас не установлена, то можно воспользоваться командой:

```shell
docker-compose up --build -d
```

Если докера нет, то переходите к разделам ниже.

### Установка зависимостей

Для установки зависимостей можно воспользоваться командой:

```shell
make venv
```

Если же программы `make` у вас не установлена, то можно воспользоваться командой:

```shell
python -m pip install --upgrade pip
python -m pip install poetry
poetry install
```

### Запуск бота VK

Для запуска бота в VK можно воспользоваться командой:

```shell
make up
```

Если же программы `make` у вас не установлена, то можно воспользоваться командой:

```shell
poetry run python -m src.vk_bot.vk_bot
```

## Для разработчиков

Чтобы добавить свой Pull Request, убедитесь, что код отформатирован, проходит тесты, а линтеры не выдают ошибки.

### Запуск `pre-commit`

Чтобы пользоваться возможностями `pre-commit` активируйте его следующей командой:

```shell
pre-commit install
```

Самим файлом с хуками является `.pre-commit-config.yaml`. В нём запускаются тесты и линтеры.

Чтобы проверить, что `pre-commit` работает можно выполнить команду:

```shell
pre-commit run --all-files
```

Все зависимости берутся из [установленных](#установка-зависимостей).

### Запуск форматировщиков

Для запуска форматировщика можно воспользоваться командой:

```shell
make format
```

Если же программы `make` у вас не установлена, то можно воспользоваться командами:

```shell
poetry run python -m isort tests src
poetry run python -m black --skip-string-normalization tests src
poetry run python -m autoflake --recursive --in-place --remove-all-unused-imports tests src
poetry run python -m unify --in-place --recursive tests src
```

### Запуск тестов

#### Локальные тесты

Для запуска тестов можно воспользоваться командой:

```shell
make tests
```

Если же программы `make` у вас не установлена, то можно воспользоваться командой:

```shell
poetry run python -m pytest --cov=src tests
```

#### Docker тесты

Также тесты можно запустить в отдельном Docker контейнере:

```shell
make docker-tests
```

Если же программы `make` у вас не установлена, то можно воспользоваться командой:

```shell
docker-compose -f docker-compose-test.yaml up --build -d
```

### Запуск линтеров

Для запуска линтеров можно воспользоваться командой:

```shell
make lint
```

Если же программы `make` у вас не установлена, то можно воспользоваться командой:

```shell
poetry run python -m flake8 --jobs 4 --statistics --show-source tests src
poetry run python -m pylint --jobs 4 --rcfile=setup.cfg tests src
poetry run python -m mypy --install-types tests src
poetry run python -m black --skip-string-normalization --check tests src
```
