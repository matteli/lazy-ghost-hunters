Lazy Ghost Hunters
==================

```
- Bonsoir à toi. En tant qu'envoyé officiel et représentant de cette ville
du Comté de l'État de New-York, je t'ordonne de cesser toutes activités surnaturelles
et de retourner immédiatement d'où tu viens ou,
si ça t'arrange, dans la plus proche dimension parallèle.
(C'est bien, ça. Ça devrait marcher Ray.)
- Es-tu un Dieu ?
- Non...
- Alors, périt !
```

[Ghost Hunters](https://www.smartgames.eu/uk/one-player-games/ghost-hunters-0) est un petit jeu matériel édité par Smart Games.
Le but du jeu est d'éclairer 6 fantômes disposés sur une grille 4x4 avec 6 pièces plastiques transparentes sur lesquelles sont dessinées 0, 1 ou 2 torches.
N'ayant pas l'âme de chercher trop longtemps et, il faut bien le dire, afin d'épater mes filles (ce qui devient de plus en plus compliqué), j'ai réalisé un petit programme nommé [Lazy Ghost Hunters](https://github.com/matteli/lazy-ghost-hunters) qui permet de trouver la solution.

Ce qui est assez rigolo dans l'exercice, c'est de réussir à modéliser le jeu. J'étais parti avec une matrice pour indiquer la position des fantômes. Puis finalement, j'ai considéré le grille comme étant un mot de 16 bits, ce qui m'a permis de modéliser très facilement.
Pour indiquer la position d'un fantôme, il suffit d'indiquer la valeur de la case (2ème ligne, 3ème colonne c'est 2^9 = 512).
Pour indiquer l'emplacement d'une pièce en forme d'équerre, j'additionne les valeurs des cases recouvertes.
Si la pièce est déplacé d'une case vers la gauche, on multiplie la valeur totale par deux.

Il suffit ensuite de tester toutes les possibilités avec de la récursivité. Je vérifie à chaque fois qu'une pièce n'en recouvre pas une autre avec un ET et que les lumières recouvrent bien les fantômes avec un XOR.

Et voilà, le résultat :

```
Indicate with 0 for no ghost and 1 for ghost:
0010
1100
0010
0101


..o←
oo↰.
↑.o↓
→o.o
```

En haut, le positionnement des fantômes qui est entré par l'utilisateur.
En bas, le résultat, les "o" pour les fantômes et les flèches qui sont normalement en couleur pour indiquer comment placer les pièces.

Je pensais que mes filles allaient me prendre pour un Dieu, finalement elles me prennent pour un tricheur...