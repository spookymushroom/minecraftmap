from nbt import nbt
from PIL import Image,ImageDraw,ImageFont
from os import path
from functools import partial

from . import constants

fontpath = path.join(path.dirname(__file__), "minecraftia", "Minecraftia.ttf")

class ColorError(Exception):
    def __init__(self,color):
        self.color = color
        self.msg = "Could not map color to nbt value: "+str(color)
        super(ColorError,self).__init__(self.msg)



class Map():
    def __init__(self,filename=None,eco=False):
        '''Map class containing nbt data and a PIL Image object, with read/write functionality. Eco means the Image object is not written to upon initialization.'''
        
        if filename:
            self.file = nbt.NBTFile(filename)
        else:
            self.file = self.gendefaultnbt()
        
        self.height = self.file["data"]["height"].value
        self.width = self.file["data"]["width"].value
        self.centerxz = (self.file["data"]["xCenter"].value, self.file["data"]["zCenter"].value)
        self.zoomlevel = self.file["data"]["scale"].value
        self.pixelcenterxy = (self.width/2, self.height/2)
        self.scalemultiplier = self.zoomlevel ** 2
        self.im = Image.new("RGB",(self.width,self.height))
        self.draw = ImageDraw.Draw(self.im)
        
        if constants.alphacolor != self.alphacolor:
            self.gencolors()
        if not eco: self.genimage()
    
    
    
    basecolors = constants.basecolors
    
    allcolors = constants.allcolors
    
    alphacolor = constants.alphacolor
    
    #uses estimationlookupdict if True, uses estimationlookup if False
    uselookupdict = False
    
    allcolorsinversemap = constants.allcolorsinversemap
    
    font = ImageFont.truetype(fontpath,8)
    
    def gendefaultnbt(self):
        '''returns an nbt object'''
        nbtfile = nbt.NBTFile()
        colors = nbt.TAG_Byte_Array(name="colors")
        colors.value = bytearray(16384)
        data = nbt.TAG_Compound()
        data.name = "data"
        data.tags = [
            nbt.TAG_Int(value=0, name="zCenter"),
            nbt.TAG_Byte(value=1, name="trackingPosition"),
            nbt.TAG_Short(value=128, name="width"),
            nbt.TAG_Byte(value=1, name="scale"),
            nbt.TAG_Byte(value=0, name="dimension"),
            nbt.TAG_Int(value=64, name="xCenter"),
            colors,
            nbt.TAG_Short(value=128, name="height")
            ]
        nbtfile.tags.append(data)
        return nbtfile
    
    
    def gencolors(self):
        '''sets allcolors list and allcolorsinversemap to match basecolors,
        and updates all of them to match alphacolor'''
        self.basecolors[0] = self.alphacolor
        self.allcolors = []
        self.allcolorsinversemap = {}
        for i in range(len(self.basecolors)):
            r = round
            if i == 0:
                    self.allcolors.extend([self.alphacolor]*4)
                    self.allcolorsinversemap[self.alphacolor] = 3
            else:
                c = self.basecolors[i]
                for n in range(4):
                    m = (180,220,255,135)[n]
                    newcolor = (r(c[0]*m/255), r(c[1]*m/255), r(c[2]*m/255))
                    self.allcolors.append(newcolor)
                    self.allcolorsinversemap[newcolor] = i*4 + n
    
    def genimage(self):
        '''updates self.im'''
        colordata = self.file["data"]["colors"].value
        rgbdata = [self.allcolors[v] for v in colordata]
        self.im.putdata(rgbdata)
    
    def imagetonbt(self,approximate=True,optimized=True,lookupindex=10):
        '''updates self.file to match self.im, approximations work but take very long, 
        optimization with constants.estimationlookup[lookupindex] is fast but imperfect'''
        rgbdata = self.im.getdata()
        try:
            if approximate:
                if optimized and lookupindex in constants.estimationlookup:
                    colordata = bytearray([self.approximate(c,lookupindex=lookupindex) for c in rgbdata])
                else:
                    colordata = bytearray([self.approximate(c) for c in rgbdata])
            else:
                colordata = bytearray([self.allcolorsinversemap[c] for c in rgbdata])
            
        except KeyError as e:
            raise ColorError(e.args[0])
        self.file["data"]["colors"].value = colordata
    
    def saveimagebmp(self,filename):
        '''Saves self.im as a bmp'''
        self.im.save(filename)
    
    def saveimagepng(self,filename):
        '''Saves self.im as png'''
        self.im.save(filename,"PNG")
    
    def saveimagejpg(self,filename):
        self.im.save(filename,"JPEG")
    
    def savenbt(self,filename=None):
        '''Saves nbt data to original file or to specified filename'''
        if filename or self.file.filename:
            self.file.write_file(filename)
    
    
    def getbyte(self,index):
        '''Gets nbt image byte at index, returns None if out of range'''
        return self.file["data"]["colors"].value[index]
    
    def setbyte(self,index,byte):
        '''Sets nbt image byte at index'''
        self.file["data"]["colors"].value[index] = byte
    
    def getpoint(self,xy):
        '''Gets nbt image byte at specific (x,y)'''
        index = xy[0] + xy[1]*self.width
        try: return self.file["data"]["colors"].value[index]
        except IndexError: return None
    
    def setpoint(self,xy,value):
        '''Sets nbt image byte at specific (x,y)'''
        index = xy[0] + xy[1]*self.width
        self.file["data"]["colors"].value[index] = value
    
    def topixel(self,xz):
        '''converts coords to pixels where x:east and z:south'''
        shiftxz = (xz[0]-self.centerxz[0],xz[1]-self.centerxz[1])
        shiftxy = (shiftxz[0],shiftxz[1])
        pixelshiftxy = (shiftxy[0]//self.scalemultiplier, shiftxy[1]//self.scalemultiplier)
        pixelxy = (self.pixelcenterxy[0]+pixelshiftxy[0], self.pixelcenterxy[1]+pixelshiftxy[1])
        return pixelxy
    
    def tocoord(self,xy):
        '''Converts pixels to coords, returns (x,z)'''
        pixelshiftxy = (xy[0]-self.pixelcenterxy[0], xy[1]-self.pixelcenterxy[1])
        blockshiftxy = (pixelshiftxy[0]*self.scalemultiplier, pixelshiftxy[1]*self.scalemultiplier)
        blockshiftxz = (blockshiftxy[0],blockshiftxy[1])
        blockxz = (blockshiftxz[0]+self.centerxz[0],blockshiftxz[1]+self.centerxz[1])
        return blockxz
    
    def colordifference(self,testcolor,comparecolor):
        '''returns rgb distance squared'''
        d = ((testcolor[0]-comparecolor[0])**2+
             (testcolor[1]-comparecolor[1])**2+
             (testcolor[2]-comparecolor[2])**2)
        return d
    
    def approximate(self,color,lookupindex=10):
        '''returns best minecraft color code from rgb,
        lookupindex refers to constants.estimationlookup and can be None'''
        try:
            return self.allcolorsinversemap[color]
        except KeyError:
            if self.uselookupdict and lookupindex in constants.estimationlookupdict:
                return constants.estimationlookupdict[lookupindex][(color[0]*lookupindex//255,color[1]*lookupindex//255,color[2]*lookupindex//255)]
            elif not self.uselookupdict and lookupindex in constants.estimationlookup:
                return constants.estimationlookup[lookupindex][color[0]*lookupindex//255][color[1]*lookupindex//255][color[2]*lookupindex//255]
            else:
                color = min(self.allcolors,key=partial(self.colordifference,color))
                return self.allcolorsinversemap[color]
