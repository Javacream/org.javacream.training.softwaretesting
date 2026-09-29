# Python-Beispiel

Die Python-Variante demonstriert vier Tests für dieselbe Funktion `get_users()`.

## Dateien

```text
python/
├── users.py
├── test_users_unit.py
├── test_users_beeceptor.py
├── test_users_local_mockserver.py
├── test_users_integration.py
├── requirements.txt
├── README.md
└── details/
    └── http-mock.md
```

## 1. Unit-Test mit `unittest.mock`

`test_users_unit.py` ersetzt `requests.get()` mit `@patch` durch einen Python-Mock. Es findet kein HTTP-Aufruf statt.

Der Test ist schnell, reproduzierbar und kann exakt festlegen, welche Daten verarbeitet werden. Er prüft außerdem, ob die erwartete URL, der Timeout und `raise_for_status()` verwendet werden.

Er prüft jedoch nicht die echte HTTP-Kommunikation.

Details: [`details/http-mock.md`](details/http-mock.md)

## 2. Online-Mock mit Beeceptor

`test_users_beeceptor.py` führt einen echten HTTP-Aufruf gegen Beeceptor aus. Die dort konfigurierte Antwort ist kontrolliert und enthält feste Testdaten.

Vor der Ausführung muss `BEECEPTOR_URL` auf den eigenen Beeceptor-Endpunkt gesetzt werden.

Die Beeceptor-Einrichtung ist sprachunabhängig beschrieben unter:

[`../common/details/beeceptor.md`](../common/details/beeceptor.md)

## 3. Lokaler MockServer mit Docker

`test_users_local_mockserver.py` verwendet echtes HTTP gegen:

```text
http://localhost:1080/users
```

Der MockServer läuft lokal in Docker. Konfiguration und Testdaten liegen unter `../common/docker/` und werden sowohl von Python als auch von C# verwendet.

Start:

```bash
cd ../common/docker
docker compose up -d
```

Details: [`../common/details/mockserver.md`](../common/details/mockserver.md)

## 4. Integrationstest gegen JSONPlaceholder

`test_users_integration.py` verwendet den echten externen Webservice.

Der Test ist bewusst **sehr pauschal**. Er prüft nur, ob mindestens ein User geliefert wird und ob die Felder die erwarteten Python-Datentypen besitzen.

Konkrete Namen, IDs oder eine feste Anzahl von Datensätzen werden nicht vorausgesetzt, weil die Daten des externen Dienstes nicht unter Kontrolle des Tests stehen. Dadurch besitzt der Test eine hohe technische Realitätsnähe, aber nur eine geringe fachliche Prüftiefe bezüglich der gelieferten Daten.

## Vergleich

| Eigenschaft | Unit-Mock | Beeceptor | Lokaler MockServer | JSONPlaceholder |
|---|---|---|---|---|
| Echtes HTTP | Nein | Ja | Ja | Ja |
| Kontrollierte Daten | Ja | Ja | Ja | Nein |
| Externer Dienst nötig | Nein | Ja | Nein | Ja |
| Detaillierte Assertions | Ja | Ja | Ja | Nur eingeschränkt |
| Prüft echte Gegenstelle | Nein | Nein | Nein | Ja |

Die vier Tests sind keine Rangfolge von schlechter zu besser. Sie prüfen unterschiedliche Aspekte und ergänzen sich.

## Ausführen

```bash
pip install -r requirements.txt
```

Einzelne Tests:

```bash
python -m unittest test_users_unit.py
python -m unittest test_users_beeceptor.py
python -m unittest test_users_local_mockserver.py
python -m unittest test_users_integration.py
```
