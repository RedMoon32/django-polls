# poll-system-api

Инструкция по запуску тестов и документации


## Разработка

Для локальной разработки требуется:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`
- `python3.8` (see `pyproject.toml` for full version)
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`

### Запуск
- `$ docker compose up` - бэк доступен по адресс http://localhost:8000/
- `$ docker exec -it [poll-system-api container id] /bin/bash`, потом `$ pytest`


## Документация

Документация по API доступна по адресу http://localhost:8000/swagger/
