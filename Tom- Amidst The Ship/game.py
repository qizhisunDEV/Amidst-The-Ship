from pygame import *
from math import *
from random import *

pX = 1100 
pY = 700
#starting position for player
level = 1
#starting level, change if a skip is needed
wave = 0
#current wave
imposters = [
                [
                [[260, 650, 0, 0], [110, 650, 0, 0], [410, 650, 0, 0], [150, 650, 0, 0], [510, 650, 0, 0], [450, 650, 0, 0], [610, 650, 0, 0]],
                 [[280, 650, 0, 0], [360, 650, 0, 2], [520, 650, 0, 2], [490, 650, 0, 0], [620, 650, 0, 0], [560, 650, 0, 0]],
                 [[220, 650, 0, 2], [310, 650, 0, 0], [430, 650, 0, 2], [620, 650, 0, 0], [570, 650, 0, 0]],
                 [[250, 650, 0, 0], [330, 650, 0, 2], [570, 650, 0, 3], [500, 650, 0, 0]],
                [[190, 650, 0, 2], [110, 650, 0, 0], [390, 650, 0, 3], [210, 250, 0, 5], [150, 320, 0, 5]],
                 [[210, 650, 0, 2], [340, 650, 0, 2], [490, 650, 0, 0], [530, 650, 0, 0], [590, 650, 0, 0], [650, 650, 0, 0], [110, 280, 0, 5]],
                 [[240, 650, 0, 3], [320, 650, 0, 2], [430, 650, 0, 2], [630, 650, 0, 0], [560, 650, 0, 0], [250, 250, 0, 5], [530, 340, 0, 5]],
                 [[250, 650, 0, 2], [310, 650, 0, 3], [520, 650, 0, 3], [570, 650, 0, 0], [510, 650, 0, 0], [450, 650, 0, 0], [610, 650, 0, 0]]
                ]
            ]
#list of list for imposters that spawn, each imposter has the the format [x, y, direction, type]
#list 0 of the list is all the imposters in the first level, list N of the imposters in
#the first level is the Nth wave.

imposter = []
#the imposters in the wave is appended to the list above in order to spawn them.
#Once a wave of enemies is cleared, the list is cleared then the next wave is spawned.

#list of list for nodes in each of the 5 waves in level 2. Each node is in the format [x, y, color].
#Each wave has 4 pairs of nodes, each row represent nodes of the same color that can be linked.
#The final row of node has 3 nodes to make sure it can link both ways as with 2 nodes, it only links 1 way.
nodes = [
        [[180, 650, (255, 0, 0)], [935, 700, (255, 0, 0)],
         [370, 650, (0, 255, 0)], [1080, 500, (0, 255, 0)],
         [270, 525, (0, 0, 255)], [650, 585, (0, 0, 255)],
         [70, 650, (255, 192, 203)], [780, 650, (255, 192, 203)], [70, 650, (255, 192, 203)]],
        [[270, 425, (255, 0, 0)], [70, 650, (255, 0, 0)],
         [650, 485, (0, 255, 0)], [1080, 500, (0, 255, 0)],
         [180, 650, (0, 0, 255)], [370, 650, (0, 0, 255)],
         [935, 700, (255, 192, 203)], [780, 650, (255, 192, 203)], [935, 700, (255, 192, 203)]],
        [[370, 650, (255, 0, 0)], [780, 650, (255, 0, 0)],
         [180, 650, (0, 255, 0)], [1080, 500, (0, 255, 0)],
         [70, 650, (0, 0, 255)], [650, 485, (0, 0, 255)],
         [270, 425, (255, 192, 203)], [935, 700, (255, 192, 203)], [270, 425, (255, 192, 203)]],
        [[1080, 650, (255, 0, 0)], [780, 650, (255, 0, 0)],
         [180, 650, (0, 255, 0)], [370, 500, (0, 255, 0)],
         [70, 650, (0, 0, 255)], [270, 485, (0, 0, 255)],
         [650, 425, (255, 192, 203)], [935, 700, (255, 192, 203)], [650, 425, (255, 192, 203)]],
        [[70, 650, (255, 0, 0)], [270, 650, (255, 0, 0)],
         [650, 650, (0, 255, 0)], [1080, 500, (0, 255, 0)],
         [370, 650, (0, 0, 255)], [180, 485, (0, 0, 255)],
         [780, 425, (255, 192, 203)], [935, 700, (255, 192, 203)], [780, 425, (255, 192, 203)]]        
         ]

#the nodes in the wave is append to the list above to be spawned.
#Works the same way as the imposter list above.
node = []

#number of nodes that are tagged by the player
nodeTagged = 0

#list of images for the pistol
pistol = []

#list of images for each type of bullet:
#plt - normal shotgun shot
#bPlt - mega-shotgun shot
#lsr - laser shot
#blt - pistol shot
plt = []
bPlt = []
lsr = []
blt = []

#screen shake
shake = [0, 0]

#current status of the player:
#-1 - dead
#0, 0.1, 0.2, 0.4 - menu
#1 - alive
status = 0

class Crewmate:
    def __init__(self, pic, x, y):
        #attributes for the player
        self.x = x
        self.y = y
        self.mx = 0
        self.my = 0
        #keeps track of health
        self.health = 80
        #which direction the player is walking- not necessarily the direction the player is facing
        self.walkDir = 1
        #when the player last walked
        self.walk_update = time.get_ticks()
        #when the player last jumped
        self.last_jump = time.get_ticks()
        #when the player last got hit
        self.last_hit = time.get_ticks()
        #keeps track of stamina
        self.stamina = 150
        #current walk frame
        self.stage = 0
        #velocity of the player horizontally: positive is going right, negative is going left
        self.momentumX = 0
        #velocity of the player vertically: positive is going down, negative is going up
        self.momentumY = 0
        #where the gun is
        self.shootDir = 0
        #how many times the player has jumped, max 3 times
        self.jumpCount = 0
        #screen shake created by the player
        self.shake = [0, 0]
        
        self.rect = Rect(x - 83, y - 85, 167, 201)

        #booleans for various player activites: jump, walk, dash, descend(down slam), gravity(if the player is falling)
        self.isGravity = True
        self.isJumping = False
        self.isWalking = False
        self.isDashing = False
        self.isDescend = False

        #images for the player, slide is not included with the base image as it needs to be rotated
        self.rightPic = pic[0]
        self.leftPic = transform.flip(pic[0], True, False)
        self.rightSlide = pic[1]
        self.leftSlide = transform.flip(pic[1], True, False)

        #sound effects, the format is s_name 
        self.s_dash = mixer.Sound("Sounds/Dodge.wav")
        self.s_dash.set_volume(0.1)
        self.s_slide = mixer.Sound("Sounds/wallcling.wav")
        self.s_slide.set_volume(0.1)
        self.s_descend = mixer.Sound("Sounds/Landing.wav")
        self.s_descend.set_volume(0.1)

    #physics for the player, decelerating when momentum is not 0
    #also responsible for making sure player hitbox stays where the player is
    #and also making sure stamina replenishes and health stays below 80.
    def physics(self):
        if self.momentumX < 0:
            self.momentumX += 1
        elif self.momentumX > 0:
            self.momentumX -= 1
        if self.momentumY < 0:
            self.momentumY += 1
        elif self.momentumY > 0:
            self.momentumY -= 1
        self.rect = self.rect.move(self.momentumX, self.momentumY)
        self.x += self.momentumX
        self.y += self.momentumY
        if self.stamina < 150:
            self.stamina += 0.5
        if self.health > 80:
            self.health = 80
        if self.isDescend == False:
            self.rect = Rect(self.x - 83, self.y - 85, 167, 201)
        else:
            if self.isWalking == False:
                self.rect = Rect(self.x - 83, self.y - 55, 167, 171)
            else:
                self.rect = Rect(self.x - 83, self.y, 167, 121)

    #gravity that constantly pulls the player down
    #gravity is off when dashing so when velocity X
    #is 0, gravity is turned back on.
    def gravity(self):
        if self.isGravity == True:
            if self.y < 700 and self.momentumY >= 0:
                self.y += 3
        if self.momentumX == 0:
            self.isGravity = True

    #jump function that mostly just keeps track of how many
    #times the player jumps and resetting the jump count
    #once the player hits the ground
    def jump(self):
        cur_time = time.get_ticks()
        jump_cd = 1500
        if cur_time - self.last_jump >= jump_cd and self.jumpCount > 0:
            self.jumpCount -= 1
            self.last_jump = cur_time
        if self.y >= 700:
            self.isJumping = False
            self.jumpCount = 0

    #function for walking, after 40 miliseconds since the last frame of the animation
    #has been played, the next one is played then the time is recorded to be used
    #for the next frame. If the player stands still, the frame is updated to the player
    #standing still. Stages are different for left and right because the image is flipped.
    def walk(self):
        cur_time = time.get_ticks()
        walk_cd = 40
        if self.isWalking:
            if self.walkDir == 0:
                self.x += 6
            elif self.walkDir == 1:
                self.x -= 6
            if self.isJumping == False and self.y == 700:
                if cur_time - self.walk_update >= walk_cd:
                    self.stage += 1
                    if self.stage >= 12:
                        self.stage = 0
                    self.walk_update = cur_time
        else:
            if self.shootDir <= 90 or self.shootDir > 270:
                self.stage = 0
            elif self.shootDir > 90 and self.shootDir <= 270:
                self.stage = 12

    #function for dashing, dashing requires 15 stamina.
    #If the player is walking, the velocity is increased depending
    #on the player walking direction. If the player is still, the velocity
    #is increased depending on the gun direction. If the player does
    #not have 15 stamina, isDashing is false as without that line, the dash
    #will be played once stamina is above 15.
    def dash(self):
        if self.isDashing and self.stamina > 15:
            self.stamina -= 15
            mixer.find_channel(True).play(self.s_dash)
            if self.isWalking:
                if self.walkDir == 0:
                    self.momentumX += 30
                    self.isGravity = False
                elif self.walkDir == 1:
                    self.momentumX -= 30
                    self.isGravity = False
            else:
                if self.shootDir <= 90 or self.shootDir > 270:
                    self.momentumX -= 30
                    self.isGravity = False
                elif self.shootDir > 90 and self.shootDir <= 270:
                    self.momentumX += 30
                    self.isGravity = False
            self.last_hit = time.get_ticks()
            self.isDashing = False
        else:
            self.isDashing = False

    #function for down slam and crouching. The down slaming portion adds to player y
    #until the player hits the ground. If any imposter is close-by when the player
    #lands, they are knocked up with a velocity of 40 and deals a slight bit of health.
    #The crouching portion activates when player y is on the ground and shifts the
    #player hitbox lower. If the player is walking while crouching (sliding), their speed
    #increases.
    def descend(self, imposter):
        if self.isDescend:
            if self.y < 700:
                if self.isDashing:
                    self.isDescend = False
                else:
                    if self.y + 40 > 700:
                        self.isDescend = False
                        self.y = 700
                        mixer.find_channel(True).play(self.s_descend)
                        self.shake[1] = 10
                        self.last_hit = time.get_ticks()
                    else:
                        self.y += 40
                        self.last_hit = time.get_ticks()
                    if self.y == 700:
                        for imp in imposter:
                            if distance(self.x, self.y, imp.x, imp.y) < 250:
                                imp.momentumY -= 30
                                imp.health -= 5
            else:
                if self.isWalking:
                    self.stage = 12
                    mixer.find_channel(True).play(self.s_slide)
                    if self.walkDir == 0:
                        self.x += 5
                    elif self.walkDir == 1:
                        self.x -= 5
                else:
                    self.stage = 6
                    
    #function for taking damage
    #the player has invincibility for 500 miliseconds after being hit normally.
    #If the player health is below or equal to 0, they die.
    def die(self, imp):
        cur_time = time.get_ticks()
        hit_cd = 500
        if cur_time - self.last_hit >= hit_cd:
            if self.rect.colliderect(imp.head_rect) or self.rect.colliderect(imp.body_rect):
                if imp.type == 0:
                    self.health -= 40
                    self.shake[0] += 8
                    self.shake[1] = 8
                elif imp.type == 1:
                    self.health -= 20
                    self.shake[0] += 4
                    self.shake[1] = 4
                elif imp.type == 3:
                    self.health -= 15
                    self.shake[0] += 3
                    self.shake[1] = 3
                self.last_hit = cur_time
            for orb in imp.orbs:
                if self.rect.collidepoint((orb[0], orb[1])):
                    self.health -= 25
                    self.shake[0] += 5
                    self.shake[1] += 5
                    self.last_hit = cur_time
            for wave in imp.wave:
                 if self.rect.collidepoint((wave[0], wave[1])):
                    self.health -= 10
                    self.shake[0] += 3
                    self.shake[1] += 3
                    self.last_hit = cur_time    
        if self.health <= 0:
            return True

    #resets all the player attributes, used for when the player dies
    def reset(self):
        self.x = 1100
        self.y = 700
        self.health = 80
        self.stamina = 150
        self.walkDir = 1
        self.stage = 0

    #draws the player and the health + stamina bars
    def draw(self, screen):
        if self.shootDir <= 90 or self.shootDir > 270: #when the player is facing right, the degrees is counted as the same on a graph, 0 being on the right.
            if self.isDescend == False: #draws the player depending on which frame they are on
                screen.blit(self.rightPic, (self.x - 83, self.y - 115), area = Rect((self.stage * 167, 0, 167, 231)))
            else:
                if self.isWalking == False: #draws the player crouching
                    screen.blit(self.rightPic, (self.x - 83, self.y - 115), area = Rect((self.stage * 167, 0, 167, 231)))
                else: 
                    slide = transform.rotate(self.rightSlide, 30) #when sliding, rotate the slide image by 30 degrees
                    slide_rect = slide.get_rect(center = (self.x, self.y)) #make sure the image stays in the same place
                    screen.blit(slide, slide_rect)
        elif self.shootDir > 90 and self.shootDir <= 270: #when the player is facing left
            if self.isDescend == False:
                screen.blit(self.leftPic, (self.x - 83, self.y - 115), area = Rect((self.stage * 167, 0, 167, 231)))
            else:
                if self.isWalking == False:
                    screen.blit(self.leftPic, (self.x - 83, self.y - 115), area = Rect((self.stage * 167, 0, 167, 231)))
                else:
                    slide = transform.rotate(self.leftSlide, -30)
                    slide_rect = slide.get_rect(center = (self.x, self.y))
                    screen.blit(slide, slide_rect)
        draw.rect(screen, (0, 255, 0), (0, 140, self.health * 10, 40), 0, 4) #draws the health bar
        #the stamina bar has 3 bars max so the below code draws them
        if self.stamina >= 50:
            draw.rect(screen, (0, 0, 255), (0, 190, 250, 30), 0, 4)
        if self.stamina >= 100:
            draw.rect(screen, (0, 0, 255), (255, 190, 250, 30), 0, 4)
        if self.stamina == 150:
            draw.rect(screen, (0, 0, 255), (510, 190, 250, 30), 0, 4)
        draw.rect(screen, (0, 0, 255), ((self.stamina // 50) * 255, 190, (self.stamina % 50) * 5, 30), 0, 4)
        draw.rect(screen, (0), (self.rect), 2)
        
    #boundaries for the player
    def bound(self):
        if self.x > 1280 - 83:
            self.x = 1280 - 83
        elif self.x < 83:
            self.x = 83
        if self.y > 700:
            self.y = 700
            
class Item:
    def __init__(self, sg, pistol, knife, bullets, x, y):
        #attributes for items
        self.x = x
        self.y = y
        self.mx = 0
        self.my = 0
        #same as the player shootDir
        self.shootDir = 0
        #shootStage is for the pistol firing animation
        self.shootStage = 0
        self.melee_stage = 0 #to keep track of knife swipe animation 
        self.weapon = 0 #current weapon: 0 for pistol, 1 for shotgun
        
        #when did certain actions happen such as when the pistol or shotgun was last fired
        self.pistol_update = time.get_ticks()
        self.sg_update = time.get_ticks()
        self.last_parried = time.get_ticks()
        #when the laser started charging
        self.charge_start = 0
        #when the last melee was started, at -500 to make sure the player can melee when spawned
        self.melee_update = -500
        #amount of time the laser has before disappearing
        self.laser_time = 0

        #amount of charged dmg the laser has
        self.charged_dmg = 0

        #starting point of the laser and end point
        self.laserStart = (0, 0)
        self.laserEnd = (0, 0)

        #tip of the current gun in the format [x, y]
        self.gunBarrel = []

        #position of the knife
        self.kX = 0
        self.kY = 0

        #screen shake produced by the weapons
        self.shake = [0, 0]

        #shots fired
        self.shots = []

        #booleans for various actions
        self.isShooting = False
        self.isSwing = False
        self.isMelee = False
        self.isCharging = False

        #images for pistol, shotgun, various bullets, and knife, 
        self.pic = [[[d for d in pistol], [transform.flip(d, False, True) for d in pistol]], [[sg], [transform.flip(sg, False, True)]]]
        self.blts = []
        self.blts.append([transform.scale(d, (3 * d.get_width(), 3 * d.get_height())) for d in bullets[0]])
        self.blts.append([transform.flip(d, False, True) for d in bullets[1]])
        self.blts.append([transform.scale(d, (3 * d.get_width(), 3 * d.get_height())) for d in bullets[2]])
        self.blts.append([transform.scale(d, (3 * d.get_width(), 3 * d.get_height())) for d in bullets[3]])
        self.kPic = [transform.flip(knife, False, True), knife]

        #sound effects
        self.s_ricochet = mixer.Sound("Sounds/Ricochet.wav")
        self.s_ricochet.set_volume(0.1)
        self.s_reload = mixer.Sound("Sounds/shellImpact.wav")
        self.s_reload.set_volume(0.1)
        self.s_click = mixer.Sound("Sounds/fistReload.wav")
        self.s_click.set_volume(0.1)
        self.s_sound = [mixer.Sound("Sounds/pistol.wav"), mixer.Sound("Sounds/shotgun.wav"), mixer.Sound("Sounds/parry.wav")]
        self.s_sound[0].set_volume(0.1)
        self.s_sound[1].set_volume(0.05)
        self.s_sound[2].set_volume(0.15)
        self.s_hurt = [mixer.Sound("Sounds/Zombie Damage 1.wav"), mixer.Sound("Sounds/Zombie Damage 2.wav"), mixer.Sound("Sounds/Zombie Damage 3.wav")]
        self.s_hurt[0].set_volume(0.1)
        self.s_hurt[1].set_volume(0.1)
        self.s_hurt[2].set_volume(0.1)
        self.s_health = mixer.Sound("Sounds/HpGet.wav")
        self.s_health.set_volume(0.1)
        self.s_headshot = mixer.Sound("Sounds/HeadBreak.wav")
        self.s_headshot.set_volume(0.1)
        self.s_weak_death = mixer.Sound("Sounds/Zombie Weak Death.wav")
        self.s_weak_death.set_volume(0.1)
        self.s_death = mixer.Sound("Sounds/Zombie Death.wav")
        self.s_death.set_volume(0.1)

    #updates the current whereabouts of the gun and the gunbarrel which changes as
    #the player moves the mouse, when the player moves the cursor close to the player
    #the cursor is held back as if not held back the gun will look very wierd (the gun will point toward the player with the handle sticking outwards)
    def update(self, player):
        self.mx, self.my = mouse.get_pos()
        self.shootDir = angle2(player.x, player.y, self.mx, self.my)
        self.shootDir += 180
        if self.shootDir > 360:
            self.shootDir -= 360
        if distance(player.x, player.y, self.mx, self.my) < 93:
            self.mx = player.x + 93 * cos(radians(self.shootDir))
            self.my = player.y - 93 * sin(radians(self.shootDir))
        if self.weapon == 0:
            self.gunBarrel = [player.x + 93 * cos(radians(self.shootDir)), player.y - 93 * sin(radians(self.shootDir))]
        elif self.weapon == 1:
            self.gunBarrel = [player.x + 150 * cos(radians(self.shootDir)), player.y - 150 * sin(radians(self.shootDir))]
        elif self.weapon == 2:
            self.gunBarrel = [player.x + 60 * cos(radians(self.shootDir)), player.y - 60 * sin(radians(self.shootDir))]
        player.shootDir = self.shootDir #player shoot direction is the same as item shoot direction, this line updates the player shootDir

    #function for moving the bullets, if a pistol shot hits a ceiling or wall, it ricochets 90 degrees using the swap function
    def bulletPhysics(self):
        for bullet in self.shots:
            if bullet[5] <= 0:
                self.shots.remove(bullet)
            if bullet[4] == 10:
                bullet[0] += bullet[2] * bullet[4] * 3
                bullet[1] += bullet[3] * bullet[4] * 3
                if bullet[1] >= 800 or bullet[1] <= 0:
                    val = swap(bullet[2], bullet[3])
                    mixer.find_channel(True).play(self.s_ricochet)
                    bullet[2] = -float(val[0])
                    bullet[3] = float(val[1])
            elif bullet[4] == 8:
                bullet[0] += bullet[2] * bullet[4] * 2
                bullet[1] += bullet[3] * bullet[4] * 2
            else:
                bullet[0] += bullet[2] * bullet[4] * 5
                bullet[1] += bullet[3] * bullet[4] * 5
            bullet[5] -= 1

    #animates the bullets by pushing forward the bullet stage which is its 8th index while the last update is its 9th.
    def bltAnimation(self):
        cur_time = time.get_ticks()
        animation_cd = 100
        for shot in self.shots:
            if cur_time - shot[8] >= animation_cd and shot[7] < 4:
                shot[7] += 1
                shot[8] = cur_time

    #shoot function that allows the play to fire the weapon
    def shoot(self, player):
        cur_time = time.get_ticks()
        shoot_cd = 10
        if self.isShooting:
            if self.weapon == 0:
                if cur_time - self.pistol_update >= shoot_cd:
                    if self.shootStage < 9: #pushes forward the frame for the pistol animation
                        self.shootStage += 1
                    elif self.shootStage == 9:
                        self.shootStage = 0
                        mixer.find_channel(True).play(self.s_sound[0])
                        #shots are in the format of [x, y, horizontal displacement, vertical displacement, speed, duration, damage, frame, last_frame_update]
                        self.shots.append([self.gunBarrel[0], self.gunBarrel[1], cos(radians(self.shootDir)), -sin(radians(self.shootDir)), 10, 50, 6, 0, cur_time])
                        self.isShooting = False #when the player shoots a weapon, jump is reset and gravity is turned off for a brief moment
                        player.isGravity = False
                        player.isJumping = False
                    self.pistol_update = cur_time
            elif self.weapon == 1:
                self.shootStage = 0 #resets the frame for the pistol when the shotgun is switched on
                for i in range(6): #shotgun fires 6 pellets
                    angl = randint(-20, 20) #creates a random spread effect for the shotgun
                    self.shots.append([self.gunBarrel[0], self.gunBarrel[1], cos(radians(angl + self.shootDir)), -sin(radians(angl + self.shootDir)), 8, 25, 1, 0, cur_time])
                    if i == 5:
                        mixer.find_channel(True).play(self.s_sound[1])
                        self.isShooting = False
                        player.isGravity = False
                        player.isJumping = False
        if self.isCharging: #charging for the laser shot on the pistol
            self.charged_dmg = 0
            self.charged_dmg = (cur_time - self.charge_start) / 200 #charged damage is related to the amount of time charged to a maximum of 5 charged damage
            if self.charged_dmg > 5:
                self.charged_dmg = 5
            self.laserStart = [self.gunBarrel[0], self.gunBarrel[1]] #sets where the laser is, end point is 800 distance away from the start point
            self.laserEnd = [800 * cos(radians(self.shootDir)) + self.gunBarrel[0], -800 * sin(radians(self.shootDir)) + self.gunBarrel[1]]
        else: #resets when the charge was last started when laser is not currently charging
            self.charge_start = 0

    #melee function responsible for everything melee related
    #also responsible for the player being able to parry its shotgun shots.
    def melee(self, player, imposter):
        cur_time = time.get_ticks()
        melee_cd = 100
        parry_cd = 50
        if self.isMelee:
            if cur_time - self.melee_update > melee_cd:
                player.last_hit = cur_time #meleeing provides invincibility to normal damage for a short bit

                #the knife changes position depending on the current weapon
                if self.weapon == 0: 
                    self.kX = player.x + 93 * cos(radians(self.shootDir -  10 * self.melee_stage))
                    self.kY = player.y - 93 * sin(radians(self.shootDir -  10 * self.melee_stage))
                elif self.weapon == 1:
                    self.kX = player.x + 150 * cos(radians(self.shootDir -  10 * self.melee_stage))
                    self.kY = player.y - 150 * sin(radians(self.shootDir -  10 * self.melee_stage))

                #if an imposter laser or orb hits comes close to the knife, it is blocked.
                for imp in imposter:
                    for laser in imp.laser:
                        if distance(laser[0], laser[1], self.kX, self.kY) < 80:
                            imp.laser.remove(laser)
                    for orb in imp.orbs:
                        if distance(orb[0], orb[1], self.kX, self.kY) < 80:
                            imp.orbs.remove(orb)

                #section that pushes the frame forward, once the frame is at 10, the melee is finished
                #and the knife position is set back to 0, 0 to not hit any more enemies
                self.melee_stage += 1
                if self.melee_stage == 10:
                    self.melee_stage = 0
                    self.isMelee = False
                    self.kX = 0
                    self.kY = 0
                    self.melee_update = cur_time
            else: #prevents a melee from going off on a delay if a melee was not available when cast
                self.isMelee = False

            #section of code for allowing the player to create mega-shots from meleeing the shotgun shots
            for shot in self.shots:
                if distance(shot[0], shot[1], self.kX, self.kY) < 80 and self.weapon == 1: #if a pellet comes close to the knife and the shotgun is out
                    if shot[4] != 13: #delete the shot
                        self.shots.remove(shot)
                    if cur_time - self.last_parried  >= parry_cd: #make sure 2 mega shots are not produced
                        mixer.find_channel(True).play(self.s_sound[2]) 
                        self.shots.append([self.gunBarrel[0], self.gunBarrel[1], cos(radians(self.shootDir)), -sin(radians(self.shootDir)), 13, 35, 90, 0, cur_time]) #add a mega-shot
                        self.last_parried = cur_time #update when the last mega-shot was created

    #draws the weapons and bullets
    def draw(self, screen, player):
        cur_time = time.get_ticks()
        direction = 0
        if self.shootDir <= 90 or self.shootDir > 270:
            direction = 0
        elif self.shootDir > 90 or self.shootDir <= 270:
            direction = 1
        if self.isShooting == False:
            if self.weapon == 0:
                curGun = transform.rotate(self.pic[self.weapon][direction][8], angle(player.x, player.y, self.mx, self.my) + 5 - direction * 10)
            elif self.weapon == 1:
                curGun = transform.rotate(self.pic[self.weapon][direction][0], angle(player.x, player.y, self.mx, self.my))
        elif self.isShooting:
            curGun = transform.rotate(self.pic[self.weapon][direction][self.shootStage], angle(player.x, player.y, self.mx, self.my) + 5 - direction * 10)
        curGun_rect = curGun.get_rect(center = (player.x, player.y))
        screen.blit(curGun, curGun_rect)
        
        if self.isMelee and self.melee_stage > 0: #draws the knife, the knife will rotate depending on its frame
            weap = transform.rotate(self.kPic[direction], angle(player.x, player.y, self.mx, self.my) - 60 - self.melee_stage * 10) #rotates the image
            weap_rect = weap.get_rect(center = (self.kX, self.kY)) #to make sure the image stays in place
            screen.blit(weap, weap_rect)
       
        for shot in self.shots: #animates the bullets
            if shot[4] == 10:
                blt = transform.rotate(self.blts[0][shot[7]], degrees(acos(shot[2])))
                blt_rect = blt.get_rect(center = (shot[0], shot[1]))
                screen.blit(blt, blt_rect)
            elif shot[4] == 8:
                blt = transform.rotate(self.blts[2][shot[7]], degrees(acos(shot[2])))
                blt_rect = blt.get_rect(center = (shot[0], shot[1]))
                screen.blit(blt, blt_rect)
            elif shot[4] == 13:
                if self.shootDir >= 0 and self.shootDir < 180:
                    blt = transform.rotate(self.blts[3][shot[7]], degrees(acos(shot[2])))
                else:
                    blt = transform.flip(transform.rotate(self.blts[3][shot[7]], 180 + degrees(acos(shot[2]))), True, False)
                blt_rect = blt.get_rect(center = (shot[0], shot[1]))
                screen.blit(blt, blt_rect)
        if self.weapon == 0:
            draw.circle(screen, (0, 0, 255), self.gunBarrel, self.charged_dmg * 7, 3) #draws a small circle for when the laser is charging
        if self.laser_time > 10: #animates the laser
            lsr = transform.rotate(self.blts[1][5 - floor(self.laser_time / 10)], angle(self.laserStart[0], self.laserStart[1], self.laserEnd[0], self.laserEnd[1]))
            lsr_rect = lsr.get_rect(center = (self.laserEnd[0]  * 0.7  + self.laserStart[0] * 0.3, self.laserEnd[1]  * 0.7 + self.laserStart[1] * 0.3))
            screen.blit(lsr, lsr_rect)
            self.laser_time -= 1
        elif self.laser_time == 10:
            self.laser_time = 0

    #function for hitting the imposter and imposters dying
    def bullet(self, imposter, player, item):
        cur_time = time.get_ticks()
        for shot in self.shots:
            #the if statement below is if the current bullet that hit the imposter is a shotgun pellet or mega-shot or a pistol shot hit the imposter's body rect
            if (imposter.body_rect.collidepoint((shot[0], shot[1])) or imposter.head_rect.collidepoint((shot[0], shot[1])) and (shot[4] == 8 or shot[4] == 13)) or (imposter.body_rect.collidepoint((shot[0], shot[1])) and shot[4] == 10):
                mixer.find_channel(True).play(self.s_hurt[randint(0, 2)])
                mixer.find_channel(True).play(self.s_health)
                if shot[4] == 10: #if it is a pistol shot
                    imposter.health -= shot[6] * 0.5
                    self.shake[0] += 2
                    self.shake[1] += 2
                else: #if it is not a pistol shot: shotgun pellet or mega-shot
                    imposter.health -= shot[6] * 1.2 + (cur_time - (shot[8] - 500)) / 100 #shotgun shots will increase damage the further it travels to compensate for its spread
                    self.shots.remove(shot) #removes the shot upon impact
                    self.shake[0] += 3
                    self.shake[1] += 3

                #pushes the imposter slightly back
                if imposter.x < player.x:
                    imposter.x -= 5
                elif imposter.x > player.x:
                    imposter.x += 5
                    
                player.health += 1 #adds slight bit of health for damaging an imposter
            elif imposter.head_rect.collidepoint((shot[0], shot[1])) and self.weapon == 0: #if a pistol shot hit the imposter in the head
                imposter.health -= shot[6] * 2 #damage is twice for hitting headshot
                mixer.find_channel(True).play(self.s_hurt[randint(0, 2)])
                mixer.find_channel(True).play(self.s_headshot)
                self.shake[0] += 4
                self.shake[1] += 4
                shot[6] -= 1
                player.health += 5
        if self.isMelee: #if a melee hits an imposter
             if imp.body_rect.collidepoint((item.kX, item.kY)):
                self.shake[0] += 5
                self.shake[1] += 5
                imposter.health -= 25  
        if self.laser_time > 0: #if the laser hits an imposter, the laser is tick damage so as long as time is above 0 it will continue to damage
            if imposter.body_rect.clipline(self.laserStart, self.laserEnd):
                imposter.health -= self.charged_dmg
                self.shake[0] += 1
                self.shake[1] += 1
                
    #function that returns true once impost health is below 0          
    def imposterDeath(self, player, imposter):
        if imposter.health <= 0: #if imposter health is below 0, player heals depending on the imposter type
            if imposter.type == 1 or imposter.type == 5:
                mixer.find_channel(True).play(self.s_weak_death)
            else:
                mixer.find_channel(True).play(self.s_death)
            if imposter.type == 0:
                player.health += 10
            elif imposter.type == 1:
                player.health += 5
            else:
                player.health += 15
            return True

        
class Imposter:
    def __init__(self, pic, x, y, direction, typ):
        #imposter attributes
        self.last_update = time.get_ticks()
        self.type = typ #imposter type

        #depending on the imposter type, they have different health and sizes
        if self.type == 0:
            self.size = 1
            self.y = y
            self.startY = y
            self.health = 10
        elif self.type == 1:
            self.size = 0.2
            self.y = y + 117.6
            self.startY = y + 117.6
            self.health = 1
        elif self.type == 2:
            self.size = 1.2
            self.y = y - 32
            self.startY = y - 32
            self.health = 30
        elif self.type == 3:
            self.size = 0.9
            self.startY = y + 24.2
            self.y = y + 24.2
            self.health = 35
        elif self.type == 4:
            self.size = 1.1
            self.startY = y - 24.2
            self.y = y - 24.2
            self.atkStage = 0 #for which move the boss is doing
            self.slam = [0, 0] #slam direction for boss slam action
            self.slamDirection = 0 #slam direction
            self.health = 2000 #change if want to lower difficulty, below 750 is way easier
        elif self.type == 5:
            self.size = 1
            self.y = y
            self.startY = y
            self.health = 15
            
        self.x = x
        self.head_rect = Rect(x - 80 * self.size, y - 76 * self.size, 165 * self.size, 60.5 * self.size) #head rect
        self.body_rect = Rect(x - 80 * self.size, y - 15.5 * self.size, 165 * self.size, 181.5 * self.size) #body rect
        self.dir = direction #direction
        self.stage = 0 #walk frame
        self.momentumX = 0 #velocity x
        self.momentumY = 0 #velocity y
        self.shake = [0, 0] #shake that the imposter produces

        #booleans for actions and conditions
        self.isIdle = True
        self.isChasing = False
        self.isStunned = False
        self.canStomp = False

        #images for idle animation and chase animation
        self.idlePic = [transform.scale(pic[0], (int(2488 * self.size), int(236 * self.size))),
                                transform.flip(transform.scale(pic[0], (int(2488 * self.size), int(236 * self.size))), True, False)]
        self.chasePic = [transform.scale(pic[1], (int(2652 * self.size), int(290 * self.size))),
                                transform.flip(transform.scale(pic[1], (int(2652 * self.size), int(290 * self.size))), True, False)]

        self.ghost = [pic[2], transform.flip(pic[2], True, False)] #pic for ghosts
        
        self.laser = []
        self.orbs = []
        self.wave = []
        self.spk = []

        #when actions have last happend
        self.orb_update = time.get_ticks()
        self.wave_update = time.get_ticks()
        self.leap_update = time.get_ticks()
        self.slam_update = time.get_ticks()
        self.dash_update = time.get_ticks()
        self.last_moved = time.get_ticks()
        self.last_stunned = time.get_ticks()
        self.last_atk = time.get_ticks()

        #sound effects
        self.s_dash = mixer.Sound("Sounds/Dodge.wav")
        self.s_dash.set_volume(0.05)
        self.s_impact = mixer.Sound("Sounds/LandingHeavy.wav")
        self.s_impact.set_volume(0.1)

    #physics similar to player physics
    def physics(self):
        if self.momentumX < 0:
            self.momentumX += 1
        elif self.momentumX > 0:
            self.momentumX -= 1
        if self.momentumY < 0:
            self.momentumY += 1
        elif self.momentumY > 0:
            self.momentumY -= 1
        if self.momentumY != 0:
            self.stage = 0
        self.body_rect = self.body_rect.move(self.momentumX, self.momentumY)
        self.head_rect = self.head_rect.move(self.momentumX, self.momentumY)
        self.x += self.momentumX
        self.y += self.momentumY
        
    #gravity the same as player gravity, also keeps the rect in position
    def gravity(self):
        if self.y < self.startY and self.momentumY >= 0:
            self.y += 8
        self.body_rect = Rect(self.x - 80 * self.size, self.y - 15.5 * self.size, 165 * self.size, 181.5 * self.size)
        self.head_rect = Rect(self.x - 80 * self.size, self.y - 76 * self.size, 165 * self.size, 60.5 * self.size)

    #function for boundaries   
    def bound(self):
        if self.x > 1280 - 165 * self.size / 2:
            self.x = 1280 - 165 * self.size / 2
        elif self.x < 165 * self.size / 2:
            self.x = 165 * self.size / 2
        if self.y > self.startY:
            self.y = self.startY
        elif self.y < 0:
            self.y = 0

    #function for boss dashing like how a player dashes
    def bossDash(self, player):
        if self.dir == 0:
            direction = 1
        elif self.dir == 1: 
            direction = -1
        mixer.find_channel(True).play(self.s_dash)
        self.momentumX = direction * (-1 + sqrt(1 + 8 * (abs(self.x - player.x) + 250))) // 2 #since the distance crossed by the momentum is n(n+1) / 2,
                                                                                                                                                    #if the distance is the distance between player x and imposter x (+250 pixels to make sure the boss reaches)
                                                                                                                                                    #we can solve for n using the quadratic formula with n being the larger of the too roots.

    #function for how the boss does its close-ranged spike attack
    #it alternates between attacking the lower portion of the player and the upper portion
    #the upper portion can be dodged by a crouch (I think)
    def bossSpk(self, player, item):    
        if self.dir == 0:
            direction = 1
        elif self.dir == 1: 
            direction = -1
        if self.atkStage % 4 == 1:
            self.spk.append([self.x, self.y, self.x + 360 * direction, self.y - 90])
        elif self.atkStage % 4 == 3:
            self.spk.append([self.x, self.y, self.x + 360 * direction, self.y + 90])
        if player.rect.clipline((self.spk[0][0], self.spk[0][1]), (self.spk[0][2], self.spk[0][3])): #if the spk clips into player hitbox, player is damaged (ignores invincibility)
            player.health -= 25
            self.spk.remove(self.spk[0])
            self.shake[0] += 10
            self.shake[1] += 10

    #function for boss slamming into the ground
    #Acheives its goal by calculating the angle between the imposter
    #and the player then setting the slam attribute to what was calculated
    def bossSlam(self, player):
        if self.dir == 0:
            direction = 1
        elif self.dir == 1: 
            direction = -1
        self.slamDirection = angle2(self.x, self.y, player.x, player.y)
        self.slamDirection += 180
        if self.slamDirection > 360:
            self.slamDirection -= 360
        if self.y < player.y:
            self.slam = [20 * cos(radians(self.slamDirection)), -20 * sin(radians(self.slamDirection))]
            self.last_atk = cur_time

    #chains all the boss moves together into one combo
    #does this by pushing forward the atkStage and updating
    #when the last move was performed so the boss can do its next move
    #after a certain cooldown.
    def bossCombo(self, player, item):
        cur_time = time.get_ticks()
        if self.atkStage == 0: #attacks that are even are dashes unless it is 8, 10, or 14
                                            #attacks 8, 10, and 14 are the boss jumping
            if cur_time - self.last_atk >= 600 and self.y >= self.startY:
                self.bossDash(player)
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 1: #attacks that are odd are spikes unless it is 7, 9, or 15
                                            #attacks 7, 9, and 15 are the boss slamming
            if cur_time - self.last_atk >= 400:
                self.bossSpk(player, item)
                self.isStunned = True #spikes make the boss stand still
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 2:
            if cur_time - self.last_atk >= 200:
                self.isStunned = False
                self.spk.clear() #clears the spikes
                self.bossDash(player)
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 3:
            if cur_time - self.last_atk >= 400:
                self.bossSpk(player, item)
                self.isStunned = True
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 4:
            if cur_time - self.last_atk >= 200:
                self.isStunned = False
                self.spk.clear()
                self.bossDash(player)
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 5:
            if cur_time - self.last_atk >= 400:
                self.bossSpk(player, item)
                self.isStunned = True
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 6:
            if cur_time - self.last_atk >= 200:
                self.isStunned = False
                self.spk.clear()
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 7: 
            if cur_time - self.last_atk >= 600 and self.y >= self.startY:
                self.isStunned = False
                self.spk.clear()
                self.momentumY = -23
                self.bossDash(player) #the boss also dashes in the air after jumping
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 8:
            afterSlam = False
            if cur_time - self.last_atk >= 400 and afterSlam == False:
                self.bossSlam(player)
                afterSlam = True #afterSlam is True after the boss determines the direction they are slamming
            self.x += self.slam[0] #moves toward the player
            self.y += self.slam[1]
            if self.y >= self.startY or self.x > 1280 - 165 * self.size / 2 or self.x < 165 * self.size / 2:
                self.slam = [0, 0]
                self.bossDash(player)
                if self.y >= self.startY and afterSlam:
                    self.shake[0] += 15
                    self.shake[1] += 15
                    mixer.find_channel(True).play(self.s_impact)
                    self.atkStage += 1
                    self.last_atk = cur_time
                if distance(self.x, self.y, player.x, player.y) <= 120: #damages the player if they are too close
                    player.health -= 15
        if self.atkStage == 9:
            if cur_time - self.last_atk >= 600 and self.y >= self.startY:
                self.isStunned = False
                self.spk.clear()
                self.momentumY = -23
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 10:
            afterSlam = False
            if cur_time - self.last_atk >= 400 and afterSlam == False:
                self.bossSlam(player)
                afterSlam = True
            self.x += self.slam[0]
            self.y += self.slam[1]
            if self.y >= self.startY or self.x > 1280 - 165 * self.size / 2 or self.x < 165 * self.size / 2:
                self.slam = [0, 0]
                self.bossDash(player)
                if self.y >= self.startY and afterSlam:
                    self.shake[0] += 15
                    self.shake[1] += 15
                    mixer.find_channel(True).play(self.s_impact)
                    self.atkStage += 1
                    self.last_atk = cur_time
                if distance(self.x, self.y, player.x, player.y) <= 120:
                    player.health -= 15
        if self.atkStage == 11:
            if cur_time - self.last_atk >= 200:
                self.bossSpk(player, item)
                self.isStunned = True
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 12:
            if cur_time - self.last_atk >= 400:
                self.isStunned = False
                self.spk.clear()
                self.bossDash(player)
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 13:
            if cur_time - self.last_atk >= 200:
                self.bossSpk(player, item)
                self.isStunned = True
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 14:
            if cur_time - self.last_atk >= 600 and self.y >= self.startY:
                self.isStunned = False
                self.spk.clear()
                self.momentumY = -(-1 + sqrt(1 + 8 * (abs(self.y - player.y) + 150))) // 1.75 #velocity y is calculated the same way as the one used for velocity x in boss dashes
                self.last_atk = cur_time
                self.atkStage += 1
        if self.atkStage == 15:
            afterSlam = False
            if cur_time - self.last_atk >= 400 and afterSlam == False:
                self.bossSlam(player)
                afterSlam = True
            self.x += self.slam[0]
            self.y += self.slam[1]
            if self.y >= self.startY or self.x > 1280 - 165 * self.size / 2 or self.x < 165 * self.size / 2:
                self.slam = [0, 0]
                self.bossDash(player)
                if self.y >= self.startY and afterSlam:
                    self.shake[0] += 10
                    self.shake[1] += 10
                    mixer.find_channel(True).play(self.s_impact)
                    self.atkStage = 0
                    self.last_atk = cur_time
                if distance(self.x, self.y, player.x, player.y) <= 120: #does more damage than the previous slams
                    player.health -= 30
            
    def ghostLaser(self, player): #function for ghost's laser attacks, determines the direction where the player is and fires a laser
        cur_time = time.get_ticks()
        laser_cd = 1200
        direction = angle2(self.x, self.y, player.x, player.y)
        direction += 180
        if direction > 360:
            direction -= 360
        if cur_time - self.last_atk >= laser_cd:
            self.laser.append([self.x, self.y, 15 * cos(radians(direction)), -15 * sin(radians(direction))])
            self.last_atk = cur_time
        for laser in self.laser:
            laser[0] += laser[2]
            laser[1] += laser[3]
            if player.rect.clipline((self.x, self.y), (laser[0], laser[1])):
                player.health -= 10
                self.laser.remove(laser)
            elif laser[1] >= 816 or laser[1] <= 0 or laser[0] >= 1280 or laser[0] <= 0:
                self.laser.remove(laser)

    #function for walking
    #imposter type 2 and 3 (the one that launches black orbs and the one that launches red orbs) dont move toward the player
    #unless the player is 700 pixels away, the other types have regular movements.
    def walk(self, player):
        cur_time = time.get_ticks()
        walk_cd = 100
        direction = 0
        if self.dir == 0:
            direction = 1
        elif self.dir == 1:
            direction = -1
        if self.isChasing and self.isStunned == False:
            if self.type == 0:
                self.x += 5 * direction
            elif self.type == 1:
                self.x += 8 * direction
            elif (self.type == 2  or self.type == 3) and distance(self.x, self.y, player.x, player.y) >= 700:
                self.x += 4 * direction
            elif self.type == 4:
                self.x += 3 * direction
            if cur_time - self.last_update >= walk_cd: #walk frames that are pushed forward
                self.stage += 1
                if self.stage >= 11:
                    self.stage = 0
                self.last_update = cur_time
        if (self.type == 2 and distance(self.x, self.y, player.x, player.y) <= 400) or (self.type == 3 and distance(self.x, self.y, player.x, player.y) <= 200): #if the player approaches type 2 or type 3 imposters, they back away until the player is 700 pixels away
            escape_cd = 1500
            if self.dir == 0:
                if cur_time - self.last_moved > escape_cd:
                    self.x += -4 * direction
                    if distance(self.x, self.y, player.x, player.y) >= 700:
                        self.last_moved = cur_time
                        
    #dashes for regular imposters, functions the same way as dashes for player
    def dash(self, player):
        cur_time = time.get_ticks()
        dash_cd = 1500
        direction = 0
        if self.dir == 0:
            direction = 1
        elif self.dir == 1: 
            direction = -1
        if cur_time - self.dash_update > dash_cd and self.isStunned == False:
            if self.type != 4:
                dash = randint(1, 4)
                if (dash == 1 and self.type == 0) or (dash == 2 and self.type == 1):
                    self.momentumX = 20 * direction
                    self.dash_update = cur_time
                    
    #function that spawns black orbs for type 2 imposters
    #when bullets hit the orbs the orbs are destroyed if the imposter is
    #within 700 pixels of the player its orb spawning speed increases
    def orbPhysics(self, player, bullets):
        cur_time = time.get_ticks()
        if distance(self.x, self.y, player.x, player.y) >= 700:
            orb_cd = 800
        else:
            orb_cd = 600
        orbDir = angle2(self.x, self.y, player.x, player.y)
        orbDir += 180
        if orbDir > 360:
            orbDir -= 360  
        for orb in self.orbs:
            if distance(orb[0], orb[1], self.x, self.y) >= 1000:
                self.orbs.remove(orb)
            orb[0] += orb[2] * 10
            orb[1] += orb[3] * 10
            for bullet in bullets:
                if distance(bullet[0], bullet[1], orb[0], orb[1]) < 20:
                    if orb in self.orbs:
                        self.orbs.remove(orb)
        if self.type == 2:
            if cur_time - self.orb_update >= orb_cd: #if the imposter can fire an orb according to the cooldown
                self.orbs.append([self.x, self.y, cos(radians(orbDir)), -sin(radians(orbDir))])
                self.orb_update = cur_time
                
    #function that spawns the red orbs (waves) for type 3 imposters
    #randomly choses the type of the orb (vertical or horizontal) then randomly (choses its location- within 200 or 300 pixels of the player)
    #bullets also destroy these orbs and its firing rate is similar to the one that is used for the black orbs.
    def wavePhysics(self, player, bullets):
        cur_time = time.get_ticks()
        wave_cd = 600
        for wave in self.wave:
            if (wave[2] == 0 and wave[0] >= 1280) or (wave[2] == 1 and wave[1] >= 700):
                self.wave.remove(wave)
            if wave[2] == 0:
                wave[1] += 10 * wave[3]
            elif wave[2] == 1:
                wave[0] += 10 * wave[3]
        if self.type == 3:
            if cur_time - self.wave_update >= wave_cd:
                if self.type != 4:
                    typ = randint(0, 1)
                    if typ == 0:
                        wav = randint(int(player.x - 200), int(player.x + 200))
                        direction = randint(0, 1)
                        if direction == 0:
                            self.wave.append([wav, 0, 0, 1])
                        elif direction == 1:
                            self.wave.append([wav, 700, 0, -1])
                        self.wave.append([wav, 0, typ, 1])
                    elif typ == 1:
                        wav = randint(int(player.y - 300), int(player.y + 300))
                        direction = randint(0, 1)
                        if direction == 0:
                            self.wave.append([0, wav, 1, 1])
                        elif direction == 1:
                            self.wave.append([1280, wav, 1, -1])
                for bullet in bullets:
                    for wave in self.wave:
                        if distance(bullet[0], bullet[1], wave[0], wave[1]) < 20:
                            self.wave.remove(wave)
                self.wave_update = cur_time
                
    #function for idle animation and when an imposter will chase the player
    #if it is a type 0, 1 or 4 imposter, it will be chasing when the player is within 800
    #pixels otherwise it is idle with its frames increasing. If it is a type 2 or 3 imposter,
    #it will idle with its frames increasing once the player is within 700 pixels and chase
    #if the player is out of that distance.
    def idle(self, player):
        walk_cd = 30
        if self.type == 0 or self.type == 1 or self.type == 4:
            if distance(self.x, self.y, player.x, player.y) >= 800:
                self.isIdle = True
                self.isChasing = False
                cur_time = time.get_ticks()
                if cur_time - self.last_update >= walk_cd:
                    if self.stage < 13:
                        self.stage += 1
                        self.last_update = cur_time
                    elif self.stage == 13:
                        self.stage = 0
                        self.last_update = cur_time
            else:
                self.isIdle = False
                self.isChasing = True
        elif self.type == 2 or self.type == 3:
            if distance(self.x, self.y, player.x, player.y) <= 700:
                self.isIdle = True
                self.isChasing = False
                cur_time = time.get_ticks()
                if cur_time - self.last_update >= walk_cd:
                    if self.stage < 13:
                        self.stage += 1
                        self.last_update = cur_time
                    elif self.stage == 13:
                        self.stage = 0
                        self.last_update = cur_time
            else:
                self.isIdle = False
                self.isChasing = True
            
    #direction of the imposter depending on where the player is
    def direction(self, player):
        if player.x <= self.x:
            self.dir = 1
        elif player.x > self.x:
            self.dir = 0

    #draws the imposters according to size and direction
    def draw(self, screen):
        cur_time = time.get_ticks()
        if self.type != 5:
            if self.isIdle == True:
                screen.blit(self.idlePic[self.dir], (self.x - 83 * self.size, self.y - 72 * self.size), area = Rect((self.stage * 166 * self.size, 0, 166 * self.size, 236 * self.size)))
            if self.isIdle == False:
                screen.blit(self.chasePic[self.dir], (self.x - 110 * self.size, self.y - 131 * self.size), area = Rect((self.stage * 221 * self.size, 0, 221 * self.size, 290 * self.size)))
        else: #for if the imposter is a ghost (type 5)
            screen.blit(self.ghost[self.dir], (self.x - 83 * self.size, self.y - 72 * self.size))
        if self.type == 4:
            draw.rect(screen, (255, 0, 0), (140, 900, self.health / 2, 40), 0, 4) #draws boss healthbar
        draw.rect(screen, (0), (140, 900, 1000, 40), 1, 4)

        #draws all the imposter created objects: orbs, waves, lasers, and spikes
        for spk in self.spk:
            draw.line(screen, (0), (self.x, self.y), (spk[2], spk[3]), 5)
        for laser in self.laser:
            draw.line(screen, (0, 0, 255), (self.x, self.y), (laser[0], laser[1]), 5)
        for orb in self.orbs:
            draw.circle(screen, (0, 255, 0), (orb[0], orb[1]), 15)
        for wave in self.wave:
            draw.circle(screen, (255, 0, 0), (wave[0], wave[1]), 20)

class Node: #for electrical nodes
    def __init__(self, x, y, col):
        #node attributes
        self.x = x
        self.y = y
        self.color = col
        self.last_tagged = time.get_ticks() #when it was tagged
        self.isTagged = False
        self.isLinked = False

    #function for the player tagging the nodes
    #detects if the player is close enough to tag it and sets the time for when it was tagged
    #if the time tagged exceeds the tag time allowed (3 seconds) it will no longer be tagged.
    def interact(self, player):
        cur_time = time.get_ticks()
        tag_timer = 3000
        if cur_time - self.last_tagged >= tag_timer:
            self.isTagged = False
        if self.isLinked == False:
            if distance(player.x, player.y, self.x, self.y) < 80:
                self.isTagged = True
                self.last_tagged = cur_time

    #function for linking the nodes, returns True if both the nodes tagged are the same color otherwise return False
    def link(self, node2):
        if self.isTagged == True and node2.isTagged == True and self.color == node2.color:
            return True
        else:
            return False

    #function for resetting the nodes for if ever the player dies
    def reset(self):
        self.isTagged = False
        self.isLinked = False

    #draws the nodes are small circles if not tagged, if tagged draws a line to the player and if linked draws a line to the other connected node
    def draw(self, screen, player, node2):
        draw.circle(screen, self.color, (self.x, self.y), 20)
        if self.isTagged == True:
            draw.line(screen, self.color, (self.x, self.y), (player.x, player.y), 10)
        if self.isLinked == True and self.color == node2.color:
            draw.line(screen, self.color, (self.x, self.y), (node2.x, node2.y), 10)

#distance function       
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

#angle function 1, this is used mostly for the rotation of images and is different from angle function 2
def angle(x1, y1, x2, y2):
    deg = degrees(acos((x2 - x1)/distance(x1, y1, x2, y2)))
    if y2 > y1:
        deg = 360 - deg
    return deg

#angle function 2, this is mainly used for the direction of objects like player/item's shootDir and the boss's slamDir
def angle2(x1, y1, x2, y2):
    deg = degrees(acos((x2 - x1)/distance(x1, y1, x2, y2)))
    if y2 > y1:
        deg = 360 - deg
    deg += 180
    if deg > 360:
        deg -= 360
    return deg

#function that returns number of nodes that are currently tagged
def numNodes():
    num =0
    for nod in node:
        if nod.isTagged == True:
            num += 1
    return num

#function that returns the number of nodes that are linked
def numLinked():
    num = 0
    for nod in node:
        if nod.isLinked == True:
            num += 1
    return num

#function that deals with the playerDeath
#its main function is to respawn enemies, reset the crewmate and reset nodes (if in level 2)
def playerDeath(imp):
    imposter.clear()
    if level == 1:
        mixer.music.stop()
        mixer.music.load("Sounds/Into The Fire.mp3")
        mixer.music.set_volume(0.5)
        mixer.music.play()
        for i in range(len(imposters[level - 1][wave])):
            imposter.append(Imposter(impPic, imposters[level - 1][wave][i][0], imposters[level - 1][wave][i][1], imposters[level - 1][wave][i][2], imposters[level - 1][wave][i][3]))
    elif level == 2:
        mobs = randint(0, 7)
        for i in range(mobs):
            typ = randint(0, 2)
            imposter.append(Imposter(impPic, randint(100, 1100), 650, 0, typ))
    elif level == 3:
        mixer.music.stop()
        mixer.music.load("Sounds/Versus.mp3")
        mixer.music.set_volume(1)
        mixer.music.play()
        imposter.append(Imposter(impPic, 400, 650, 0, 4))
    crewmate.reset()

#function for swapping 2 values           
def swap(val1, val2):
    return [val2, val1]

#function that draws the background of everything, the player, and the enemies
def drawBack(screen, crewmate, imposter, item, shake, status):
    screen.fill((255, 255, 255))
    if status == 1:
        if level == 1:
            screen.blit(hallway, ((7 - wave) * (-1330) - 435 + shake[0], shake[1] - 299))
            screen.blit(lvl1obj, (1280 - lvl1obj.get_width(), 0))
        elif level == 2:
            screen.blit(electrical, (-188 + shake[0], shake[1] - 299))
            screen.blit(lvl2obj, (1280 - lvl2obj.get_width(), 0))
        elif level == 3:
            screen.blit(reactor, (-104 + shake[0], -180 + shake[1]))
            screen.blit(lvl3obj, (1280 - lvl3obj.get_width(), 0))
        for imps in imposter:
            imps.draw(screen)
        crewmate.draw(screen)
        if level == 2:
            for n in range(len(node) - 1):
                node[n].draw(screen, crewmate, node[n + 1])
        item.draw(screen, crewmate)
        screen.blit(emblem[item.weapon], (0, 0))
    elif status == -1:
        screen.blit(dead, (0, 0))
    elif status == 0:
        screen.blit(title, (0, 0))
    elif status == 0.1:
        screen.blit(obj, (0, 0))
    elif status == 0.2:
        screen.blit(tips, (0, 0))
    elif status == 0.4:
        screen.blit(fun, (0, 0))
    elif status == 0.8:
        screen.blit(credit, (0, 0))
    display.flip()

init()
mixer.init()
mixer.music.set_volume(0.1)
mixer.set_num_channels(16)
screen = display.set_mode((1280, 960))

#loads all the images
pic = image.load("AmongUs/pic.png").convert_alpha() 
for i in range(10):
    pistol.append(image.load("Pistol/Pistol" + str(i) + ".png").convert_alpha())
    
for j in range(5):
    plt.append(image.load("shot/sg" + str(j) + ".png").convert_alpha())
    blt.append(image.load("shot/p" + str(j) + ".png").convert_alpha())
    lsr.append(image.load("shot/l" + str(j) + ".png").convert_alpha())
    bPlt.append(image.load("shot/b" + str(j) + ".png").convert_alpha())
bullets = [blt, lsr, plt, bPlt]

sgPic = image.load("AmongUs/shotgun.png").convert_alpha()
impIdle = image.load("AmongUs/impIdle.png").convert_alpha()
impChase = image.load("AmongUs/impChase.png").convert_alpha()
ghost = image.load("AmongUs/ghost.png").convert_alpha()
impPic = [impIdle, impChase, ghost]
hallway = image.load("AmongUs/hallway.png").convert()
electrical = image.load("AmongUs/electrical.png").convert()
knife = image.load("AmongUs/knife.png").convert_alpha()
reactor = image.load("AmongUs/reactor.png").convert()
dead = image.load("AmongUs/dead.png").convert_alpha()
title = image.load("AmongUs/title.png").convert()
tips = image.load("AmongUs/Combos.png").convert()
obj = image.load("AmongUs/info.png").convert()
credit = image.load("AmongUs/credits.png").convert()
lvl1obj = image.load("Obj/Contaminant.png").convert()
lvl2obj = image.load("Obj/Electrical.png").convert()
lvl3obj = image.load("Obj/Survive.png").convert()
pEmblem = image.load("AmongUs/pEmblem.png").convert_alpha()
sgEmblem = image.load("AmongUs/sgEmble.png").convert_alpha()
emblem = [pEmblem, sgEmblem]
fun = image.load("AmongUs/fun.png").convert()
slide = image.load("AmongUs/slide.png").convert_alpha()
crewPic = [pic, slide]

laser = mixer.Sound("Sounds/laser.wav") #loads the laser sound
laser.set_volume(0.1)

crewmate = Crewmate(crewPic, pX, pY) #constructs the player
item = Item(sgPic, pistol, knife, bullets, pX, pY) #constructs the items and weapons
#imposter.append(Imposter(impPic, 400, 650, 0, 4))
#^ to skip to level 3 and spawn the boss

for i in range(len(imposters[level - 1][wave])): #constructs each of the enemies in the first wave
    imposter.append(Imposter(impPic, imposters[level - 1][wave][i][0], imposters[level - 1][wave][i][1], imposters[level - 1][wave][i][2], imposters[level - 1][wave][i][3]))
for n in nodes[0]: #constructs the nodes
    node.append(Node(n[0], n[1], n[2]))
myClock = time.Clock()
running = True

while running:
    #code below is for user input
    mx, my = mouse.get_pos()
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if status != 1 and status != -1: #if in the menu
            if evt.type == MOUSEBUTTONDOWN:
                if Rect(434, 394, 407, 136).collidepoint((mx, my)) and status == 0:
                    status += 0.1
                elif Rect(766, 341, 370, 190).collidepoint((mx, my)) and status == 0.1:
                    status += 0.1
                elif Rect(766, 341, 370, 190).collidepoint((mx, my)) and status == 0.2:
                    status += 0.2
                elif Rect(163, 683, 970, 200).collidepoint((mx, my)) and status == 0.4:
                    status = 1
                    mixer.music.load("Sounds/Into The Fire.mp3")
                    mixer.music.set_volume(0.5)
                    mixer.music.play(-1)
                elif Rect(18, 831, 170, 90).collidepoint((mx, my)) and status == 0:
                    running = False
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    if status == 0.4:
                        status -= 0.2
                    elif status == 0.2 or status == 0.1:
                        status -= 0.1
                    elif status == 0 or status == 0.8:
                        running = False
        if status == -1: #if in death screen
            if evt.type == KEYDOWN:
                if evt.key == K_r and status == -1:
                    status = 1
                    playerDeath(imposter)
                elif evt.key == K_ESCAPE:
                    running = False
        if status == 1: #if alive
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    cur_time = time.get_ticks()
                    if item.weapon == 0:
                        if cur_time - item.pistol_update > 400:
                            item.isShooting = True
                            item.pistol_update = cur_time
                    elif item.weapon == 1:
                        if cur_time - item.sg_update > 300:
                            item.isShooting = True
                            item.sg_update = cur_time
                elif evt.button == 3:
                    if item.weapon == 0: #laser starts charging
                        item.isCharging = True
                        item.laserStart = (0, 0)
                        item.laserEnd = (0, 0)
                        item.charge_start = time.get_ticks()
            elif evt.type == MOUSEBUTTONUP:
                if evt.button == 3 and item.weapon == 0: #laser ends charging when button is lifted
                    item.isCharging = False
                    item.laser_time = 50
                    shake_time = 40
                    mixer.find_channel(True).play(laser)
                    item.laserStart = (item.gunBarrel[0], item.gunBarrel[1])
                    item.laserEnd = (600 * cos(radians(item.shootDir)) + item.gunBarrel[0], 600 * -sin(radians(item.shootDir)) + item.gunBarrel[1])
            elif evt.type == MOUSEWHEEL: #changing weapons via mouse wheel
                if evt.y < 0:
                    item.weapon += 1
                    if item.weapon == 2:
                        item.weapon = 0
                elif evt.y > 0:
                    item.weapon -=1
                    if item.weapon == -1:
                        item.weapon = 1
            elif evt.type == KEYDOWN:
                if evt.key == K_a:
                    crewmate.isWalking = True
                    crewmate.walkDir = 1
                if evt.key == K_d:
                    crewmate.isWalking = True
                    crewmate.walkDir = 0
                if evt.key == K_s:
                    crewmate.isDashing = True
                if evt.key == K_c:
                    item.isMelee = True
                if evt.key == K_b:
                    item.weapon -=1
                    if item.weapon == -1:
                        item.weapon = 1
                if evt.key == K_LCTRL: 
                    if crewmate.stamina >= 30 and crewmate.y < 700:
                        crewmate.isDescend = True
                        crewmate.stamina -= 30
                    elif crewmate.y >= 700:
                        crewmate.isDescend = True
                if evt.key == K_ESCAPE:
                    running = False
                if evt.key == K_1:
                    item.weapon = 0
                    item.isShooting = False
                elif evt.key == K_2:
                    item.weapon = 1
                    item.isShooting = False
                elif evt.key == K_SPACE and crewmate.isJumping == False and crewmate.jumpCount < 3:
                    if crewmate.shootDir <= 90 or crewmate.shootDir > 270:
                        crewmate.stage = 7
                    elif crewmate.shootDir > 90 and crewmate.shootDir <= 270:
                        crewmate.stage = 4
                    crewmate.momentumY = -20
                    crewmate.jumpCount += 1
                    crewmate.last_jump = time.get_ticks()
                    crewmate.isJumping = True
            elif evt.type == KEYUP:
                if evt.key == K_a and crewmate.walkDir == 1:
                    crewmate.isWalking = False
                elif evt.key == K_d and crewmate.walkDir == 0:
                    crewmate.isWalking = False
                elif evt.key == K_LCTRL and crewmate.y >= 700: #for releasing crouch
                    crewmate.isDescend = False

    #adds all the screen shake produced together for screen offset
    for k in imposter:
        shake[0] = shake[0] + k.shake[0] * 2
        shake[1] = shake[1] + k.shake[1] * 2
        k.shake = [0, 0]
    shake[0] = shake[0] + crewmate.shake[0] * 2 + item.shake[0] #shake is [offset in x, offset in y] that is used to sum all the screen shake to produce the screen offset used when blitting the background
    shake[1] = shake[1] + crewmate.shake[1] * 2 + item.shake[1]
    crewmate.shake = [0, 0]
    item.shake = [0, 0]
    if shake[0] > 0:
        shake[0] -= 1
    if shake[1] > 0:
        shake[1] -= 1
    
    screen_offset = [0, 0]
    if shake != [0, 0]:
        screen_offset[0] = randint(0, shake[0] * 2) - shake[0] #these pieces of screen shake code I based on some parts of this video https://www.youtube.com/watch?v=3nhQLJq0Lwk&
        screen_offset[0] = randint(0, shake[1] * 2) - shake[1]
    
    if status == 1: #if the player is alive run all these functions that make the game work
        crewmate.physics()
        crewmate.gravity()
        crewmate.walk()
        crewmate.jump()
        crewmate.dash()
        crewmate.descend(imposter)
        item.update(crewmate)
        item.bulletPhysics()
        item.bltAnimation()
        item.shoot(crewmate)
        item.melee(crewmate, imposter)
        for imp in imposter: #for each imposter run these functions
            imp.walk(crewmate)
            imp.physics()
            imp.gravity()
            imp.bound()
            imp.dash(crewmate)
            if imp.type == 2: #the black orbs is specialized to only type 2 imposters
                imp.orbPhysics(crewmate, item.shots)
            elif imp.type == 3: #the red orbs is specialized to only type 3 imposters
                imp.wavePhysics(crewmate, item.shots)
            elif imp.type == 4: #the boss combo is specialized to only the boss
                imp.bossCombo(crewmate, item)
            elif imp.type == 5: #the laser is only specialized to the ghost
                imp.ghostLaser(crewmate)
            imp.idle(crewmate)
            imp.direction(crewmate)
            item.bullet(imp, crewmate, item)
            if item.imposterDeath(crewmate, imp):
                if imp.type == 0 or imp.type == 2 or imp.type == 3:
                    spawns = randint(1, 5)
                    if spawns < 4:
                        for i in range(spawns):
                            imposter.append(Imposter(impPic, imp.x + i * 20, 650, imp.dir, 1))
                    else:
                        for i in range(6 - spawns):
                            imposter.append(Imposter(impPic, randint(200, 1000), randint(250,  400), imp.dir, 5))
                shake_time = 12
                imposter.remove(imp)
            if crewmate.die(imp) == True: #if the player dies, go to the death screen, reset all the nodes, and reset the waves
                status = -1
                wave = 0
                node.clear()
                for m in nodes[0]:
                    node.append(Node(m[0], m[1], m[2]))
        if len(imposter) == 0: #if the current wave is cleared
            if level == 1 and crewmate.x <= 100: #for the first level, if the crewmate goes to the left into the next section of the hall, the wave increases and player health replenishes to full
                wave += 1
                item.laserStart = (0, 0)
                item.laser_time = 0
                item.laserEnd = (0, 0)
                crewmate.health = 80
            if wave == 8: #if the wave count reaches 8, that means the player is going to the next level
                level += 1
                crewmate.x = 1100
                wave = 0
            if level == 1 and crewmate.x <= 100: #spawns new wave of imposters once the player enters the next section of the hall
                for i in range(len(imposters[level - 1][wave])):
                    imposter.append(Imposter(impPic, imposters[level - 1][wave][i][0], imposters[level - 1][wave][i][1], imposters[level - 1][wave][i][2], imposters[level - 1][wave][i][3]))
                crewmate.x = 1100
                crewmate.rect = Rect(crewmate.x - 83, crewmate.y - 85, 167, 201)
            elif level == 2: #if it is level 2 and the room has no enemies, spawn a random amount of enemies with random types anywhere in the room
                mobs = randint(1, 4)
                while mobs > 0 and wave < 5:
                    typ = randint(0, 3)
                    if typ == 0 or typ == 2:
                        mobs -= 1
                    if typ == 3:
                        mobs -= 2
                    x = randint(100, 1100)
                    imposter.append(Imposter(impPic, x, 650, 0, typ))

        if level == 2: #block of code that deals with nodes
            for d in range(len(node) - 1):
                    if node[d].isLinked == False: #if the current node in the loop is not linked with anything and the player has no nodes tagged or the player has already tagged a node of the same color,
                        if numNodes() == 0 or node[d].color == nodeTagged.color: #interact with the node and tag it.
                            node[d].interact(crewmate) 
                            nodeTagged = node[d]
                    if node[d].link(node[d + 1]): #checks if each pair of node is linked, if linked, it is no longer tagged
                        node[d].isLinked = True
                        node[d + 1].isLinked = True
                        node[d].isTagged = False
                        node[d + 1].isTagged = False
            if numLinked() == 8: #if the number of linked nodes is 8, clear the node and construct the next wave of nodes
                node.clear()
                wave += 1
                if wave == 5: #if the last wave of nodes is done, kill all the imposters
                    imposter.clear()
                if wave < 5:
                    for m in nodes[wave]:
                        node.append(Node(m[0], m[1], m[2]))
            if wave == 5 and crewmate.x <= 100: #once the last wave of nodes is done and the crewmate has went to the left, the level will increase
                item.laserStart = (0, 0)
                item.laserEnd = (0, 0)
                crewmate.x = 1100
                crewmate.rect = Rect(crewmate.x - 83, crewmate.y - 85, 167, 201)
                level += 1
                mixer.music.stop()
                mixer.music.load("Sounds/Versus.mp3")
                mixer.music.set_volume(1)
                mixer.music.play()
                imposter.append(Imposter(impPic, 400, 650, 0, 4))
                crewmate.health = 80
        if level == 3 and len(imposter) == 0: #once the boss is dead, go to the credits screen
            status = 0.8
            mixer.music.stop()
            level = 1
    drawBack(screen, crewmate, imposter, item, shake, status) #draws everything last
    crewmate.bound()
    myClock.tick(60)
display.flip()
    
quit() 
