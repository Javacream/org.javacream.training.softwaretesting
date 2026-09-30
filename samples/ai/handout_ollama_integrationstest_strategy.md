# Handout: Einen LLM-Integrationstest schrittweise verbessern

## 1. Ausgangssituation

Wir möchten automatisiert testen, ob eine Anwendung mit einem lokal laufenden Ollama-LLM kommunizieren kann.

Als Ausgangspunkt verwenden wir einen bewusst einfachen Test:

```python
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def test_ollama_prompt():
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": "Was ist die Hauptstadt von Frankreich?",
            "stream": False
        },
        timeout=30
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["response"].strip()
    assert "Paris" in data["response"]
```

Der Test funktioniert – vorausgesetzt:

- Ollama ist installiert und läuft auf dem lokalen Rechner.
- Das Modell `llama3.2` ist installiert.
- Der Ollama-Server ist unter Port `11434` erreichbar.
- `pytest` und `requests` sind installiert.

Die Python-Abhängigkeiten können beispielsweise installiert werden mit:

```bash
pip install pytest requests
```

### Ollama vorbereiten

Zunächst prüfen wir, ob der Ollama-Server bereits erreichbar ist:

```bash
curl http://localhost:11434/api/tags
```

Falls Ollama nicht bereits als Hintergrunddienst läuft, kann der Server gestartet werden mit:

```bash
ollama serve
```

Standardmäßig ist er anschließend unter folgender Adresse erreichbar:

```text
http://localhost:11434
```

Das benötigte Modell wird einmalig heruntergeladen:

```bash
ollama pull llama3.2
```

Ein interaktiver Test des Modells ist möglich mit:

```bash
ollama run llama3.2
```

Anschließend kann unser Test ausgeführt werden:

```bash
pytest -v
```

> **Hinweis:** Je nach Betriebssystem und Installation kann Ollama bereits als Hintergrunddienst laufen. In diesem Fall ist ein zusätzliches `ollama serve` nicht erforderlich.

Damit haben wir bereits einen wichtigen Unterschied zu vielen klassischen Tests: **Unser Test ist von einem externen System abhängig.**

---

## 2. Was testen wir eigentlich?

Bevor wir den Test verbessern, sollten wir klären, welche Aussagen er trifft.

Momentan überprüft er gleich mehrere Dinge:

```text
pytest
  │
  ├── HTTP-Verbindung funktioniert
  │
  ├── Ollama antwortet
  │
  ├── Modell ist vorhanden
  │
  ├── Antwort besitzt erwartete JSON-Struktur
  │
  ├── LLM erzeugt überhaupt Text
  │
  └── Antwort enthält "Paris"
```

Das ist charakteristisch für einen **Integrationstest**. Wir testen nicht eine einzelne Python-Funktion isoliert, sondern das Zusammenspiel unseres Testcodes mit einem tatsächlich laufenden Ollama-System.

Das bringt Konsequenzen mit sich: Der Test ist langsamer als ein typischer Unit-Test und kann aufgrund äußerer Bedingungen fehlschlagen.

---

## Schritt 1: Arrange – Act – Assert sichtbar machen

Unser Test lässt sich zunächst strukturieren, ohne sein Verhalten zu verändern.

```python
def test_ollama_prompt():
    # Arrange
    request_data = {
        "model": MODEL,
        "prompt": "Was ist die Hauptstadt von Frankreich?",
        "stream": False
    }

    # Act
    response = requests.post(
        OLLAMA_URL,
        json=request_data,
        timeout=30
    )

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["response"].strip()
    assert "Paris" in data["response"]
```

Die drei Phasen eines Tests werden damit deutlich:

**Arrange** stellt die Voraussetzungen und Testdaten bereit.

**Act** führt die zu testende Aktion aus.

**Assert** überprüft das Ergebnis.

Die Struktur ist besonders hilfreich, wenn Tests später umfangreicher werden.

---

## Schritt 2: Mehrere Dinge werden gleichzeitig geprüft

Betrachten wir die Assertions genauer:

```python
assert response.status_code == 200
assert "response" in data
assert data["response"].strip()
assert "Paris" in data["response"]
```

Hier stecken unterschiedliche Anforderungen:

1. Der HTTP-Aufruf war erfolgreich.
2. Die Ollama-Antwort besitzt die erwartete Struktur.
3. Das LLM hat Text erzeugt.
4. Der Inhalt der Antwort entspricht unserer Erwartung.

Für einen ersten Integrationstest ist das akzeptabel. Trotzdem sollten wir uns bewusst machen, dass ein Fehlschlag unterschiedliche Ursachen haben kann.

Bei

```python
assert response.status_code == 200
```

liegt vermutlich ein technisches Problem vor.

Bei

```python
assert "Paris" in data["response"]
```

dagegen funktioniert die technische Integration möglicherweise einwandfrei – lediglich der generierte Inhalt entspricht nicht unserer Erwartung.

Damit stoßen wir auf eine Besonderheit beim Testen generativer KI:

> **Technische Korrektheit und inhaltliche Korrektheit sind zwei unterschiedliche Testziele.**

---

## Schritt 3: Aussagekräftigere Assertions

Die Standardausgabe einer fehlgeschlagenen Assertion kann verbessert werden.

Statt:

```python
assert response.status_code == 200
```

verwenden wir:

```python
assert response.status_code == 200, (
    f"Ollama antwortete mit HTTP {response.status_code}: "
    f"{response.text}"
)
```

Auch die inhaltliche Prüfung kann mehr Informationen liefern:

```python
assert "Paris" in data["response"], (
    f"Unerwartete LLM-Antwort: {data['response']}"
)
```

Unser Test wird dadurch nicht zuverlässiger. Aber ein Fehler lässt sich wesentlich leichter analysieren.

Das ist eine wichtige Eigenschaft guter Tests:

> Ein guter Test stellt nicht nur einen Fehler fest. Er hilft auch dabei, dessen Ursache zu finden.

---

## Schritt 4: Technische und inhaltliche Tests trennen

Nun können wir zwei unterschiedliche Testziele formulieren.

### Technischer Integrationstest

```python
def test_ollama_returns_response():
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": "Hallo",
            "stream": False
        },
        timeout=30
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["response"].strip()
```

Dieser Test interessiert sich nicht dafür, **was** das Modell antwortet.

Er prüft lediglich:

```text
Python → HTTP → Ollama → Modell → Antwort
```

### Inhaltlicher Test

```python
def test_ollama_knows_capital_of_france():
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": "Was ist die Hauptstadt von Frankreich?",
            "stream": False
        },
        timeout=30
    )

    assert response.status_code == 200

    answer = response.json()["response"]

    assert "Paris" in answer
```

Jetzt sind die Verantwortlichkeiten der Tests klarer getrennt.

---

## Schritt 5: Duplizierung erkennen

Durch die Aufteilung haben wir allerdings ein neues Problem erzeugt.

Beide Tests enthalten denselben HTTP-Aufruf. Bei weiteren Tests entsteht schnell viel duplizierter Code.

Jetzt lohnt sich eine kleine Hilfsfunktion:

```python
def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    assert response.status_code == 200

    return response.json()["response"]
```

Der eigentliche Test wird deutlich kompakter:

```python
def test_ollama_knows_capital_of_france():
    answer = ask_ollama(
        "Was ist die Hauptstadt von Frankreich?"
    )

    assert "Paris" in answer
```

Das Testziel ist nun auf den ersten Blick erkennbar.

---

## Schritt 6: Gehören Assertions in eine Hilfsfunktion?

Unsere Hilfsfunktion enthält momentan:

```python
assert response.status_code == 200
```

Das ist diskutabel.

Eine Alternative wäre:

```python
def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()["response"]
```

Jetzt übernimmt die Hilfsfunktion die Kommunikation und meldet technische HTTP-Fehler über eine Exception.

Der Test enthält nur noch die fachliche Erwartung:

```python
def test_ollama_knows_capital_of_france():
    answer = ask_ollama(
        "Was ist die Hauptstadt von Frankreich?"
    )

    assert "Paris" in answer
```

Damit entsteht eine klarere Trennung:

```text
ask_ollama()
    ↓
technische Kommunikation

test_...
    ↓
Testfall und Erwartung
```

---

## Schritt 7: Konfiguration nicht fest einbauen

Momentan stehen Server und Modell fest im Quellcode:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"
```

Das wird problematisch, sobald der Test auf einem anderen Rechner oder in einer CI/CD-Pipeline läuft.

Wir können Umgebungsvariablen verwenden:

```python
import os


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)
```

Der lokale Aufruf funktioniert weiterhin ohne zusätzliche Konfiguration.

Bei Bedarf kann aber beispielsweise ein anderes Modell verwendet werden:

```bash
OLLAMA_MODEL=gemma3 pytest -v
```

Damit haben wir einen wichtigen Grundsatz umgesetzt:

> Veränderliche Umgebungsinformationen sollten nicht unnötig im Testcode fest verdrahtet werden.

---

## Schritt 8: Was passiert, wenn Ollama nicht läuft?

Wenn Ollama nicht erreichbar ist, kann beispielsweise eine `ConnectionError` auftreten.

Der Test erscheint dann als:

```text
FAILED
```

Aber bedeutet das tatsächlich, dass die getestete Software fehlerhaft ist?

Nicht unbedingt. Vielleicht wurde der Test lediglich in einer Umgebung gestartet, in der Ollama nicht verfügbar ist.

Wir können deshalb vor dem Test prüfen, ob Ollama erreichbar ist. Mit pytest bietet sich dafür eine Fixture an:

```python
import pytest
import requests


@pytest.fixture
def ollama_available():
    try:
        requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )
    except requests.RequestException:
        pytest.skip("Ollama ist nicht erreichbar")
```

Der Test verwendet die Fixture:

```python
def test_ollama_knows_capital_of_france(ollama_available):
    answer = ask_ollama(
        "Was ist die Hauptstadt von Frankreich?"
    )

    assert "Paris" in answer
```

Ist Ollama nicht vorhanden, erhalten wir nun:

```text
SKIPPED
```

statt:

```text
FAILED
```

Damit lernen wir einen wichtigen Unterschied kennen:

```text
PASSED   → getestete Erwartung erfüllt
FAILED   → getestete Erwartung verletzt
SKIPPED  → Test konnte unter diesen Bedingungen nicht sinnvoll ausgeführt werden
```

---

## Schritt 9: Integrationstests kennzeichnen

Da unsere Ollama-Tests externe Infrastruktur benötigen, sollten wir sie von schnellen Unit-Tests unterscheiden können.

pytest unterstützt hierfür **Marker**:

```python
import pytest


@pytest.mark.integration
def test_ollama_knows_capital_of_france(ollama_available):
    answer = ask_ollama(
        "Was ist die Hauptstadt von Frankreich?"
    )

    assert "Paris" in answer
```

In `pytest.ini` registrieren wir den Marker:

```ini
[pytest]
markers =
    integration: Tests mit externen Systemen
```

Nun können ausschließlich Integrationstests ausgeführt werden:

```bash
pytest -m integration
```

Oder wir schließen sie aus:

```bash
pytest -m "not integration"
```

Das wird insbesondere für CI/CD-Pipelines wichtig: Nicht jeder Test muss in jeder Phase einer Pipeline ausgeführt werden.

---

## Schritt 10: Das LLM deterministischer machen

Ein klassisches Programm sollte bei identischer Eingabe normalerweise ein reproduzierbares Ergebnis liefern.

Bei einem LLM ist das nicht selbstverständlich.

Für Tests können wir deshalb die Generierung möglichst deterministisch konfigurieren:

```python
def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()["response"]
```

Eine niedrige Temperature reduziert die Variabilität der Ausgabe.

Aber wichtig ist:

> Wir sollten daraus nicht ableiten, dass sich ein LLM damit wie eine deterministische klassische Funktion verhält.

Gerade diese Grenze ist für Softwaretests von KI-Systemen interessant.

---

## Schritt 11: Fragile Assertions vermeiden

Unsere Assertion

```python
assert "Paris" in answer
```

ist bereits besser als:

```python
assert answer == "Paris"
```

Denn das Modell könnte völlig korrekt antworten:

```text
Die Hauptstadt von Frankreich ist Paris.
```

Ein exakter Stringvergleich würde dann fehlschlagen.

Wir könnten die Prüfung noch etwas robuster machen:

```python
assert "paris" in answer.lower()
```

Damit akzeptieren wir beispielsweise:

```text
Paris
PARIS
Die Hauptstadt ist Paris.
```

Hier zeigt sich ein fundamentaler Unterschied zwischen klassischen Tests und LLM-Tests:

Bei einer klassischen Funktion können wir häufig einen exakten Sollwert formulieren:

```python
assert add(2, 3) == 5
```

Bei generierter natürlicher Sprache testen wir dagegen häufig **Eigenschaften einer zulässigen Antwort**:

```python
assert "paris" in answer.lower()
```

---

## Schritt 12: Mehrere Testfälle parametrisieren

Nun wollen wir mehrere einfache Wissensfragen testen.

Eine schlechte Lösung wäre:

```python
def test_france():
    ...

def test_germany():
    ...

def test_italy():
    ...
```

pytest ermöglicht parametrisierte Tests:

```python
@pytest.mark.integration
@pytest.mark.parametrize(
    "country, capital",
    [
        ("Frankreich", "Paris"),
        ("Deutschland", "Berlin"),
        ("Italien", "Rom"),
    ],
)
def test_capitals(ollama_available, country, capital):
    answer = ask_ollama(
        f"Was ist die Hauptstadt von {country}?"
    )

    assert capital.lower() in answer.lower()
```

Aus einer Testfunktion entstehen drei Testfälle.

pytest zeigt sie auch getrennt an:

```text
test_capitals[Frankreich-Paris]
test_capitals[Deutschland-Berlin]
test_capitals[Italien-Rom]
```

Damit sind **Testlogik und Testdaten voneinander getrennt**.

---

## Schritt 13: Die endgültige Struktur

Unser Test könnte nun beispielsweise so aussehen:

```python
import os

import pytest
import requests


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


def ask_ollama(prompt):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            },
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["response"]


@pytest.fixture
def ollama_available():
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=2,
        )
        response.raise_for_status()
    except requests.RequestException:
        pytest.skip("Ollama ist nicht erreichbar")


@pytest.mark.integration
def test_ollama_returns_response(ollama_available):
    answer = ask_ollama("Antworte mit einem kurzen Satz.")

    assert answer.strip()


@pytest.mark.integration
@pytest.mark.parametrize(
    "country, capital",
    [
        ("Frankreich", "Paris"),
        ("Deutschland", "Berlin"),
        ("Italien", "Rom"),
    ],
)
def test_capitals(ollama_available, country, capital):
    answer = ask_ollama(
        f"Was ist die Hauptstadt von {country}?"
    )

    assert capital.lower() in answer.lower()
```

---

## Was haben wir verbessert?

| Ausgangsproblem | Verbesserung | Testkonzept |
|---|---|---|
| Test schwer zu überblicken | Arrange–Act–Assert | Teststruktur |
| Mehrere Testziele vermischt | Tests getrennt | Single Responsibility |
| Wenig Informationen bei Fehlern | bessere Fehlermeldungen | Diagnostizierbarkeit |
| HTTP-Code dupliziert | `ask_ollama()` | Wiederverwendung |
| Server/Modell fest codiert | Environment Variables | Testkonfiguration |
| Ollama fehlt | `pytest.skip()` | Testvoraussetzungen |
| Langsamer externer Test | Marker | Testklassifikation |
| Variable LLM-Ausgabe | Temperature reduzieren | Reproduzierbarkeit |
| Exakter Stringvergleich zu fragil | Eigenschaften prüfen | robuste Assertions |
| Wiederholte Testfunktionen | `parametrize` | datengetriebene Tests |

Der entscheidende Punkt ist: **Der erste Test war nicht „falsch“.** Er hat funktioniert. Erst indem wir weitere Anforderungen an Wartbarkeit, Fehlersuche, Wiederholbarkeit und verschiedene Ausführungsumgebungen stellen, entstehen die Verbesserungen.

Ein sinnvoller nächster Schritt ist die Frage, welche Teile davon tatsächlich als echte Ollama-Integrationstests ausgeführt werden müssen und welche Teile durch Unit-Tests mit Mocking isoliert getestet werden können.
