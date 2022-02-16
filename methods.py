from pathlib import Path


def digit_break(num): #breaks a digit into its component parts. Accepts an int only. works
    result = [i for i in str(num)]
    for i in range(len(str(num))):
            result[-(i+1)] = int(num%(10**(i+1))/(10**i))
    return result

def saveInSameFolder(filename): #not sure if it works
    path = str(Path(__file__).absolute())
    split =  path.split("\\")
    final = ""
    for i in range(len(split)):
        if i != len(split) - 1:
            final = final + split[i] + "\\" 
    finalpath = final.rstrip() + filename.rstrip()
    return finalpath

def rgb_2_hsl(color): #functional!, slightly off because rounding
    r = color[0]
    g = color[1]
    b = color[2]
    h = 0
    s = 0
    l = 0
    r1 = r/255
    g1 = g/255
    b1 = b/255
    Cmax = max(r1,g1,b1)
    Cmin = min(r1,g1,b1)
    delta = Cmax - Cmin
    #calculate hue
    if delta == 0:
        h = 0
    else:
        if Cmax == r1:
            h = 60 * (((g1 - b1)/delta)%6)
        if Cmax == g1:
            h = 60 * (((b1 - r1)/delta)+2)
        if Cmax == b1:
            h = 60 * (((r1 - g1)/delta)+4)
    #calculate lightness
    l = (Cmax + Cmin)/2
    #calculate saturation
    if delta == 0:
        s = 0
    else:
        s = delta/(1 - abs(2*l - 1))
    return (int(round(h)),int(round(s*100)),int(round(l*100)))


def hsl_2_rgb(color): #works, slightly off because rounding
    h = color[0]
    s = color[1]/100
    l = color[2]/100
    C =  (1 - abs(2*l - 1)) * s 
    X = C * (1 - abs((h/60)%2 - 1))
    m = l - C/2
    rgb1 = [0,0,0] 
    if 0 <= h < 60:
        rgb1 = [C,X,0]
    elif 60 <= h < 120:
        rgb1 = [X,C,0]
    elif 120 <= h < 180:
        rgb1 = [0,C,X]
    elif 180 <= h < 240:
        rgb1 = [0,X,C]
    elif 240 <= h < 300:
        rgb1 = [X,0,C]
    elif 300 <= h < 360:
        rgb1 = [C,0,X] 
    
    r = (rgb1[0] + m) * 255
    g = (rgb1[1] + m) * 255
    b = (rgb1[2] + m) * 255
    
    return (int(round(r)),int(round(g)),int(round(b)))

def hue_change(color, delta): #accepts hsl, returns hsl
    if delta > 360 or delta < -360:
        print("ERROR INVALID DELTA TO CHANGE HUE")
        return None
    if color[0] + delta < 360:
        return (color[0] + delta, color[1], color[2])
    else:
        return (color[0] + delta - 360, color[1], color[2])
    
