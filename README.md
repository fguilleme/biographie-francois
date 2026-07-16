# Biographie de François Guillemé

Ce dépôt rassemble les souvenirs, le parcours informatique, les voyages et les documents d’archives de François Guillemé.

Le projet distingue trois types de contenu :

- **Souvenir personnel** : récit fondé sur la mémoire de François ;
- **Fait vérifié** : information recoupée par une source extérieure ;
- **À confirmer** : date, nom ou détail encore incertain.

## Commencer ici

- [Chronologie générale](chronologie.md)
- [Structure canonique du dépôt](meta/structure-depot.md)
- [Index des personnes](personnes.md)
- [Registre des sources](sources.md)
- [Questions ouvertes](meta/questions-ouvertes.md)
- [Dernière édition PDF](build/book/Biographie-Francois-latest.pdf)
- [Dernier corpus Notebook/RAG](build/notebook/notebook-biographie-francois-latest.zip)

## Organisation

### Récits destinés au livre

- `famille/`
- `scolarite/`
- `formation/`
- `militaire/`
- `professionnel/`
- `sante/`
- `informatique/`
- `voyages/`
- `souvenirs/`

### Documentation et sources

- `connaissances/` — fiches sur les personnes, organisations et lieux ;
- `archives/` — magazines, photos, logiciels et documents primaires ;
- `bundles/` — paquets de séance et transcriptions historiques ;
- `inbox/` — éléments encore à classer ;
- `journal/` — comptes rendus et notes de travail ;
- `meta/` — règles éditoriales et questions ouvertes.

### Publication automatique

- `tools/publish.py` — générateur du livre et du corpus ;
- `.github/workflows/publish.yml` — publication automatique ;
- `build/book/` — éditions PDF ;
- `build/notebook/` — corpus Notebook/RAG ;
- `build/reports/` — rapports de publication.

Le dépôt Git est la source de vérité. Les fichiers de `build/` sont des artefacts générés et immédiatement téléchargeables.

## Règles de classement

- Une transcription vocale ambiguë n'est jamais transformée silencieusement en certitude.
- Les corrections explicites de François priment sur les premières formulations.
- Chaque dossier distingue autant que possible le souvenir personnel, l'interprétation et le fait vérifié extérieurement.
- Les noms, dates et termes techniques incertains sont centralisés dans les questions ouvertes.
- Les archives primaires sont conservées sans réécriture.
- Les nouveaux fichiers évitent les espaces et utilisent de préférence des noms en minuscules séparés par des tirets.

Ce dépôt est un travail en cours. Les textes seront corrigés et enrichis au fur et à mesure des souvenirs et des recherches documentaires.

## Ajouts 1983–1984

- [Retour en région parisienne et formation informatique](professionnel/1983-retour-region-parisienne-formation-informatique.md)
- [CBS et le Coleco Adam](professionnel/1984-cbs-coleco-adam.md)
- [Stage et CDI chez LINCS](professionnel/1984-lincs.md)
- [Accident de la Scirocco](sante/1984-accident-scirocco.md)
- [Voyage aux États-Unis et au Mexique](voyages/1984-etats-unis-mexique.md)
- [Guatemala, lac Atitlán et remontée vers les États-Unis](voyages/1984-guatemala-remontee-etats-unis.md)
- [Sylvette](connaissances/personnes/sylvette.md)
- [San Pedro La Laguna](connaissances/lieux/san-pedro-la-laguna.md)
- [Transcription de la séance du 14 juillet 2026](bundles/archive/sessions/2026/2026-07-14-transcript.md)
- [Transcription de la séance du 15 juillet 2026](bundles/archive/sessions/2026/2026-07-15-transcript.md)
