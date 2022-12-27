# Shopping cart API

[![Tests](https://github.com/BorisPlaton/text_search_api/actions/workflows/tests.yml/badge.svg)](https://github.com/BorisPlaton/text_search_api/actions/workflows/tests.yml)

The application for searching documents via text fragments. It is a solution for the test [task](https://freezing-helicopter-7fb.notion.site/Python-67777c95bdbe4e59856c59b707349f2d).

Implemented via [FastAPI](https://fastapi.tiangolo.com/).

## Setup

### Development

#### .env.dist

All environment variables that are used in development are specified in the `.env.dist` file. This file is used in the `docker-compose.dev.yml` file and shell scripts.

#### Virtual environment

Firstly, you must install all necessary dependencies. [Poetry](https://python-poetry.org/) is used as a package manager, so print the following command to install all necessary dependencies:

```
$ poetry install --no-root
```

Afterwards, activate it:

```
$ . .venv/bin/activate
```

#### Shell scripts

You have a bunch of scripts in the `scripts` directory. Some of them are used in production, and some are for development purposes. All scripts have a description. Thus, you may familiarize yourself with them.

### Production

#### .env

Before starting the application, you must create `.env` in the root folder. You already have a `.env.prod` file, which contains the template of the `.env` file and some default values.

#### Start application

You have a `docker-compose.yml` file in the root directory with all necessary configuration. If you have created the `.env` file, you will start the application if you print the following command:

```
$ docker-compose up
```

The application works on the `8888` port.
