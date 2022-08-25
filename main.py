
import sys
sys.dont_write_bytecode = True
#sys.path.append('./')

import pygame

import drivers
import engine
import scene

LocalsVar = locals()

pygame.init()
pygame.display.init()
pygame.font.init()

yaml_file = drivers.yaml.yaml_driver.YamlDriver()
config = yaml_file.read(read_file='data/config.yml')

window = pygame.display.set_mode(config['window_size']) # pygame.RESIZABLE
window_title = pygame.display.set_caption(config['window_title'])
window_icon = pygame.display.set_icon(pygame.image.load(config['window_icon']))
window_clock = pygame.time.Clock()

is_scene = 'game'
scene_list = {
                'game':scene.game.Game(),
            }

RUN = True
while RUN == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        scene_list[is_scene].scene_event(event)
    
    window.fill((0,0,0,0))
    window.blit(scene_list[is_scene].renderer(), (0,0))
    
    pygame.display.update()
    window_clock.tick(config['window_fps'])