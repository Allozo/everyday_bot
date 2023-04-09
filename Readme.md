## Запуск локально

```shell
poetry run python -m src.vk_bot.vk_bot
```

## Запуск в docker-compose

```shell
docker-compose up --build -d
```

## Тестирование

```shell
poetry run python -m pytest --cov=src tests/
```

## Форматирование

```shell
poetry run python -m black .
```