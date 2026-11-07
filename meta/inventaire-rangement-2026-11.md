# Inventaire de rangement — novembre 2026

## État du dépôt

La structure principale est déjà utile : chapitres par thème, connaissances, archives, scripts et publications. Les difficultés viennent surtout de **l'absence d'un index de lecture complet**, de fichiers hérités de premières séances, de plusieurs index thématiques mélangés aux chapitres et de deux systèmes d'archivage des conversations.

## Rangement effectué

1. **README** réécrit avec les récits jusqu'au 7 novembre 2026, les points d'entrée et les dossiers.
2. **Index chronologique de lecture** créé dans [index-recits.md](index-recits.md) : les chapitres sont désormais accessibles sans explorer tous les répertoires.
3. **Aide-mémoire des anecdotes** : les deux souvenirs informatiques racontés en novembre sont déjà reliés à leurs chapitres dans `inbox/2026/2026-10-19-anecdotes.md`.
4. **Chronologie** mise à jour au fil des séances, avec dates incertaines conservées.

## Éléments à rationaliser sans perdre de données

| Emplacement | Constat | Décision |
| --- | --- | --- |
| `informatique/atari-st.md`, `informatique/dai.md`, `informatique/debuts.md`, `informatique/djinntel.md`, `informatique/oric.md` | Anciens index et résumés au même niveau que les chapitres ; risque de répétition dans le PDF | Les garder pour l'instant ; distinguer les index des chapitres dans une future évolution du générateur |
| `voyages/bretagne.md`, `voyages/ocean-indien.md`, `voyages/israel.md`, `voyages/afrique-du-sud.md` | Index ou chapitres à compléter mélangés aux récits | Ne pas supprimer ; reprendre au cas par cas |
| `raw conversations/` | Archives récentes dans un chemin contenant un espace | **Ne pas déplacer sans migration contrôlée** des liens et du script de publication |
| `bundles/archive/` et `bundles/bundle-biographie-2026-07-*/` | Exports et copies historiques pouvant paraître redondants | Conserver : pièces de traçabilité, pas des chapitres actifs |
| `build/book/`, `build/notebook/`, `build/reports/` | Nombreuses versions datées générées automatiquement | Conserver les versions historiques tant qu'une politique d'archivage n'a pas été choisie |
| `archives/magazines/assets/` | Scans, captures et un PDF mélangés | Réorganisation ultérieure après vérification des références |
| `inbox/` | Certaines notes sont déjà traitées | Les marquer comme traitées, sans perdre les formulations initiales |

## Précaution technique

Le générateur `tools/publish.py` sélectionne actuellement **tous les `.md` à la racine des dossiers narratifs** pour le PDF. Déplacer ou créer un index Markdown dans ces dossiers peut donc modifier le livre automatiquement. Les nouveaux index transversaux vont dans `meta/`, qui est exclu de l'édition PDF.

Les déplacements massifs ne sont pas effectués : il faut d'abord mettre à jour le générateur, vérifier tous les liens relatifs et comparer les sorties avant/après. **Aucun récit, aucune archive brute, aucun PDF historique n'a été supprimé.**

## Prochaine étape de maintenance

Séparer explicitement, dans le générateur, les **chapitres destinés au livre** des **index et brouillons**, puis migrer progressivement les archives brutes vers un chemin normalisé, avec liens de compatibilité ou redirections documentées.
