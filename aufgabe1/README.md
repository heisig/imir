# Aufgabe 1

#### Ziel: 
- Implementierung eines Booleschen Retrievals für Text
#### Datensatz:
- (dbpedia Extended Abstracts Dump)
    - Deutsch: http://downloads.dbpedia.org/2016-04/core-i18n/de/long_abstracts_de.ttl.bz2 (239MB)
    - Englisch: http://downloads.dbpedia.org/2016-04/core-i18n/en/long_abstracts_en.ttl.bz2 (742MB)

##### Aufbau:
`<http://de.dbpedia.org/resource/Aussagenlogik>` `<http://dbpedia.org/ontology/abstract>`\
"Die Aussagenlogik ist ein Teilgebiet der Logik, das sich mit Aussagen\
[...]."@de .

`<http://de.dbpedia.org/resource/Alan_Smithee>` `<http://dbpedia.org/ontology/abstract>`\
"Alan Smithee steht als Pseudonym f\u00FCr einen fiktiven Regisseur, der ilme verantwortet,\
[...]."@de .

Jede Zeile startet mit `<Ressource-URI>` und endet mit „.“


##### Anforderungen:
- Jede Ressource steht für ein Dokument, nach dem gesucht werden kann.
- Lediglich der Abstract soll durchsuchbar sein (Volltextsuche)
- Jede Anfrage soll zurückliefern
    1. ID der gefundenen Ressource (=in deren Abstract Suchbegriff auftritt)
    2. Gesamtzahl der gefundenen Ressourcen/Dokumente
    3. Gesamtzahl des Auftretens des Suchbegriffs in der Ergebnismenge
- AND, OR, NOT, Phrasensuche (z.B. „Teilgebiet der Logik“)

##### Einschränkung/Vereinfachung:
- Case-insensitive (alle Wörter in Kleinbuchstaben konvertieren!)
- Kein Ranking
- Sonderzeichen und Umlaute beibehalten
- Kein Stemming, keine Stoppwort-Eliminierung

##### Herausforderungen:
- Verarbeitung der Ausgangsdatei -> Index aufbauen
- Aufbau einer Invertierten Liste (siehe Vorlesung), dateibasiert
- Effiziente Ermittlung der Dokumentenliste pro Term
- Effiziente Implementierung der Booleschen Operatoren
    - OR (=Dokumentlisten-Vereinigung)
    - AND (=Dokumentenlisten-Schnittmenge)
    - NOT (=Vereinigung der Dokumentenlisten aller anderen Terme)
- Phrasensuche
    - AND-Suche, aber exakt in angegebener Reihenfolge!
    - Speicherung der Position(en) des Terms je Dokument

##### Bedingungen:
- Umsetzung in Java, C# oder Python
- Keine zusätzl. Bibliotheken oder Frameworks verwenden!
- Minimalanforderung: Ein- und Ausgabe über Kommandozeile (Indexierung starten, Anfrage stellen, Ergebnisse auflisten)
- Optional: kleine grafische Oberfläche

##### Abgabe:
- bis spätestens 21.11. (oder früher)
- ZIP: Executables + Readme + Source Code (sinnvoll kommentiert)
- Per Mail (im Anhang oder über Downloadlink) an *BetreuerEmailAdresse*
- bitte alle Gruppenmitglieder namentlich in der Mail nochmal nennen!
