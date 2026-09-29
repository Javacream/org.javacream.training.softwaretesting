# Beeceptor: Online-Mock-Server einrichten

## Ziel

Beeceptor stellt einen öffentlich erreichbaren Mock-Endpunkt bereit, der auf `GET /users` mit fest definierten JSON-Daten antwortet. Derselbe Endpoint kann von den Python- und C#-Beispielen verwendet werden.

## Endpoint erstellen

Öffne Beeceptor und erstelle über **Create Endpoint** einen neuen Endpoint, zum Beispiel:

```text
softwaretesting-users
```

Beeceptor erzeugt daraus eine eigene URL. Verwende die tatsächlich im Dashboard angezeigte URL.

## Mocking Rule

Lege unter **Mocking Rules** eine Regel an:

| Einstellung | Wert |
|---|---|
| HTTP Method | `GET` |
| Request Path | `/users` |
| Status Code | `200` |
| Content-Type | `application/json` |

Response Body:

```json
[
  {
    "id": 101,
    "name": "Test User One",
    "username": "testuser1",
    "email": "user1@test.example"
  },
  {
    "id": 102,
    "name": "Test User Two",
    "username": "testuser2",
    "email": "user2@test.example"
  }
]
```

Speichere die Regel.

## Endpoint testen

Rufe im Browser den Pfad `/users` deines Endpoints auf. Als Antwort sollten die beiden definierten User erscheinen.

## Weitere Möglichkeiten

Zusätzliche Regeln können beispielsweise `404`, `500`, leere Listen, unvollständiges JSON oder verzögerte Antworten simulieren.

Beeceptor-Endpunkte sind öffentlich erreichbar. Verwende deshalb keine vertraulichen oder personenbezogenen Testdaten.
