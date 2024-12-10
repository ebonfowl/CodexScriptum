from PIL import Image, ImageDraw, ImageFont
from random import randint

img = Image.open("C:/Users/acampitelli/Pictures/CofI_HowlingYote.png")
# img.show()
WIDTH, HEIGHT = img.size

#font = ImageFont.truetype("C:/Windows/Fonts/BRITANIC.ttf", 7)
font = ImageFont.truetype("C:/Windows/Fonts/ARIAL.ttf", 8)
cell_width, cell_height = 8, 8

img = img.resize((int(WIDTH / cell_width), int(HEIGHT / cell_height)), Image.NEAREST)
new_width, new_height = img.size
img = img.load()

new_img = Image.new('RGB', (WIDTH, HEIGHT), ("#836088"))
d = ImageDraw.Draw(new_img)

for i in range(new_height):
    for j in range(new_width):
        r, g, b = img[j, i]
#         r, g, b, a = img[j, i] # use this line if you have an image with alpha value
        k = int((r + g + b) / 3)
        if k > 100:
            text = ""
            # d.rectangle((j * cell_width, j * cell_width, i * cell_height, i * cell_height), fill=(255, 0, 0, 128), width = cell_width)
        else:
            value = randint(0, 2)
            if value == 1:
                text = "1"
            else:
                text = "0"
        d.text((j * cell_width, i * cell_height), text=text, font=font, fill=("white"))

new_img.show()
new_img.save("C:/Users/acampitelli/Pictures/CofI_HowlingYote_binary.png")