# Testarten im Softwaretesting

Für eine allgemeine Einführung in Softwaretesting ist es sinnvoll,
Testarten nicht nur nach einer einzigen Dimension aufzulisten. Begriffe
wie **Unit-Test**, **Regressionstest** und **Lasttest** beschreiben
unterschiedliche Aspekte: **Testebene, Testziel oder Anlass**.

## Nach Testebene

  -----------------------------------------------------------------------
  Testart                             Kurzbeschreibung
  ----------------------------------- -----------------------------------
  **Unit-Test / Komponententest**     Testet eine einzelne, möglichst
                                      isolierte Einheit wie Funktion,
                                      Methode, Klasse oder Modul.

  **Integrationstest**                Prüft das Zusammenspiel mehrerer
                                      Komponenten, z. B. Anwendung und
                                      Datenbank oder mehrere Services.

  **Systemtest**                      Testet das vollständige System als
                                      Ganzes gegen seine Anforderungen.

  **End-to-End-Test (E2E)**           Prüft einen vollständigen
                                      fachlichen Ablauf über mehrere
                                      Komponenten hinweg, möglichst aus
                                      Sicht des Anwenders.

  **Akzeptanztest / Abnahmetest**     Prüft, ob das System die fachlichen
                                      Anforderungen erfüllt und
                                      abgenommen werden kann.
  -----------------------------------------------------------------------

## Nach Testziel

  -----------------------------------------------------------------------
  Testart                             Kurzbeschreibung
  ----------------------------------- -----------------------------------
  **Funktionaler Test**               Prüft, ob eine geforderte Funktion
                                      das fachlich erwartete Ergebnis
                                      liefert.

  **Negativtest**                     Prüft das Verhalten bei ungültigen
                                      Eingaben, falscher Verwendung oder
                                      Fehlerbedingungen.

  **Grenzwerttest**                   Testet gezielt Werte an und
                                      unmittelbar neben definierten
                                      Grenzen.

  **Performance-Test**                Untersucht Antwortzeiten, Durchsatz
                                      und Ressourcenverbrauch.

  **Lasttest**                        Prüft das Verhalten unter einer
                                      erwarteten oder erhöhten Anzahl
                                      gleichzeitiger Zugriffe bzw. hoher
                                      Last.

  **Stresstest**                      Belastet das System über die
                                      vorgesehenen Grenzen hinaus und
                                      untersucht Verhalten und
                                      Stabilität.

  **Security-Test**                   Prüft sicherheitsrelevante
                                      Eigenschaften und mögliche
                                      Schwachstellen.

  **Usability-Test**                  Untersucht Bedienbarkeit und
                                      Benutzerfreundlichkeit.

  **Kompatibilitätstest**             Prüft das Verhalten in
                                      unterschiedlichen Umgebungen, z. B.
                                      Betriebssystemen oder Browsern.

  **Robustheitstest**                 Prüft, wie sich das System bei
                                      unerwarteten Eingaben oder
                                      problematischen
                                      Umgebungsbedingungen verhält.
  -----------------------------------------------------------------------

## Nach Anlass bzw. Vorgehensweise

  -----------------------------------------------------------------------
  Testart                             Kurzbeschreibung
  ----------------------------------- -----------------------------------
  **Regressionstest**                 Prüft nach Änderungen, ob bereits
                                      funktionierende Eigenschaften
                                      weiterhin funktionieren.

  **Re-Test / Wiederholungstest**     Prüft gezielt, ob ein zuvor
                                      festgestellter Fehler tatsächlich
                                      behoben wurde.

  **Smoke-Test**                      Kurzer, breit angelegter Test, ob
                                      die wichtigsten Funktionen
                                      grundsätzlich funktionieren und
                                      weiteres Testen sinnvoll ist.

  **Explorativer Test**               Testen ohne vollständig vorab
                                      festgelegte Testfälle; Lernen,
                                      Testentwurf und Testdurchführung
                                      erfolgen gleichzeitig.

  **Sanity-Test**                     Kurzer, fokussierter Test, ob eine
                                      konkrete Änderung grundsätzlich
                                      plausibel funktioniert.
  -----------------------------------------------------------------------

## Einordnung

Diese Kategorien schließen sich **nicht gegenseitig aus**. Ein Test kann
beispielsweise gleichzeitig ein **Integrationstest**, ein **funktionaler
Test** und ein **Regressionstest** sein. Die Bezeichnungen beantworten
unterschiedliche Fragen:

-   **Wo teste ich?** → Unit, Integration, System, E2E
-   **Was untersuche ich?** → Funktion, Performance, Security,
    Robustheit ...
-   **Warum bzw. wann teste ich?** → Regression, Re-Test, Smoke-Test
