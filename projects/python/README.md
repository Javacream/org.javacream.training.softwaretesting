# Python-Projekt einrichten und Tests ausführen

## 1. Projektstruktur

Das Projekt verwendet eine `src`-Struktur. Der eigentliche Anwendungscode befindet sich unter `src/books`, die Tests liegen getrennt davon im Verzeichnis `test`.

```text
python/
├── pyproject.toml
├── README.md
├── src/
│   └── books/
│       ├── __init__.py
│       ├── booksservice.py
│       ├── storeservice.py
│       └── ...
└── test/
    ├── test_configuration.py
    ├── test_create_book.py
    └── ...
```

Das Package `books` wird als Python-Package installiert. Dadurch können Anwendung und Tests mit regulären Imports arbeiten, ohne den Python-Suchpfad (`PYTHONPATH`) manuell verändern zu müssen.

### Die Datei `pyproject.toml`

Die Datei `pyproject.toml` beschreibt das Python-Projekt und enthält Informationen, die insbesondere für die Installation und den Build des Projekts benötigt werden.

In unserem Projekt erfüllt sie mehrere Aufgaben:

- Sie legt fest, welches **Build-System** für das Python-Projekt verwendet wird.
- Sie enthält grundlegende **Projektinformationen**, beispielsweise den Namen und die Python-Version.
- Sie definiert, dass sich die Python-Packages unterhalb des Verzeichnisses `src` befinden.
- Sie legt die **Abhängigkeiten** der Anwendung fest, beispielsweise `PyYAML`.
- Sie legt fest, welche zusätzlichen Dateien zum Package gehören, beispielsweise `config.yaml`.

Dadurch kann `pip` das Projekt mit

```bash
python -m pip install -e .
```

korrekt installieren.

Der Punkt `.` verweist dabei auf das aktuelle Projektverzeichnis. `pip` findet dort die `pyproject.toml`, liest die darin enthaltene Projektbeschreibung und weiß dadurch unter anderem, wo sich das Package `books` befindet und welche Abhängigkeiten installiert werden müssen.

Die `pyproject.toml` übernimmt damit eine zentrale Rolle für die **Beschreibung, Paketierung und Installation** des Projekts. Die benötigten Einstellungen müssen nicht über lokale Pfade oder manuell gesetzte Umgebungsvariablen vorgenommen werden.

## 2. In das Projektverzeichnis wechseln

Die folgenden Kommandos werden im Hauptverzeichnis des Projekts ausgeführt. Das ist das Verzeichnis, in dem sich die Datei `pyproject.toml` befindet.

Beispiel:

```bash
cd python
```

## 3. Projekt installieren

Vor der ersten Verwendung wird das Projekt mit `pip` installiert:

```bash
python -m pip install -e .
```

### Bedeutung des Kommandos

`python -m pip` startet `pip` mit dem aktuell verwendeten Python-Interpreter.

Die Option `-e` steht für **editable**.

Das Projekt wird damit nicht einfach als unveränderliche Kopie installiert. Stattdessen verweist die Installation auf das lokale Projektverzeichnis.

Der Punkt `.` bezeichnet das aktuelle Verzeichnis. Dort findet `pip` die Datei `pyproject.toml` mit der Beschreibung des Python-Projekts.

Die Kombination

```bash
python -m pip install -e .
```

bedeutet somit sinngemäß:

> Installiere das Python-Projekt aus dem aktuellen Verzeichnis als bearbeitbares Projekt.

Dabei werden auch die in `pyproject.toml` angegebenen Abhängigkeiten installiert.

## 4. Alle Tests ausführen

Zum Ausführen aller Tests verwenden wir das in Python enthaltene Testframework `unittest`:

```bash
python -m unittest discover -s test -v
```

### `python -m unittest`

Mit

```bash
python -m unittest
```

wird das Python-Modul `unittest` gestartet.

`unittest` gehört zur Python-Standardbibliothek. Es muss daher nicht separat installiert werden.

### `discover`

```bash
python -m unittest discover
```

aktiviert die automatische Testsuche.

Die einzelnen Testdateien müssen dadurch nicht beim Aufruf angegeben werden. `unittest` sucht selbstständig nach geeigneten Tests.

### Option `-s`

```text
-s test
```

`-s` steht für **start directory**.

Damit wird festgelegt, in welchem Verzeichnis die automatische Suche nach Tests beginnen soll.

In unserem Projekt liegen die Tests im Verzeichnis `test/`. Deshalb verwenden wir:

```text
-s test
```

### Option `-v`

```text
-v
```

steht für **verbose**.

Diese Option beeinflusst nicht die Testausführung, sondern die Darstellung der Ergebnisse. Die einzelnen ausgeführten Tests und ihr jeweiliges Ergebnis werden angezeigt.

Beispielsweise:

```text
test_create (...) ... ok
test_delete (...) ... ok
test_find_by_isbn (...) ... ok
```

Ohne `-v` würde `unittest` stattdessen hauptsächlich Punkte für erfolgreiche Tests ausgeben.

## 5. Wie werden Testdateien gefunden?

`unittest discover` verwendet standardmäßig das Dateimuster:

```text
test*.py
```

Eine Testdatei sollte daher beispielsweise heißen:

```text
test_booksservice.py
test_create_book.py
test_configuration.py
```

Eine Datei wie

```text
booksservice_test.py
```

würde mit dem Standardmuster dagegen nicht automatisch gefunden.

Das Muster kann explizit mit `-p` angegeben werden:

```bash
python -m unittest discover -s test -p "test*.py" -v
```

`-p` steht für **pattern**.

Da `test*.py` bereits das Standardmuster von `unittest discover` ist, benötigen wir diese Option in unserem Projekt nicht. Deshalb verwenden wir den kürzeren Aufruf:

```bash
python -m unittest discover -s test -v
```

# Änderungen am Projekt

## Änderungen an der Fachanwendung

Die Fachanwendung befindet sich unter:

```text
src/books/
```

Beispielsweise können Änderungen an `src/books/booksservice.py` vorgenommen werden.

Da das Projekt mit

```bash
python -m pip install -e .
```

als **editable** installiert wurde, muss es nach einer normalen Änderung am Python-Quellcode **nicht erneut installiert werden**.

Nach dem Speichern der Änderung können unmittelbar wieder die Tests ausgeführt werden:

```bash
python -m unittest discover -s test -v
```

Der typische Ablauf ist damit:

```text
Fachanwendung ändern
        ↓
Änderungen speichern
        ↓
Tests ausführen
        ↓
Testergebnisse überprüfen
```

### Wann muss erneut installiert werden?

Eine erneute Installation kann erforderlich sein, wenn sich die Projektkonfiguration oder die Abhängigkeiten ändern.

Wurde beispielsweise `pyproject.toml` geändert und eine neue Abhängigkeit hinzugefügt, sollte erneut ausgeführt werden:

```bash
python -m pip install -e .
```

## Vorhandene Tests ändern

Bestehende Tests befinden sich im Verzeichnis `test/`.

Wird lediglich der Inhalt einer vorhandenen Testdatei geändert, ist **keine erneute Installation** notwendig.

Nach dem Speichern genügt wieder:

```bash
python -m unittest discover -s test -v
```

## Neue Tests hinzufügen

Neue Testdateien werden ebenfalls im Verzeichnis `test` angelegt.

Damit sie von der automatischen Testsuche gefunden werden, sollte ihr Dateiname mit `test` beginnen und auf `.py` enden.

Beispiel:

```text
test_update_book.py
```

Innerhalb der Datei werden die Tests wie gewohnt als `unittest`-Tests definiert.

Beispiel:

```python
import unittest


class TestSomething(unittest.TestCase):

    def test_something(self):
        self.assertEqual(2, 1 + 1)
```

Nach dem Speichern ist **keine erneute Installation** notwendig.

Der neue Test wird beim nächsten Aufruf automatisch berücksichtigt:

```bash
python -m unittest discover -s test -v
```

Man muss den neuen Test also nicht irgendwo registrieren oder in eine zentrale Testsuite eintragen.

## Zusammenfassung des normalen Arbeitsablaufs

### Einmalig nach dem Auschecken oder Entpacken

```bash
python -m pip install -e .
```

### Tests ausführen

```bash
python -m unittest discover -s test -v
```

### Fachanwendung geändert

Speichern und Tests erneut ausführen:

```bash
python -m unittest discover -s test -v
```

### Vorhandenen Test geändert

Speichern und Tests erneut ausführen:

```bash
python -m unittest discover -s test -v
```

### Neuen Test hinzugefügt

Testdatei unter `test/` mit einem Namen nach dem Muster `test*.py` anlegen und anschließend ausführen:

```bash
python -m unittest discover -s test -v
```

### `pyproject.toml` oder Abhängigkeiten geändert

Projekt erneut installieren:

```bash
python -m pip install -e .
```

Danach die Tests ausführen:

```bash
python -m unittest discover -s test -v
```

## 6. Tests mit pytest ausführen

Zusätzlich zu `unittest` kann das Projekt mit **pytest** ausgeführt werden. Die vorhandenen Tests müssen dafür nicht umgeschrieben werden: pytest kann auch Tests ausführen, die mit `unittest.TestCase` implementiert wurden.

`pytest` und das Plugin `pytest-html` sind in der `pyproject.toml` als optionale Testabhängigkeiten definiert. Um die Fachanwendung zusammen mit diesen Testwerkzeugen zu installieren, wird verwendet:

```bash
python -m pip install -e ".[test]"
```

`[test]` wählt dabei die in der `pyproject.toml` unter `project.optional-dependencies` definierte Gruppe `test` aus. Diese enthält `pytest` und `pytest-html`.

Anschließend können alle Tests mit pytest ausgeführt werden:

```bash
python -m pytest test -v
```

`test` bezeichnet das Verzeichnis mit den Tests. Die Option `-v` steht auch bei pytest für **verbose** und sorgt für eine ausführlichere Ausgabe der einzelnen Tests.

## 7. HTML-Testreport erzeugen

Das Plugin `pytest-html` ergänzt pytest um die Möglichkeit, die Testergebnisse als HTML-Datei auszugeben.

Der Report wird mit folgendem Kommando erzeugt:

```bash
python -m pytest test -v --html=reports/test-report.html --self-contained-html
```

Die Option

```text
--html=reports/test-report.html
```

legt Pfad und Namen der erzeugten HTML-Datei fest. Der Report wird in diesem Fall unter

```text
reports/test-report.html
```

gespeichert.

Die Option

```text
--self-contained-html
```

sorgt dafür, dass benötigte Styles und andere Ressourcen direkt in die HTML-Datei eingebettet werden. Der Report besteht dadurch aus einer einzelnen HTML-Datei und kann einfach im Browser geöffnet, archiviert oder weitergegeben werden.

Das Verzeichnis `reports/` enthält generierte Testergebnisse und ist deshalb in `.gitignore` eingetragen. HTML-Reports werden damit nicht versehentlich in das Git-Repository aufgenommen.

### Normaler Ablauf mit HTML-Report

Nach der einmaligen Installation der Testabhängigkeiten

```bash
python -m pip install -e ".[test]"
```

kann nach Änderungen an Fachanwendung oder Tests direkt ein neuer Report erzeugt werden:

```bash
python -m pytest test -v --html=reports/test-report.html --self-contained-html
```

Der vorhandene Report wird dabei durch den neuen Testreport ersetzt.

### `unittest` oder pytest?

Die Tests selbst bleiben weiterhin `unittest`-Tests. Es stehen nun zwei Möglichkeiten zur Ausführung zur Verfügung:

```bash
python -m unittest discover -s test -v
```

führt die Tests mit dem Test Runner der Python-Standardbibliothek aus.

```bash
python -m pytest test -v
```

führt dieselben Tests mit pytest aus. Für den HTML-Report wird pytest zusammen mit dem Plugin `pytest-html` verwendet.
