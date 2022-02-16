from PIL import Image
import methods 
filename = "monkey_boat.png"
pixelate = True #pixelate realistic images to make it less obvious I stole them
if pixelate == True:
    img = Image.open(filename)
    size = 64
    imgSmall = img.resize((size,size),resample=Image.BILINEAR)
    result = imgSmall.resize(img.size,Image.NEAREST)
    filename1 = "oogabooga" + str(size) + ".jpg"
    result.save(filename1)
else:
    filename1 = filename


result = Image.open(filename1)

width, height = result.size
print(width,height, result.size)
delta = 80
for x in range(width):
    for y in range(height):
        color = result.getpixel((x,y))
        delta_color = methods.hue_change(methods.rgb_2_hsl(color), delta)
        result.putpixel((x,y), methods.hsl_2_rgb(delta_color))
        
    print(str(round(x/width*100, 3)) + " % done")

result.save("shift.jpg")


