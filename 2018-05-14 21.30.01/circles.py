import os
import shutil
import subprocess
import math

from datetime import datetime
from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import Tuple
from random import randint

@dataclass
class Circle: 
    radius: float
    location: Tuple[int, int]
    angle: int = 0
    fill: str = "black" 

    @property
    def x(self):
        return self.location[0]

    @property
    def y(self):
        return self.location[1]

    def draw(self): 
        DRAW.ellipse((self.x - self.radius, 
                     self.y - self.radius,
                     self.x + self.radius,
                     self.y + self.radius), fill=self.fill)
    
    def step(self):
        step = self.radius
        rad_angle = math.radians(self.angle)
        self.location = (self.x + step*math.cos(rad_angle), 
                         self.y + step*math.sin(rad_angle))

# Get the current time, use it as the directory we save everything in
SAVE_DIR = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
os.mkdir(SAVE_DIR)
shutil.copy(__file__, SAVE_DIR)  # Save a copy of this script so that we can recreate stuff

# The size of the image
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1000
# Create a new image
CURRENT_IMAGE = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
DRAW = ImageDraw.Draw(CURRENT_IMAGE)

# Missing: initial setup
circles = []
for _ in range(100):
    rad = randint(1, 20)
    x = randint(0, IMAGE_WIDTH)
    y = randint(0, IMAGE_HEIGHT)
    circles.append(Circle(rad, (x, y), angle=randint(0, 360)))

# How many iterations?
MAX_ITERATIONS = 100
# The main loop, mess with the image for each iteration
for i in range(MAX_ITERATIONS):
    for circle in circles:
        circle.draw()
        circle.step()
    # Manipulate the image before saving it
    CURRENT_IMAGE.save(os.path.join(SAVE_DIR, "{}.png".format(i)))

    # Every so often print out something so we get a sense of progress
    if i % 10 == 0:
        print('Iteration {}'.format(i), flush=True)


def gifit(image_loc, gif_name, fps=12):
    """ Creates a GIF from all the pngs in the provide image_loc """
    import glob
    import moviepy.editor as mpy

    os.chdir(image_loc)
    file_list = glob.glob('*.png')
    list.sort(file_list, key=lambda x: int(x.split('.png')[0]))
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{}.gif'.format(gif_name), fps=fps)


gifit(SAVE_DIR, 'final')
subprocess.run('start final.gif', shell=True)