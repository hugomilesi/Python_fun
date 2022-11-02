import pygame
import sys
import asyncio
import time
from constants import *
from sprites import BG, Ground, Plane, Spikes

#Game Variables
high_score = 0
score = 0

class Game:
    def __init__(self):

        #Start the screen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #handles game over
        self.active = True
        #title
        pygame.display.set_caption('Tappy Plane')
        self.clock = pygame.time.Clock()                             #Sets the framerate
        self.game_font = pygame.font.Font('Font/kenvector_future_thin.ttf' ,40)
        
        #get scale factor
        bg_height = pygame.image.load('PNG/background.png').get_height() #480 px
        
        self.scale_factor = HEIGHT/bg_height
        

        #LOAD SPRITES
        self.all_sprites = pygame.sprite.Group()
        # for masks
        self.collision_sprites = pygame.sprite.Group()
        
        #sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor/1.8)
         
       # TIME BETWEEN SPAWNS
        self.spike_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spike_timer, 1400) 
    
        #text
        self.font = pygame.font.Font('Font/kenvector_future.ttf', 30)
        self.score = 0
        self.start_offset = 0
        
        #sounds
        self.music = pygame.mixer.Sound('sounds/RetroRide.wav')
        self.music.play(loops = -1)
        self.death = pygame.mixer.Sound('sounds/hit.mp3')
        
        #menu
        self.menu_surf = pygame.image.load('PNG/UI/textGameOver.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WIDTH/2, HEIGHT/2))
      
    def collisions(self):
            #pygame method to handle collisions 
                # first param is the main object(the plane) we want to check for collision
                
                # second param are the enviroment
                
                # the third checks if the plane has collided with one of the environ-
                #ment sprites, since we want to collide with everything, we define as 
                #False.
            if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False,
                                           pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
                self.death.play()
                #removes spike spawning
                for spikes in self.collision_sprites.sprites():
                    if spikes.sprite_type == 'spikes':
                        spikes.kill()
                        
                self.active = False #game over
                self.plane.kill()
       
    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            score_surf = self.font.render(str(self.score), True, 'Black')
            score_rect = score_surf.get_rect(midtop = (WIDTH/2, HEIGHT/10))
            self.screen.blit(score_surf, score_rect)
            
        else: #stop score count
            #position below menu
            y = HEIGHT/2 + 50
            
            score_surf = self.font.render(f"Your score: {str(self.score)}", True, 'Black')
            score_rect = score_surf.get_rect(midtop = (WIDTH/2, y))
            self.screen.blit(score_surf, score_rect)
        
    
    async def run(self):
        last_time = time.time() 
        while True:
            
            #for update() method
            dt = time.time() - last_time
            last_time = time.time()
        
   #---------------------------------Events handler--------------------------------- 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.active:
                        self.plane.fly()
                    elif event.key == pygame.K_SPACE and not self.active:
                        self.plane = Plane(self.all_sprites, self.scale_factor/2)
                        self.start_offset = pygame.time.get_ticks()
                        self.active = True
                        
                        
                # spike spawns event        
                if event.type == self.spike_timer and self.active:
                    # multiply the scale factor to make the spikes bigger
                    Spikes([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)
#-------------------------------------------------------------------------------------            
            
            self.screen.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.display_score()
            
            if self.active: 
                self.collisions()  
            else:
                self.screen.blit(self.menu_surf, self.menu_rect) 

            pygame.display.update()
            await asyncio.sleep(0)
            self.clock.tick(FRAMERATE)
if __name__ == '__main__':
    game = Game()
    #game.run()
    asyncio.run(game.run())





    
    
    