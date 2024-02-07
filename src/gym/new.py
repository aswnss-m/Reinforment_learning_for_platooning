import numpy as np
import gym
import pygame
from gym import spaces
import hashlib
def hash_state(state):
    state_str = "".join(map(str, state))
    return int(hashlib.sha256(state_str.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

# Custom Platooning Environment
# class PlatooningEnv(gym.Env):
#     def __init__(self, config):
#         self.config = config
#         self.action_space = spaces.Discrete(3)  # 3 possible actions: accelerate, maintain speed, decelerate
#         self.observation_space = spaces.Box(low=0.0, high=100.0, shape=(2,), dtype=np.float32)

#     def reset(self):
#         # Initialize the states
#         self.leader_velocity = self.config['leader_velocity']
#         self.following_distance = self.config['following_distance']
#         self.following_velocity = np.random.uniform(low=self.leader_velocity - 5, high=self.leader_velocity + 5)
#         return np.array([self.following_distance, self.following_velocity])

#     def step(self, action):
#         # Update the following AV's velocity based on the chosen action
#         if action == 0:  # Accelerate
#             self.following_velocity += self.config['acceleration']
#         elif action == 1:  # Maintain speed
#             pass
#         else:  # Decelerate
#             self.following_velocity -= self.config['acceleration']

#         # Compute the reward
#         reward = -np.abs(self.following_velocity - self.leader_velocity) - np.abs(self.following_distance - self.config['desired_distance'])

#         # Update the following AV's distance to the leader
#         self.following_distance += self.following_velocity

#         # Check if the episode is done
#         done = self.following_distance > self.config['max_distance'] or self.following_distance < self.config['min_distance']

#         return np.array([self.following_distance, self.following_velocity]), reward, done, {}
#     def render(self, mode='human'):
#         print(f"Leader Velocity: {self.leader_velocity}, Following Velocity: {self.following_velocity}, Distance: {self.following_distance}")
import pygame
import numpy as np

class PlatooningEnv(gym.Env):
    def __init__(self, config):
        self.config = config
        self.action_space = spaces.Discrete(3)  # 3 possible actions: accelerate, maintain speed, decelerate
        self.observation_space = spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32)
        self.width, self.height = 800, 400
        self.leader_pos = (self.width // 2, self.height // 2)
        self.following_pos = None
        self.leader_velocity = self.config['leader_velocity']
        self.following_distance = self.config['following_distance']
        self.following_velocity = np.random.uniform(low=self.leader_velocity - 5, high=self.leader_velocity + 5)
        self.frame_rate = 60
        self.window = None

        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))

    # def reset(self):
    #     self.following_distance = self.config['following_distance']
    #     self.following_velocity = np.random.uniform(low=self.leader_velocity - 5, high=self.leader_velocity + 5)
    #     self.following_pos = (self.width // 2 - self.following_distance, self.height // 2)
    def reset(self):
        self.following_distance = self.config['following_distance']
        self.following_velocity = np.random.uniform(low=self.leader_velocity - 5, high=self.leader_velocity + 5)
        self.following_pos = (self.width // 2 - self.following_distance, self.height // 2)
        return np.array([self.following_distance, self.following_velocity])

    # def step(self, action):
    #     # Update the following AV's velocity based on the chosen action
    #     if action == 0:  # Accelerate
    #         self.following_velocity += self.config['acceleration']
    #     elif action == 1:  # Maintain speed
    #         pass
    #     else:  # Decelerate
    #         self.following_velocity -= self.config['acceleration']

    #     # Compute the reward
    #     reward = -np.abs(self.following_velocity - self.leader_velocity) - np.abs(self.following_distance - self.config['desired_distance'])

    #     # Update the following AV's distance to the leader
    #     self.following_distance += self.following_velocity

    #     # Check if the episode is done
    #     done = self.following_distance > self.config['max_distance'] or self.following_distance < self.config['min_distance']

    #     return np.array([self.following_distance, self.following_velocity]), reward, done, {}
    def step(self, action):
        if action == 0:  # Accelerate
            self.following_velocity += self.config['acceleration']
        elif action == 1:  # Maintain speed
            pass
        else:  # Decelerate
            self.following_velocity -= self.config['acceleration']

        # Update the following AV's distance to the leader
        self.following_distance += self.following_velocity

        # Compute the reward
        reward = -np.abs(self.following_velocity - self.leader_velocity) - np.abs(self.following_distance - self.config['desired_distance'])

        # Check if the episode is done
        done = self.following_distance > self.config['max_distance'] or self.following_distance < self.config['min_distance']

        # Update the following AV's position
        self.following_pos = (self.following_pos[0] + self.following_velocity, self.following_pos[1])

        # Render the environment
        self.render()

        return np.array([self.following_distance, self.following_velocity]), reward, done, {}

    def render(self):
        self.window.fill((0, 0, 0))
        pygame.draw.circle(self.window, (0, 255, 0), self.leader_pos, 10)
        if self.following_pos is not None:
            pygame.draw.circle(self.window, (255, 0, 0), self.following_pos, 10)
        pygame.display.flip()
        pygame.time.Clock().tick(self.frame_rate)

    def close(self):
        pygame.quit()
# Q-learning agent
# class QLearningAgent:
#     def __init__(self, observation_space, action_space):
#         self.Q = np.zeros((observation_space.shape[0], action_space.n))
#         self.lr = 0.1
#         self.gamma = 0.95

#     def update_Q(self, state, action, reward, next_state, done):
#         max_next_Q = np.max(self.Q[tuple(next_state)])
#         self.Q[tuple(state), action] += self.lr * (reward + self.gamma * max_next_Q - self.Q[tuple(state), action])

#     def get_action(self, state):
#         return np.argmax(self.Q[tuple(state.reshape(1, -1))])
class QLearningAgent:
    def __init__(self, observation_space, action_space):
        self.Q = np.zeros((10 ** 8, action_space.n))
        self.lr = 0.1
        self.gamma = 0.95

    def update_Q(self, state, action, reward, next_state, done):
        state_hash = hash_state(state)
        next_state_hash = hash_state(next_state)
        max_next_Q = np.max(self.Q[next_state_hash])
        self.Q[state_hash, action] += self.lr * (reward + self.gamma * max_next_Q - self.Q[state_hash, action])

    def get_action(self, state):
        state_hash = hash_state(state)
        return np.argmax(self.Q[state_hash])
# Train the RL agent
config = {'leader_velocity': 60, 'following_distance': 10, 'desired_distance': 15, 'acceleration': 2, 'max_distance': 100, 'min_distance': 0}
env = PlatooningEnv(config)
state = env.reset()
agent = QLearningAgent(env.observation_space, env.action_space)

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False

    while not done:
        action = agent.get_action(state)
        next_state, reward, done, _ = env.step(action)
        if next_state is not None:
            agent.update_Q(state, action, reward, next_state, done)
        state = next_state
        env.render()

print("Finished training!")