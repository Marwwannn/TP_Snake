# Projet Jeu Snake

## Description

Ce projet est une implémentation du jeu Snake créer seul par marwan le goat, en utilisant python et la bibliothèque pygame 

## Architecture du projet
### Classe Entity

J'ai pas touché.

### Class MovingEntity

J'ai créer en premier lieu les getter et setter. Je n'ai pas eu l'envie et le temps de mettre les variable en privé. Mais j'ai mis des condition sur les modification pour un minimume de sureté.
En suite j'ai mis des condition sur les direction pour ne pas avoir de probleme car on se deplace soit de l'axe X ou Y pas les 2 en meme temps.

### Class Snake

Elle herite de 'MovingEntity' car c'est une entité !!!!!  Création de la méthode update pour la réecriture de la classe mère. Elle me permet de MAJ la nouvelle tete du serpent et de supprimer la queu si elle ne doit pas grandir.
La methode draw sert a dessiner le serpent grace au position stocker dans la liste de pair (x,y) dans body
J'ai créer la methode head_pos pour retourner directement la tête du serpends et pas directement tout son corp. J'ai fais ça car nous allons en avoir besoin pour savoir si il a toucher la pomme.
Apres des getter et setter.

### Class Food

Elle herite elle aussi de 'MovingEntity'. Dans le constructeur de la classe j'ai crées de sposition aléatoir de la pomme qui vas de 0 a max_ecran avec des pas de 'taille de la cellule' pour quelle apparesse sur la cellule et pas entre.
Ensuite j'ai overrite sur la methode draw en dessinant un carre (meme si j'ai utiliser rect) vert pour la pomme.
J'ai créer un getter pour la pos de la pomme et un spawn pour la faire réaparettre.

### Class Game

Elle réunie tout les classe, Donc dans le constructeur tu fais appele au class plus a des variable dont tu as besoin comme score, game_over, etc... 
handle_events est une methode qui ecoute ton clavier pour que moi je dise ce que quoi( comme flèche du bas) fais quoi (changement de direction). Je fais attention que si je vais a une direction elle ne vas pas a l'encontre de la direction precedante,
en gros si tu vas vers le bas la prochaine action ne peux pas etre le haut et vise versa pareil pour la gauche et la droite. Elle permet de controller que le serpent ne fasse pas de demi trour.

Dans le Update j'appele les update de ma classe food et snake et je verifie si grace au update si il y a pas de game over ou autre puis dans ma methode je verifie la position de la tête du serpent avec la position de la pomme si oui,
on refais apparaitre la pomme puis on le fais grandir.

La methode Draw de game est le seul endroit ou j'ai utiliser de l'ia pour le dessin car j'etait seul et je voulais pas perdre du temps avec les methode de la bibliothèque python. 
J'avais fais un efffort de documentation pour les draw des autre classe car elle etais assez simple mais la il fallais dessiner l'ecran puis le texte sur l'ecrant ensuite la taille etc...

La methode Run est le maitre du jeu, elle appelle la methode handle_events pour les deplacement, puis je mets a jour a chaque deplacement en appelelant la methode Update etr dessin pour tout dessiner.
j'ai ajouter 2 variable qui est self.clock.tick(Snake.DEFAULT_SPEED) qui permettais de reguler la frame rate au deplacement du snake et une variable pour rendre plus rapide le serpent suivant sont score(un a 10 et un a 20, je vous invite a tester).

J'ai voulus que mon jeu soit jouable a l'infinie sans fermer et relancer, donc je me suis rensegné et ajouter un boutton restart est vraiment long et surment que j'utiliserais gpt mais j'ai trouver une autre solution créer une methode qui renitisialise mes varibale et
que si j'apuis sur R quand je suis en game over ça relance tout car je reste dans le while meme si je suis en game over.
