from pygame import *
from random import randint, random, choice



init()
font.init()

font1 = font.Font(None, 50)
win = font1.render('U WIN', True, (230, 50, 10))
lose = font1.render('U LOSE >:[', True, (50, 200, 10))

score = 0
scores = font1.render('Your score:', True, (129, 200, 60))



goal = 15 
skipped = 0 
skipped_str = font1.render("Skipped UFO's:", True, (78, 130, 10))

max_skipped = 8




clock = time.Clock()

scr_w = 1700
scr_h = 1000


#-----------------------------Создание окна
screen = display.set_mode((scr_w, scr_h))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(1700, 1000))
bg = transform.scale(image.load('sc_game_bg.jpg'),(1700, 1000))
screen.blit(background, (0, 0))
#-----------------------------------------GAMEMUSIC
mixer.init()
mixer.music.load("space.mp3")
mixer.music.play()
mixer.music.set_volume(0.1)
bullet_sound = mixer.Sound('shoot_sound.mp3')
peek_sound = mixer.Sound('peek.mp3')
agrsound = mixer.Sound('bossscream.mp3')
gameover_m = mixer.Sound('lose.wav')
#-----------------------------------------------------GAME T or F
game = True
finish = False
#------------------------------------------------------- class gamesprite

def print_text(message, x, y, font_color=(0, 0, 0), font_type='shrift.ttf', font_size=50):
    font_type = font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.btn_color = (165, 42, 42)
        self.btn_color1 = (128, 0, 0)
    
    def draw(self, x, y, message, action=None, font_size=100):
        mouse1 = mouse.get_pos()
        click = mouse.get_pressed()

        if x < mouse1[0] + self.width and y < mouse1[1] < y + self.height:
            draw.rect(screen, self.btn_color1, (x, y, self.width, self.height))
            if click[0] == 1:
                peek_sound.play()
                time.delay(300)
                if action is not None:
                    if action == quit:
                        quit()
                    else:
                        action()

        else:
            draw.rect(screen, self.btn_color, (x, y, self.width, self.height))
            

        print_text(message, x + 30, y + 40)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_speed, dirx, diry, size_x, size_y):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = dirx
        self.rect.y = diry

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Boss(sprite.Sprite):
    def __init__(self, player_image,player_speed, dirx, diry, size_x, size_y, health):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = dirx
        self.rect.y = diry
        self.health = 30
        self.shooted = False

    def attack(self,ast):
        ast.reset()

    def update(self):
        if self.rect.y < -50:
            self.rect.y += self.speed
    
    def logic(self):
        if self.health == 30 or self.health == 25 or self.health == 20 or self.health == 15 or self.health == 10 or self.health == 5:
            # asteroid = Asteroid('asteroid.png', 3,770, 0, 130, 130, randint(0,1), 3)
            # self.attack(asteroid)
            return True
            
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self, x):
        self.rect.centerx = x
        
        keys = key.get_pressed()
        
        # if keys[K_a] and self.rect.x > 5:
        #     self.rect.x -= self.speed
        # elif keys[K_d] and self.rect.x < scr_w - 80:
        #     self.rect.x += self.speed
    


    def fire(self):
        bullet = Bullet('bullet.png', 30, self.rect.centerx, self.rect.top, 30, 50)
        bullets.add(bullet)
        
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=  self.speed
        global skipped
        if self.rect.y >  scr_h:
            self.rect.x =  randint(80, scr_w - 80)
            self.rect.y = 0
            skipped = skipped + 1

class Space_ships(GameSprite):
    def update(self):
        self.rect.y -=  self.speed
        if self.rect.y >  scr_h:
            self.rect.y += 100

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed - 10
        if self.rect.y < 0:
            self.kill()

class Asteroid(sprite.Sprite):
    def __init__(self, player_image,player_speed, dirx, diry, size_x, size_y, direction, health):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = dirx
        self.rect.y = diry
        self.direction = direction 
        self.health = health
    
    def update(self):
        if self.direction == 0:
            self.rect.x += self.speed + randint(15, 25)
            self.rect.y += self.speed 
        elif self.direction == 1:
            self.rect.x -= self.speed + randint(15,25)
            self.rect.y += self.speed 
    def update2(self):
        if self.rect.x < 5:
            self.direction = 0
        elif self.rect.x >= 1600:
            self.direction = 1

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


posY = randint(-800, -500)

def show_menu():
    menu_bg = transform.scale(image.load('menu_bg.png'),(1700, 1000))
    show = True

    start_btn = Button(500, 150)
    quit_btn = Button(500, 150)

    
    while show:
        keys = key.get_pressed()

        for events in event.get():
            if events.type == QUIT:
                quit()
                break
            elif keys[K_u] and keys[K_p]:
                secret_game()
                show = False
                
        
        screen.blit(menu_bg, (0, 0))
        start_btn.draw(500, 300, 'START NEW GAME', start_game, font_size=50)
        quit_btn.draw(500, 600, '             QUIT', quit, font_size=50)

        display.flip()
        clock.tick(90)





# bullet = Bullet('bullet.png', player.rect.x, player.rect.y, 8)


bullets = sprite.Group()


def start_game():
    global game, score, scores, skipped, posY

    score, skipped = 0, 0

    player = Player('rocket.png', 15, 600, 690, 100, 110)
    

    imgs = ['ufo.png','ufo2.png']

    
    monsters = sprite.Group()
    
    for i in range(1, 8):
        img_enemy = choice(imgs)
        monster = Enemy(img_enemy, randint(5,10), randint(80, scr_w - 80), posY, 100, 80)
        monsters.add(monster)

    mixer.music.load("space.mp3")
    mixer.music.play()

    game = True
    while game:
        keys = key.get_pressed()
        clock.tick(90)
        
        m_x, m_y = mouse.get_pos()      

        left, middle, right = mouse.get_pressed()
        

        skipped1 = font1.render(str(skipped), True, (100, 50, 10))
        score_str = font1.render(str(score), True, (100, 50, 10))
        for events in event.get():
            if events.type == QUIT:
                game = False
            elif events.type == MOUSEBUTTONDOWN:
                mouse_presses = mouse.get_pressed()
                if mouse_presses[0]:
                    bullet_sound.play()
                    player.fire()
            elif keys[K_f] :
                start_game()
            
                    
        collides = sprite.groupcollide(bullets, monsters, True, True ) 
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(1,7), randint(80, scr_w - 80), randint(-90, 50), 100, 80)
            monsters.add(monster)
            print(score)
        
                    

            
        keys = key.get_pressed()
        screen.blit(background,(0, 0))
        
        player.update(m_x)

        monsters.update()
        bullets.update()
        

        player.reset()
        monsters.draw(screen)
        
        
        bullets.draw(screen)

        screen.blit(scores, (50, 50))
        screen.blit(score_str, (250, 50))
        screen.blit(skipped_str, (50, 100))
        screen.blit(skipped1, (310, 100))

        if skipped >= max_skipped:
            screen.blit(lose, (800, 500))
            mixer.music.stop()
            display.update()
            time.delay(2000)
            show_menu()
            game = False
            
        if score >= 30:
            screen.blit(win, (800, 500))
            display.update()
            time.delay(600)

            boss_fight()
            game = False
            display.update()
            
            
        display.update()



def secret_game():
    player_s = Player('чикаа.png', 5, 15, 500, 70, 80)

    q, w, e = 350, 500, 650
    sides = [q,w,e]

    s_ships = sprite.Group()
    for i in range(1,7):
        
        ship_s = Space_ships('ship_s.png',4,randint(400, 900),1000,86,64)
        s_ships.add(ship_s)
    

    s_game = True
    while s_game:
        up, down = 0, 0

        for events in event.get():
            if events.type == QUIT:
                show_menu()
                s_game = False
        
        
         
        keys = key.get_pressed()

        
        if up == 0:    
            if keys[K_w] and player_s.rect.x > 5:
                up = 1
                player_s.rect.y -= player_s.speed
        
        if down == 0:
            if keys[K_s] and player_s.rect.x < scr_w - 80:
                down = 1
                player_s.rect.y += player_s.speed
        
        screen.blit(bg,( 0, 0))

        s_ships.update()

        player_s.reset()
        s_ships.draw(screen)

        display.update()

def boss_fight():
    global asteroid

    font2 = font.Font(None, 50)
    skipped_ast = 0
    skipped_ast_str = font2.render('skipped asteroids:',True, (0, 215, 150))
    

    player = Player('rocket.png', 15, 600, 690, 100, 110)
    asteroid = Asteroid('asteroid.png', 3,770, 0, 130, 130, randint(0,1), 5)
    
    r_hand_boss = Boss('right_t.png', 5, 400, -300, 200, 600, 15)
    l_hand_boss = Boss('left_t.png', 5, 1000, -300, 200, 600, 15)
    
    

    fight = True
    while fight:
        clock.tick(90)
        skipped_str = font2.render(str(skipped_ast),True, (0, 215, 150))

        m_x, m_y = mouse.get_pos()      

        left, middle, right = mouse.get_pressed()

        for events in event.get():
            if events.type == QUIT:
                show_menu()
                fight = False

            elif events.type == MOUSEBUTTONDOWN:
                mouse_presses = mouse.get_pressed()
                if mouse_presses[0]:
                    bullet_sound.play()
                    player.fire()
        
        if asteroid is not None:
            allbullets = bullets.sprites()
            for _bullet in allbullets:
                try:
                    if sprite.collide_circle(asteroid ,_bullet):
                        asteroid.health -= 1
                        bullets.remove(_bullet)
                    
                    if asteroid.health <= 0:
                        del asteroid
                        asteroid = None
                        r_hand_boss.shooted = False
                except Exception as e:
                    print(f'Bag: {e}')

        screen.blit(background,(0, 0))
        
        player.update(m_x)
        bullets.update()

        

        if skipped_ast == 3:
            fight = False
            mixer.music.stop()
            gameover_m.play()
            show_menu()

        if r_hand_boss.logic() and not r_hand_boss.shooted:
            agrsound.play()
            asteroid = Asteroid('asteroid.png', 3,770, 0, 130, 130, randint(0,1), 5)
            r_hand_boss.shooted = True
        if asteroid.rect.y > 800:
            skipped_ast += 1
            del asteroid
            asteroid = None
            r_hand_boss.shooted = False

        # allbullets = bullets.sprites()
        # for _bullet in allbullets:
        #     if sprite.collide_circle(asteroid ,_bullet):
        #         r_hand_boss.health -= 1
        #         bullets.remove(_bullet)

        screen.blit(skipped_ast_str, (10, 100))
        screen.blit(skipped_str, (330, 100))

        if asteroid is not None:
            asteroid.update()
            asteroid.update2()
        

        r_hand_boss.logic()
        l_hand_boss.logic()
        r_hand_boss.update()
        l_hand_boss.update()


        player.reset()
        if asteroid is not None:
            asteroid.reset()
        r_hand_boss.reset()
        l_hand_boss.reset()
        
        bullets.draw(screen)

        display.update()
    
show_menu()


