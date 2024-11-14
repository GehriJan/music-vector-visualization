#import "@preview/charged-ieee:0.1.3": ieee
#import "@preview/acrostiche:0.4.0": *

#init-acronyms((
  "PCA": ("Principal Component Analysis"),
  //"t-SNE": ("t-distributed S")
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
Vereinfacht wird zu Beginn die Kovarianz-Matrix  $S$ des Datensatzes berechnet.
Dann werden die Eigenvektoren dieser Matrix berechnet und nach dem Betrag ihrer jeweiligen Eigenwerte sortiert.
Von diesen $n$ Eigenvektoren werden nun, je nach Anwendungsfall, die $k$ ersten gewählt ($k<=n$).
Mit einer weiteren Matrix $W$, die jene gewählten Eigenvektoren als Zeilenvektoren hat,
wird nun die Transformation der Ausgangstupel in den (meist niedriger-dimensionalen) Raum durchgeführt. @metmppca

Das folgende Beispiel gibt dieser mathematischen Definition eine handfeste Intuition.
Hier entspricht #acr("PCA") dem iterativen Auswählen von zueinander orthogonalen Linien durch den Datensatz, die diesen am besten teilen.
_Am besten_ bedeutet hier, dass die Varianz der Projektionen auf diese Linie maximal sind. @metmppca

#figure(
  image("assets/pca_example.png"),
  caption: [Veranschaulichung von #acr("PCA") mit $n = k = 2$]
)






//todo: mathematische grundlagen und erklärung
//todo: beispiel/visualisierung
== t-SNE

== comparison

= Installation

= Umsetzungsbeispiel

