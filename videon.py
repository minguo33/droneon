import os
import csv
import random


import find_poles

#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\20\4\mclane_rd\video\DJI_0016.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\24\3\Roby Farm RD\Video\DJI_0012.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_14_wilhite_east\video\DJI_0038.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd\video\DJI_0067.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd\video\DJI_0082.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd\video\DJI_0116.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd\video\DJI_0134.SRT'
#dataf = r'X:\Engineering\GIS\Images\DroneCollected\Boone\2020_pre_construction\video\DJI_0001.SRT'
dataf = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\10\7\Parkade\video\DJI_0002.SRT'

#movie = dataf.replace('.SRT', '.MOV')
movie = dataf.replace('.SRT', '.MP4')

filename = os.path.basename(movie)
directory = os.path.abspath(os.path.join(dataf, os.pardir))
parent = os.path.abspath(os.path.join(directory, os.pardir))

try:
    job_title =  directory.split('SUBSTATIONS', 1)[1]
except:
    job_title = directory.split('DroneCollected', 1)[1]

sheet = []
line = ""
linestring = 'LINESTRING('
wkt = linestring

polelist = find_poles.get_poles()

f = []
#for (dirpath, dirnames, filenames) in os.walk(r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd\video'):
for (dirpath, dirnames, filenames) in os.walk(directory):
    f.extend(filenames)
    break

for x in f:
    print(x)
    if x.rfind('.SRT') > -1:
        dataf  = os.path.join(directory, x)
        print(dataf)
        
        movie = dataf.replace('.SRT', '.MP4')
        filename = os.path.basename(movie)


        with open(dataf, 'r') as vidfile:
            all_lines = vidfile.readlines()
            count = 0
            running_count = 1
            coline = linestring
            first = None
            for x in all_lines:
                if x.rfind('-->') > -1: #Should be the timestamp
                    timestamp1, timestamp2 = x.split('-->')
                    fullstamp = x
                if x.rfind('HOME(') > -1:  #Set home point and first coordinate
                    time = x[x.rfind(') ')+2:]
                    
                    if running_count ==1:
                        first = x[x.rfind('(')+1:x.rfind(')')].replace(',', ' ')
                        coline = linestring + first + ","
                        previous_coords = first
                if  x.rfind('GPS(') > -1: #Should be coordinates in the stream

                    
                    coordst = x[x.rfind('(')+1:x.rfind(')')-3].replace(',', ' ')
                    coords = x[x.rfind('(')+1:x.rfind(')')-3].replace(',', ' ') 

                    if previous_coords.rfind(coords) > -1:
                        print('skipped', coline, coords)
                        pass
                    else:
                        previous_coords = coords
                        coords = coords.replace(' ', '0' +str(random.randint(0,9)) +' ')+ '0' + str(random.randint(0,9)) #We add a little jiggle to the flight.
                        coline = coline + coords + ")"

                        latitude, longitude = (coords.split(' '))
                        pole_match = find_poles.get_match(polelist, float(latitude), float(longitude))
                                             
                        print(coline, coords, pole_match)
                        if coline.rfind(coords) > 998:
                            pass
                        else:
                            #coline = coline.replace(' ', '0' + str(random.randint(0,99)) + ' ').replace(',', '0' + str(random.randint(0,99)) + ',' ).replace(')', '0' + str(random.randint(0,99)) + ')' )   
                            sheet.append([filename, pole_match, '  ' , time, job_title, coline, ' ', ' ', ' ', running_count, fullstamp, directory, movie, ' ', ' '])
                            count = 0
                            running_count = running_count + 1

                            coline = linestring  + coords + ","



                    
                    wkt = wkt + coords + ","

            
            wkt = wkt[:-1] + ')'
            print(wkt)


desc = ['file', 'pole', 'date', 'time', 'job', 'wkt', 'z', 'lat', 'long', 'direction', 'timestamp', 'folder','path', 'status', 'notes']


with open (directory + r'\flightline.csv', "w", newline = '') as f:
    wr=csv.writer(f)
    wr.writerow(desc)

    #wr.writerow([filename, ' ', '  ' , ' ', job_title, wkt, ' ', ' ', ' ', ' ', ' ', directory, ' ', ' ', ' '])

    for x in sheet:
        wr.writerow(x)
                

print("\n\n ============= Done =============")
