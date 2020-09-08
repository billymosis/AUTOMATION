import subprocess
import os
import pandas as pd
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw


# constants
gdal = r'C:/Program Files/QGIS 3.12/bin/'
gdalTranslate = gdal+'gdal_translate.exe'
src = r"D:/mrican/GIS/MERICAN UPDATE_240220.ecw"
Folder = r"D:/mrican/LiDAR"
DATA = r"D:\mrican\LiDAR\Sentul\Sentul.csv"
font = ImageFont.truetype("arial.ttf", 15)

def Quote(item):
    return "\"" + item + "\""

# Get data - reading the CSV file
df = pd.read_csv(DATA,delimiter=',')
tuples = [tuple(x) for x in df.values]
Saluran = 'Sentul'

for x in tuples:
    X = x[1]
    Y = x[2]
    NamaFile = x[0]
    print(NamaFile)
    dst = f"{Folder}/{Saluran}/{NamaFile}.tif"
    wld = f"{Folder}/{Saluran}/{NamaFile}.wld"
    cmd = f"-projwin {X-50} {Y+50} {X+50} {Y-50} -of GTiff -co COMPRESS=NONE -co BIGTIFF=IF_NEEDED"
    os.makedirs(os.path.dirname(dst),exist_ok=True)

    #Bikin WLD file untuk Projection
    with open(wld, 'w') as f:
        f.write(f"0.15000000\n0.00000000\n0.00000000\n-0.15000000\n{X-50}\n{Y+50}")

    #Crop
    fullCmd = ' '.join([gdalTranslate, cmd, Quote(src), Quote(dst)])
    subprocess.call(fullCmd)

    #PIL
    img = Image.open(dst)
    size = img.size
    print(size[1])

    draw = ImageDraw.Draw(img)
    draw.text((10, size[1]-50),f"{NamaFile}",(0,0,0),font=font,align='left')
    draw.text((10, size[1]-30),f"{Saluran}",(0,0,0),font=font)
    img.save(dst)
