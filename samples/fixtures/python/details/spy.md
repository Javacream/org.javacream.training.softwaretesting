# Spying mit `unittest.mock`

Ein **Spy** beobachtet den Aufruf einer echten Funktion, ohne deren Verhalten durch ein simuliertes Ergebnis zu ersetzen.

Python stellt in `unittest.mock` keine eigene Klasse `Spy` bereit. Im Beispiel wird deshalb ein generischer Spy auf Basis von `Mock` und `side_effect` erzeugt.

## Der generische Spy

```python
def create_spy(function, logfile):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)

        with open(logfile, "a", encoding="utf-8") as log:
            log.write(f"Function: {function.__name__}\n")
            log.write(f"Args: {args}\n")
            log.write(f"Kwargs: {kwargs}\n")
            log.write(f"Return value: {result}\n")
            log.write("\n")

        return result

    return Mock(side_effect=wrapper)
```

`create_spy()` erhält zwei Informationen:

- die zu beobachtende Funktion,
- die Datei, in die die Aufrufe geschrieben werden.

Die zurückgegebene Instanz ist weiterhin ein `Mock`. Deshalb stehen die üblichen Funktionen von `unittest.mock` zur Prüfung der Aufrufe zur Verfügung.

## `side_effect`

Der entscheidende Mechanismus ist:

```python
return Mock(side_effect=wrapper)
```

Wird der Mock aufgerufen, führt `unittest.mock` die angegebene `wrapper`-Funktion aus.

Der Wrapper erhält dieselben Positions- und Keyword-Argumente:

```python
def wrapper(*args, **kwargs):
```

Anschließend ruft er die echte Funktion auf:

```python
result = function(*args, **kwargs)
```

Damit bleibt das reale Verhalten erhalten.

## Logging

Nach dem echten Aufruf stehen sowohl die Eingaben als auch der Rückgabewert zur Verfügung:

```python
log.write(f"Function: {function.__name__}\n")
log.write(f"Args: {args}\n")
log.write(f"Kwargs: {kwargs}\n")
log.write(f"Return value: {result}\n")
```

Für `get_users()` kann die Datei beispielsweise so aussehen:

```text
Function: get_users
Args: ()
Kwargs: {}
Return value: [User(id=1, name='Leanne Graham', ...), ...]
```

Damit enthält das Log mehr Informationen als `call_args_list` allein: Neben den Aufrufargumenten werden auch der Name der beobachteten Funktion und ihr tatsächlicher Rückgabewert protokolliert.

## Verwendung mit `get_users()`

Der Spy wird mit einer beliebigen Funktion erzeugt:

```python
spy = create_spy(get_users, "spy-calls.log")
```

Der Test ruft anschließend nicht `get_users()` direkt auf, sondern den Spy:

```python
users = spy()
```

Der Ablauf ist:

```text
Test
  |
  v
Mock / Spy
  |
  v
side_effect: wrapper()
  |
  +----> ruft get_users() auf
  |          |
  |          v
  |       requests.get()
  |          |
  |          v
  |       JSONPlaceholder
  |
  +----> protokolliert Funktion
  +----> protokolliert Argumente
  +----> protokolliert Rückgabewert
  |
  v
Rückgabewert an den Test
```

## Aufrufe mit `Mock` prüfen

Obwohl der Wrapper das Logging übernimmt, bleibt der zurückgegebene Spy ein normales `Mock`-Objekt.

Deshalb kann der Test zusätzlich schreiben:

```python
spy.assert_called_once_with()
```

Weitere Möglichkeiten sind beispielsweise:

```python
spy.assert_called()
spy.assert_called_once()
spy.call_count
spy.call_args
spy.call_args_list
```

Das Logging und die eingebauten Prüfmechanismen von `Mock` erfüllen also unterschiedliche Aufgaben.

## Generischer Einsatz

`create_spy()` ist nicht an `get_users()` gebunden:

```python
user_spy = create_spy(get_users, "spy-calls.log")
other_spy = create_spy(other_function, "spy-calls.log")
```

Da `*args` und `**kwargs` weitergereicht werden, funktioniert der Ansatz auch für Funktionen mit Parametern.

## Unterschied zum Mock

Ein klassischer Mock kann das Verhalten vollständig ersetzen:

```python
mock = Mock()
mock.return_value = [...]
```

```text
Test -> Mock -> simuliertes Ergebnis
```

Der hier implementierte Spy führt dagegen die echte Funktion aus:

```text
Test -> Spy -> echte Funktion
          |
          +--> protokolliert Aufruf und Ergebnis
```

Der Spy ist damit vor allem ein **Beobachter**.

## Einordnung des Tests

Im Beispiel ruft `get_users()` weiterhin den echten JSONPlaceholder-Webservice auf. Der Spy isoliert die Funktion also nicht von ihrer HTTP-Abhängigkeit.

Der Test bleibt deshalb von Netzwerk und externem Webservice abhängig. Der Einsatz eines Spys bestimmt nicht die Testebene, sondern beschreibt die Art, wie eine Interaktion beobachtet wird.
