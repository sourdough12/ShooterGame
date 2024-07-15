#Create your own shooter

from pygame import *
x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from pygame import *
import time as timer
window_width = 900
window_height = 900
window = display.set_mode((window_width, window_height))

from random import randint, choice

bg = transform.scale( image.load('galaxy.jpg'), (window_width, window_height))
class Character(sprite.Sprite):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y,speed,hp):
        super().__init__()
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.image = transform.scale(image.load(self.filename),(self.size_x,self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.hp = hp
        self.max_hp = hp
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class UFO(Character):
    def update(self):
        self.rect.y += self.speed
        global pass_count
        if self.rect.y > window_height:
            pass_count += 1
            print(pass_count)
            self.respawn()
    def respawn(self):
        self.rect.y = 0
        self.rect.x = randint(100,window_width-100)
        self.speed = randint(5,10)
    def isShot(self):
        global kill_count
        print('UFO is shot')
        self.hp -= 1
        if self.hp <= 0:
            if self.max_hp == 2:
                self.respawn()
                self.hp = self.max_hp
            else:
                self.kill()
            kill_count += 1
class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            #print('Destroy bullet')
class Asteroid(Character):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y,speed,hp):
        self.speed_x = speed * choice([1,-1])
        self.speed_y = speed * choice([1,-1])
        super().__init__(filename,size_x,size_y,pos_x,pos_y,speed,hp)
    def update(self):
        self.rect.y -= self.speed_y
        self.rect.x -= self.speed_x         
        

asteroid_group = sprite.Group()
asteroid_group.add(Asteroid('asteroid.png',50,50, randint(int(window_width/2)-200, int(window_width/2)+200), randint(int(window_height/2)-200,int(window_height/2)+200),2,1))
asteroid_time = timer.time()
asteroid_reload = 2
create_asteroid = True

bullet_group = sprite.Group()
clip_size = 50
bullet_remain = clip_size

player1 = Character('rocket.png',100,100,400,700,8,15)

clock = time.Clock()
fps = 60
font.init()
style = font.SysFont(None,50)

pass_count = 0

game = True
finish = False
ufo_group = sprite.Group()
for i in range(3):
    x = randint(100,window_width-100)
    spd = randint(3,8)
    ufo_type = choice(['ufo.png','ufo1.png'])
    ufo_group.add(UFO(ufo_type,50,75,x,0,spd,2))

last_fire_time = timer.time()
fire_rate = 0.25
reload_time = 2
reloading = False
reload_blink_count = 0
isCreateBoss = True
boss_respawn = 5

kill_count = 0
while game:
    display.update()
    clock.tick(fps)

    window.blit(bg, (0,0)) 
    player1.draw()
    ufo_group.draw(window)
    bullet_group.draw(window)
    asteroid_group.draw(window)

    text_count = style.render('Count:'+str(pass_count),True,(255,255,255))
    window.blit(text_count,(50,100))
    text_hp = style.render('HP:'+str(player1.hp),True,(255,255,255))
    window.blit(text_hp,(750,100))
    text_bullet = style.render('BULLET:'+str(bullet_remain)+'/'+str(clip_size), True, (255,255,255))
    window.blit(text_bullet,(600,200))
    text_kill = style.render('KILL:'+str(kill_count), True, (255,255,255))
    window.blit(text_kill,(600,100))

    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        ufo_group.update()
        bullet_group.update()
        asteroid_group.update()

        key_pressed = key.get_pressed()
        if key_pressed[K_w] and player1.rect.y > 0:
            player1.rect.y -= player1.speed   
        if key_pressed[K_s] and player1.rect.y < window_height-player1.size_y:
            player1.rect.y += player1.speed   
        if key_pressed[K_d] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x += player1.speed 
        if key_pressed[K_a] and player1.rect.x > 0:
            player1.rect.x -= player1.speed
        if key_pressed[K_SPACE] and timer.time() - last_fire_time > fire_rate and bullet_remain > 0 and reloading == False:
            #print('SHOOT')
            bullet_group.add(Bullet('bullet.png',25,25,player1.rect.x,player1.rect.y,20,10))
            bullet_remain -= 1
            last_fire_time = timer.time()
        if key_pressed[K_r]:
            reloading = True
            start_reload_time = timer.time()
            
        if reloading == True:
            if timer.time() - start_reload_time > reload_time:
                bullet_remain = clip_size
                reloading = False
            else:
                if reload_blink_count < 20:
                    text_reload = style.render('Reloading...',True, (255,255,255))
                elif reload_blink_count < 40:
                    text_reload = style.render('',True,(255,255,255))
                else:
                    reload_blink_count = 0
                reload_blink_count += 1
                window.blit(text_reload,(300,200))


       

        collide_list = sprite.spritecollide(player1,ufo_group,False)
        for collided_ufo in collide_list:
            if collided_ufo.max_hp == 2:
                collided_ufo.respawn()  
                player1.hp -= 1
            else:
                collided_ufo.kill()
                player1.hp -= 2
                


        collide_dictionary = sprite.groupcollide(bullet_group,ufo_group,True,False)
        for colllided_bullet in collide_dictionary.keys():
            ufo_list = collide_dictionary[colllided_bullet]
            hit_ufo = ufo_list[0]
            hit_ufo.isShot()

        #win condition
        if kill_count >= 20:
            finish = True
        if player1.hp <= 0:
            finish = True

        #special event
        if kill_count == boss_respawn:
            if isCreateBoss == True:
                ufo_group.add(UFO('ufo_boss.png',100,125,x,0,spd,5))
                isCreateBoss = False
                boss_respawn += 5
            else: 
                isCreateBoss = True

        if timer.time() - asteroid_time  > asteroid_reload:
            if create_asteroid == True:
                asteroid_group.add(Asteroid('asteroid.png',50,50, randint(int(window_width/2)-200, int(window_width/2)+200), randint(int(window_height/2)-200,int(window_height/2)+200),2,1))
                create_asteroid = False
                asteroid_reload += 2
            else:
                create_asteroid = True


    else:
        if player1.hp > 0:
            text_result = style.render('YOU WIN', True,(255,255,255))
        else:
            text_result = style.render('YOU LOSE', True,(255,255,255))
        window.blit(text_result, (200,200))      

# class Wall(Character):
#     def __init__(self,size_x,size_y,pos_x,pos_y):
#         self.size_x = size_x
#         self.size_y = size_y
#         self.pos_x = pos_x
#         self.pos_y = pos_y
#         self.image = Surface((size_x, size_y))
#         self.image.fill((212, 17, 17))
#         self.rect = self.image.get_rect()
#         self.rect.x = pos_x
#         self.rect.y = pos_y


# player1 = Character('cyborg.png',50, 50, 600, 200, 8)
# player2 = Character('hero.png',50,50,300,300,5)
# treasure = Character('treasure.png',75,75,800,600,0)

# #w1 = Wall(50,300,100,100)
# #w2 = Wall(50,150,300,100)
# #w3 = Wall(50,300,500,100)

# wall_list = []
# wall_list.append(Wall(30,300,100,100))
# wall_list.append(Wall(300,30,100,400))
# wall_list.append(Wall(300,30,400,400))
# wall_list.append(Wall(30,300,670,100))
# wall_list.append(Wall(300,30,670,70))
# wall_list.append(Wall(30,150,300,400))
# wall_list.append(Wall(30,200,500,500))

# route_list = [(200,200),(500,500),(300,500),(600,500)]
# route = 0
# for i in range(6):
#     #x = random.randint(0,window_width/5)*5
#     #y = random.randint(0,window_width/5)*5
#     x = random.randint(0,window_width)
#     y = random.randint(0,window_height)
#     route_list.append((x,y))
    
# ok_x = False
# ok_y = False
# hp = 3
# font.init()
# style = font.SysFont(None,50)



# game = True
# finish = False
# while game:
#     window.blit(bg, (0,0))
#     for e in event.get():
#         if e.type == QUIT:
#             game = False
    
#     if finish == False:
#         safety_x = player1.rect.x
#         safety_y = player1.rect.y


    
#         for wall in wall_list:
#             isCollide = sprite.collide_rect(player1,wall)
#             if isCollide:
#                 player1.rect.x = safety_x  
#                 player1.rect.y = safety_y
        
#         goto_x, goto_y = route_list[route]
#         if ok_x == False:
#             d = abs(player2.rect.x - goto_x)
#             if player2.rect.x < goto_x:
#                 player2.rect.x += min(player2.speed, d)
#             elif (player2.rect.x > goto_x):
#                 player2.rect.x -= min(player2.speed, d)
#             else:
#                 ok_x = True

#         if ok_y == False:
#             d = abs(player2.rect.y - goto_y)
#             if player2.rect.y < goto_y:
#                 player2.rect.y += min(player2.speed, d)
#             elif player2.rect.y > goto_y:
#                 player2.rect.y -= min(player2.speed, d)
#             else:
#                 ok_y = True


#         if ok_x == True and ok_y == True:
#             route+=1
#             ok_x = False
#             ok_y = False
#             if route == len(route_list):
#                 route = 0


#         isCollide = sprite.collide_rect(player1,player2)
#         if isCollide:
#             hp -= 1
#             player1.rect.x = 600
#             player1.rect.y = 200
#             if hp <= 0:
#                 print('YOU LOSE')
#                 finish = True
#         isCollide_Treasure = sprite.collide_rect(player1,treasure)
#         if isCollide_Treasure:
#             print('YOU WIN')
#             finish = True
#     else:
#         if hp <= 0:
#             text_result = style.render('YOU LOSE', True,(255,255,255))
#         else:
#             text_result = style.render('YOU WIN', True,(255,255,255))
#         window.blit(text_result, (200,200))


#     text_hp = style.render('HP:'+str(hp), True,(255,255,255))
#     window.blit(text_hp, (10,10))

#     player1.show()
#     player2.show()
#     treasure.show()

#     for wall in wall_list:
#         wall.show()


