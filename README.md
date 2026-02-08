# FastAPI Movie catalog

## Develop

### Setup:

Right click `movie-catalog` -> Mark directory as -> Sources Root

### Configure pre-commit

Install pre-commit hook

```shell
pre-commit install
```

### Install

Install packages
```shell
uv install
```

### Run:

Go to work dir:
```shell
cd movie-catalog
```
Run dev server:
```shell
fastapi dev
```

## Snippets

```shell
python -c 'import secrets; print(secrets.token_urlsafe(16))'
```
