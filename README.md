# Публикация комиксов

Скрипт предназначен для публикации случайных комиксов XKCD в группе Вконтакте.

## Как установить

Для написания скрипта использовался __Python 3.10.0__
Инструмент для управления зависимостями __Poetry__

1. Склонировать репозиторий.
2. Создать виртуальное окружение.
3. Установить зависимости:
```
poetry install
```
4. Переименовать файл .env_example в .env

```bash
mv .env_example .env
```
5. В .env нужно внести VK_ACCESS_TOKEN, VK_GROUP_ID.
Пример файла .env:
```text
VK_ACCESS_TOKEN={Ваш токен}
VK_GROUP_ID={ID группы, в которую будут публиковаться комиксы}
```

Для получения VK_ACCESS_TOKEN:
- Создать приложение https://dev.vk.com/ (тип приложения standalone)

- Получить client_id приложения (нажмите редактировать рядом с созданным приложением)
- Получить VK_ACCESS_TOKEN запросом через браузер:
```text
https://oauth.vk.com/authorize?client_id={ID Вашего приложения}&scope=photos,groups,wall,offline&response_type=token&v=5.131
```

6. Запуск приложения:
```bash
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
