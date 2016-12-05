Simple Python 3 editor for Minecraft Maps in NBT format. Allows editing the map image with the Python Image Library or by editing bytes in the native format. 

The Map class defined in the module provides convenient reading and writing of minecraft map nbt data using Thomas Woolford's nbt library. 
It allows for direct reading and writing in minecraft's native color format with the getbyte(), setbyte(), getpoint(), and setpoint() methods, and it allows for PIL-based editing using the draw attribute. The saveimagebmp() and saveimagepng() methods are front-ends for PIL's Image.save(), and the savenbt() method allows for saving the nbt data into the same file, or into a new one. Be careful that the draw (PIL) and file (nbt) attributes are not syncronized and must be updated manually with genimage() and imagetonbt() methods. Also use caution when drawing in color, as any non-minecraft colors (check allcolors on an initiated Map) will raise a ColorError.

Maps are initiated with the filename of the nbt map file and optionally with eco=True, which removes the resource-intensive genimage() on startup. The font included in the package as Map.font is Andrew Tyler's Minecraftia. The PIL method text() of the draw attribute can take it as the font= named argument.

Requires PIL and Thomas Woolford's NBT library.
Includes Andrew Tyler's Minecraftia font.

Testing :P
