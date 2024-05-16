# Griptape Astra DB Vector Store Driver

## Usage

`poetry install --with dev,test`

Get Astra DB credentials and an OpenAI API key, export them as environment variables:

```
OPENAI_API_KEY
ASTRA_DB_APPLICATION_TOKEN
ASTRA_DB_API_ENDPOINT
# Optional: ASTRA_DB_KEYSPACE
```

Try `poetry run pytest tests/` and `poetry run python examples/example.py`.

### Versions and status

`0.1.0` (as of 2024-05-16): a very first prototype, not for production usage yet!
