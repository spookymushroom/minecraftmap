from nbt import nbt
from PIL import Image,ImageDraw,ImageFont
from os import path

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
        self.gencolors()
        
        if not eco: self.genimage()
    
    
    
    basecolors = [(0, 0, 0), (127, 178, 56), (247, 233, 163), (199, 199, 199),
        (255, 0, 0), (160, 160, 255), (167, 167, 167), (0, 124, 0),
        (255, 255, 255), (164, 168, 184), (151, 109, 77), (112, 112, 112),
        (64, 64, 255), (143, 119, 72), (255, 252, 245), (216, 127, 51),
        (178, 76, 216), (102, 153, 216), (229, 229, 51), (127, 204, 25),
        (242, 127, 165), (76, 76, 76), (153, 153, 153), (76, 127, 153),
        (127, 63, 178), (51, 76, 178), (102, 76, 51), (102, 127, 51),
        (153, 51, 51), (25, 25, 25), (250, 238, 77), (92, 219, 213),
        (74, 128, 255), (0, 217, 58), (129, 86, 49), (112, 2, 0)]
    
    font = ImageFont.truetype(fontpath,8)
    
    def gendefaultnbt(self):
        nbtfile = nbt.NBTFile()
        colors = nbt.TAG_Byte_Array(name="colors")
        colors.value = bytes(16384)
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
        '''sets allcolors list and allcolorsinversemap'''
        self.allcolors = []
        self.allcolorsinversemap = {}
        for i in range(len(self.basecolors)):
            r = round
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
    
    def imagetonbt(self):
        '''updates self.file to match self.im'''
        rgbdata = self.im.getdata()
        try: colordata = bytearray([self.allcolorsinversemap[c] for c in rgbdata])
        except KeyError as e:
            raise ColorError(e.args[0])
        self.file["data"]["colors"].value = colordata
    
    def saveimagebmp(self,filename):
        '''Saves self.im as a bmp'''
        self.im.save(filename)
    
    def saveimagepng(self,filename):
        '''Saves self.im as png'''
        self.im.save(filename,"PNG")
    
    def savenbt(self,filename=None):
        '''Saves nbt data to original file or to specified filename'''
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
        '''Converts coords to pixels where x:east and z:south'''
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

    def approximate(self,color):
        '''wip, supposed to return best approximation of color'''
        bestdist = 500
        bestcolor = (0,0,0)
        for c in self.allcolors:
            d=((color[0]-c[0])**2+(color[1]-c[1])**2+(color[2]-c[2])**2)**.5
            if d < bestdist:
                bestdist = d
                bestcolor = c
        print(d)
        return bestcolor
