# Gemeinsamer MockServer

Diese Docker-Konfiguration wird von den Python- und C#-Tests gemeinsam verwendet.

## Start

```bash
docker compose up -d
```

Der Endpoint ist anschließend erreichbar unter:

```text
http://localhost:1080/users
```

## Status

```bash
docker compose ps
```

## Logs

```bash
docker compose logs mockserver
```

## Stoppen

```bash
docker compose down
```
