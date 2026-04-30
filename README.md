# 🐍 Projet Jeu Snake

## Description

Ce projet est une implémentation du jeu Snake créer seul par marwan le goat, en utilisant python et la bibliothèque pygame.
Le joueur contrôle un serpent qui doit manger de la nourriture pour grandir tout en évitant de se mordre ou de toucher les murs.

## Prérequis
- Python 3.x
- Pygame : `pip install pygame`

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/marwy/TP_Snake.git
cd TP_Snake
```

2. Installer Pygame :
```bash
pip install pygame
```

3. Lancer le jeu :
```bash
python Game.py
```

## Contrôles

| Touche | Action |
|--------|--------|
| ↑ | Aller en haut |
| ↓ | Aller en bas |
| ← | Aller à gauche |
| → | Aller à droite |
| R | Relancer la partie (après Game Over) |

## Architecture du projet

### Classe Entity

J'ai pas touché.

### Class MovingEntity

J'ai créer en premier lieu les getter et setter. Je n'ai pas eu l'envie et le temps de mettre les variable en privé. Mais j'ai mis des condition sur les modification pour un minimume de sureté.
En suite j'ai mis des condition sur les direction pour ne pas avoir de probleme car on se deplace soit de l'axe X ou Y pas les 2 en meme temps.

### Class Snake

Elle hérite de 'MovingEntity' car c’est une entité !!!!! Création de la méthode update pour la réécriture de la classe mère. Elle me permet de MAJ la nouvelle tête du serpent et de supprimer la queue si elle ne doit pas grandir.
La méthode draw sert à dessiner le serpent grâce aux positions stockées dans la liste de paires (x, y) dans body.
J’ai créé la méthode head_pos pour retourner directement la tête du serpent et pas directement tout son corps. J’ai fait ça car nous allons en avoir besoin pour savoir s’il a touché la pomme.
Après, des getter et setter.

### Class Food

Elle hérite elle aussi de 'MovingEntity'. Dans le constructeur de la classe, j’ai créé des positions aléatoires de la pomme qui vont de 0 à max_ecran avec des pas de 'taille de la cellule' pour qu’elle apparaisse sur la cellule et pas entre.
Ensuite, j’ai override sur la méthode draw en dessinant un carré (même si j’ai utilisé rect) vert pour la pomme.
J’ai créé un getter pour la pos de la pomme et un spawn pour la faire réapparaître.

### Class Game

Elle réunit toutes les classes. Donc dans le constructeur, tu fais appel aux classes plus à des variables dont tu as besoin comme score, game_over, etc...
handle_events est une méthode qui écoute ton clavier pour que moi je dise ce que quoi (comme flèche du bas) fait quoi (changement de direction). Je fais attention que si je vais à une direction, elle ne va pas à l’encontre de la direction précédente,
en gros si tu vas vers le bas, la prochaine action ne peut pas être le haut et vice versa, pareil pour la gauche et la droite. Elle permet de contrôler que le serpent ne fasse pas de demi-tour.

Dans le Update, j’appelle les update de ma classe food et snake et je vérifie si grâce au update s’il n’y a pas de game over ou autre, puis dans ma méthode je vérifie la position de la tête du serpent avec la position de la pomme, si oui,
on refait apparaître la pomme puis on le fait grandir.

La méthode Draw de game est le seul endroit où j’ai utilisé de l’IA pour le dessin car j’étais seul et je ne voulais pas perdre du temps avec les méthodes de la bibliothèque python.
J’avais fait un effort de documentation pour les draw des autres classes car elles étaient assez simples, mais là il fallait dessiner l’écran puis le texte sur l’écran, ensuite la taille, etc...

La méthode Run est le maître du jeu, elle appelle la méthode handle_events pour les déplacements, puis je mets à jour à chaque déplacement en appelant la méthode Update et le dessin pour tout dessiner.
J’ai ajouté 2 variables, dont self.clock.tick(Snake.DEFAULT_SPEED) qui permettait de réguler la frame rate au déplacement du snake et une variable pour rendre plus rapide le serpent suivant son score (un à 10 et un à 20, je vous invite à tester).

J’ai voulu que mon jeu soit jouable à l’infini sans fermer et relancer, donc je me suis renseigné et ajouter un bouton restart est vraiment long et sûrement que j’utiliserais gpt, mais j’ai trouvé une autre solution : créer une méthode qui réinitialise mes variables et
que si j’appuie sur R quand je suis en game over, ça relance tout car je reste dans le while même si je suis en game over.

### Bonus

J'ai repondus a ces condition :
- Ajouter pas de demi-tour (contrainte sur set_direction), condition
- Empêcher le serpent de faire demi-tour instantanément, condition
- Création d'un exécutable (a n de lancer le jeu facilement) ,j'ai utiliser PyInstaller avec la commande ( python3 -m PyInstaller --onefile --windowed Game.py). L'executable se trouve dans le document 'dist'
- Ajouter un système d'états (menu, running, paused, game_over) via un pattern State ( a moitier car j'ai juste fais running), j'ai fais un restart et game over. Il me manque seulement paused
- Un speed de vitesse avec des palier de score (10 et 20 pts)


## Réponse aux questions

- Quels sont les rôles respectifs de Snake, Food, Game ?

  Snake gère les element du serpent comme le deplacement, sa gestion de son corp, sa representation graphique. Food gère ma position de la pomme et sa representation graphique.
  Game reuni tout le monde, crée chauque entité verifie des condition comme pour le score si ces deux entité été a la meme position alors +1 au score etc... la partie graphique les titre la fenetre de jeu etc...

- Donnez un exemple concret où l'accès direct à snake._body pourrait casser le jeu.

  C'est quand on vide la liste du snake, donc pas de tête et donc on peux plus jouer au jeu.

-  Expliquez le polymorphisme ici : quelle interface implicite partagent Food/Snake ?

   Avec Entity elle permet de facilement mettre/ dessiner les entité et ça sert a ça le polymorphisme.

- Pourquoi Food.update() existe alors qu'il ne fait rien ?

  Car elle herite indirectement de la methode mére qui est entity car il herite de MovingEntity, elle existe mais ne sert a rien dans food. C'est ça le polymorphisme.

- Pourquoi CELL_SIZE et DEFAULT_SPEED sont des attributs de classe et pas d'instance ?

  Car elle doit avoir la meme valeur peu importe les instance.

- Donnez un exemple où set_cell_size() protège le programme (valeurs invalides)

  if value > 0: Je verifie que la valeur est toujour positive.

## Auteur

Marwy

## Licence

Ce projet est réalisé dans le cadre d'un TP.
