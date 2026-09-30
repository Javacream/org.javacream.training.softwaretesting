# Handout: Prompt Engineering und Testen

## 1. Warum Prompt Engineering ein Testing-Thema ist

Bei klassischer Software erwarten wir häufig für einen definierten Input einen eindeutig bestimmbaren Output:

```text
Input -> Verarbeitung -> Output
```

Bei Anwendungen mit Large Language Models (LLMs) hängt die Ausgabe dagegen von mehreren Faktoren ab:

```text
Prompt + Kontext + Modell + Modellparameter -> Output
```

Die Ausgabe kann zudem variieren, obwohl die fachliche Aufgabe gleich bleibt. Deshalb genügt es nicht, einen Prompt einmal auszuprobieren und die Antwort visuell zu beurteilen.

**Prompt Engineering wird zum Engineering, wenn gewünschtes Verhalten spezifiziert, getestet und bei Änderungen erneut überprüft wird.**

---

## 2. Bestandteile eines Prompts

Ein nützliches Grundschema ist:

```text
Kontext/Rolle
+ Aufgabe
+ Eingabedaten
+ Constraints
+ Ausgabeformat
+ gegebenenfalls Beispiele
```

### Beispiel

```text
Du unterstützt ein Softwaretest-Team bei der Klassifikation
von Fehlerberichten.

Bestimme Kategorie und Schweregrad des folgenden Berichts.

Erlaubte Kategorien:
bug, usability, performance, security

Erlaubte Schweregrade:
low, medium, high, critical

Wenn die Informationen nicht ausreichen, verwende "unknown".
Erfinde keine zusätzlichen Informationen.

Antworte ausschließlich als JSON mit den Feldern
category, severity und summary.

Fehlerbericht:
Seit Version 2.4 beendet sich die Anwendung beim Import einer
leeren CSV-Datei. Bei Dateien mit mindestens einer Datenzeile
funktioniert der Import.
```

Eine mögliche Antwort:

```json
{
  "category": "bug",
  "severity": "medium",
  "summary": "Import einer leeren CSV-Datei führt zum Programmabbruch"
}
```

Die strukturierte Antwort lässt sich wesentlich leichter automatisiert prüfen als ein frei formulierter Text.

---

## 3. Wichtige Prompting-Techniken

### Zero-shot

Das Modell erhält die Aufgabe ohne Lösungsbeispiele.

```text
Ordne den Fehler einer Kategorie zu:
bug, usability, performance oder security.
```

### Few-shot

Das Modell erhält zusätzlich Beispiele für gewünschtes Verhalten.

```text
"Der Export benötigt bei 10.000 Datensätzen über 90 Sekunden."
-> performance

"Nach drei falschen Login-Versuchen wird das Konto nicht gesperrt."
-> security
```

Beispiele können die Aufgabe präzisieren, beeinflussen aber gleichzeitig das Modellverhalten. Deshalb sollten Tests auch Fälle umfassen, die sich deutlich von den Beispielen unterscheiden.

### Constraints

Constraints begrenzen erlaubte Antworten:

```text
Verwende ausschließlich folgende Kategorien:
bug, usability, performance, security.
```

Solche Regeln lassen sich häufig direkt automatisiert testen.

### Decomposition

Komplexe Aufgaben können in Teilaufgaben zerlegt werden:

```text
1. Fasse das beobachtete Verhalten zusammen.
2. Bestimme die Kategorie.
3. Bestimme den Schweregrad.
4. Nenne fehlende Informationen.
```

### Structured Output

Wo die Antwort von Software weiterverarbeitet werden soll, ist eine definierte Struktur wie JSON meist besser testbar als Freitext.

---

## 4. Das Testorakel-Problem

Ein klassischer Test kann ein eindeutiges Ergebnis erwarten:

```python
assert add(2, 3) == 5
```

Bei natürlicher Sprache können dagegen mehrere Antworten korrekt sein:

```text
Import einer leeren CSV-Datei führt zum Programmabbruch.
```

und

```text
Die Anwendung stürzt ab, wenn eine CSV-Datei keine Datenzeilen enthält.
```

Ein exakter Stringvergleich wäre deshalb kein sinnvolles Testorakel.

Entscheidend ist die Unterscheidung zwischen **deterministisch prüfbaren Eigenschaften** und **semantisch zu bewertenden Eigenschaften**.

---

## 5. Vier Ebenen des Prompt-Testings

### 1. Struktur

Ist die Ausgabe technisch korrekt?

```python
result = json.loads(response)
assert "category" in result
assert "severity" in result
assert "summary" in result
```

### 2. Regeln

Werden definierte Constraints eingehalten?

```python
assert result["category"] in {
    "bug", "usability", "performance", "security", "unknown"
}
```

Weitere Beispiele sind Wertebereiche, Pflichtfelder und maximale Textlängen.

### 3. Inhalt

Entspricht die fachliche Klassifikation der Erwartung?

Beispiel:

```text
Nach drei falschen Login-Versuchen kann der Benutzer
unbegrenzt weitere Passwörter ausprobieren.
```

Bei ausreichend klar definierten Kategorien kann beispielsweise `security` als Referenzklassifikation hinterlegt werden.

### 4. Qualität

Komplexer sind Fragen wie:

- Ist die Zusammenfassung fachlich korrekt?
- Enthält die Antwort erfundene Informationen?
- Wurden relevante Angaben berücksichtigt?
- Ist eine Begründung nachvollziehbar?

Hier reicht eine klassische Assertion häufig nicht aus.

---

## 6. Möglichkeiten zur Evaluation

Je nach Eigenschaft kommen unterschiedliche Verfahren infrage:

- klassische Assertions,
- Schema- und Regelprüfungen,
- Vergleich mit Referenzwerten,
- menschliche Bewertung,
- semantische Bewertungsverfahren,
- LLM-as-a-Judge.

### LLM-as-a-Judge

Dabei bewertet ein LLM die Antwort anhand vorgegebener Kriterien.

Beispiel:

```text
Bewerte die Zusammenfassung nach folgendem Kriterium:
Sie darf keine Informationen enthalten, die nicht aus dem
Fehlerbericht hervorgehen.

Antworte mit PASS oder FAIL und einer kurzen Begründung.
```

Ein LLM-Judge ist jedoch **kein unfehlbares Testorakel**. Auch seine Bewertungen können variieren oder systematische Fehler enthalten. Seine Qualität muss deshalb ebenfalls überprüft werden; bei wichtigen Evaluationen können menschliche Stichproben sinnvoll sein.

---

## 7. Eine Testsuite für Prompts

Eine gute Testsuite enthält nicht nur typische Eingaben.

| Testklasse | Beispiel |
|---|---|
| Normalfall | klar beschriebener Fehler |
| Grenzfall | sehr kurzer Bericht |
| Fehlende Information | wichtige Angaben fehlen |
| Widerspruch | Angaben widersprechen sich |
| Irrelevante Information | viele unnötige Details |
| Unbekannter Fall | passt nicht in vorgegebene Kategorien |
| Problematische Eingabe | Eingabetext enthält selbst Anweisungen |

Testdaten können beispielsweise als JSON versioniert werden:

```json
[
  {
    "id": "T001",
    "input": "Import einer leeren CSV-Datei führt zum Absturz.",
    "expected_category": "bug"
  },
  {
    "id": "T002",
    "input": "Der Export von 100000 Datensätzen benötigt 8 Minuten.",
    "expected_category": "performance"
  }
]
```

Referenzwerte sind nur sinnvoll, wenn die zugrunde liegenden Anforderungen und Kategorien ausreichend klar definiert sind.

---

## 8. Prompt Regression Testing

Eine Prompt-Änderung kann einige Fälle verbessern und gleichzeitig andere verschlechtern.

Deshalb sollte nach einer Änderung dieselbe Evaluation erneut ausgeführt werden:

```text
Prompt v1 -> Evaluation-Dataset -> Ergebnisse
Prompt v2 -> Evaluation-Dataset -> Ergebnisse
                         ↓
                      Vergleich
```

Eine höhere Gesamtquote allein reicht nicht aus. Wichtig ist auch, **welche einzelnen Testfälle sich verändert haben**.

```text
4 Testfälle verbessert
2 Testfälle verschlechtert
```

Die verschlechterten Fälle sind mögliche Regressionen.

Damit ergibt sich eine direkte Parallele zum klassischen Softwaretesting:

```text
Codeänderung   -> Regressionstest
Promptänderung -> Prompt-Regressionstest
```

Prompts, Testdaten und Bewertungskriterien sollten deshalb versioniert werden.

---

## 9. Vom Prompt zum Engineering-Prozess

```text
Prompt ausprobieren
        ↓
Prompt strukturieren
        ↓
Anforderungen explizit machen
        ↓
Testfälle definieren
        ↓
automatisiert evaluieren
        ↓
Regressionen erkennen
        ↓
Prompt und Tests versionieren
```

### Merksatz

> Ein guter Prompt ist nicht einfach ein Prompt, der einmal eine gute Antwort erzeugt. Entscheidend ist, ob das gewünschte Verhalten anhand definierter Kriterien über relevante Testfälle hinweg überprüft werden kann.
