#import "@preview/charged-ieee:0.1.3": ieee
#import "@preview/acrostiche:0.4.0": *

#init-acronyms((
  "PCA": ("Principal Component Analysis"),
  "t-SNE": ("t-distributed Stochastic Neighbour Embedding"),
  "SNE": ("Stochastic Neighbour Embedding")
))

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
  figure-supplement: [Fig.],
)
#outline()
= Grundlagen

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

#acr("t-SNE") erweitert #acr("SNE") in zwei Weisen. Zum Einen passt es die Wahrscheinlichkeitsverteilungen so an, sodass $p_(i j) = p_(j i)$ und $p_(i j) = p_(j i)$ $forall i,j$, zum Anderen nutzt es im niedrig-dimensionalen Raum nicht die Gaußverteilung zur Ermittlung des Nachbarn, sondern die t-Verteilung nach Student.

== Vergleich von #acr("PCA") und #acr("t-SNE")
Im Folgenden werden #acr("PCA") und #acr("t-SNE") anhand unterschiedlicher Kriterien verglichen @comparison:
#table(
  columns: (auto, auto, auto),
  align: horizon,
  table.header(
    [*Kriterium*],[* #acr("PCA") *], [*#acr("t-SNE")*],
  ),
  [Ziel der Dimensionsreduktion], [Maximieren der Varianz], [Erhalten von lokaler Struktur],
  [Linearität], [Linear], [Nicht-Linear],
  [Iterativ?], [Ja], [Nein],
  [Berechnungs-komplexität], [$Omicron (d^2 n + n^3)$], [$Omicron (n^2)$]
)

= Installation

= Umsetzungsbeispiel

