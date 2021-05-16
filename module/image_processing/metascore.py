import cv2 as cv2
import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

## DIMSNESIONS OF THE IMAGE
## THAT WE WANT TO GENERATE
IMAGE_WIDTH = 192
IMAGE_HEIGHT = 192
IMAGE_DIM = (IMAGE_WIDTH, IMAGE_HEIGHT)

## THE BACKGROUND COLORS FOR THE DIFFERENT
## TYPES OF RECOMMENDATIONS THAT WE HAVE
BACKGROUND_COLOR_OUTSTANDING = (102, 204, 51)
BACKGROUND_COLOR_MIXED = (255, 204, 51)
BACKGROUND_COLOR_BAD = (255, 0, 0)

## VALUES FOR WHEN THE BACKGROUND
## COLORS SHOULD BE CHANGED
OUTSTANDING_MINIMUM_VALUE = 75
TERRIBLE_MAXIMUM_VALUE = 40

## SETTINGS FOR THE FONT
## BASED ON WEBSITE OF METACRITIC
FONT_FAMILY = 'arialbd.ttf'
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 68

def create_meta_score(score):

    # initialize the default 
    # font and text for the image
    font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)
    text = str(round(score))

    # create an empty image with    
    # the correct background color 
    # based on the score that has beensa
    # provided
    if score >= OUTSTANDING_MINIMUM_VALUE:
        image = Image.new('RGB', IMAGE_DIM, BACKGROUND_COLOR_OUTSTANDING)
    elif score >= TERRIBLE_MAXIMUM_VALUE:
        image = Image.new('RGB', IMAGE_DIM, BACKGROUND_COLOR_MIXED)
    else:
        image = Image.new('RGB', IMAGE_DIM, BACKGROUND_COLOR_BAD)

    # create drawable object
    # and calculate the size of
    # the text that we want to place
    # in the image
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    
    # Draw score in the 
    # center of the image
    offsetX = (IMAGE_WIDTH - width) * 0.5
    offsetY = (IMAGE_HEIGHT - height) * 0.5
    draw.text((offsetX, offsetY), text, fill=FONT_COLOR, font=font)

    # Convert PIL to cv2 image object and return
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def game_not_found():

    # initialize the default 
    # font and text for the image
    font = ImageFont.truetype(FONT_FAMILY, int(FONT_SIZE * 0.5))
    text = "404\n Not Found"

    # Create ERROR image with bad background
    image = Image.new('RGB', IMAGE_DIM, BACKGROUND_COLOR_BAD)
    draw = ImageDraw.Draw(image)

    # calculate line properties
    # for easy acess in the loop
    line_height = 10
    lines = text.splitlines()
    line_offset = (IMAGE_HEIGHT / len(lines)) - line_height

    # Write each line of the message
    # in the center of the image
    for line in lines:
        width, height = draw.textsize(line, font=font)
        offsetX = (IMAGE_WIDTH - width) * 0.5
        offsetY = (line_offset - height)
        
        draw.text((offsetX, offsetY), line, fill=FONT_COLOR, font=font)
        line_offset += height + line_height
    
    # Convert PIL to cv2 image object and return
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def game_not_rated():

    # initialize the default 
    # font and text for the image
    font = ImageFont.truetype(FONT_FAMILY, int(FONT_SIZE * 0.5))
    text = "Not Rated"

    # Create ERROR image with mixed background
    image = Image.new('RGB', IMAGE_DIM, BACKGROUND_COLOR_MIXED)

    # create drawable object
    # and calculate the size of
    # the text that we want to place
    # in the image
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)

    # Draw message in the 
    # center of the image
    offsetX = (IMAGE_WIDTH - width) * 0.5
    offsetY = (IMAGE_HEIGHT - height) * 0.5
    draw.text((offsetX, offsetY), text, fill=FONT_COLOR, font=font)
    
    # Convert PIL to cv2 image object and return
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
