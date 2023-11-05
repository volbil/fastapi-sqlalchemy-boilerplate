# FastAPI SQLAlchemy Boilerplate

This is (somewhat) production-ready API template built using FastAPI (with Pydantic 2), SQLAlchemy ORM, Alembic for migrations and pytest for tests. It also uses Dynaconf for config file and apscheduler for task scheduling however, it would be a good idea to replace them with something better.

This template is heavily inspired by [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) and [FastAPI and async SQLAlchemy 2.0 with pytest done right](https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html) with some changes.

## Setup

First step would be to set up Poetry virtual environment and install dependencies:

```bash
poetry shell
poetry install
```

After that you need to copy [settings.example.toml](docs/settings.example.toml) to root of your project and rename it to `settings.toml` and put your data into it. Same goes for [alembic.example.ini](alembic.example.ini). Rename it to `alembic.ini` and update `sqlalchemy.url` with your database URL.

Next step is to initialize database using Alembic (I assume by this point you already have PostgreSQL instance running with database created):

```bash
alembic upgrade head
```

Finally to launch API run uvicorn web server:

```bash
uvicorn run:app --port=7272 --reload
```

## Migrations

Using Alembic you can make changes to database schema by creating migrations and upgrading to them:

```bash
alembic revision --autogenerate -m "Migration name"
alembic upgrade head
```

You can also downgrading to previous revision by running:

```bash
alembic downgrade -1
```

I recommend checking out [tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) from Alembic developers. It would give you better idea how you can use this tool.

## Deployment

There is many ways to deploy your FastAPI backend for example by using Docker but I often use systemd for my deployments. First you must create systemd service with content from [boilerplate.service](docs/boilerplate.service) (keep in mind that you should update system user's username and path to code directory). After that you can start service:

```bash
sudo systemctl enable boilerplate
sudo systemctl start boilerplate
```

If you wan't you can also setup [sync-boilerplate.service](docs/sync-boilerplate.service) which is responsible for running scheduled tasks from [sync.py](sync.py) in background using same approach as main service.

Finally you can create nginx reverse proxy to expose your api to the world. You can copy content of [nginx.conf](docs/nginx.conf) to `/etc/nginx/sites-available/api.example.com.conf` (same as before first you must edit config before running it). Once it's done you can enable this config by running:

```bash
sudo ln -s /etc/nginx/sites-available/api.example.com.conf /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

After that your website should be available at `api.example.com` (assuming you've pointed DNS to your server).
