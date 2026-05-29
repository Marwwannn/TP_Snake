# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (reseau Q + trainer + agent DQN).
import os
import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


MAX_MEMORY = 100_000
BATCH_SIZE = 1000


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
        try:
            self.load_state_dict(torch.load(path))
        except Exception:
            # poids incompatibles avec l'architecture courante
            return False
        self.eval()
        return True


class QTrainer:
    """
    Boucle d'apprentissage Q-learning :
      target = reward                       si done
      target = reward + gamma * max(Q(s'))  sinon
    Loss MSE entre Q(s)[action] et target.
    """

    def __init__(self, model, lr=0.001, gamma=0.9):
        self.model = model
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.long)
        reward = torch.tensor(np.array(reward), dtype=torch.float)

        if state.dim() == 1:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            done = (done,)

        pred = self.model(state)
        target = pred.clone()
        for i in range(len(done)):
            q_new = reward[i]
            if not done[i]:
                q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
            target[i][torch.argmax(action[i]).item()] = q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()


class Agent:
    """
    Agent DQN complet :
      - replay memory (deque max 100k)
      - politique epsilon-greedy
      - train_short_memory (1 transition apres chaque step)
      - train_long_memory (batch 1000 a la fin de chaque partie)
    """

    def __init__(self, eps_start=80, eps_decay_per_game=1, lr=0.001, gamma=0.9):
        self.n_games = 0
        self.eps_start = eps_start
        self.eps_decay_per_game = eps_decay_per_game
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet()
        self.trainer = QTrainer(self.model, lr=lr, gamma=gamma)

    @property
    def epsilon(self):
        return max(0, self.eps_start - self.n_games * self.eps_decay_per_game)

    def get_action(self, state):
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

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
# ##################################################
