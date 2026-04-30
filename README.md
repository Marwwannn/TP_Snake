# 🐍 Projet Jeu Snake

Un jeu Snake classique développé en Python avec Pygame.

## Description

Ce projet est une implémentation du célèbre jeu Snake utilisant la programmation orientée objet.
Le joueur contrôle un serpent qui doit manger de la nourriture pour grandir tout en évitant de se mordre ou de toucher les murs.

## Architecture du projet

Le projet utilise une architecture orientée objet avec les classes suivantes :

| Classe | Rôle |
|--------|------|
| `Entity` | Classe de base définissant l'interface commune (`update`, `draw`) |
| `MovingEntity` | Gère la logique de déplacement (direction, vitesse) |
| `Snake` | Le serpent du joueur (corps, croissance, collisions) |
| `Food` | La nourriture à collecter |
| `Game` | Orchestre le jeu (boucle principale, événements, affichage) |

## Installation

### Prérequis
- Python 3.x
- Pygame

### Étapes

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

## Fonctionnalités

- Déplacement fluide du serpent
- Croissance du serpent en mangeant la nourriture
- Affichage du score en temps réel
- Détection des collisions (murs et soi-même)
- Écran Game Over avec possibilité de rejouer
- Augmentation de la difficulté selon le score

## Captures d'écran

*À venir*

## Auteur

Marwy

## Licence

Ce projet est réalisé dans le cadre d'un TP.
