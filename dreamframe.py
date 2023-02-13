#! /usr/bin/env python
import sys, random, argparse
import time
import requests
import io
import base64
from PIL import Image, ImageDraw, ImageFont

class New_Class(object):
    pass

def sentence_generator(rules, symbol, non_terminal, sentence):
    rand_count={}           #stores rule as value, key is the cumulative probability of the rule
    #for writing tree structure
    #base case
    if symbol not in non_terminal.keys():
        sentence.append(symbol)
    else:
        total_count = float(non_terminal[symbol])
        current_count=0
        #find all rules applicable for given non-terminal symbol
        for rule in rules:
            if rule[1]==symbol:
                current_count = current_count + float(rule[0])/total_count
                rand_count[current_count] = rule
        r = random.random()
        apply_rule = []
        #select rule according to the number generated and probabilities calculated
        for prob in sorted(rand_count.keys()):
            if prob >= r:
                apply_rule = rand_count[prob]
                break
        for s in apply_rule[2:len(apply_rule)]:
            sentence_generator(rules,s,non_terminal,sentence)  #extra space for bracket

def add_text_to_image(draw, image_height, epd_width, title_text="", artist_text="",
                        title_location= 25,
                        artist_location=5,
                        padding=5,
                        opacity=100,
                        title_size=25,
                        artist_size=15):

    title_font = ImageFont.truetype('/usr/share/fonts/droid/DroidSansMono.ttf', size=title_size)
    artist_font = ImageFont.truetype('/usr/share/fonts/droid/DroidSansMono.ttf', size=artist_size)
    # proceed flag only to be set if set by prerequisite requirements
    proceed = False

    title_box = (0, image_height, 0, image_height)

    if title_text != "" and title_text is not None:
        title_box = draw.textbbox((epd_width / 2, image_height - title_location),
                                    title_text, font=title_font, anchor="mb")
        proceed = True

    artist_box = title_box

    if artist_text != "" and artist_text is not None:
        artist_box = draw.textbbox((epd_width / 2, image_height - artist_location),
                                    artist_text, font=artist_font, anchor="mb")
        proceed = True


    draw_box = max_area([artist_box, title_box])
    draw_box = tuple(sum(x) for x in zip(draw_box, (-padding, -padding, padding, padding)))
    
    draw_box = min_area([(0, 0, epd_width, image_height), draw_box])

    # Only draw if we previously set proceed flag
    if proceed is True:

        # while (title_box is None or title_box[0] > draw_box[2] - draw_box[0] or title_box[1] > draw_box[3] - draw_box[1]) and title_size > artist_size:
        while (title_box is None or title_box[0] < draw_box[0] or title_box[1] < draw_box[1]) and title_size > artist_size:
            title_font = ImageFont.truetype('/usr/share/fonts/droid/DroidSansMono.ttf', size=title_size)
            title_box = draw.textbbox((epd_width / 2, image_height - title_location),
                                        title_text, font=title_font, anchor="mb")
            title_size -= 1

        draw.rectangle(draw_box, fill=(255, 255, 255, opacity))
        # draw.text((epd_width / 2, image_height - title_location), title_text, font=title_font,
        #             anchor="mb", fill=(0,0,0), stroke_width=1, stroke_fill=(255,255,255))
        # draw.text((epd_width / 2, image_height - artist_location), artist_text, font=artist_font,
        #             anchor="mb", fill=(0,0,0), stroke_width=1, stroke_fill=(255,255,255))

        title_outline = max(2, min(title_size//5, 4))
        artist_outline = max(2, min(artist_size//5, 4))

        draw.text((epd_width / 2, image_height - title_location), title_text, font=title_font,
                    anchor="mb", fill=(255,255,255), stroke_width=title_outline, stroke_fill=(0,0,0))
        draw.text((epd_width / 2, image_height - artist_location), artist_text, font=artist_font,
                    anchor="mb", fill=(255,255,255), stroke_width=artist_outline, stroke_fill=(0,0,0))

    return draw

def min_area(area_list):
    # initialise
    a, b, c, d = area_list[0]

    # find max for each element
    for t in area_list:
        at, bt, ct, dt = t
        a = max(a, at)
        b = max(b, bt)
        c = min(c, ct)
        d = min(d, dt)
    tup = (a, b, c, d)
    return tup

def max_area(area_list):
    # initialise
    a, b, c, d = area_list[0]

    # find max for each element
    for t in area_list:
        at, bt, ct, dt = t
        a = min(a, at)
        b = min(b, bt)
        c = max(c, ct)
        d = max(d, dt)
    tup = (a, b, c, d)
    return tup


def get_image(prompt, path='.', suffix=''):
    url = "http://192.168.50.147:7860"

    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 800,
        "height": 480,
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        # png_payload = {
        #     "image": "data:image/png;base64," + i
        # }
        # response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        # pnginfo = PngImagePlugin.PngInfo()
        # pnginfo.add_text("parameters", response2.json().get("info"))

        title, desc = gen_description(prompt)
        add_text_to_image(ImageDraw.Draw(image, 'RGBA'), 480, 800, title, desc)

        image.save(f'output{suffix}.png')#, pnginfo=pnginfo)

def gen_description(prompt):
    for c in '[]()':
        prompt = prompt.replace(c, '')

    parts = prompt.split(',', 1)
    title = " ".join(parts[0].split())

    desc = ""
    if len(parts) > 1:
        desc = " ".join(parts[1].split())
    return (title, desc)

def main(argv):
    parser = argparse.ArgumentParser(description='Options and Arguments')
    parser.add_argument('g_arg', help="Path of the grammar file to be used")
    parser.add_argument('num_sent', nargs='?',default=1, type=int, help="Number of sentences to be generated (Default: 1)")
    parser.add_argument('prefix', nargs='?', type=str, help="The prefix and location to write the file")
    c = New_Class()
    parser.parse_args(args=argv, namespace=c)
    grammar = open(c.g_arg)

    lines = grammar.readlines()
    rules=[]
    non_terminal={} #stores total of odds of non-terminal symbol which is the key
    for l in lines:
        if l!='\n' and l[0]!='#':
            l_tokens = l.split()
            for token in l_tokens:
                #ignore comments in grammar
                if '#' in token:
                    l_tokens=l_tokens[0:l_tokens.index(token)]
                    break
            rules.append(l_tokens)
            #calculate cumulative probabilities
            if l_tokens[1] not in non_terminal.keys():
                non_terminal[l_tokens[1]] = float(l_tokens[0])
            else:
                non_terminal[l_tokens[1]] += float(l_tokens[0])

    now = int(time.time())
    for i in range(0,c.num_sent):
        sentence = []
        sentence_generator(rules,'ROOT',non_terminal, sentence)
        sen = ' '.join(sentence)
        print(sen)
        get_image(sen, suffix=f'_{now}_{i}')

if __name__ == "__main__":
    main(sys.argv[1:])

