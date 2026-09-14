# Présentation du système
Machine à présenter : Cellule robotique avec convoyeur décrite dans ressources_payga/RIF_GT_TP1_2024.pdf
La présentation sera minimale, au vu de ce qui est demandé aux étudiants. Ce sera à eux de faire la conception du réseau et de l'architecture ainsi que le schéma synoptique. 

# Travail à faire
## Besoin : 
On désire mettre en oeuvre le traitement de la pièce par une cellule robotique scara. Il s'agira de faire tremper des gobelet dans une cuve pendant un temps minimum de 10s et un temps maximum de 1 min. 
On dispose de 4 cuves pouvant être utilisés en parallèle. 
On dispose de la cellule présentée dans la ressource décrite ci-dessus. 
Pour des raisons de sécurité, le robot et l'automate gérant l'IHM devront être sur un réseau séparé du réseau de l'entreprise.

Les ordinateurs de la salle occupent les adresses IP 172.16.180.1/24 à 172.16.180.17/24
La commande devra se faire via le protocole Ethernet/IP dont une description aura été fournie par l'enseignant (cours au tableau et support papier)

Images qui seront intégrées au document, ajoutées dans le dossier imgs (mode brouillon en attendant) : 
    - robot.jpg
    - convoyeur.jpg
    - panneau_electrique_convoyeur.jpg
    - IHM.jpg
    - baie_cs9.jpg
    - vue_globale.jpg

## Philosophie de la séance. 
Les étudiants doivent rendre un rapport par équipe de trois qui comportera les livrables suivants : 
- Un schéma synoptique de l'installation
- Un schéma de l'architecture réseau contenant les adresses IP des différents équipements
- Une étude des modes de fonctionnement de la cellule robotique et de l'automate 
    - Chaque mode du GMMA qui sera utilisé devra être décrit précisément : 
        - Conditions d'entrée et de sortie
        - Actions réalisées par le mode
- Cartographie mémoire au sein de l'automate M340 pour l'échange des informations avec le robot, l'IHM et le convoyeur.
- Sécurités éventuelles à mettre en oeuvre
- Trajectoires du robot envisagées avec leurs types de mouvements (linéaire, circulaire, etc.) et les vitesses associées.


