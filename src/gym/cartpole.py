import gym
from gym import spaces
import numpy as np

class AutonomousVehicleEnv(gym.Env):
    def __init__(self):
        super(AutonomousVehicleEnv, self).__init__()
        
        # Define action space (e.g., steering angle)
        self.action_space = spaces.Discrete(3)  # Example: left, straight, right
        
        # Define observation space (e.g., position, velocity, etc.)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(3,))
        
        # Define initial state
        self.reset()
    
    def reset(self):
        # Reset the environment to initial state
        self.vehicle_position = 0
        self.vehicle_velocity = 0
        self.target_position = np.random.uniform(-1, 1)  # Random target position
        
        # Return initial observation
        return np.array([self.vehicle_position, self.vehicle_velocity, self.target_position])
    
    def step(self, action):
        # Execute action (e.g., adjust steering angle)
        # Update vehicle state (e.g., position, velocity)
        self.vehicle_position += self.vehicle_velocity
        self.vehicle_velocity += action  # Example: acceleration
        
        # Calculate reward based on distance to target
        reward = -np.abs(self.vehicle_position - self.target_position)
        
        # Check if episode is done (e.g., vehicle reaches target or goes out of bounds)
        done = abs(self.vehicle_position - self.target_position) < 0.1
        
        # Return next observation, reward, done flag, and additional info
        next_observation = np.array([self.vehicle_position, self.vehicle_velocity, self.target_position])
        return next_observation, reward, done, {}
    
    def render(self, mode='human'):
        # Visualize the environment (optional)
        pass

# Example usage:
env = AutonomousVehicleEnv()
obs = env.reset()
done = False
total_reward = 0

while not done:
    action = env.action_space.sample()  # Random action for demonstration
    obs, reward, done, _ = env.step(action)
    total_reward += reward
    print("Observation:", obs)
    print("Reward:", reward)
    print("Total Reward:", total_reward)
    print("---")

print("Episode finished. Total reward:", total_reward)
