import pygame
import numpy as np
import sys

class AutonomousVehicleEnvGUI:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Autonomous Vehicle Environment")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def draw(self, vehicle_position, target_position):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.screen_width / 2 - 5, 0, 10, self.screen_height))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(vehicle_position * 100 + self.screen_width / 2), self.screen_height // 2), 10)
        pygame.draw.circle(self.screen, (0, 255, 0), (int(target_position * 100 + self.screen_width / 2), self.screen_height // 2), 10)
        pygame.display.flip()

    def run(self, env):
        running = True
        obs = env.reset()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            action = env.action_space.sample()
            obs, reward, done, _ = env.step(action)
            self.draw(obs[0], obs[2])
            self.clock.tick(60)

            if done:
                obs = env.reset()

if __name__ == "__main__":
    env_gui = AutonomousVehicleEnvGUI()
    env = AutonomousVehicleEnv()

    env_gui.run(env)
