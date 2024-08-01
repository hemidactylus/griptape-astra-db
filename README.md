# Griptape Astra DB Vector Store Driver

**WARNING: this project has been retired: the Astra DB driver is now in the main Griptape project. [GO THERE](https://docs.griptape.ai/latest/griptape-framework/drivers/vector-store-drivers/#astra-db)**

_I repeat: do not use this connector anymore! What follows is kept for archival purposes only._

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

### Version history

See [CHANGES](CHANGES) file.
