# Séance du 16 juillet 2026 — Publication automatique

## Décision

À la fin de chaque séance, la formule suivante déclenche la publication :

> « Fin de séance. Fais la publication. »

## Pipeline convenu

- Le dépôt Git reste la source de vérité.
- Les nouveaux souvenirs sont intégrés aux chapitres, à la chronologie, aux connaissances et aux questions ouvertes.
- La séance est archivée.
- Une édition PDF complète est générée depuis les fichiers Markdown principaux.
- Un corpus ZIP est produit pour NotebookLM ou un système RAG personnel.
- Les artefacts générés sont rangés sous `build/`.
- La publication est versionnée et poussée dans GitHub.

## Mise en œuvre

- Générateur : `tools/publish.py`.
- Automatisation : `.github/workflows/publish.yml`.
- Sorties :
  - `build/book/Biographie-Francois-vAAAA-MM-JJ.pdf` ;
  - `build/book/Biographie-Francois-latest.pdf` ;
  - `build/notebook/notebook-biographie-francois-AAAA-MM-JJ.zip` ;
  - `build/notebook/notebook-biographie-francois-latest.zip` ;
  - `build/reports/publication-AAAA-MM-JJ.md`.

Cette séance n'ajoute pas de nouvel épisode biographique après l'intégration du voyage Guatemala–San Diego. Elle fixe le processus éditorial de fin de séance.
