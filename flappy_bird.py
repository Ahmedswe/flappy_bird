import pygame
import sys 
import random
import os
pygame.init()




class window():
    def __init__(self):
        self.width = 800
        self.height = 550
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.sky = pygame.image.load('images\\Sky.png')
        self.sky = pygame.transform.scale(self.sky,(self.width,500))
        self.ground = pygame.image.load('images\\ground.png')
        self.ground = pygame.transform.scale(self.ground,(830,150))
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.welcome_screen = pygame.image.load("images\\welcome_screen.jpg") 
        self.welcome_screen = pygame.transform.scale(self.welcome_screen,(800,600))
        self.game_over_img = pygame.image.load("images\\game_over.png")
        self.start_button = pygame.image.load(r"images\\start_button.jpg")
        self.start_button = pygame.transform.scale(self.start_button,(80,40))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = [self.width/4,self.height/1.5]
        self.exit_button = pygame.image.load(r"images\\exit.png")
        self.exit_button = pygame.transform.scale(self.exit_button,(40,40))
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.center = [self.width/2.5,self.height/2]
        self.replay_button = pygame.image.load(r"images\\replay.png")
        self.replay_button = pygame.transform.scale(self.replay_button,(40,40))
        self.replay_button_rect = self.replay_button.get_rect()
        self.replay_button_rect.center = [self.width/1.6,self.height/2]
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.SysFont("default",40)
        self.game_over = False
    
    
    
    def display_screen(self):
        pygame.display.update()
        self.clock.tick(30)
       
        self.screen.blit(self.sky,(0,0))
        self.screen.blit(self.ground,(self.ground_scroll,450))
        
        if self.game_over == False:
            self.ground_scroll -= self.scroll_speed
        if abs(self.ground_scroll) > 30:
            self.ground_scroll = 0     
    
    def gameover_and_restart(self):
        if game_screen.game_over == True:
            self.screen.blit(self.game_over_img,(240,130))
            self.screen.blit(self.exit_button,(self.exit_button_rect.topleft))
            self.screen.blit(self.replay_button,(self.replay_button_rect.topleft))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.exit_button_rect.collidepoint(mouse_pos):
                        sys.exit()
                    elif self.replay_button_rect.collidepoint(mouse_pos):
                        bird.rect.center = [game_screen.width/5,game_screen.height/2]
                        self.game_over = False
                        bird.first_flap = False
                        bird.flap = True
                        game_screen.score = 0
                        pipe_group.empty()
                        gameloop()
                        
    def score_and_highscore(self):
        score_text = self.font.render(f"score : {self.score}","black",True)
        self.screen.blit(score_text,(0,0))
        with open("images\\high_score.txt","r+") as file:
            high_score = file.read()
        high_score_text = self.font.render(f"high_score : {high_score}",True,"black")
        self.screen.blit(high_score_text,(598,0))
        if game_screen.score > (int(float(high_score))):
            high_score = game_screen.score
        with open("images\\high_score.txt","w") as file:
            file.write(str(high_score))
        if game_screen.score >= 1.0:
            self.score = int(self.score)
            
game_screen = window()
        
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.counter = 0
        self.first_flap = False
        self.flap = True
        self.velocity = 0
        self.images = [pygame.image.load(f"images\\bird{i}.png") for i in range(1,4)]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
        
    
    def update(self):
        self.image = self.images[self.index]
        cooldown = 7
        self.counter+=1
        if self.counter >= cooldown and game_screen.game_over == False:
            self.counter = 0
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        if self.velocity < 10 and game_screen.game_over == False:
            self.velocity += 0.6
        if self.first_flap == True and game_screen.game_over == False: 
            self.rect.y += self.velocity
        if self.first_flap == True:
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity)
            
        if self.rect.centery <= 0:
            self.rect.centery = 0
            game_screen.game_over = True
        if self.rect.centery >= 430:
            game_screen.game_over = True
        if pygame.sprite.spritecollide(self,pipe_group,False,pygame.sprite.collide_mask):
            game_screen.game_over = True
            
        
    
    def fly(self):
            self.velocity = -8
            self.rect.y += self.velocity
            
            
bird = Bird(100,game_screen.height/2)
bird_group = pygame.sprite.Group()
bird_group.add(bird)
                        
            
    
        
game_screen = window()

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.pass_pipe = False
        self.image = pygame.image.load(("images\pipe.jpg"))
        self.image = pygame.transform.scale(self.image,(40,random.randint(100,200)))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [x,y]
       
        if position == -1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.topleft = [x,y]
    
    def update(self):
        if game_screen.game_over == False:
            self.rect.x -= 4
        if self.rect.x <= -30:
            self.kill()
  

        if self.rect.left == 30 and game_screen.game_over == False:
            game_screen.score += 0.5
          
         
            

    
pipe_group = pygame.sprite.Group() 

def create_pipe():
    if game_screen.game_over == False and bird.first_flap == True:
        top_pipe = Pipe(830,random.randint(-20,0),-1)
        btm_pipe = Pipe(830,450,1)
        pipe_group.add(top_pipe)
        pipe_group.add(btm_pipe)
    

  


  
            
            
            

        

        
        
    
        
        
        
        
def main_menu():
    while True:
        pygame.display.update()
        game_screen.screen.blit(game_screen.welcome_screen,(0,0))
        game_screen.screen.blit(game_screen.start_button,(game_screen.start_button_rect.topleft))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == pygame.BUTTON_LEFT and game_screen.start_button_rect.collidepoint(mouse_pos) or event.button == pygame.BUTTON_RIGHT and game_screen.start_button_rect.collidepoint(mouse_pos):
                    gameloop()
      
def gameloop():
    cooldown = 55
    counter = 56
    while True:
        
        game_screen.display_screen()
        pipe_group.draw(game_screen.screen)
        if counter > cooldown:
            create_pipe()
            counter = 0
        counter += 1
        pipe_group.update()
        game_screen.gameover_and_restart()
        bird_group.draw(game_screen.screen)
        bird_group.update()
        game_screen.score_and_highscore()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_screen.game_over == False and bird.flap == True:
                    bird.first_flap = True
                    bird.fly()
                    bird.flap == False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and game_screen.game_over == False:
                    bird.first_flap = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT or event.button == pygame.BUTTON_RIGHT and game_screen.game_over == False and bird.flap == True:
                    bird.first_flap = True
                    bird.fly()
                    bird.flap = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT or event.button == pygame.BUTTON_RIGHT and game_screen.game_over == False:
                    bird.flap = True
        
        
        
        
main_menu()