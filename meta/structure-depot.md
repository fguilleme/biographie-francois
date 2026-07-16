# Structure canonique du dépôt

Ce document définit le rôle de chaque répertoire. Il sert de référence pour les futurs rangements et évite que les archives, les sources narratives et les fichiers générés soient mélangés.

## Sources narratives

Les dossiers suivants contiennent les textes destinés à alimenter le livre :

- `famille/`
- `scolarite/`
- `formation/`
- `militaire/`
- `professionnel/`
- `sante/`
- `informatique/`
- `voyages/`
- `souvenirs/`

Chaque fichier doit décrire un épisode, une période ou un thème clairement identifié. Les noms commencent autant que possible par une année ou une période.

## Connaissances et index

- `connaissances/` : fiches de référence sur les personnes, lieux et organisations.
- `chronologie.md` : repères temporels généraux.
- `personnes.md` : index des personnes.
- `sources.md` : registre des sources et témoignages.
- `meta/` : règles éditoriales, questions ouvertes et documentation du projet.

## Archives

- `archives/magazines/` : scans, captures et documents de presse.
- `archives/photos/` : photographies originales.
- `archives/logiciels/` : logiciels, captures et documents techniques d'époque.
- `bundles/archive/` : transcriptions et exports historiques déjà intégrés au projet.

Les archives sont des sources primaires. Elles ne doivent pas être réécrites ni supprimées après intégration.

## Bundles

- `bundles/bundle-biographie-YYYY-MM-DD/` : paquet de travail décompressé d'une séance.
- `bundles/bundle-biographie-YYYY-MM-DD.zip` : copie transportable correspondante.

Les bundles sont conservés pour la traçabilité. Ils ne sont pas utilisés comme chapitres du livre une fois leur contenu intégré.

## Travail en cours

- `inbox/` : notes ou souvenirs encore à classer.
- `journal/` : comptes rendus de travail et conversations structurées.

Un document ne doit rester dans `inbox/` que tant qu'il n'a pas été intégré dans un dossier narratif ou documentaire.

## Publication

- `tools/` : scripts de génération et de maintenance.
- `.github/workflows/` : automatisation GitHub Actions.
- `build/book/` : éditions PDF générées.
- `build/notebook/` : corpus Notebook/RAG générés.
- `build/reports/` : rapports de publication.

Le contenu de `build/` est régénérable, mais il est volontairement versionné afin de fournir une édition immédiatement téléchargeable.

## Règles de rangement

1. Ne jamais placer un nouveau chapitre dans `bundles/` ou `archives/`.
2. Ne jamais modifier silencieusement une archive primaire.
3. Éviter les dossiers contenant des espaces pour tout nouveau contenu.
4. Utiliser des noms de fichiers en minuscules, séparés par des tirets.
5. Conserver les incertitudes dans le texte et dans `meta/questions-ouvertes.md`.
6. Mettre à jour les liens après tout déplacement de fichier.
7. Préférer un rangement non destructif : copier, vérifier les liens, puis seulement supprimer l'ancien emplacement.

## Nettoyage progressif

Les anciens chemins incohérents, notamment `raw conversations/`, seront migrés progressivement vers une arborescence d'archives cohérente. Aucune migration massive ne doit être faite sans vérifier les liens et le contenu complet des fichiers concernés.
