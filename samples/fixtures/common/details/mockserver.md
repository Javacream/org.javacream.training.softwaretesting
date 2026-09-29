# Lokaler HTTP-Mock mit MockServer

## Zweck

MockServer stellt einen lokalen HTTP-Server mit kontrollierten Antworten bereit. In diesem Beispiel läuft er in Docker und wird sowohl vom Python- als auch vom C#-Beispiel verwendet.

Der gemeinsame Endpoint lautet:

```text
GET http://localhost:1080/users
```

## Dateien

```text
common/docker/
├── compose.yaml
├── mockserverInitialization.json
└── README.md
```

## Start

```bash
cd common/docker
docker compose up -d
```

Port `1080` des Containers wird auf Port `1080` des Rechners veröffentlicht.

## Expectations

MockServer bezeichnet die Zuordnung einer erwarteten Anfrage zu einer definierten Antwort als **Expectation**.

`mockserverInitialization.json` definiert eine Expectation für:

```text
GET /users
```

Die Antwort enthält Status `200`, `application/json` und zwei fest definierte User.

Die Compose-Datei setzt:

```text
MOCKSERVER_INITIALIZATION_JSON_PATH=/config/mockserverInitialization.json
```

und bindet die JSON-Datei in den Container ein. Dadurch werden die Expectations bereits beim Start geladen.

## Abgrenzung zum Unit-Mock

Beim Unit-Mock wird der HTTP-Zugriff innerhalb des Programms ersetzt. Es findet kein Netzwerkverkehr statt.

Beim MockServer-Test bleibt der HTTP-Client unverändert:

```text
Anwendung
   |
   v
HTTP-Client
   |
   v
HTTP über localhost
   |
   v
MockServer im Docker-Container
```

Damit werden HTTP-Aufruf, Response und JSON-Verarbeitung tatsächlich einbezogen.

## Abgrenzung zu Beeceptor

Beeceptor und MockServer liefern beide kontrollierte Antworten über echtes HTTP.

Beeceptor läuft als externer Online-Dienst. MockServer läuft lokal in Docker. Die MockServer-Konfiguration liegt direkt im Projekt, kann versioniert werden und wird von beiden Sprachbeispielen gemeinsam genutzt.

## Weitere Tests

Weitere Expectations können unter anderem folgende Situationen simulieren:

- `404 Not Found`
- `500 Internal Server Error`
- leere Listen
- fehlerhafte oder unvollständige JSON-Daten
- verzögerte Antworten

## Stoppen

```bash
cd common/docker
docker compose down
```
