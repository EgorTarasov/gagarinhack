![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)

# ITHub Colledge

## Описание 
Наш сервис представляет собой цифровую платформа для адаптации первокурсников,
которая с помощью ИИ помогает освоиться студентам в новой образовательной среде и гибко настроить свою траекторию развития

## Особенности 
- Сбор информации: Мы собрали всю имеющуюся информацию о колледже для обучения модели: документы, новости, контакты и т.д.
- Интеграция с вк: Определяем интересы пользователей через Вконтакте, что позволяет составлять полный профиль пользователя
- Рекомендации: Первокурсник найдёт у нас персональные подборки сообществ, новостей, а также получит анализ полученных достижений
- Чат-бот: наша предобученная и полностью бесплатная ИИ-модель с полным доступом в Интернет готова ответить
на любые волнующие студентов вопросы: от расположения корпусов до помощи в выборе образовательного трека
- Телеграмм-бот, собирающий отзывы и потребности студентов по процессу адаптации

## Как начать 
Чтобы начать использовать сервис, просто зайдите на нашу веб-страницу и зарегистрируйтесь. 

### [Ссылка на прототип](https://dino-misis.ru/)
### [Ссылка на техническую документацию к backend](https://api.larek.tech/docs)


## Техническая  часть

## Стек приложения
__Бэкенд__: Docker, фреймворк FastApi, базы данных: PostgreSQL и ClickHouse, llm Модель mistral и хранилище S3

__Фронтенд__: React, Tailwind, TypeScript, MobX

# Запуск приложения

## Установка 

  
Для запуска приложения сначала требуется скачать его исходный код с GitHub, используя Git. Убедитесь, что у вас установлен Git, следуя инструкциям для вашей операционной системы (Windows, Mac, Linux). После установки выполните следующую команду в терминале:



```bash
git clone https://github.com/EgorTarasov/gagarinhack
```

Перед запуском приложения необходимо убедиться, что все значения переменных окружения в файле `src/.env` заполнены корректно. Для этого скопируйте файл `.env.example` и вставьте валидные значения. Вы можете выполнить следующую команду в терминале для копирования:

bashCopy code

`cp src/.env.example src/.env`

Затем откройте файл `src/.env` в текстовом редакторе и внесите необходимые значения для переменных окружения, такие как база данных, ключи API и другие конфигурационые параметры, которые могут быть необходимы для вашего приложения. После этого вы будете готовы к запуску вашего приложения.

Далее, для упрощения развертывания приложения, требуется установить Docker. Вы можете скачать и установить Docker и docker-compose с официального сайта [Docker](https://www.docker.com/). После установки Docker выполните следующую команду в терминале, находясь в каталоге `src` :

```bash
docker compose up -d
```

Это запустит приложение в контейнерах Docker, обеспечивая изоляцию и портативность.

После запуска приложения будет доступна техническая документация по ссылке `http://<domain из .env>/docs`


## Команда
[Кирилл, Frontend](https://t.me/biskwiq)

[Даня, ML](https://t.me/denmalbas007)

[Лиза, Product designer](https://t.me/lissey_t)

[Егор, Backend](https://t.me/tarasov_egor)

[Андрей, Backend](https://t.me/using_namespace)

