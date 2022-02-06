from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height


def main():
    '''
    Testing draw_multiple_line_text
    '''
    #image_width
    size = 128
    fontsize = 32

    all_fonts = ['FreeMono.ttf','FreeSans.ttf','TimesNewRoman.ttf']  


    t = set(["Engineering","Anish Bhetuwal","Abiskar Timsina","Electrical","Engineer","Computer","Object Oriented Programming","Hello","Hello World"])
    image = Image.new('RGB', (size,size), color = (255,255,255))
    

    #TODO: generate random fonts
    #TODO: generate embedding for each character for eg. H E L L O as image so each character has a different embedding.
    for i in t:
        f = random.randint(0,2)
        fo = f"Pillow/Tests/fonts/{all_fonts[f]}"
        font = ImageFont.truetype(fo, fontsize)
        image = Image.new('RGB', (size,size), color = (255,255,255))
        text1 = i
        text_color = (0,0,0)
        random_height = random.randint(0,460)
        text_start_height = random_height
        draw_multiple_line_text(image, text1, font, text_color, text_start_height)
        image.save(f'./dataset/{text1}.jpg')
if __name__ == "__main__":
    main()
