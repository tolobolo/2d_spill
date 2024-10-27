
import pygame
from random import randint
from enum import Enum, auto



WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
screen_height = 1000
screen_width = 1000


def split_into_chunks(n, x):
    # Full chunks
    full_chunks = n // x

    # Remainder after full chunks
    remainder = n % x

    # Create the list of chunks
    chunks = [x] * full_chunks  # full chunks of size x

    # Add the remainder chunk
    if remainder > 0:
        chunks.append(remainder)

    # If you want to pad with 0s to match a fixed number of chunks (like in the example of 5)
    while len(chunks) < 3:
        chunks.append(0)

    return chunks

class Player_Life:
    width = 50
    height = 50
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.life = 12
        self.max_life = self.life
        self.name = name
        self.rec = (self.x , self.y, self.width, self.height)
        self.hearts = [
            pygame.image.load(f"heart_{i}.png").convert_alpha() for i in range(5)
        ]
        self.dead: bool = False

    def increase(self):
        self.life += 1
        self.life = min(self.max_life, self.life)

    def decrease(self):
        self.life -= 1
        if life < 0:
            self.dead  = True
        return self.dead


    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        for idx, heart_idx in enumerate(split_into_chunks(self.life, 4)):
            image = self.hearts[heart_idx]

            scaled_image = pygame.transform.scale(image, (self.width, self.height) )

            x = self.x + (self.width * idx)

            self.rec = screen.blit(scaled_image, (x, self.y))

class Nothing:
    width = 30
    height = 30
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, BLACK, self.rec)

class Tower:
    width = 60
    height = 90

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = name
        self.image = pygame.image.load("tower.png")
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        self.rec = screen.blit(self.scaled_image, (self.x, self.y))

class Enemy:
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.last_pos = [(self.x, self.y)]
        self.speed = 2
        self.target_y = randint(0, screen_height - self.height)
        self.target_x = randint(0, screen_width - self.width)
        self.life = 10

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
            self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, WHITE, self.rec)

    def movement_enemy(self, objects, p_x, p_y):
        distance_player = ((self.x - p_x)**2 + (self.y - p_y)**2)**0.5

        if abs(distance_player) < 80 + self.width:
            self.target_x = p_x
            self.target_y = p_y

        distance_x = self.target_x - self.x
        distance_y = self.target_y - self.y

        if abs(distance_x) > self.speed / 2 and abs(distance_y) > self.speed / 2:
            if abs(distance_x) >= abs(distance_y):
                if distance_x > 0:
                    self.x += self.speed
                else:
                    self.x -= self.speed
            else:
                if distance_y > 0:
                    self.y += self.speed
                else:
                    self.y -= self.speed
        else:
            self.target_y = randint(0, screen_height - self.height)
            self.target_x = randint(0, screen_width - self.width)

        self.rec = pygame.Rect(self.x, self.y,self.width, self.height)

        for obj in objects:
            if isinstance(obj, (Wall, Chest, Tower)):
                if self.rec.colliderect(obj.rec):
                        dx =self.rec.centerx - obj.rec.centerx
                        dy = self.rec.centery - obj.rec.centery

                        if abs(dx) > abs(dy):
                            if dx > 0:
                                self.x = obj.rec.right
                            else:
                                self.x = obj.rec.left - self.rec.width
                        else:
                            if dy > 0:
                               self.y = obj.rec.bottom
                            else:
                                self.y = obj.rec.top - self.rec.height

            if isinstance(obj, (Player)):
                if self.rec.colliderect(obj.sword_rec):
                    print("pogo")
                    self.life -= 10


                      #  print(self, "collided with ", obj)

class Wall:
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load("wall.png")
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))

    def __str__(self):
        return self.name


    __repr__ = __str__

    def draw(self):
        self.rec = screen.blit(self.scaled_image, (self.x, self.y))

class Chest:
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        image = pygame.image.load("chest.png")
        self.scaled_image = pygame.transform.scale(image, (self.width, self.height))

    def draw(self):
        self.rec = screen.blit(self.scaled_image, (self.x, self.y))

    def __str__(self):
        return self.name

    __repr__ = __str__

class Direction(Enum):
    XPLUS = auto()
    XMINUS = auto()

class Player:
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.speed = 5
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colliding = []
        self.hearts = Player_Life("Life: " + self.name, 30, 30)
        self.keydown = False
        #attack variabler

        self.direction = "x+"
        self.sword_image = pygame.image.load(f"sword_{self.direction}.png")
        self.sword_rec = self.sword_image.get_rect(midleft = self.rec.midleft)
        self.sword_image = pygame.image.load("sword_x+.png")


        self.show_sword = False

    def __str__(self):
        return self.name

    __repr__ = __str__

    def update_life(self, objects):

        for obj in objects:
            if isinstance(obj, Enemy):
                if self.rec.colliderect(obj.rec):
                   # print(self, "collided with", obj)

                    if obj not in self.colliding:
                        self.hearts.decrease()
                        self.colliding.append(obj)

                else:
                    if obj in self.colliding:
                        self.colliding.remove(obj)

            if isinstance(obj, Chest):
                if self.rec.colliderect(obj.rec):
                   # print(self, "collided with ", obj)

                    if obj not in self.colliding:
                        self.hearts.increase()
                        self.colliding.append(obj)

                else:
                    if obj in self.colliding:
                        self.colliding.remove(obj)

        return self.hearts.life

    def update_pose(self, objects):
        new_background = False
        button = pygame.key.get_pressed()

        if button[pygame.K_a]:
            self.x -= self.speed
            self.direction = "x-"
        if button[pygame.K_d]:
            self.x += self.speed
            self.direction = "x+"
        if button[pygame.K_w]:
            self.y -= self.speed
            self.direction = "y-"
        if button[pygame.K_s]:
            self.y += self.speed
            self.direction = "y+"
        if button[pygame.K_SPACE]:
            self.show_sword = True




        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)


        for obj in objects:

            if isinstance(obj, Wall):
                if self.rec.colliderect(obj.rec):
                    dx =self.rec.centerx - obj.rec.centerx
                    dy = self.rec.centery - obj.rec.centery

                    if abs(dx) > abs(dy):
                        if dx > 0:
                            self.x = obj.rec.right
                        else:
                            self.x = obj.rec.left - self.rec.width
                      #  print(self, "collided with ", obj)
                    else:
                        if dy > 0:
                         self.y = obj.rec.bottom
                        else:
                            self.y = obj.rec.top - self.rec.height
                       # print(self, "collided with ", obj)

            elif isinstance(obj, Tower):
                if self.rec.colliderect(obj.rec):
                       # print(self, "collided with", obj)
                        new_background = True

        return new_background

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, self.rec)

        if self.show_sword:
            self.sword_image = pygame.image.load(f"sword_{self.direction}.png")
            self.sword_image = pygame.transform.scale_by(self.sword_image,0.3)
            if self.direction == "x+":
                self.sword_rec = self.sword_image.get_rect(midleft = self.rec.midleft)
                self.sword_rec = screen.blit(self.sword_image, self.sword_rec)
            if self.direction == "x-":
                self.sword_rec = self.sword_image.get_rect(midright = self.rec.midright)
                self.sword_rec = screen.blit(self.sword_image, self.sword_rec)
            if self.direction == "y+":
                self.sword_rec = self.sword_image.get_rect(midtop = self.rec.midtop)
                self.sword_rec = screen.blit(self.sword_image, self.sword_rec)
            if self.direction == "y-":
                self.sword_rec = self.sword_image.get_rect(midbottom = self.rec.midbottom)
                self.sword_rec = screen.blit(self.sword_image, self.sword_rec)

def create_world(name: str):

    kart = open(name, "r")
    all_objects = []
    enemies = []
    walls = []
    chests = []
    towers = []
    nothings = []
    x = 0
    y = 0
    player = None

    if name.startswith("tower"):
        background_image = pygame.image.load("tower.background.png")
    else:
        background_image = pygame.image.load("main.background.jpg")

    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    for line in kart.readlines():
        y += 30
        x = 0
        for col in line:
            x += 30
            if col == ".":
                continue
            elif col == "N":
                nothing = Nothing("nothing" + str(x) + str(y), x, y)
                nothings.append(nothing)
                all_objects.append(nothing)
            elif col == "P":
                player = Player("player" + str(x) + str(y), x, y)
                all_objects.append(player.sword_rec)
                all_objects.append(player)
            elif col == "X":
                wall = Wall("wall " + str(x) + str(y), x, y)
                walls.append(wall)
                all_objects.append(wall)
            elif col == "C":
                chest = Chest("chest " + str(x) + str(y), x, y)
                chests.append(chest)
                all_objects.append(chest)
            elif col == "E":
                enemy = Enemy("enemy " + str(x) + str(y), x, y)
                enemies.append(enemy)
                all_objects.append(enemy)
            elif col == "T":
                tower = Tower("tower " + str(x) + str(y), x, y)
                towers.append(tower)
                all_objects.append(tower)

    if player is None:
        raise RuntimeWarning("player must be in the map")

    return enemies, walls, chests, all_objects, player, towers, kart, background_image, nothings


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    tekst_size = pygame.font.Font(None, 60)

    new_background = False

    enemies, walls, chests, all_objects, player, towers, kart, background_image, nothings = create_world("world.map")

    running = True
    while running:

        tekst = tekst_size.render(f"player, {player.direction}", True, RED)
        tekst_rect = tekst.get_rect(center = (240, 30))
        screen.blit(background_image, (0, 0))

        if new_background:

            enemies, walls, chests, all_objects, player, towers, kart, background_image, nonthings = create_world("tower.map")
            crashable_objects = walls + chests + towers

        screen.blit(background_image, (0, 0))
        screen.blit(tekst, tekst_rect )

        if player.hearts.dead:
            tekst = tekst_size.render("GAME OVER", True, RED)
            tekst_rect = tekst.get_rect(center = (240, 30))
            screen.blit(tekst, tekst_rect )
            enemies, walls, chests, all_objects, player, towers, kart, background_image, nonthings = create_world("world.map")
            player.hearts.dead = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        for chest in chests:
            chest.draw()
        for wall in walls:
            wall.draw()
        enemies = [enemy for enemy in enemies if enemy.life > 0]
        for obj in all_objects[:]:
            if isinstance(obj, Enemy):
                if obj.life <= 0:
                    all_objects.remove(obj)

        for enemy in enemies:
            enemy.movement_enemy(all_objects, player.x, player.y)
            enemy.draw()
        for tower in towers:
            tower.draw()
        for nothing in nothings:
            nothing.draw()

        new_background = player.update_pose(all_objects)
        life = player.update_life(all_objects)
        player.draw()
        player.hearts.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(60)
