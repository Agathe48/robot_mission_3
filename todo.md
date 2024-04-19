# Todo

- [ ] dans le mouvement, faire en sorte que l'agent vert n'aille pas sur un déchet jaune, que l'agent jaune n'aille pas sur un déchet rouge (à coordonner avec la tache suivante) (sauf last column quand l'agent cherche a drop)  (LATER)


--> faire des agents chefs de chaque couleur pour coordonner les autres (pas abimé)
--> si chef abimé il previent et un autre devient chef ou election d'un nouveau chef (LATER)


--> envoyer la grille des déchets, les picked_up_waste, le transformed waste et si tu drops
--> les chefs communiquent entres eux


Principe mouvement amélioré et comm:
- le chef de chaque zone (sauf rouge) va clean la colonne de droite de dépôt (Agathe Plu et Laure)
- covering des autres agents : il se positionne a l'emplacement donné par le chef (dans une cellule le plus à gauche, en ayant divisé par le nombre d'agents classiques, sauf pour rouge où l'on compte aussi le chef), puis il avance vers la droite (ils peuvent ramasser un déchet uniquement s'il est sur la case ou l'agent se trouve (on ne devie pas)), ensuite descend/monte et mouvement droite-gauche (dans ce cas, si dechet transformer) (Oumaima et Agathe Poulain)
- après le covering effectué, les autres vont recevoir des ordres du chef pour aller chercher des déchets (Agathe Plu et Laure)