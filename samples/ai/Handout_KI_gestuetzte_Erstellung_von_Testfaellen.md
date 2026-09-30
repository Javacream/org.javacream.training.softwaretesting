# Handout: KI-gestützte Erstellung von Testfällen

## 1. KI als Unterstützung beim Testdesign

Generative KI kann Quellcode, Anforderungen, Fehlerbeschreibungen und vorhandene Tests analysieren und daraus Testideen bzw. Testfälle ableiten.

Dabei ist entscheidend, **welche Informationsbasis** verwendet wird:

- vorhandene Implementierung
- Spezifikation oder Anforderungen
- Code Review und Fehlerhypothesen
- Spezifikation und Implementierung gemeinsam
- vorhandene Testsuite

Die Informationsbasis bestimmt, welche Aussagen über das erwartete Verhalten überhaupt möglich sind.

> **Code beschreibt, was eine Implementierung tut. Eine Spezifikation beschreibt, was sie tun soll.**

---

## 2. Tests aus einer vorhandenen Implementierung

Beispiel:

```python
def shipping_cost(weight, express=False):
    if weight <= 0:
        raise ValueError("weight must be positive")
    if weight <= 2:
        cost = 4.99
    elif weight <= 10:
        cost = 7.99
    else:
        cost = 12.99

    if express:
        cost += 5.0

    return cost
```

Ein geeigneter Analyseauftrag an ein LLM lautet beispielsweise:

```text
Analysiere die Funktion aus Sicht eines Testers.
Identifiziere Eingabeklassen und Grenzwerte und leite daraus Normalfälle,
Grenzfälle und Fehlerfälle ab. Erfinde keine fachlichen Anforderungen.
Markiere Verhalten, dessen fachliche Richtigkeit ohne Spezifikation
nicht beurteilt werden kann.
```

Naheliegende Testpunkte sind die Grenzen `0`, `2` und `10` sowie die Kombination mit `express`.

### Einschränkung

Aus dem Code lässt sich erkennen, dass `weight <= 0` abgewiesen wird. Daraus folgt jedoch nicht, dass dies auch fachlich richtig ist.

Implementierungsbasierte Tests eignen sich besonders zum Erkennen von:

- Verzweigungen
- Grenzwerten
- Eingabeklassen
- Exceptions
- Sonderfällen
- Kombinationen von Parametern

---

## 3. Vom Code Review zum Regressionstest

KI kann statische Analyse und dynamische Tests miteinander verbinden.

Beispiel:

```python
def apply_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("invalid discount")

    discount = price * discount_percent
    return price - discount
```

Ein Review kann die Berechnung als verdächtig erkennen. Statt die Aussage „Hier ist ein Bug“ ungeprüft zu übernehmen, wird eine **Fehlerhypothese** formuliert.

Ein reproduzierender Test könnte sein:

```python
def test_apply_discount_10_percent():
    assert apply_discount(100, 10) == 90
```

Nach Bestätigung des Fehlers und seiner Behebung bleibt der Test erhalten.

Der Ablauf lautet:

```text
Code Review
    ↓
Fehlerhypothese
    ↓
reproduzierender Test
    ↓
Fehlerbehebung
    ↓
Regressionstest
```

Damit wird aus einem KI-Hinweis ein nachvollziehbarer Testprozess.

---

## 4. Testfälle aus Spezifikationen

Beispielspezifikation:

> Für Bestellungen ab 50 Euro ist der Standardversand kostenlos. Unter 50 Euro kostet er 4,99 Euro. Expressversand kostet unabhängig vom Bestellwert zusätzlich 5 Euro. Bestellwerte müssen größer als 0 Euro sein.

Ein strukturierter Prompt kann klassische Testentwurfsverfahren vorgeben:

```text
Analysiere die Spezifikation.

1. Identifiziere Geschäftsregeln.
2. Bilde Äquivalenzklassen.
3. Bestimme Grenzwerte.
4. Ermittle relevante Kombinationen.
5. Erstelle positive und negative Testfälle.
6. Gib Eingabe und erwartetes Ergebnis an.
7. Kennzeichne unklare Anforderungen, statt Annahmen zu erfinden.
```

### Grenzwertanalyse

Für die Grenze von 50 Euro sind beispielsweise relevant:

- knapp unter 50 Euro
- genau 50 Euro
- knapp über 50 Euro

### Äquivalenzklassen

Beispielsweise:

- ungültiger Bestellwert
- gültiger Bestellwert unter 50 Euro
- gültiger Bestellwert ab 50 Euro

### Kombinationen

Zusätzlich muss Standard- und Expressversand berücksichtigt werden.

Generative KI ersetzt dabei die klassischen Testentwurfsverfahren nicht. Sie kann helfen, sie konsequent und schnell anzuwenden.

---

## 5. Spezifikation und Implementierung gemeinsam analysieren

Sind Soll und Ist vorhanden, sollten sie bewusst getrennt analysiert werden:

```text
1. Leite Tests ausschließlich aus der Spezifikation ab.
2. Analysiere danach die Implementierung.
3. Vergleiche Soll- und Ist-Verhalten.
4. Identifiziere mögliche Abweichungen.
5. Erstelle gezielte Tests für diese Abweichungen.
```

Die Reihenfolge reduziert das Risiko, dass das vorhandene Implementierungsverhalten unbemerkt zum erwarteten Verhalten erklärt wird.

Dabei gilt:

```text
Spezifikation  → erwartetes Verhalten / Testorakel
Implementierung → System under Test
```

---

## 6. KI-generierte Tests müssen selbst geprüft werden

Ein automatisch erzeugter Test ist nicht automatisch ein guter Test.

Typische Schwächen sind:

- falsche erwartete Ergebnisse
- fehlende Grenzfälle
- redundante Tests
- schwache Assertions
- erfundene Anforderungen
- unnötiges oder falsches Mocking
- Tests, die auch bei fehlerhafter Implementierung erfolgreich wären

Beispiel:

```python
def test_shipping_cost():
    result = shipping_cost(5)
    assert result is not None
```

Dieser Test sagt kaum etwas über die Korrektheit der Berechnung aus.

Ein Review der generierten Tests sollte daher unter anderem fragen:

```text
Welche Verhaltensweisen werden tatsächlich geprüft?
Welche Grenzwerte fehlen?
Welche Tests sind redundant?
Welche Assertions sind zu schwach?
Welche Tests könnten trotz eines Fehlers grün bleiben?
Welche erwarteten Ergebnisse sind nicht durch die Spezifikation begründet?
```

---

## 7. Mutation Testing als Qualitätsprüfung

Eine zusätzliche Möglichkeit zur Bewertung einer Testsuite ist **Mutation Testing**. Dabei werden kleine Änderungen – sogenannte Mutanten – künstlich in die Implementierung eingebaut.

Beispiele:

```text
<   → <=
+   → -
True → False
```

Wenn die Tests einen solchen Fehler erkennen, wird der Mutant „getötet“. Bleiben die Tests grün, obwohl sich relevantes Verhalten geändert hat, deutet dies auf eine Schwäche der Testsuite hin.

Mutation Testing kann deshalb gerade bei KI-generierten Tests helfen, zwischen **vielen Tests** und **wirksamen Tests** zu unterscheiden.

---

## 8. Zusammenfassung

| Ausgangslage | Typische Nutzung der KI | Zu beachtendes Risiko |
|---|---|---|
| Implementierung | Pfade und Grenzwerte ableiten | Ist-Verhalten wird als Soll interpretiert |
| Code Review | Fehlerhypothesen und Regressionstests | falsche Fehlerhypothesen |
| Spezifikation | systematische Testfallableitung | erfundene Annahmen |
| Spezifikation + Code | Soll/Ist-Abweichungen suchen | Vermischung beider Quellen |
| Testsuite | Lücken und schwache Assertions suchen | oberflächliche Qualitätsbewertung |

Der sinnvolle Prozess ist:

```text
Informationsbasis
      ↓
Testanalyse
      ↓
Testideen
      ↓
Testfälle
      ↓
Testimplementierung
      ↓
Review der Tests
      ↓
Regressionstests
```

> **KI kann Testanalyse und Testdesign erheblich beschleunigen. Die Verantwortung für Testbasis, Testorakel und Testqualität bleibt beim Menschen.**
