#import "@preview/charged-ieee:0.1.3": ieee
#import "@preview/acrostiche:0.4.0": *

#init-acronyms((
  "PCA": ("Principal Component Analysis"),
  "t-SNE": ("t-distributed SNE"),
  "SNE": ("Stochastic Neighbour Embedding")
))

#set page(numbering: "1")
#show: ieee.with(
  title: [Visualisierung von Musikdaten mittels t-SNE und PCA am Beispiel pgvector],
  abstract: [
    //todo: write abstract
  ],
  authors: (
    (
      name: "Jannis Gehring",
      department: [INF22B, Data Warehouse],
      organization: [Duale Hochschule Baden-Württemberg (DHBW)],
      location: [Stuttgart, Deutschland],
      email: "inf22115@lehre.dhbw-stuttgart.de"
    ),
  ),
  index-terms: (),
  bibliography: bibliography("refs.bib"),
  paper-size: "din-d4",
  figure-supplement: [Figure],
)
#show raw: it => text(
      font: "PT Mono",
      it
)

#outline(depth: 1)

= Einleitung
In modernen Datawarehouse-systemen handelt es sich um große und vielfältige Datenmengen. Um aus diesen Daten sinnvolle Schlussfolgerungen zu ziehen, müssen sie meist aufs wesentliche reduziert werden. Eine Methode ist hierbei die Dimensionsreduktion, bei der hochdimensionale Daten (bis zu mehrere tausend Dimensionen) in niedrig-dimensionale Daten (meist 2/3-dimensional) umgewandelt werden. Im Folgenden werden die Dimensionsreduktionsverfahren #acr("PCA") und #acr("t-SNE") beschrieben und implementiert. Die Datenspeicherung erfolgt in einer PostgreSQL Datenbank. Als Datengrundlage dient ein kaggle-Datensatz mit Musikdaten aus Spotify.

= Theoretische Grundlagen

== #acrfull("PCA")
#acrfull("PCA") ist ein lineares Verfahren zur Dimensionsreduktion. Es wurde in der ersten Hälfte des zwanzigsten Jahrhunderts entwickelt, fand aber aufgrund seiner Berechnungsanforderungen erst in den 60ern breite Anwendung. @MACKIEWICZ1993303

Mathematisch liegt #acr("PCA") eine Eigenvektorberechnung zugrunde.
Vereinfacht wird zu Beginn die Kovarianz-Matrix $bold(S)$
//$ bold(S) = sum_n ((bold(t_n)-bold(overline(t)))(bold(t_n)-bold(overline(t)))^T)/N $
des Datensatzes berechnet.
Dann werden die Eigenvektoren dieser Matrix berechnet und nach dem Betrag ihrer jeweiligen Eigenwerte sortiert.
Von diesen $n$ Eigenvektoren werden nun, je nach Anwendungsfall, die $k$ ersten gewählt ($k<=n$).
Mit einer weiteren Matrix $bold(W)$, die jene gewählten Eigenvektoren als Zeilenvektoren hat,
wird nun die Transformation der Ausgangstupel in den (meist niedriger-dimensionalen) Raum durchgeführt. @metmppca

Das folgende Beispiel gibt dieser mathematischen Definition eine handfeste Intuition.
Hier entspricht #acr("PCA") dem iterativen Auswählen von zueinander orthogonalen Linien durch den Datensatz, die diesen am besten teilen.
_Am besten_ bedeutet hier, dass die Varianz der Projektionen auf diese Linie maximal sind. @metmppca

#figure(
  image("assets/pca_example.png"),
  caption: [Veranschaulichung von #acr("PCA") mit $n = k = 2$]
)

== #acrfull("t-SNE")
#acrfull("t-SNE") ist ein nicht-lineares Verfahren zur Dimensionsreduktion. Es wurde 2008 als Weiterentwicklung des Verfahrens #acr("SNE") vorgestellt.

Zentral für #acr("SNE") ist, dass Nachbarschaftsbeziehungen des hochdimensionalen Raums so gut wie möglich im niedrig-dimensionalen Raum erhalten bleiben müssen.
Hier zu wird im Ausgangsraum $X$ die Wahrscheinlichkeit $p_(j|i)$ definiert.
Wenn vom Punkt $x_i in X$ ein zufälliger Nachbar gewählt wird, wobei nähere Punkte anhand einer Gauß-verteilung wahrscheinlicher sind als fernere, dann bezeichnet $p_(j|i)$ die Wahrscheinlichkeit, dass hierbei der Punkt $x_j$ gewählt wird.

Genau die gleichen Beziehungen werden im niedrig-dimensionalen Raum $Y supset {y_i,y_j}$ definiert, wobei die Wahrscheinlichkeit hier mit $q_(j|i)$ bezeichnet wird.

Ziel von #acr("SNE") ist nun, die Punkte aus $X$ so auf $Y$ abzubilden, dass $q_(j|i)$ für alle $i$ und $j$ möglichst nahe an $p_(j|i)$ ist. Dies wird mittels eines Gradient-Descent Algorithmus durchgeführt.

#acr("t-SNE") erweitert #acr("SNE") in zwei Weisen. Zum Einen werden $p$ und $q$ so neu definiert, dass $p_(i j) = p_(j i)$ und $p_(i j) = p_(j i)$ $forall i,j$.
Zum Anderen nutzt es im niedrig-dimensionalen Raum nicht die Gaußverteilung zur Ermittlung des Nachbarn, sondern die t-Verteilung nach Student.

== Vergleich von #acr("PCA") und #acr("t-SNE")
Im Folgenden werden #acr("PCA") und #acr("t-SNE") anhand unterschiedlicher Kriterien verglichen @comparison:
#table(
  columns: (auto, auto, auto),
  align: center,
  table.header(
    [*Kriterium*],[* #acr("PCA") *], [*#acr("t-SNE")*],
  ),
  [Ziel der Dimensionsreduktion], [Maximieren der Varianz], [Erhalten von lokaler Struktur],
  [Linearität], [Linear], [Nicht-Linear],
  [Iterativ?], [Nein], [Ja],
  [Berechnungs-komplexität], [$Omicron (d^2 n + n^3)$\*], [$Omicron (n^2)$]
)
\* $d$ ist die Anzahl der Dimensionen des Ursprungsraumes, $n$ die Anzahl der Datenpunkte

= Verwendete Technologien
== Datenbank: PostgreSQL mit pgvector und psycopg
*PostgreSQL* ist ein opensource relationales Datenbankmanagementsystem. Es geht zurück auf das POSTGRES Projekt von 1986 an der University of California, wird aber immer noch weiterentwickelt und ist weit verbreitet. @postgresdocs
PostgreSQL kann sowohl mit einem cli als auch über einen Webclient, pgadmin, bedient werden.

*Pgvector* ist eine Erweiterung von PostgreSQL, die den Datentyp _vector_ einführt und es so erlaubt, Vektoren in SQL zu speichern. Desweiteren verfügt sie über Funktionen wie nearest-neighbour-search und  Abstandsberechnungen (cosine-distance, L1/L2 distance, etc.). @pgvectorgithub

*Psycopg* ist ein PostgreSQL Adapter für Python, der es ermöglicht, ```sql INSERT```, ```sql UPDATE```, ```sql SELECT``` sowie viele weitere SQL-Statements direkt aus Python heraus auszuführen. Da Psycopg auch Pgvector unterstützt, erlaubt es, alle für dieses Projekt relevanten Datenbankoperationen direkt in Python zu schreiben. @psycopgdocs

== Algorithmen: scikit-learn
*scikit-learn* ist eine Python Bibliothek für Machine Learning. Neben Klassifikations-, Regressions-, Clustering- und weiteren Algorithmen implementiert scikit-learn auch Dimensionsreduktionsverfahren wie #acr("PCA") und #acr("t-SNE"). @scikitlearn

== Visualisierung: plotly
*plotly* ist eine opensource Visualisierungsbibliothek für Python, die mehr als 40 unterschiedliche Graphen unterstützt. Plotly ist für dieses Projekt besonders gut geeignet, weil die Visualisierungen interaktiv sind, dass heißt es kann beispielsweise gezoomt werden und Informationen zu einzelnen Datenpunkten können _on-hover_ angezeigt werden. @plotly

== Datensatz: <datensatz>
Als Datengrundlage dient ein Datensatz von kaggle namens "Spotify Tracks Genre". Dieser verfügt über 89741 Songs aus 114 Genres.
Zu jedem Song werden neben der track_id 19 Werte gespeichert, von denen die Folgenden für dieses Projekt von Interesse sind @data:
1. *Meta-informationen*
  - Name des Songs
  - Name des Künstlers
  - Name des Genres
2. *Audio-parameter*

  Diese Parameter werden von Spotify ermittelt und beziehen sich auf den musikalischen Charakter des Songs.
  #figure(
    table(
      columns: (auto, auto),
      align: center,
      table.header(
        [*Parameter*],[*Interval/Einheit*],
      ),
      [Danceability], [\[0;1\]],
      [Energy], [\[0;1\]],
      [Loudness], [db],
      [Speechiness], [\[0;1\]],
      [Acousticness], [\[0;1\]],
      [Instrumentalness], [\[0;1\]],
      [Liveness], [\[0;1\]],
      [Valence\*], [\[0;1\]],
    ),
  )
  \* _Valence_ beschreibt, wie musikalisch positiv ein Song ist.
= Umsetzungsbeispiel

== Projektaufbau
Das Projekt ist in drei Hauptordner aufgeteilt:
1. ``` ./data ```\
  Dieser Ordner enthält die in einer csv-Datei gespeicherten Daten. (Siehe auch @datensatz)
2. ``` ./doc ```\
  Dieser Ordner enthält alle Dokumente, die zur Erstellung und Kompilierung dieser Dokumentation mit #link("https://typst.app/")[Typst] notwendig sind
3. ``` ./src ```\
  Der source-code des Projekts. (Siehe auch @code)

== Codeablauf <code>
Im folgenden wird der implementierte Prozess aus prozeduraler Sicht und Datensicht beschrieben:
#figure(
  image("assets/flowchart.drawio.png"),
  caption: [Flowchart der Implementierung]
)


== How-to: Setupprozess
Es folgt eine Schritt für Schritt Anleitung für das Aufsetzen der Umgebung. Annahme ist, dass alle Terminalcommands aus dem obersten Verzeichnis des git-repositories ausgeführt werden und Docker und Python mit venv installiert sind.

1. *Starten von Docker*\
  macOS: ```sh open -a docker```
2. *Starten der Docker-container*\
  ```sh docker-compose up -d```
3. *Aufsetzen einer venv*\
  ```sh python3 -m venv venv```
4. *Starten der venv*\
  zsh/macOS: ```sh source venv/bin/activate ```
5. *Installieren der pip-packages*\
  ```sh pip install -r requirements.txt```
6. *Erstellen der Datenbank in pgAdmin*\
  - Aufrufen von ```sh 127.0.0.1:5016```
  - Anmelden mit E-mail: _batiken-tableau-0u\@icloud.com_ und Passwort: _password_
  - Anlegen einer neuen Datenbank namens _vector_

== How-to: Nutzungsprozess



