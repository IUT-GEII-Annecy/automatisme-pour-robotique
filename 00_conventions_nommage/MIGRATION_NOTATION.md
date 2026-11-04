# Migration de la convention de nommage

## Introduction

La convention de nommage utilisée jusqu'ici dans les supports de la cellule robotisée EtherNet/IP reposait sur une notation **inspirée de la notation hongroise** : chaque identifiant portait un préfixe de portée (`m_`), une ou plusieurs lettres de type (`x`, `i`, `int`, `r`, `ui`, `udi`, `t`, `a<N>`), un préfixe d'origine IO-Scanning (`nix`, `nqx`) ou encore le nom technique du bloc instancié (`Inst<Bloc><Mode>`).

Cette notation est aujourd'hui jugée **dépassée** : les environnements IEC 61131-3 modernes (Codesys, TwinCAT, Control Expert) affichent le type de chaque variable à la complétion et au survol, ce qui rend l'encodage du type dans le nom redondant, et les guides de style actuels (PLCopen *Coding Guidelines*, conventions Beckhoff/Codesys pour les champs de structures et les instances) privilégient des noms métier courts en camelCase. La nouvelle convention vise donc :

- des identifiants **lisibles et centrés sur le métier** (`busy`, `errorID`, `velocity`) ;
- un alignement sur les pratiques **PLCopen / Codesys / TwinCAT** ;
- la conservation des seuls marqueurs porteurs de sens : origine IO-Scanning (`in`/`out`), rôle et mode GEMMA des instances, préfixe `status` des objets de passage de paramètres.

### Règles de la convention cible

| Élément | Ancienne forme | Nouvelle forme |
|---|---|---|
| Types (maison / uniVALplc) | `T<Nom>` / `T_<Nom>` | **inchangé** |
| Champs de structure | `m_<type><Nom>` | `<nom>` (camelCase, minuscule initiale) |
| Booléens IO-Scanning autonomes | `nix<Nom>` / `nqx<Nom>` | `in<Nom>` / `out<Nom>` |
| Objets métier (`<rôle><Équipement>`, from/to) | — | **inchangé** |
| Instances de blocs fonctionnels | `Inst<Bloc><Mode>` | `<rôle><Mode>` (`<rôle>` seul si commun à tous les modes) |
| Objets `TCtrlStatusGroup*` | `ctrlStatusGroup<Rôle><Mode>` | `status<Rôle><Mode>` |
| Sections/transitions SFC GEMMA | `GM_S_<Mode>`, `GM_T_<A>to<B>` | **inchangé** |

### Périmètre et méthode

- Recensement exhaustif par `grep -rn` des fichiers `.tex` et `.st` de `02_TP/TP_0X/` (TP_02, TP_03, TP_04), formes `m_` et `m\_` (LaTeX) comprises : **16 identifiants distincts, 52 occurrences (lignes)**. Les PDF sont ignorés.
- Colonne « PDF collègues » : occurrences trouvées par `pdftotext` dans `ressources_payga/RIF_*.pdf` (nombre d'occurrences par fichier). **Non éditables ici**, à titre d'information : l'enseignant décidera s'il propose la même évolution à ses collègues.
- Les identifiants présents uniquement dans les PDF sont listés aussi (colonne 02_TP vide) pour information.
- Les renommages marqués *(proposé)* découlent de la règle générale et ne figuraient pas dans la liste d'exemples validée : à confirmer.
- `02_TP/TP_04/` ne contient actuellement aucune occurrence. `02_TP/InstallationControlExpert/` (hors périmètre `TP_0X`) contient aussi `m_xActivityBit`, `m_tActivationDuration`, `m_tTaskPeriod` dans `codesys/*.tex`.

## 1. Champs de structure (suppression de `m_` + lettre(s) de type)

| Ancien nom | Nouveau nom | Occurrences dans `02_TP/` (fichier : lignes) | PDF collègues (`ressources_payga/RIF_*.pdf`) |
|---|---|---|---|
| `m_Inputs` | `inputs` | `02_TP/TP_02/HMI_types_FB.st` : 3 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_Outputs` | `outputs` | `02_TP/TP_02/HMI_types_FB.st` : 4<br>`02_TP/TP_03/GMMA.tex` : 21<br>`02_TP/TP_03/manipulations.tex` : 26 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (6)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_Screen` | `screen` | `02_TP/TP_03/manipulations.tex` : 26 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (4) |
| `m_a5tankLine` | `tankLine` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_cartesianPos` | `cartesianPos` (déjà conforme hors `m_`) | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_iCurvSpeed_mm_per_s` | `curvSpeed_mm_per_s` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_iMovementID` | `movementID` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_iStateGmma` | `stateGmma` | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_intPartNumber` | `partNumber` | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_intStateGmma` | `stateGmma` *(proposé)* | `02_TP/TP_03/manipulations.tex` : 26 | RIF_RBT_TP3_2024.pdf (4) |
| `m_ixJ1Plus` | `j1Plus` *(proposé)* | — | RIF_RBT_TP5_2024.pdf (1) |
| `m_ixJ2Plus` | `j2Plus` *(proposé)* | — | RIF_RBT_TP5_2024.pdf (1) |
| `m_ixJ3Up` | `j3Up` *(proposé)* | — | RIF_RBT_TP5_2024.pdf (1) |
| `m_ixJ4Plus` | `j4Plus` *(proposé)* | — | RIF_RBT_TP5_2024.pdf (1) |
| `m_jointPos` | `jointPos` (déjà conforme hors `m_`) | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_na4qxHex7Seg` | `hex7Seg` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nixAuto` | `auto` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixEmptyTank0` | `emptyTank0` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixEmptyTank4` | `emptyTank4` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixEmptyTanks` | `emptyTanks` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixJ1Minus` | `j1Minus` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixJ1Plus` | `j1Plus` | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nixJ2Minus` | `j2Minus` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixJ2Plus` | `j2Plus` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nixJ3Down` | `j3Down` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixJ3Up` | `j3Up` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nixJ4Minus` | `j4Minus` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixJ4Plus` | `j4Plus` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nixLoadTank0` | `loadTank0` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixManu` | `manu` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixStopRequest` | `stopRequest` | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nixUnloadTank4` | `unloadTank4` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_nqxArmUnderPower` | `armUnderPower` | — | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (1) |
| `m_nqxBlueColumn` | `blueColumn` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxGreenColumn` | `greenColumn` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxLightLoadTank0` | `lightLoadTank0` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxLightLoadTank1` | `lightLoadTank1` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxLightLoadTank2` | `lightLoadTank2` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxLightLoadTank3` | `lightLoadTank3` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxLightStopRequest` | `lightStopRequest` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxLightUnLoadTank4` | `lightUnLoadTank4` *(proposé)* | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_nqxRedColumn` | `redColumn` | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_qToR` | `toR` | `02_TP/TP_03/GMMA.tex` : 21 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (1) |
| `m_rAcceleration` | `acceleration` | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_rCartesianVel` | `cartesianVel` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_rDeceleration` | `deceleration` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_rRotationalVel` | `rotationalVel` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_rVelocity` | `velocity` | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_tActivationDuration` | `activationDuration` *(proposé)* | `02_TP/TP_02/codesys/application.tex` : 10<br>`02_TP/TP_02/codesys/classes.tex` : 34<br>`02_TP/TP_02/codesys/heritage.tex` : 18<br>`02_TP/TP_03/codesys/application.tex` : 10<br>`02_TP/TP_03/codesys/classes.tex` : 34<br>`02_TP/TP_03/codesys/heritage.tex` : 18<br>`02_TP/TP_04/codesys/application.tex` : 10<br>`02_TP/TP_04/codesys/classes.tex` : 34<br>`02_TP/TP_04/codesys/heritage.tex` : 18 | — |
| `m_tElapsedTime` | `elapsedTime` | — | RIF_RBT_TP2_2024.pdf (1) |
| `m_tTaskPeriod` | `taskPeriod` *(proposé)* | `02_TP/TP_02/codesys/application.tex` : 14<br>`02_TP/TP_02/codesys/classes.tex` : 35<br>`02_TP/TP_03/codesys/application.tex` : 14<br>`02_TP/TP_03/codesys/classes.tex` : 35<br>`02_TP/TP_04/codesys/application.tex` : 14<br>`02_TP/TP_04/codesys/classes.tex` : 35 | — |
| `m_transitionParam` | `transitionParam` (déjà conforme hors `m_`) | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_udiErrorID` | `errorID` | `02_TP/TP_02/TCtrlStatusGroup.st` : 7 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (3)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_uiBufferMode` | `bufferMode` | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_uiCoordSystem` | `coordSystem` | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_uiToolNumber` | `toolNumber` | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_uiTransitionMode` | `transitionMode` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xActive` | `active` | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xActivityBit` | `activityBit` *(proposé)* | `02_TP/TP_02/codesys/application.tex` : 6<br>`02_TP/TP_02/codesys/classes.tex` : 33, 40<br>`02_TP/TP_02/codesys/heritage.tex` : 17<br>`02_TP/TP_02/codesys/properties.tex` : 47, 50<br>`02_TP/TP_03/codesys/application.tex` : 6<br>`02_TP/TP_03/codesys/classes.tex` : 33, 40<br>`02_TP/TP_03/codesys/heritage.tex` : 17<br>`02_TP/TP_03/codesys/properties.tex` : 47, 50<br>`02_TP/TP_04/codesys/application.tex` : 6<br>`02_TP/TP_04/codesys/classes.tex` : 33, 40<br>`02_TP/TP_04/codesys/heritage.tex` : 17<br>`02_TP/TP_04/codesys/properties.tex` : 47, 50 | — |
| `m_xBusy` | `busy` | `02_TP/TP_02/TCtrlStatusGroup.st` : 4 | RIF_RBT_TP2_2024.pdf (2)<br>RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xCommandAborted` | `commandAborted` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xCommandTransferred` | `commandTransferred` *(proposé)* | — | RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xDone` | `done` | `02_TP/TP_02/TCtrlStatusGroup.st` : 5 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (1)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xEnable` | `enable` | `02_TP/TP_02/TCtrlStatusGroup.st` : 3 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (2) |
| `m_xError` | `error` | `02_TP/TP_02/TCtrlStatusGroup.st` : 6 | RIF_RBT_TP2_2024.pdf (1)<br>RIF_RBT_TP3_2024.pdf (3)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xExecute` | `execute` | — | RIF_RBT_TP3_2024.pdf (2)<br>RIF_RBT_TP4_2024.pdf (1)<br>RIF_RBT_TP5_2024.pdf (1) |
| `m_xStatus` | `status` | — | RIF_RBT_TP3_2024.pdf (2) |
| `m_xTimeOut` | `timeOut` *(proposé)* | `02_TP/TP_02/TCtrlStatusGroup.st` : 8 | RIF_RBT_TP2_2024.pdf (1) |

## 2. Variables booléennes autonomes obtenues par IO-Scanning (`nix`→`in`, `nqx`→`out`)

| Ancien nom | Nouveau nom | Occurrences dans `02_TP/` (fichier : lignes) | PDF collègues (`ressources_payga/RIF_*.pdf`) |
|---|---|---|---|
| `nixAid` | `inAid` | — | RIF_GT_TP1_2024.pdf (1) |
| `nixDgt` | `inDgt` | — | RIF_GT_TP1_2024.pdf (1) |
| `nixDpo` | `inDpo` | — | RIF_GT_TP1_2024.pdf (1) |
| `nixDpp` | `inDpp` | — | RIF_GT_TP1_2024.pdf (1) |
| `nqxBE` | `outBE` | — | RIF_GT_TP1_2024.pdf (1) |
| `nqxBP` | `outBP` | — | RIF_GT_TP1_2024.pdf (1) |
| `nqxCB` | `outCB` | — | RIF_GT_TP1_2024.pdf (1) |
| `nqxCR` | `outCR` | — | RIF_GT_TP1_2024.pdf (1) |
| `nqxCV` | `outCV` | — | RIF_GT_TP1_2024.pdf (1) |

## 3. Instances de blocs fonctionnels (suppression de `Inst` + nom du bloc)

| Ancien nom | Nouveau nom | Occurrences dans `02_TP/` (fichier : lignes) | PDF collègues (`ressources_payga/RIF_*.pdf`) |
|---|---|---|---|
| `InstGroupResetD2` | `resetD2` | — | RIF_RBT_TP3_2024.pdf (1) |
| `InstMoveAxisAbsoluteF4` | `moveAxisF4` *(proposé)* | — | RIF_RBT_TP5_2024.pdf (1) |
| `InstMoveLinearAbsoluteF1` | `moveLinearF1` *(proposé)* | — | RIF_RBT_TP4_2024.pdf (1) |

## 4. Objets de statut `TCtrlStatusGroup` / `TCtrlStatusGroupPower` (`ctrlStatusGroup`→`status`)

| Ancien nom | Nouveau nom | Occurrences dans `02_TP/` (fichier : lignes) | PDF collègues (`ressources_payga/RIF_*.pdf`) |
|---|---|---|---|
| `ctrlStatusGroupContinueD2` | `statusContinueD2` | — | RIF_RBT_TP3_2024.pdf (1) |
| `ctrlStatusGroupContinueF4` | `statusContinueF4` | — | RIF_RBT_TP5_2024.pdf (1) |
| `ctrlStatusGroupPower` | `statusPower` | — | RIF_RBT_TP3_2024.pdf (2) |
| `ctrlStatusGroupRead` | `statusRead` | `02_TP/TP_02/communicationCS99.tex` : 62, 82, 92 | RIF_RBT_TP2_2024.pdf (3) |
| `ctrlStatusGroupResetD2` | `statusResetD2` | — | RIF_RBT_TP3_2024.pdf (1) |
| `ctrlStatusGroupStopD2` | `statusStopD2` | — | RIF_RBT_TP3_2024.pdf (1) |
| `ctrlStatusGroupStopF4` | `statusStopF4` | — | RIF_RBT_TP5_2024.pdf (1) |
| `ctrlStatusGroupWrite` | `statusWrite` | `02_TP/TP_02/communicationCS99.tex` : 63, 83, 92 | RIF_RBT_TP2_2024.pdf (3) |
