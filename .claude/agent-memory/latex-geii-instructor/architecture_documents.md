# Architecture standard des documents LaTeX -- dépôt supports-automatisme-robotique/02_AutomatismeRobotique

Ce fichier décrit le patron de fichiers à utiliser pour tout futur document
pédagogique de type **cours / ressource / analyse fonctionnelle** (pas TP/TD
avec questions) dans CE dépôt. Il est autonome : à lire sans connaître une
conversation particulière.

## Patron validé (référence : `01_conception/`, `Ressources_EthernetIP/`, `02_analyse_fonctionnelle/`)

Chaque document vit dans son propre sous-dossier, avec 4 fichiers + 2 sous-dossiers :

```
NN_nom_du_document/
├── <NomDocument>.tex   % fichier directeur, à compiler
├── preamble.tex        % titre / sous-titre / entête (spécifique au document)
├── main.tex            % \tableofcontents + liste des \input{sources/...}
├── sources/            % un fichier .tex par section/mode/partie de contenu
└── imgs/               % images (peut être vide, ne bloque pas la compilation
                         %   grâce aux \IfFileExists{...}{...}{cadre réservé})
```

### Fichier directeur (`<NomDocument>.tex`) -- deux variantes selon le type

**Type cours / ressource / analyse fonctionnelle** (classe `cours`, sans cleveref) :

```latex
\documentclass[cours, noCustomPackages]{UPSTI_Document}
\usepackage{IUT_Annecy}
\usepackage{logos_iut}
\usepackage{gitinfo2}          % optionnel, génère un numéro de version depuis git
\input{preamble.tex}
\input{../preamble_module.tex} % préambule commun au module (couleurs, listings, etc.)
\documentVersion{E}
\newcommand{\UPSTInumeroVersion}{...}
\newcommand{\UPSTInumero}{...}
\begin{document}
\input{main.tex}
\end{document}
```

**Type TD/TP avec questions** (classe `td` ou `TP`, avec cleveref) :

```latex
\documentclass[td, noCustomPackages]{UPSTI_Document}
\usepackage{IUT_Annecy}
\usepackage{logos_iut}
\usepackage[french]{cleveref}   % <-- SEULE différence structurelle importante
\input{preamble.tex}
\input{../preamble_module.tex}
\documentVersion{E}
\newcommand{\UPSTInumero}{TD01}
\newcommand{\UPSTIduree}{4h}
\newcommand{\UPSTImessage}{...}
\newcommand{\UPSTInumeroVersion}{1.0}
\begin{document}
\input{main.tex}
\end{document}
```

### `preamble.tex` (par document)

Contient uniquement les commandes de titre/entête, ex. :
```latex
\newcommand{\UPSTItitreEnTete}{...}
\newcommand{\UPSTItitre}{...}
\newcommand{\UPSTIsousTitreEnTete}{...}
```

### `main.tex`

```latex
\tableofcontents
\input{sources/introduction.tex}
\input{sources/partie1.tex}
...
```

## Pièges identifiés (déjà rencontrés dans ce dépôt)

1. **`preamble_IUT.tex` n'existe pas.** D'anciens documents du dépôt semblent
   le référencer (chemin type `\input{../../../../preamble_IUT.tex}`) mais ce
   fichier est absent du dépôt : toute compilation qui le référence échoue.
   Ne JAMAIS réutiliser cette chaîne d'input. Le fichier commun réellement
   présent et fonctionnel est `<Module>/preamble_module.tex` (un niveau
   au-dessus du dossier du document, ex. `../preamble_module.tex` depuis
   `02_analyse_fonctionnelle/`).

2. **`\cref` n'est PAS disponible dans le patron cours/ressource.** Le patron
   `cours` (voir ci-dessus) ne charge PAS `\usepackage[french]{cleveref}`,
   contrairement au patron `td`/`TP`. Dans un document de type cours/ressource,
   utiliser `\ref{...}` (jamais `\cref`) sauf si l'on ajoute explicitement
   `\usepackage[french]{cleveref}` dans le fichier directeur.

3. **Labels sans `:`.** Ne jamais utiliser de labels du type `\label{sec:xxx}`.
   Utiliser une forme sans caractère spécial, ex. `\label{secModeA5}`,
   `\label{secIntroduction}`. Motif : compatibilité cleveref/babel-french
   utilisés ailleurs dans le dépôt (le `:` dans un label peut interagir avec
   des extensions actives dans d'autres documents du même dépôt/build).

## Compilation

Utiliser `lualatex` (imposé par `UPSTI_Document`), deux passes minimum pour
résoudre les références croisées (`\ref`/`\label`) et la table des matières :

```bash
cd <dossier_du_document>
rm -rf /tmp/verif_xxx && mkdir -p /tmp/verif_xxx
latexmk -pdf -interaction=nonstopmode -output-directory=/tmp/verif_xxx <NomDocument>.tex
```

Si la compilation réussit, copier le PDF résultant à la racine du dossier du
document, puis nettoyer le dossier temporaire.

4. **Titre optionnel de `UPSTIremarque`/`UPSTIinfo`/`UPSTIwarning` (bclogo).**
   L'argument optionnel `[titre]` de ces environnements ne supporte pas de
   manière fiable une combinaison virgule + commande de formatage type
   `\texttt{...}` dans le titre (ex.
   `[Le X, lui aussi, réservé en \texttt{\%MW}]`) : cela peut provoquer une
   erreur fatale de compilation (`! File ended while scanning use of
   \@tempc.`). Garder ces titres en texte simple, sans virgule interne ni
   commande de formatage complexe ; réserver le formatage riche au corps de
   l'environnement.

## Versionning gitinfo2 (dépôt initialisé le 2026-09-13)

Le dépôt racine `/home/ubuntu/01_Enseignement/supports-automatisme-robotique/`
est désormais un dépôt git (initialisé le 2026-09-13, branche `master`). Les
documents qui chargent `\usepackage{gitinfo2}` et utilisent
`\newcommand{\UPSTInumeroVersion}{\gitAuthorDate\if \gitDirty*dirty \fi}`
(patron cours/ressource, cf. ci-dessus) nécessitent que ce dépôt existe et que
ses hooks git soient installés pour fonctionner -- sinon `gitinfo2` émet un
warning « I can't find the file '.git/gitHeadInfo.gin' » et affiche
« (None) » comme version.

Hooks installés dans `.git/hooks/` (identiques, tous exécutables) :
`post-commit`, `post-checkout`, `post-merge`. Contenu = le script
`post-xxx-sample.txt` fourni par le paquet gitinfo2
(`/usr/share/doc/texlive-doc/latex/gitinfo2/post-xxx-sample.txt` sur ce
système) : il régénère `.git/gitHeadInfo.gin` après chaque commit/checkout/
merge à partir de `git log -1 --pretty=format:...`.

**Si le mécanisme cesse de fonctionner** (nouveau clone, `.git` supprimé,
hooks perdus car non versionnés par git lui-même) : recopier ce script dans
les trois emplacements de `.git/hooks/`, les rendre exécutables
(`chmod +x`), puis faire un commit ou `git checkout` pour régénérer le
`.gin`. Sans commit git, `\gitAuthorDate` etc. restent à `(None)`.

`gitinfo2` remonte l'arborescence jusqu'à 4 niveaux (option `maxdepth`) pour
trouver le `.git` : un dépôt à la racine du projet suffit donc pour tous les
sous-dossiers de documents.

## Voir aussi

Pour les conventions UPSTI générales (environnements `UPSTIinfo`, `UPSTIidee`,
`UPSTIwarning`, `UPSTIPreparation`, `UPSTIManipulation`, etc.), se référer à la
mémoire d'agent globale (`~/.claude/agent-memory/latex-geii-instructor/MEMORY.md`)
qui documente ces environnements pour le module POO -- ils sont définis
globalement dans `~/texmf` et réutilisables dans tous les modules, y compris
Automatisme pour la Robotique.
