import pygame
from constants import *
from random import randint, choice

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        #background
        bg_image = pygame.image.load('PNG/background.png').convert()
        
        #using scale factor to fit the background
        full_height = bg_image.get_height() * scale_factor
        full_width  = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
    
        #background
        self.image = pygame.Surface((full_width * 2,full_height))  
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))
          
          
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
    def update(self, dt):
        """Delta Time make fps smoother"""
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0: #if image gets out of the screen
            self.pos.x = 0 
        self.rect.x = round(self.pos.x)
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'
        
        #floor
        ground_surf = pygame.image.load('PNG/ground.png').convert_alpha()
        #width = 1346
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        
        #position
        self.rect=self.image.get_rect(bottomleft = (0, HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)
       
        #mask
        # mask makes a kind of outline around the pixel image, making the hitbox more
        #precise 
        self.mask = pygame.mask.from_surface(self.image)
        
        
        
    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        
        self.rect.x = round(self.pos.x)
    
class Plane(pygame.sprite.Sprite):
    def __init__(self, groups,scale_factor):
        super().__init__(groups)
        
        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
        #rect
        self.rect = self.image.get_rect(midleft = (WIDTH/20, HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        #movements
        self.gravity = 750
        self.direction = 0
        
        #sounds
        self.fly_sound = pygame.mixer.Sound('sounds/sounds_jump.wav')
        self.fly_sound.set_volume(0.3)
        
        #mask makes a kind of outline around the pixel image, making the hitbox more
        #precise 
        self.mask = pygame.mask.from_surface(self.image)
        
    def import_frames(self, scale_factor):
        self.frames = []
        
        for i in range(1,4):
            #loading the 3 images
            surf = pygame.image.load(f"PNG/Planes/planeYellow{i}.png").convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)             
            self.frames.append(scaled_surface)
    
    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        #gives the falling impression
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
    
    def fly(self):
        self.direction = -300
        self.fly_sound.play()
        
    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.05 , 1)
        self.image = rotated_plane
         #mask makes a kind of outline around the pixel image, making the hitbox more
        #precise 
        self.mask = pygame.mask.from_surface(self.image)
    
    #handle movements and animations
    #the order inside the update function matters
    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Spikes(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'spikes'
        
        orientation = choice(('up', 'down'))
        surf = pygame.image.load(f"PNG/rock{choice(('Snow', 'Ice'))}.png").convert_alpha()
        # escaling
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
        
        # spawn gap
        x = WIDTH + randint(20, 200)
        
        if orientation  == 'up':
            y_upperspike = HEIGHT + randint(40, 100)
            self.rect = self.image.get_rect(midbottom = (x, y_upperspike))    
        else:
            y_downspike = 0 - (randint(40, 100))
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x, y_downspike))
        
        #mask
        # mask makes a kind of outline around the pixel image, making the hitbox more
        #precise 
        self.mask = pygame.mask.from_surface(self.image)

        #tracks sprite position       
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        # spike speed
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        # destroy past spikes
        if self.rect.right <= -100:
            #kill is a method of pygame.sprite, since we're inheriting it, we can use.
            self.kill()

            
            