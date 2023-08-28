import os
import csv
import random
import subprocess

import find_poles

gdalPath =r'X:\Engineering\GIS\SOFTWARE\GDAL\release-1900-gdal-3-0-0-mapserver-7-4-0\bin\gdalinfo.exe'

directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\05\3\shelton_ln_2020_08_07\orthophotos'
directory = r'X:\Engineering\GIS\Images\DroneCollected\2019_05_29_floods\Orthomosaics\OpenDroneMapper\2019_05_29'


(_, _, filenames) = next(os.walk(directory))

candidates = []

for x in filenames:
    candidates.append(directory + r'\ '.strip() + x)
    

parent = os.path.abspath(os.path.join(directory, os.pardir))

try:
    job_title =  directory.split('SUBSTATIONS', 1)[1]
except:
    job_title = directory.split('DroneCollected', 1)[1]

sheet = []
line = ""
linestring = 'POLYGON(('
wkt = linestring

polelist = find_poles.get_poles()
infoDict = {}
for x  in range(0, len(candidates)):
    print(candidates[x])
    
    coords = {}
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    valid = False
    process = subprocess.Popen([gdalPath,candidates[x]],startupinfo=startupinfo,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    for tag in process.stdout:
        if tag.rfind('Upper Left') > -1:
            valid = True
            coords['Upper Left'] = (tag[tag.rfind('(')+1:tag.rfind(')')].strip()).split(',')
        elif tag.rfind('Lower Left') > -1:
            valid = True
            coords['Lower Left'] = (tag[tag.rfind('(')+1:tag.rfind(')')].strip()).split(',')
        elif tag.rfind('Lower Right') > -1:
            valid = True
            coords['Lower Right'] = tag[tag.rfind('(')+1:tag.rfind(')')].strip().split(',')          
        elif tag.rfind('Upper Right') > -1:
            valid = True
            coords['Upper Right'] = tag[tag.rfind('(')+1:tag.rfind(')')].strip().split(',')
            
        coords[candidates[x]] = coords

    try:

        
        wkt = wkt + coords['Upper Left'][0] + ' ' + coords['Upper Left'][1] + ','
        wkt = wkt + coords['Lower Left'][0] + ' ' + coords['Lower Left'][1] + ','
        wkt = wkt + coords['Lower Right'][0] + ' ' + coords['Lower Right'][1] + ','
        wkt = wkt + coords['Upper Right'][0] + ' ' + coords['Upper Right'][1] + ','
        wkt = wkt + coords['Upper Left'][0] + ' ' + coords['Upper Left'][1] + '))'

        infoDict[candidates[x]] = wkt #This ensures that we only add entries for data that HAVE coordinates returned from gdalinfo

        sheet.append([os.path.basename(candidates[x]), ' ', ' ', ' ', job_title, wkt, ' ', ' ', ' ', ' ', ' ', parent, candidates[x], ' ', ' '])

    except:
        print('skipped ', candidates[x])

        

        
    wkt ='POLYGON (('


for x in infoDict:
    print(x, infoDict[x])

desc = ['file', 'pole', 'date', 'time', 'job', 'wkt', 'z', 'lat', 'long', 'direction', 'timestamp', 'folder','path', 'status', 'notes']

with open (directory + r'\orthophotos.csv', "w", newline = '') as f:
    wr=csv.writer(f)
    wr.writerow(desc)

    #wr.writerow([filename, ' ', '  ' , ' ', job_title, wkt, ' ', ' ', ' ', ' ', ' ', directory, ' ', ' ', ' '])

    for x in sheet:
        wr.writerow(x)
                

with open (directory + r'\orthophotos.csv', "a", newline = '') as f:
    wr=csv.writer(f)

    #wr.writerow([filename, ' ', '  ' , ' ', job_title, wkt, ' ', ' ', ' ', ' ', ' ', directory, ' ', ' ', ' '])

    for x in sheet:
        wr.writerow(x)
                



                

