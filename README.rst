=====================
Minecraft Maps Editor
=====================

Simple Python 3 editor for Minecraft maps (the item) in NBT format. Allows editing the map image with the Python Image Library or by editing bytes in the color native format. 

---------------------

Usage::

 import minecraftmap
 filepath = "/Users/spookymushroom/AppData/Roaming/.minecraft/saves/Test World/data/map_0.dat"
 
 # The False eco value indicates that __init__ should run genimage to update im (the PIL image)
 m = minecraftmap.Map(filepath,eco=False)
 
 # The '8' byte in Minecraft's color format is equivalent to (174, 164, 115)
 print(m.allcolors[8]) 
 
 # The allcolorsinversemap dictionary will return the byte value of a color
 # when any native Minecraft map color is passed into it
 print(m.allcolorsinversemap[(174, 164, 115)])
 
 if m.getbyte(6747) != 8:
    m.setbyte(6747,8)
 
 # Equivalent to getbyte(6747) for a 128x128 map
 if m.getpoint((91,52)) != 8:
    m.setpoint((91,52),8)
 
 # Updates Map.im (PIL) to match Map.file (NBT)
 m.genimage()
 
 # PIL methods
 m.draw.rectangle((0,0,128,128),fill=(56,58,89))
 m.draw.text((40,40),"testing",font=m.font)
 
 # Save Map.im (The PIL.Image object) to a file
 m.saveimagepng("map_0.png") #front-end for m.im.save
 m.saveimagejpg("map_0.jpg") #front-end for m.im.save
 
 # PIL.Image.save method
 m.im.save("map_0_customqual.jpg","JPEG",quality=80)
 
 # Updates Map.file (NBT data) to match Map.im (PIL image)
 # Versions before 0.2 require that the image contains only native colors
 m.imagetonbt()
 
 # Saves Map.file to an NBT file
 # If filename argument is left blank, it saves data to
 # the original file as identified by m.file.filename
 print(m.file.filename)
 m.savenbt()

---------------------

:Requires: Thomas Woolford's NBT library
:Requires: Python Image Library (Pillow)
:Includes: Andrew Tyler's Minecraftia font
