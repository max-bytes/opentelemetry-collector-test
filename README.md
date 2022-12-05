# Sample setup for testing opentelemetry collector

usecases:

* k8s behavior monitoring for TSA
* ...

## start containers

```bash
docker-compose up -d
```

## Run metrics-producing python app

```bash
python3.10 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt

# run
python single_value.py
# or
python streaming_values.py # stop using Ctrl+C
```

See the raw metrics published by the collector and read by prometheus here: <http://localhost:8889/metrics>

## see metrics in prometheus

<http://localhost:9090>

queries:

```prometheus
test_gauge
```

```prometheus
test_single_gauge
```

## collector healthcheck

<http://localhost:13133>
