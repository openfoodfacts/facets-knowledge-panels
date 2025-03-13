# Testing

### docker setup
```bash
make build_lang
docker compose run --rm facets-api pytest tests
```
or
```bash
make all
```

### virtual env setup
- Checkout `tests` directory
```bash
make build_lang
pytest 
```
