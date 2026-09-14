# Extraction de `ALLIER.STU`

Source : `/home/ubuntu/supports-autom-robotique/02_AutomatismeRobotique/fichiers_etudiants/ALLIER.STU`

## Sections Structured Text

| # | Fichier | Section (Aspbo) | Prog. voisin | Aperçu |
|---|---------|-----------------|--------------|--------|
| 01 | `st/01_MAIN.st` | `-` | `MAIN` | `Step_2.t>=T#1s AND Type_mouv_linaire.m_xDone` |
| 02 | `st/02_D1_POST.st` | `-` | `D1_POST` | `Step_5.t>=T#3s AND prehenseurScara.m_xSaisie AND Type_mouv_l` |
| 03 | `st/03_MAIN.st` | `-` | `MAIN` | `Type_mouv_linaire.m_xDone = true` |
| 04 | `st/04_MAIN.st` | `-` | `MAIN` | `Type_mouv_linaire.m_xDone AND A5.t>=T#2s` |
| 05 | `st/05_GEMMA.st` | `-` | `GEMMA` | `Type_mouv_linaire.m_xDone = true` |
| 06 | `st/06_Aspbo1oT6_U.st` | `Aspbo1oT6$U` | `GEMMA` | `Step_5.t>=T#3s` |
| 07 | `st/07_Aspbo3oT5_U.st` | `Aspbo3oT5$U` | `GEMMA` | `Type_Reset.m_xDone AND Type_Stop.m_xDone AND Type_Power.m_xS` |
| 08 | `st/08_A6_SFC.st` | `-` | `A6_SFC` | `Step_2.t>=T#1s` |
| 09 | `st/09_Aspbo3oT2_U.st` | `Aspbo3oT2$U` | `A1_POST` | `Type_Power.m_xStatus` |
| 10 | `st/10_Aspbo3oT3_U.st` | `Aspbo3oT3$U` | `A1_POST` | `Type_mouv_linaire.m_xDone AND A5.t>=T#2s` |
| 11 | `st/11_Aspbo1oT8_U.st` | `Aspbo1oT8$U` | `A1_POST` | `guichet_IN.m_nixAid AND NOT guichet_IN.m_nixDgt` |
| 12 | `st/12_Aspbo1oT9_U.st` | `Aspbo1oT9$U` | `A1_POST` | `Step_2.t>=T#1s` |
| 13 | `st/13_A1_POST.st` | `-` | `A1_POST` | `guichet_IN.m_nixAid AND guichet_IN.m_nixDgt` |
| 14 | `st/14_A1_POST.st` | `-` | `A1_POST` | `NOT xDefaut AND NOT Type_Power.m_xDone` |

## Grafcets

| # | Fichier | Section (Aspbo) | Prog. voisin | Étapes | Transitions |
|---|---------|-----------------|--------------|--------|-------------|
| 01 | `sfc/01_A6_SFC.*` | `-` | `A6_SFC` | 6 | 6 |
| 02 | `sfc/02_MAIN.*` | `-` | `MAIN` | 6 | 7 |
| 03 | `sfc/03_A1_POST.*` | `-` | `A1_POST` | 6 | 7 |
