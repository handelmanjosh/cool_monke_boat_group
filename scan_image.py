from PIL import Image, ImageFont, ImageDraw
import os.path
import methods 
import nft_variables
import numpy as np
import random


all_colors = {"red":[((0,11), (350,360))],"orange":[((12,46))],"yellow":[((47,70))],"green":[((71,150))],"light_blue":[((151,196))],"blue":[((197,274))],"pink":[((275,349))]}
base_filename = "pointy"
filename = base_filename + ".jpg"

img = Image.open(filename)

width, height = img.size

data = {"blade":[], "blade_shadow":[], "hilt":[], "pommel":[], "background":[], "border":[]}
#get data on sword color position
for w in range(width):
    for h in range(height):
        color = img.getpixel((w,h))
        color_hsl = methods.rgb_2_hsl(color)
        if color_hsl[2] > 94:
            data["background"].append((w,h))
        elif color_hsl[2] < 5:
            data["border"].append((w,h))
        else:
            if 0 <= color_hsl[0] <= 11 or 350 <= color_hsl[0] <= 360:
                data["hilt"].append((w,h))
            if 151 <= color_hsl[0] <= 274:
                data["blade"].append((w,h))
            if 47 <= color_hsl[0] <= 70:
                data["pommel"].append((w,h))
            if 71 <= color_hsl[0] <= 150:
                data["blade_shadow"].append((w,h))
    print(str(w/width*100) + " % done")

f = open(base_filename + "_sword_nft_info.txt", "w")
f.write("data = " + str(data))
f.close()


final = nft_variables.colors



count = 0
for i2 in final:
    primary = i2
    shadow = [primary[0], primary[1], primary[2]-20]
    if i2[0] + 180 <= 360:
        temp1 = i2[0] + 180
    else:
        temp1 = i2[0] - 180
    background = [temp1, i2[1], i2[2]]
    shift = 60
    if primary[0] + 180 > 360:
        temp = primary[0] - 180
    else:
        temp = primary[0] + 180

    comp1 = [temp - shift, primary[1], primary[2]-10]
    comp2 = [temp + shift, primary[1], primary[2]-10]
    
    if comp2[0] > 360:
        comp2[0] = comp2[0] - 360
    if comp1[0] < 0:
        comp1[0] = abs(comp1[0])
    if comp1[0] < comp2[0] + 10 and comp1[0] > comp2[0] - 10:
        comp2[2] = 0
    for i in data["blade"]:
        img.putpixel(i, methods.hsl_2_rgb(primary))
    for i in data["pommel"]:
        img.putpixel(i, methods.hsl_2_rgb(comp1))
    for i in data["hilt"]:
        img.putpixel(i, methods.hsl_2_rgb(comp2))
    for i in data["blade_shadow"]:
            img.putpixel(i, methods.hsl_2_rgb(shadow))
    for i in data["background"]:
        img.putpixel(i, methods.hsl_2_rgb(background))


    size = 512 #have to resize to get rid of imperfections
    imgSmall = img.resize((size,size),resample=Image.BILINEAR)
    result = imgSmall.resize(img.size,Image.NEAREST)

    #trait assignment
    traits = []
    result2 = ImageDraw.Draw(result)
    trait_list = nft_variables.trait_list
    oldnum = 69
    num = 0
    mean =50
    stdev = 15
    while len(traits) < 2:
        num = random.randint(0, len(trait_list)-1)
        while num == oldnum:
            num = random.randint(0, len(trait_list)-1)
        traits.append(trait_list[num])
        oldnum = num
    while len(traits) < 4:
        stat = abs(round(np.random.normal(loc=mean, scale=stdev)))
        traits.append(stat)
    
    text = traits[0] + str(traits[2]) + "   " + traits[1] + str(traits[3])

    #text adding
    
    box  = [10,1275,1490,1475]
    x1, y1, x2, y2 = box
    w = 10000
    text_size = 150
    while w > width:
        font = ImageFont.truetype("VT323-Regular.ttf", text_size)
        w, h =  result2.textsize(text, font=font)
        text_size = text_size - 10
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    text_color = (0,0,0)
    b_color = methods.hsl_2_rgb(background)
    b_average = (b_color[0] + b_color[1] + b_color[2])/3
    if b_color[0] - 10 < b_average < b_color[0]+10:
        text_color = (255,255,255)
    result2.text((x,y), text, text_color, font=font, align="center")

    new_traits = [str(i).rstrip(": '").lstrip("[") for i in traits]
    save_path = r"C:\Users\xeony\Desktop\Code\nft\finished_nft"
    complete_filename = os.path.join(save_path, base_filename + str(count) + str(new_traits) + ".jpg")
    result.save(complete_filename)
    print(str(count/len(final)*100) + "% done")
    count += 1


