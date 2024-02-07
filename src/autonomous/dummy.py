import gym
from stable_baselines import PPO2
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.callbacks import BaseCallback
from gym.spaces import Box, Discrete
from gym.envs.box2d.car_racing import CarRacing
import numpy as np

class CarRacingEnv(CarRacing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Modify the observation space
        self.observation_space = Box(low=0, high=255, shape=(4, 96, 96), dtype=np.uint8)

        # Modify the action space
        low = np.array([-1, -1, -1])
        high = np.array([+1, +1, +1])
        self.action_space = Discrete(5)
        self.action_map = {
            0: np.array([-0.2, 0.0, 0.0]) * high,
            1: np.array([+0.2, 0.0, 0.0]) * high,
            2: np.array([0.0, -1.0, 0.0]) * high,
            3: np.array([0.0, +1.0, 0.0]) * high,
            4: np.zeros(3) * high,
        }

    def _step(self, action):
        if action == 4:
            action = np.zeros(3) * high
        else:
            action = self.action_map[action]

        return super()._step(action)

class TimeoutCallback(BaseCallback):
    def __init__(self, max_timesteps):
        super().__init__()
        self.max_timesteps = max_timesteps

    def _on_step(self):
        if self.num_timesteps >= self.max_timesteps:
            return True

        return False

def train_model():
    # Create the environment
    env = CarRacingEnv(grayscale=1, discretize_actions="hard", frames_per_state=4)
    env = DummyVecEnv([lambda: env])

    # Initialize the PPO2 algorithm
    model = PPO2(CnnPolicy, env, verbose=1)

    # Add a timeout callback
    model.learn(total_timesteps=1000000, callback=TimeoutCallback(max_timesteps=1000000))

    # Save the trained model
    model.save("car_racing_weights")

train_model()