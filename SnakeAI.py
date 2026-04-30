import os
import random
import numpy as np
import torch
import torch.nn as nn


class Linear_QNet(nn.Module):
    """
    Reseau de neurones simple (MLP) pour Q-learning.
      Input  : 11 features de l'etat (voir GameAI.get_state)
      Hidden : 256 neurones, activation ReLU
      Output : 3 Q-values, une par action (tout droit / droite / gauche)
    """

    def __init__(self, input_size=11, hidden_size=256, output_size=3):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        return self.linear2(x)

    def save(self, file_name="model.pth", folder="model"):
        os.makedirs(folder, exist_ok=True)
        torch.save(self.state_dict(), os.path.join(folder, file_name))

    def load(self, file_name="model.pth", folder="model"):
        path = os.path.join(folder, file_name)
        if not os.path.exists(path):
            return False
        self.load_state_dict(torch.load(path))
        self.eval()
        return True


class Agent:
    """
    Agent DQN.
    Pour l'instant : juste la politique epsilon-greedy et l'acces au reseau.
    L'entrainement (replay memory, optimizer, target network) viendra dans
    train.py a la prochaine session.
    """

    def __init__(self, eps_start=80, eps_decay_per_game=1):
        self.n_games = 0
        self.eps_start = eps_start
        self.eps_decay_per_game = eps_decay_per_game
        self.model = Linear_QNet()

    @property
    def epsilon(self):
        return max(0, self.eps_start - self.n_games * self.eps_decay_per_game)

    def get_action(self, state):
        """
        Politique epsilon-greedy :
          - avec proba epsilon : action aleatoire (exploration)
          - sinon              : argmax du reseau (exploitation)
        Retourne un vecteur one-hot de taille 3.
        """
        action = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            move = int(torch.argmax(q_values).item())
        action[move] = 1
        return action
