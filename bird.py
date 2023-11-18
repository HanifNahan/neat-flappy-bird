import pygame, os, math

bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))), 
               pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))), 
               pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))]

class Bird:
  images = bird_images
  max_rotation = 25
  rotation_velocity = 20
  animation_time = 3

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.tilt = 0
    self.tick_count = 0
    self.velocity = 0
    self.height = self.y
    self.image_count = 0
    self.image = self.images[0]

  def jump(self):
    self.velocity = -10.5
    self.tick_count = 0
    self.height = self.y

  def move(self):
    self.tick_count += 1
    d = self.velocity*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
    if d >= 16:
      d = 16
    if d < 0:
      d -= 2
    self.y = self.y + d
    if d < 0 or self.y < (self.height + 50) :
      if self.tilt < self.max_rotation:
        self.tilt = self.max_rotation
    else:
      if self.tilt > -90:
        self.tilt = self.rotation_velocity
  
  def draw(self, win):
    self.image_count += 1
    if self.image_count < self.animation_time:
        self.image = self.images[0]
    elif self.image_count < self.animation_time * 2:
        self.image = self.images[1]
    elif self.image_count < self.animation_time * 3:
        self.image = self.images[2]
    elif self.image_count < self.animation_time * 4:
        self.image = self.images[1]
    elif self.image_count < self.animation_time * 4 + 1:
        self.image = self.images[0]
        self.image_count = 0

    # if self.tilt < 90:
    #     self.tilt += self.rotation_velocity

    if self.tilt <= -80:
        self.image = self.images[1]
        self.image_count = self.animation_time * 2

    rotated_image = pygame.transform.rotate(self.image, self.tilt)
    new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
    win.blit(rotated_image, new_rect.topleft)


  def get_mask(self):
    return pygame.mask.from_surface(self.image)