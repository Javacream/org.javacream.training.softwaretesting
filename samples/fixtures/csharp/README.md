# C#-Beispiel

Die C#-Variante bildet dieselben vier Tests wie das Python-Beispiel ab. Als Testframework wird **xUnit**, für den Unit-Test zusätzlich **Moq** verwendet.

## Dateien

```text
csharp/
├── UserService.cs
├── UserServiceUnitTests.cs
├── BeeceptorTests.cs
├── LocalMockServerTests.cs
├── IntegrationTests.cs
├── HttpTestingExample.Tests.csproj
└── README.md
```

## Produktionscode und Dependency Injection

`UserService` erzeugt seinen `HttpClient` nicht selbst, sondern erhält ihn über den Konstruktor:

```csharp
public UserService(HttpClient httpClient)
{
    this.httpClient = httpClient;
}
```

Diese Form der Dependency Injection erleichtert den Austausch der HTTP-Infrastruktur im Test.

## 1. Unit-Test mit Moq

`UserServiceUnitTests.cs` verwendet keinen echten HTTP-Server. Stattdessen wird der von `HttpClient` intern verwendete `HttpMessageHandler` mit Moq ersetzt.

Damit können eine kontrollierte HTTP-Antwort und feste JSON-Daten simuliert werden, ohne Netzwerkverkehr zu erzeugen.

Der Test prüft außerdem, ob tatsächlich ein `GET` auf `/users` ausgeführt wird.

## 2. Online-Mock mit Beeceptor

`BeeceptorTests.cs` verwendet einen echten `HttpClient` und einen echten HTTP-Aufruf. Die Gegenstelle ist der kontrollierte Online-Mock bei Beeceptor.

Vor der Ausführung muss `BeeceptorBaseUrl` durch die tatsächlich eingerichtete Beeceptor-URL ersetzt werden.

Die gemeinsame Anleitung liegt unter:

[`../common/details/beeceptor.md`](../common/details/beeceptor.md)

## 3. Lokaler MockServer mit Docker

`LocalMockServerTests.cs` verwendet:

```text
http://localhost:1080/users
```

Der MockServer und seine Testdaten werden gemeinsam mit der Python-Variante verwendet.

Start:

```bash
cd ../common/docker
docker compose up -d
```

Details: [`../common/details/mockserver.md`](../common/details/mockserver.md)

## 4. Integrationstest gegen JSONPlaceholder

`IntegrationTests.cs` verwendet die echte externe JSONPlaceholder-API.

Wie im Python-Beispiel ist dieser Test bewusst **nur pauschal**. Er prüft, ob Daten geliefert werden und ob die wesentlichen Felder plausible Werte besitzen.

Er prüft keine feste Anzahl von Datensätzen und keine konkreten Namen oder IDs. Diese Daten gehören dem externen Dienst und stehen nicht unter Kontrolle des Tests.

Damit besitzt der Integrationstest eine hohe technische Realitätsnähe, aber eine deutlich geringere Prüftiefe der konkreten Antwortdaten als die Tests mit kontrollierten Mocks.

## Vergleich

| Eigenschaft | Unit-Mock | Beeceptor | Lokaler MockServer | JSONPlaceholder |
|---|---|---|---|---|
| Echtes HTTP | Nein | Ja | Ja | Ja |
| Kontrollierte Daten | Ja | Ja | Ja | Nein |
| Externer Dienst nötig | Nein | Ja | Nein | Ja |
| Detaillierte Assertions | Ja | Ja | Ja | Nur eingeschränkt |
| Prüft echte Gegenstelle | Nein | Nein | Nein | Ja |

## Ausführen

Pakete wiederherstellen und Tests starten:

```bash
dotnet restore
dotnet test
```

Sollen die Tests einzeln ausgeführt werden, kann xUnit über `dotnet test --filter` gefiltert werden, zum Beispiel:

```bash
dotnet test --filter UserServiceUnitTests
dotnet test --filter BeeceptorTests
dotnet test --filter LocalMockServerTests
dotnet test --filter IntegrationTests
```

Vor `LocalMockServerTests` muss der gemeinsame Docker-MockServer gestartet werden. Vor `BeeceptorTests` muss die eigene Beeceptor-URL eingetragen sein.
