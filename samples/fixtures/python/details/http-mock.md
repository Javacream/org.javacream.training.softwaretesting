# HTTP-Mock mit `unittest.mock`

Der Unit-Test ersetzt `requests.get()` durch ein Mock-Objekt und führt deshalb keinen echten HTTP-Aufruf aus.

## Der `@patch`-Decorator

```python
@patch("users.requests.get")
def test_get_users(self, mock_get):
```

`patch()` ersetzt für die Dauer des Tests `users.requests.get` durch ein Mock-Objekt. Dieses wird als `mock_get` an die Testmethode übergeben. Nach Ende des Tests wird das ursprüngliche Objekt automatisch wiederhergestellt.

Gepatcht wird dort, wo der getestete Code das Objekt verwendet. Da `users.py` `requests.get()` aufruft, lautet das Patch-Ziel `users.requests.get`.

## Rückgabewert simulieren

```python
mock_response = Mock()
mock_get.return_value = mock_response
```

`return_value` bestimmt, welches Objekt der simulierte Aufruf von `requests.get()` zurückliefert.

Mit

```python
mock_response.json.return_value = [...]
```

wird die Rückgabe von `response.json()` definiert.

Die Kette sieht damit vereinfacht so aus:

```text
get_users()
    |
    | requests.get(...)
    v
mock_get
    |
    | return_value
    v
mock_response
    |
    | json()
    v
definierte Testdaten
```

## Aufrufe prüfen

```python
mock_get.assert_called_once_with(
    "https://jsonplaceholder.typicode.com/users",
    timeout=5
)
```

prüft, ob der Mock genau einmal mit den erwarteten Argumenten aufgerufen wurde.

Der Unit-Test ist schnell und reproduzierbar. Er prüft die eigene Logik sehr gezielt, aber keine echte HTTP-Kommunikation.
