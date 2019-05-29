import pygame
from pygame.locals import *

class Ship():
    def __init__(self, screen_rect):
        self.ship = pygame.image.load('images/ship.png')
        self.rect = self.ship.get_rect()
        
        self.rect.bottom = screen_rect.bottom
        self.rect.centerx = screen_rect.centerx

        self.x = 0
        self.vel = 10
        
        self.lasers = []
        self.laserCount = 0
        self.maxShot = 3
        self.lenEnemyList = 21

        self.laserSound = pygame.mixer.Sound('sound/laser.wav')
        self.hitSound = pygame.mixer.Sound('sound/hit.wav')
        self.score = 0
        self.shots = 0
        
        

    def movement(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.x = -self.vel   
            elif event.key == K_RIGHT:
                self.x = self.vel
            elif event.key == K_SPACE:
                if len(self.lasers) < self.maxShot:
                    self.lasers.append(Laser(self.rect.centerx, self.rect.top))
                    self.laserSound.play()
                    self.shots += 1
        if event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT): self.x = 0

    def update(self):
        self.rect.x += self.x
        for laser in self.lasers:
            laser.update()

        for i in range(len(self.lasers) - 1, -1, -1):
            if not self.lasers[i].is_alive:
                del self.lasers[i]
                
    def draw(self, screen):
        screen.blit(self.ship, self.rect.topleft)
        for laser in self.lasers:
            laser.draw(screen)

    def collision(self, enemy_list):
        for laser in self.lasers:
            for enemy in enemy_list:
                if pygame.sprite.collide_circle(laser, enemy):
                    self.hitSound.play()
                    if len(enemy_list) < self.lenEnemyList:
                        prem = self.lenEnemyList - len(enemy_list)
                        self.score += 10
                        self.lenEnemyList = len(enemy_list)
                    self.score += 2
                    self.update()
                    laser.is_alive = False
                    enemy.hit()
   
class Laser():
    def __init__(self, x, y):
        self.laser = pygame.image.load('images/laser.png')
        self.rect  = self.laser.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.is_alive = True

    def update(self):
        self.rect.y -= 8
        if self.rect.y < 0: self.is_alive = False
        
    def draw(self, screen):
        screen.blit(self.laser, self.rect.topleft)



class Enemy():
    def __init__(self, x, y, group = None):
        if group is 1:
            self.enemies = [pygame.image.load('level_1/enemy_1.png'),
                            pygame.image.load('level_1/enemy_1.png'),
                            pygame.image.load('level_1/enemy_2.png'),
                            pygame.image.load('level_1/enemy_2.png'),
                            pygame.image.load('level_1/enemy_3.png'),
                            pygame.image.load('level_1/enemy_3.png'),
                            pygame.image.load('level_1/enemy_4.png'),
                            pygame.image.load('level_1/enemy_4.png'),
                            pygame.image.load('level_1/enemy_1.png')]
            self.health = 1
            self.vel = 4
        elif group is 2:
            self.enemies = [pygame.image.load('level_2/enemy_1.png'),
                            pygame.image.load('level_2/enemy_1.png'),
                            pygame.image.load('level_2/enemy_2.png'),
                            pygame.image.load('level_2/enemy_2.png'),
                            pygame.image.load('level_2/enemy_3.png'),
                            pygame.image.load('level_2/enemy_3.png'),
                            pygame.image.load('level_2/enemy_4.png'),
                            pygame.image.load('level_2/enemy_4.png'),
                            pygame.image.load('level_2/enemy_1.png')]
            self.health = 5
            self.vel = 3
        elif group is 3:
            self.enemies = [pygame.image.load('level_3/enemy_1.png'),
                            pygame.image.load('level_3/enemy_1.png'),
                            pygame.image.load('level_3/enemy_2.png'),
                            pygame.image.load('level_3/enemy_2.png'),
                            pygame.image.load('level_3/enemy_3.png'),
                            pygame.image.load('level_3/enemy_3.png'),
                            pygame.image.load('level_3/enemy_4.png'),
                            pygame.image.load('level_3/enemy_4.png'),
                            pygame.image.load('level_3/enemy_1.png')]
            self.health = 10
            self.vel = 2
        
        self.rect = self.enemies[0].get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.hitbox = [x - 25, y - 5, 0, 0]

        self.is_alive = True
        self.animeCount = 0
        self.stop = False
        

        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.textDefeat = self.font.render('LOSS', True, (0, 255, 0))
        self.textDefeatRect = self.textDefeat.get_rect()   
    
    def update(self):
        if self.rect.y > 400:
            self.stop = True
            
        elif not self.stop:
            if self.vel > 0:
                if self.rect.x < 700:
                    self.rect.x += self.vel
                    self.hitbox[0] += self.vel
                else:
                    self.vel = self.vel * -1
                    self.rect.y += 50
                    self.hitbox[1] += 50
                    self.animeCount = 0
            else:
                if self.rect.x > 10:
                    self.rect.x += self.vel
                    self.hitbox[0] += self.vel
                else:
                    self.vel = self.vel * -1
                    self.rect.y += 50
                    self.hitbox[1] += 50
                    self.animeCount = 0

    def draw(self, screen):
        if not self.stop:
            if self.animeCount + 1 >= 27:
                self.animeCount = 0

            if self.vel > 0:
                screen.blit(self.enemies[self.animeCount // 3], self.rect.topleft)
                self.animeCount += 1
            else:
                screen.blit(self.enemies[self.animeCount // 3], self.rect.topleft)
                self.animeCount += 1
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 5))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 5))
        else:
            screen.blit(self.textDefeat, self.textDefeatRect)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.is_alive = False

        
class Game():
    def __init__(self):
        pygame.init()
        
        width, height = 800, 500
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Space Invaders")
        
        pygame.mouse.set_visible(False)

        self.ship = Ship(self.screen.get_rect())
        
        self.fontScore = pygame.font.SysFont('comicsans', 25, True)
        self.textScore = self.fontScore.render('Score: ' + str(0), 1, (0, 255, 128))
        self.score = 0
        self.shots = 0

        self.music = pygame.mixer.music.load('sound/music1.wav')
        pygame.mixer.music.play(-1)
        
        self.enemiesFirstGroup = []
        self.enemiesSecondGroup = []
        self.enemiesThirdGroup = []
        self.first = False
        self.second = False
        self.third = True
        
        for row in 20, 120, 220:
            for column in 20, 120, 220, 320, 420, 520, 620:
                self.enemiesFirstGroup.append(Enemy(column, row, 1))
        for row in 20, 120, 220:
            for column in 20, 120, 220, 320, 420, 520, 620:
                self.enemiesSecondGroup.append(Enemy(column, row, 2))
        for row in 20, 120, 220:
            for column in 20, 120, 220, 320, 420, 520, 620:
                self.enemiesThirdGroup.append(Enemy(column, row, 3))
  
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.text_paused = self.font.render('PAUSED', True, (0, 255, 0))
        self.text_paused_rect = self.text_paused.get_rect(center = self.screen.get_rect().center)

        self.background = pygame.image.load('images/background.jpg')
    
        self.clock = pygame.time.Clock()
        self.score = 0
        self.run()
        self.sound()


    def sound(self):
        laserSound = pygame.mixer.Sound('sound/laser.wav')
        hitSound = pygame.mixer.Sound('sound/hit.wav')
        music = pygame.mixer.music.load('sound/music.wav')
        pygame.mixer.music.play(-1)

        
    def run(self):
        RUNNING = True
        PAUSED = False
        
        while RUNNING:
            self.clock.tick(27)

            for event in pygame.event.get():
                if event.type is pygame.QUIT: RUNNING = False
                    
                if event.type is KEYDOWN:
                    self.keys = pygame.key.get_pressed
                    if event.key is K_ESCAPE:
                        RUNNING = False
                    if event.key is K_p:
                        PAUSED = not PAUSED
                
                if not PAUSED:
                    self.ship.movement(event)

            if not PAUSED:
                self.ship.update()
                
                
                if len(self.enemiesFirstGroup) is 0:
                    self.first = False
                    self.second = True
                if len(self.enemiesSecondGroup) is 0:
                    self.second = False
                    self.third = True

                # 1 LEVEL
                if self.first:
                    for enemy1 in self.enemiesFirstGroup:
                        enemy1.update()
                # 2 LEVEL 
                if self.second:
                    for enemy2 in self.enemiesSecondGroup:
                        enemy2.update()
                # 3 LEVEL       
                if self.third:
                    for enemy3 in self.enemiesThirdGroup:
                        enemy3.update()
                
                if self.first: self.ship.collision(self.enemiesFirstGroup)
                if self.second: self.ship.collision(self.enemiesSecondGroup)
                if self.third: self.ship.collision(self.enemiesThirdGroup)   
                
                if self.first:
                    for i in range(len(self.enemiesFirstGroup) - 1, -1, -1):
                        if self.enemiesFirstGroup[i].stop:
                            Menu(self.ship.score, self.ship.shots)
                        if not self.enemiesFirstGroup[i].is_alive:
                            del self.enemiesFirstGroup[i]
                if self.second:
                    for j in range(len(self.enemiesSecondGroup) - 1, -1, -1):
                        if self.enemiesSecondGroup[j].stop:
                            Menu(self.ship.score, self.ship.shots)
                        if not self.enemiesSecondGroup[j].is_alive:
                            del self.enemiesSecondGroup[j]
                if self.third:
                    for k in range(len(self.enemiesThirdGroup) - 1, -1, -1):
                        if self.enemiesThirdGroup[k].stop:
                            Menu(self.ship.score, self.ship.shots)
                        if not self.enemiesThirdGroup[k].is_alive:
                            del self.enemiesThirdGroup[k]

                self.screen.blit(self.background, (0, 0))
                self.ship.draw(self.screen)
                
                textScore = self.fontScore.render('Score: ' + str(self.ship.score), 1, (0, 255, 128))
                self.screen.blit(textScore, (705, 480))

                textShots = self.fontScore.render('Shots: ' + str(self.ship.shots), 1, (0, 255, 128))
                self.screen.blit(textShots, (5, 480))
            
            if self.first:
                for enemy1 in self.enemiesFirstGroup:
                    enemy1.draw(self.screen)
            if self.second:
                for enemy2 in self.enemiesSecondGroup:
                    enemy2.draw(self.screen)
            if self.third:
                for enemy3 in self.enemiesThirdGroup:
                    enemy3.draw(self.screen)
                    
            if PAUSED:
                self.screen.blit(self.text_paused, self.text_paused_rect)
            
            pygame.display.update()
        
        pygame.quit()

            

class Menu:
            
    def __init__(self, score = None, shots = None):
        pygame.init()
        width, height = 800, 500
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Space Invaders Menu")
        pygame.mouse.set_visible(False)
        
        self.background = pygame.image.load('images/background.jpg')
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()

        self.ship = Ship(self.screen.get_rect())
        self.score = score
        self.shots = shots

        self.music = pygame.mixer.music.load('sound/music.wav')
        pygame.mixer.music.play(-1)
        if score is not None:
            with open('Space Invaders Tab.txt', 'a', encoding = 'utf-8') as file:
                file.write('\n# - - - - - - - - - - - - - - - - - - - - #\n')
                file.write(f'Score {self.score}\n')
                file.write(f'Shots  {self.shots}\n')
                file.write('\n# - - - - - - - - - - - - - - - - - - - - #\n')
                    
                
                
        
        self.font = pygame.font.SysFont('comicsans', 50, True)
        self.fontMovement = pygame.font.SysFont('comicsans', 30, True)
        self.fontScore = pygame.font.SysFont('comicsans', 20, True)
        
        # START
        self.textStart = self.font.render('START', True, (0, 255, 0))
        self.textStartRect = (55, 55, 155, 60)
        # HELP
        self.textHelp = self.font.render('HELP', True, (0, 255, 0))
        self.textHelpRect = (325, 55, 155, 60)
        # HELP TEXT
        self.handling = False
        self.textHandlingMovement = self.fontMovement.render('MOVEMENT:  <- LEFT KEY : RIGHT KEY ->', True, (0, 255, 0))
        self.textHandlingFire = self.fontMovement.render('FIRE:                     SPACEBAR', True, (0, 255, 0))
        self.textHandlingPause = self.fontMovement.render('PAUSE:                       P', True, (0, 255, 0))
        self.textHandlingQuit = self.fontMovement.render('QUIT:                        ESC', True, (0, 255, 0))        
        self.textHandlingMovementRect = (150, 150)
        self.textHandlingFireRect = (150, 175)
        self.textHandlingPauseRect = (150, 200)
        self.textHandlingQuitRect = (150, 225)
        # EXIT
        self.textExit = self.font.render('EXIT', True, (0, 255, 0))
        self.textExitRect = (585, 55, 155, 60)
        # SCORE
        self.textScore = self.fontScore.render('LAST SCORE: ' + str(self.score), True, (0, 255, 0))
        self.textScoreRect = (150, 250)
        self.textShots = self.fontScore.render('LAST SHOTS FIRED: ' + str(self.shots), True, (0, 255, 0))
        self.textShotsRect = (150, 270)
        
        self.run()
        
        
    def run(self):
        RUNNING = True
        PAUSED = False
       
        while RUNNING:
            self.clock.tick(27)
 
            for event in pygame.event.get():
                if event.type is pygame.QUIT: RUNNING = False
                   
                if event.type is KEYDOWN:
                    self.keys = pygame.key.get_pressed
                    if event.key is K_ESCAPE:
                        RUNNING = False
                    if event.key is K_p:
                        PAUSED = not PAUSED
               
                if not PAUSED:
                    self.ship.movement(event)


                    
            self.screen.blit(self.background, (0, 0))
            # START
            self.screen.blit(self.textStart, self.textStartRect)
            pygame.draw.rect(self.screen, (0, 255, 128), (40, 40, 155, 60), 5)

            if len(self.ship.lasers) > 0:
                if  40 < self.ship.lasers[0].rect.centerx < 200:
                    if self.ship.lasers[0].rect.centery < 115:
                        Game()
                    
            # HELP
            self.screen.blit(self.textHelp, self.textHelpRect)
            pygame.draw.rect(self.screen, (0, 255, 128), (300, 40, 155, 60), 5)
            if len(self.ship.lasers) > 0:
                if 300 < self.ship.lasers[0].rect.centerx < 460:
                    if self.ship.lasers[0].rect.centery < 115:
                        if not self.handling:
                            self.ship.lasers[0].is_alive = False
                            self.handling = True
                        else:
                            self.ship.lasers[0].is_alive = False
                            self.handling = False
                                   
            # EXIT
            self.screen.blit(self.textExit, self.textExitRect)
            pygame.draw.rect(self.screen, (0, 255, 128), (560, 40, 155, 60), 5)
            if len(self.ship.lasers) > 0:
                if 560 < self.ship.lasers[0].rect.centerx < 720:
                    if self.ship.lasers[0].rect.centery < 115:
                        RUNNING = False
                    

            
            if self.handling:
                self.screen.blit(self.textHandlingMovement, self.textHandlingMovementRect)
                self.screen.blit(self.textHandlingFire, self.textHandlingFireRect)
                self.screen.blit(self.textHandlingPause, self.textHandlingPauseRect)
                self.screen.blit(self.textHandlingQuit, self.textHandlingQuitRect)

            if self.shots is not None or self.score is not None:
                self.screen.blit(self.textScore, self.textScoreRect)
                self.screen.blit(self.textShots, self.textShotsRect)
                
            self.ship.update()
            self.ship.draw(self.screen)

            pygame.display.update()
                        
       
        pygame.quit()
                
            
                    
if __name__ == '__main__':
    Menu()
    

