# 🤖 Anonymous ChatBot in Telegram 📱

[![Telegram Bot](https://img.shields.io/badge/Telegram-@TokumeiChatto-blue)](https://t.me/TokumeiChatto_bot)

A ChatBot that allows users to exchange messages anonymously. The main idea is to allow people to communicate without having to reveal their identity.
A bot was created for the demonstration [@TokumeiChatto](https://t.me/TokumeiChatto_bot)

## System dependencies

- Python 3.11+
- Docker
- docker-compose
- make
- poetry

## Deployment

### Via [Docker](https://www.docker.com/)

- Rename `.env.dist` to `.env` and configure it
- Configure url in `alembic.ini`
- Run `make app-build` command then `make app-run` to start the bot

### Via Systemd service

- Configure and start [PostgreSQL](https://www.postgresql.org/)
- Rename `.env.example` to `.env` and configure it
- Configure url in `alembic.ini`
- Run database migrations with `make migrate` command
- Configure `telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

## Development

### Setup environment

```bash
poetry install
```

### Update database tables structure

**Make migration script:**

```bash
make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES rev_id=ID_MIGRATION
```

**Run migrations:**

```bash
make migrate
```

### Update locales

1. Parse new used localization keys to update locales files
   (`make i18n locale=TRANSLATION_LOCALE`)
2. Write new locales in `.ftl` files by `translations/TRANSLATION_LOCALE`
3. Restart the bot

## Used technologies

- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
