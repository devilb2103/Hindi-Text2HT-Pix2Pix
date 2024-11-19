import os
import re
import cv2
import torch
import numpy as np
import torch.nn as nn
from tqdm import tqdm
import albumentations as A
import torch.optim as optim
import matplotlib.pyplot as plt
from Generator import Generator
from utils import load_checkpoint
from torch.utils.data import DataLoader
from albumentations.pytorch import ToTensorV2
from PIL import Image, ImageDraw, ImageFont, features

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LEARNING_RATE = 2e-4
# MODEL_DIR = "Projects\\Pix2Pix Tex2HT\\Models\\gen.pth.tar"
MODEL_DIR = "Models\\gen.pth.tar"

gen = Generator(in_channels=1, features=64).to(DEVICE)
gen.eval()
opt_gen = optim.Adam(gen.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))
load_checkpoint(os.path.normpath(os.path.join(os.getcwd(), MODEL_DIR)), gen, opt_gen, LEARNING_RATE, device=DEVICE)
transform_only_input = A.Compose([A.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], max_pixel_value=255.0,), ToTensorV2(),])
font_path = os.path.join(os.path.dirname(__file__), "Fonts\\Amiko-Regular.ttf")

def text_to_image(text, font_path, height=100, padding=10):
    font = ImageFont.truetype(font_path, size=90, layout_engine=ImageFont.Layout.RAQM)
    temp_image = Image.new("L", (1, 1), color=255)
    draw = ImageDraw.Draw(temp_image)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width = text_width + 2 * padding
    image_height = height
    image = Image.new("L", (image_width, image_height), color=255)
    draw = ImageDraw.Draw(image)
    text_position = (padding, (image_height - text_height) // 2)
    draw.text(text_position, text, font=font, fill=0)
    return image

def resize_and_pad(image, target_size=(256, 256)):
    original_size = image.size
    ratio = min(target_size[0] / original_size[0], target_size[1] / original_size[1])
    new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
    new_image = Image.new("L", target_size, color=255)
    top_left_x = (target_size[0] - new_size[0] + 10) // 2  # Horizontal center
    top_left_y = (target_size[1] - new_size[1]) // 2  # Vertical center
    new_image.paste(resized_image, (top_left_x, top_left_y))
    return new_image

def createImg(word, font_path):
    image = text_to_image(word, font_path)
    image = resize_and_pad(image)
    return image

def convertImg(img: Image) -> Image:
    img = np.asarray(img)
    img = transform_only_input(image=img)["image"]
    img = img.unsqueeze(0)
    x = img.to(DEVICE)
    with torch.amp.autocast('cuda'):
        y_fake = gen(x)
    y_fake_np = (y_fake[0].detach().cpu().numpy()[0] * 255).clip(0, 255).astype(np.uint8)
    return y_fake_np

def crop_and_resize(img_array, target_height):
    # Step 1: Find the bounding box of non-white regions
    # Assuming white is represented as 255 and black text as 0
    _, binarized_image = cv2.threshold(img_array, 128, 255, cv2.THRESH_BINARY)  # Adjust threshold as needed

    coords = np.column_stack(np.where(binarized_image < 255))  # Find non-white pixels
    if coords.size == 0:
        # If there is no black content, return the original or a blank target-sized image
        return np.full((target_height, int(target_height * img_array.shape[1] / img_array.shape[0])), 255, dtype=np.uint8)
    
    # Get the bounding box for the non-white pixels
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    # Crop the image using the bounding box
    cropped_image = img_array[y_min:y_max + 1, x_min:x_max + 1]

    # Step 2: Resize while maintaining aspect ratio based on target height
    h, w = cropped_image.shape
    aspect_ratio = w / h
    target_width = int(target_height * aspect_ratio)
    
    # Resize the cropped image to the target height
    resized_image = cv2.resize(cropped_image, (target_width, target_height), interpolation=cv2.INTER_AREA)
    
    return resized_image

def getWordImage(word, max_height=256):
    min_height = round((max_height * 200) / 256)
    image = createImg(word, font_path)
    image = convertImg(image)
    contains_matras_above_shirorekha = any(char in ['ि', 'ै', 'ी', 'े', 'ृ'] for char in word)
    image = crop_and_resize(image, max_height if contains_matras_above_shirorekha else min_height)
    return image

def filter_hindi_letters(sentence):
    # Regular expression to match only Hindi letters and spaces
    hindi_letters_only = re.sub(r'[^\u0900-\u097F\s]+', '', sentence)
    return hindi_letters_only

def place_words_on_canvas(font_size, sentence, canvas_width, debug=False):

    words = filter_hindi_letters(sentence).split()
    word_images = []
    for word in words:
        word_images.append(np.asarray(getWordImage(word, max_height=font_size)))

    # Start with an initial canvas height

    def setRatio(line_height, num):
        return round(line_height * (num / 256))
    

    line_height = font_size
    x_offset, y_offset = setRatio(line_height, 60), setRatio(line_height, 60)
    idx = 0
    
    canvas = Image.new('L', (canvas_width, line_height + setRatio(line_height, 120)), 255)  # 'L' mode for grayscale
    
    for word_img in word_images:
        contains_matras_above_shirorekha = any(char in ['ि', 'ै', 'ी', 'े', 'ृ'] for char in words[idx])
        word_pil = Image.fromarray(word_img)
        # if debug:
        #     word_pil = add_green_borders(word_pil)
        word_width, word_height = word_pil.size

        # Check if the word exceeds the current canvas width and needs a new line
        if x_offset + word_width > canvas_width:
            x_offset = setRatio(line_height, 60)
            y_offset += line_height + np.random.randint(setRatio(line_height, 30), setRatio(line_height, 60))

            # Dynamically expand the canvas height if the new line goes beyond the current canvas height
            if y_offset + line_height > canvas.height:
                new_height = canvas.height + line_height + np.random.randint(setRatio(line_height, 30), setRatio(line_height, 60)) + setRatio(line_height, 56)
                new_canvas = Image.new('L', (canvas_width, new_height), 255)
                new_canvas.paste(canvas, (0, 0))
                canvas = new_canvas

        # Paste the word image onto the canvas
        canvas.paste(word_pil, (x_offset, y_offset if contains_matras_above_shirorekha else y_offset + setRatio(line_height, 56)))
        x_offset += word_width + np.random.randint(setRatio(line_height, 45), setRatio(line_height, 45) + (word_width * 0.1))
        
        idx += 1
    return canvas

print(np.asarray(getWordImage("खनिज")))
