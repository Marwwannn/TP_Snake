# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (reseau Q + trainer + agent DQN).
# -----------------------------------------------------------------------------
# Ce fichier contient 3 classes :
#   - Linear_QNet : HERITE de torch.nn.Module -> c'est le RESEAU DE NEURONES.
#   - QTrainer    : n'herite de rien -> contient la regle d'apprentissage.
#   - Agent       : n'herite de rien -> le "joueur IA" (memoire + decisions).
# POURQUOI : ces classes implementent un DQN (Deep Q-Learning) qui apprend,
#   partie apres partie, quelle action choisir selon l'etat du jeu.
# -----------------------------------------------------------------------------
import os                                       # Pour gerer les chemins/dossiers de sauvegarde
import random                                   # Pour l'exploration aleatoire et l'echantillonnage
from collections import deque                   # File a taille limitee : sert de "memoire" a l'agent

import numpy as np                              # Manipulation de tableaux (etats/actions)
import torch                                    # Bibliotheque de deep learning (PyTorch)
import torch.nn as nn                           # Modules reseaux de neurones
import torch.optim as optim                     # Optimiseurs (ici Adam)


MAX_MEMORY = 100_000                            # Taille maximale de la memoire de replay (nb de transitions)
BATCH_SIZE = 1000                               # Taille d'un lot d'entrainement (long memory)

# Dossier "model" situe a cote de ce fichier (IA/model), peu importe d'ou on
# lance le script -> la sauvegarde/chargement du reseau marche toujours.
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")


class Linear_QNet(nn.Module):                   # Reseau de neurones ; HERITE de nn.Module (obligatoire dans PyTorch)
    """
    Reseau de neurones simple (MLP) pour Q-learning.
      Input  : 11 features de l'etat (voir GameAI.get_state)
      Hidden : 256 neurones, activation ReLU
      Output : 3 Q-values, une par action (tout droit / droite / gauche)
    """

    def __init__(self, input_size=11, hidden_size=256, output_size=3):  # 11 entrees -> 256 caches -> 3 sorties
        super().__init__()                      # Initialise la classe mere nn.Module (indispensable)
        self.linear1 = nn.Linear(input_size, hidden_size)   # 1ere couche : 11 -> 256
        self.linear2 = nn.Linear(hidden_size, output_size)  # 2eme couche : 256 -> 3

    def forward(self, x):                       # Passe avant : calcule la sortie a partir de l'entree x
        x = torch.relu(self.linear1(x))         # Couche 1 + activation ReLU (met les negatifs a 0)
        return self.linear2(x)                  # Couche 2 : renvoie les 3 Q-values (une par action)

    def save(self, file_name="model.pth", folder=MODEL_DIR):  # Sauvegarde les poids du reseau (dans IA/model)
        os.makedirs(folder, exist_ok=True)      # Cree le dossier "model" s'il n'existe pas
        torch.save(self.state_dict(), os.path.join(folder, file_name))  # Ecrit les poids dans IA/model/model.pth

    def load(self, file_name="model.pth", folder=MODEL_DIR):  # Charge des poids sauvegardes (depuis IA/model)
        path = os.path.join(folder, file_name)  # Construit le chemin du fichier
        if not os.path.exists(path):            # Si le fichier n'existe pas...
            return False                        # ...echec : il faut d'abord entrainer
        try:                                    # On tente de charger...
            self.load_state_dict(torch.load(path))  # Charge les poids dans le reseau
        except Exception:                       # Si les poids ne correspondent pas a l'architecture...
            # poids incompatibles avec l'architecture courante
            return False                        # ...echec propre
        self.eval()                             # Passe le reseau en mode "evaluation" (pas d'entrainement)
        return True                             # Chargement reussi


class QTrainer:                                 # Contient la logique d'apprentissage (ne herite de rien)
    """
    Boucle d'apprentissage Q-learning :
      target = reward                       si done
      target = reward + gamma * max(Q(s'))  sinon
    Loss MSE entre Q(s)[action] et target.
    """

    def __init__(self, model, lr=0.001, gamma=0.9):  # model=reseau, lr=vitesse d'apprentissage, gamma=importance du futur
        self.model = model                      # Le reseau a entrainer
        self.gamma = gamma                      # Facteur d'actualisation (poids des recompenses futures)
        self.optimizer = optim.Adam(model.parameters(), lr=lr)  # Optimiseur Adam pour ajuster les poids
        self.criterion = nn.MSELoss()           # Fonction de perte : erreur quadratique moyenne

    def train_step(self, state, action, reward, next_state, done):  # Une etape d'entrainement (1 ou plusieurs transitions)
        state = torch.tensor(np.array(state), dtype=torch.float)        # Convertit l'etat en tenseur PyTorch
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)  # Idem pour l'etat suivant
        action = torch.tensor(np.array(action), dtype=torch.long)      # Action en tenseur d'entiers
        reward = torch.tensor(np.array(reward), dtype=torch.float)     # Recompense en tenseur flottant

        if state.dim() == 1:                    # Si on a une seule transition (vecteur 1D)...
            state = state.unsqueeze(0)          # ...on la transforme en lot de taille 1
            next_state = next_state.unsqueeze(0)  # Idem etat suivant
            action = action.unsqueeze(0)        # Idem action
            reward = reward.unsqueeze(0)        # Idem recompense
            done = (done,)                      # 'done' devient un tuple a un element

        pred = self.model(state)                # Q-values predites par le reseau pour l'etat actuel
        target = pred.clone()                   # Copie des predictions : on va y corriger la valeur de l'action jouee
        for i in range(len(done)):              # Pour chaque transition du lot...
            q_new = reward[i]                   # Cas "fin de partie" : la cible est juste la recompense
            if not done[i]:                     # Si la partie continue...
                q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))  # ...recompense + futur attendu
            target[i][torch.argmax(action[i]).item()] = q_new  # On corrige la Q-value de l'action reellement jouee

        self.optimizer.zero_grad()              # Remet les gradients a zero avant le calcul
        loss = self.criterion(target, pred)     # Calcule l'erreur entre cible et prediction
        loss.backward()                         # Retropropagation : calcule les gradients
        self.optimizer.step()                   # Met a jour les poids du reseau


class Agent:                                    # Le "joueur IA" complet (ne herite de rien)
    """
    Agent DQN complet :
      - replay memory (deque max 100k)
      - politique epsilon-greedy
      - train_short_memory (1 transition apres chaque step)
      - train_long_memory (batch 1000 a la fin de chaque partie)
    """

    def __init__(self, eps_start=80, eps_decay_per_game=1, lr=0.001, gamma=0.9):  # Parametres d'exploration et d'apprentissage
        self.n_games = 0                        # Nombre de parties jouees (sert a reduire l'exploration)
        self.eps_start = eps_start              # Niveau d'exploration de depart (epsilon initial)
        self.eps_decay_per_game = eps_decay_per_game  # Diminution d'epsilon a chaque partie
        self.memory = deque(maxlen=MAX_MEMORY)  # Memoire de replay (oublie les plus vieilles transitions)
        self.model = Linear_QNet()              # Le reseau de neurones de l'agent
        self.trainer = QTrainer(self.model, lr=lr, gamma=gamma)  # L'entraineur associe au reseau

    @property                                   # 'epsilon' se calcule automatiquement comme un attribut
    def epsilon(self):                          # Taux d'exploration courant (decroit avec les parties)
        return max(0, self.eps_start - self.n_games * self.eps_decay_per_game)  # Ne descend jamais sous 0

    def get_action(self, state):                # Choisit une action a partir de l'etat
        action = [0, 0, 0]                      # Action encodee en 3 cases (une seule sera a 1)
        if random.randint(0, 200) < self.epsilon:  # Avec une probabilite liee a epsilon -> EXPLORATION
            move = random.randint(0, 2)         # On choisit une action au hasard (0,1,2)
        else:                                   # Sinon -> EXPLOITATION (on suit le reseau)
            state_tensor = torch.tensor(state, dtype=torch.float)  # Etat converti en tenseur
            with torch.no_grad():               # Pas de calcul de gradient (on ne fait que predire)
                q_values = self.model(state_tensor)  # Le reseau predit les 3 Q-values
            move = int(torch.argmax(q_values).item())  # On prend l'action a la meilleure Q-value
        action[move] = 1                        # On active l'action choisie
        return action                           # Renvoie l'action [x,x,x]

    def remember(self, state, action, reward, next_state, done):  # Stocke une transition en memoire
        self.memory.append((state, action, reward, next_state, done))  # Ajoute le 5-uplet a la memoire de replay

    def train_short_memory(self, state, action, reward, next_state, done):  # Entrainement immediat (1 transition)
        self.trainer.train_step(state, action, reward, next_state, done)  # Apprend tout de suite apres le pas

    def train_long_memory(self):                # Entrainement par lot (a la fin de chaque partie)
        if len(self.memory) > BATCH_SIZE:       # Si on a assez de souvenirs...
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # ...on tire un lot aleatoire de 1000 transitions
        else:                                   # Sinon (pas encore assez)...
            mini_sample = self.memory           # ...on prend toute la memoire
        states, actions, rewards, next_states, dones = zip(*mini_sample)  # On separe les 5 colonnes du lot
        self.trainer.train_step(states, actions, rewards, next_states, dones)  # On entraine sur tout le lot d'un coup
# ##################################################
