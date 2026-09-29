# HTTP-Testing-Beispiele in Python und C#

Das Projekt zeigt dieselbe Testidee parallel in Python und C#.

```text
http-testing-examples/
├── README.md
├── python/
├── csharp/
└── common/
    ├── docker/
    └── details/
```

`python/` und `csharp/` enthalten jeweils vier Testvarianten:

1. isolierter Unit-Test mit Mock,
2. echter HTTP-Aufruf gegen Beeceptor,
3. echter HTTP-Aufruf gegen lokalen MockServer,
4. Integrationstest gegen JSONPlaceholder.

`common/` enthält die sprachunabhängigen Bestandteile:

- Beeceptor-Anleitung,
- MockServer-Anleitung,
- gemeinsame Docker-Compose-Konfiguration,
- gemeinsame MockServer-Testdaten.

Die sprachspezifischen READMEs erläutern Implementierung, Testframework und Aussagekraft der jeweiligen Tests.
