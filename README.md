# Proxera Python Client

Drop-in replacement for the OpenAI Python SDK that routes all requests through [Proxera](https://getproxera.com) — giving you logging, cost tracking, rate-limit management, and provider failover with zero code changes.

## Install

```bash
pip install proxera
```

## Quick Start

```python
import proxera

client = proxera.get_client()  # reads PROXERA_API_KEY from env
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

That's it. Every call goes through Proxera's proxy and shows up in your dashboard.

## Configuration

| Parameter | Env Variable | Default |
|-----------|-------------|---------|
| `proxera_key` | `PROXERA_API_KEY` | *(required)* |
| `base_url` | `PROXERA_BASE_URL` | `https://api.getproxera.com/v1` |

### Constructor arguments

```python
client = proxera.get_client(
    proxera_key="px-live_...",       # or set PROXERA_API_KEY
    tags=["my-app", "experiment-1"], # X-Proxera-Tags header
    team="research",                 # X-Proxera-Team header
    provider="anthropic",            # X-Proxera-Provider header
)
```

### Async

```python
import proxera

client = proxera.get_async_client()
response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

### Wrapper classes

If you prefer an object that holds its config:

```python
client = proxera.Client(tags=["my-app"])
client.chat.completions.create(model="gpt-4o", messages=[...])
```

## Usage with LangChain

```python
from langchain_openai import ChatOpenAI
import proxera

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key="px-live_...",
    openai_api_base="https://api.getproxera.com/v1",
)
llm.invoke("Hello!")
```

Or reuse a Proxera client:

```python
import proxera
from langchain_openai import ChatOpenAI

client = proxera.get_client()
llm = ChatOpenAI(model="gpt-4o", client=client)
```

## Documentation

Full docs at [docs.getproxera.com](https://docs.getproxera.com).

## License

MIT
