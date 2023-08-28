from exif import Image  #need to install exif library to python 
from shutil import copy2
import datetime
import csv
import subprocess
#from os import walk, path, makedirs
import os
import find_poles


# https://pythonconquerstheuniverse.wordpress.com/2008/06/04/gotcha-%E2%80%94-backslashes-in-windows-filenames/
# How to handle backslashes in paths for python.  (Comments have good solutions too.  'string_with_backslashes '.strip()

#How to add libraries to QGIS' python
#  https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/

#How to call exiftool from python
#https://stackoverflow.com/questions/21697645/how-to-extract-metadata-from-a-image-using-python

#How to hide console window from subprocess.popen
#https://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/


#Source: https://en.proft.me/2015/09/20/converting-latitude-and-longitude-decimal-values-p/
#If this isn't robust enough another option would be : https://pypi.org/project/LatLon/
def dms2dd(degrees, minutes, seconds, direction='N'):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd;



exifToolPath = 'X:\Engineering\GIS\Images\DroneCollected\exiftool(-k).exe'

up_to_date_poles = 'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\poles.csv'

directory = r'X:\Engineering\GIS\Images\DroneCollected\ROW Pilot\Shelton LN\South images'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\24\3\Roby Farm RD\PoleInspection'
directory = r'X:\Engineering\GIS\Images\DroneCollected\2019_05_29_floods\Photos and Movies\2019_05_29\Hancock Hill Rd'


#directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\24\3\Roby Farm RD\lookdown'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\20\4\mclane_rd\poles'
#directory = r'X:\Engineering\GIS\Images\DroneCollected\ROW Pilot\mclane_rd\Fast'
#directory = r'X:\Engineering\GIS\Images\DroneCollected\ROW Pilot\mclane_rd\Slow'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\20\4\mclane_rd\Slow'

#directory = r'X:\Engineering\GIS\Images\DroneCollected\2019_05_29_floods\Photos and Movies\2019_06_07\Hartsburg'
#directory = r'X:\Engineering\GIS\Images\DroneCollected\2019_05_29_floods\Photos and Movies\2019_05_29\Huntsdale'
#directory = r'X:\Engineering\GIS\Images\DroneCollected\2019_05_29_floods\Photos and Movies\2019_05_24\Hartsburg'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_14_wilhite_east'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\22\4\2020_10_16_weejo_ct'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd'
directory = r'X:\Engineering\GIS\Images\DroneCollected\Boone\2020_pre_construction'
directory = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\10\7\Parkade'

try:
    job_title =  directory.split('SUBSTATIONS', 1)[1]
except:
    job_title = directory.split('DroneCollected', 1)[1]


(_, _, filenames) = next(os.walk(directory))


candidates = []
category = r'\pole_insp_'
#category = r'\overview_'
for x in filenames:
    candidates.append(directory + r'\ '.strip() + x)


        
filename = r'\DJI_0249.JPG'
path = directory + filename


parent_directory = os.path.basename(directory)

pole_list = []

polelist = find_poles.get_poles()

##with open(up_to_date_poles) as polefile:
##    reader = csv.DictReader(polefile)
##    for row in reader:
##        pole_list.append([row['ï»¿label'],float(row['lat']), float(row['long'])])
    

print(len(pole_list))

leftmost_x = None
rightmost_x = None

upmost_y = None
downmost_y = None

sheet = []
pole_sheet = []
row_sheet = []

infoDict = {}

pic_dic = {}
pole_dic = {}
row_dic = {}



for x  in range(0, len(candidates)):
    #print(candidates[x], filenames[x])
    with open(candidates[x], 'rb') as image_file:
        filename, file_extension = os.path.splitext(candidates[x])
        filename = os.path.basename(candidates[x])
        my_image = Image(image_file)

        if filename.rfind('.csv') > -1:
            #Don't process the csvs
            continue

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        #Use a subprocess to call exiftool in order to access the exif data that exif can't reach.
        process = subprocess.Popen([exifToolPath,candidates[x]],startupinfo=startupinfo,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
        
        for tag in process.stdout:
            line = tag.strip().split(':')
            infoDict[line[0].strip()] = line[-1].strip()

        direction = 'unknown'
        try:
            #0 Degrees is north, -90 is west, 90 east and I'm not sure what it says when you point it exactly south if you get 180 or -180.
            #camera_direction = infoDict['Yaw']                 # Not in every file
            camera_direction1 = infoDict['Flight Yaw Degree']
            #camera_direction2 = infoDict['Camera Yaw']          # Camera Yaw is usually the same as Gimbal Yaw - Not in every file.
            camera_direction3 = float(infoDict['Gimbal Yaw Degree'])   # The gimbal yaw is the camera heading relative to true north.  https://mavicpilots.com/threads/exif-xmp-heading-information.45853/

            absolute_altitude = infoDict['Absolute Altitude']
            relative_altitude = infoDict['Relative Altitude']

            if camera_direction3 > 0:  #East
                if camera_direction3 > 0 and camera_direction3 <= 22.5: #North
                    direction = 'N'
                elif camera_direction3 > 22.5 and camera_direction3 <= 67.5:
                    direction = 'NE'
                elif camera_direction3 > 67.5 and camera_direction3 <= 112.5:
                    direction = 'E'
                elif camera_direction3 > 112.5 and camera_direction3 <= 157.5:
                    direction = 'SE'
                elif camera_direction3 > 157.5:
                    direction = 'S'                        
            else: # West
                if abs(camera_direction3) > 0 and abs(camera_direction3) <= 22.5: #North
                    direction = 'N'
                elif abs(camera_direction3) > 22.5 and abs(camera_direction3) <= 67.5:
                    direction = 'NW'
                elif abs(camera_direction3) > 67.5 and abs(camera_direction3) <= 112.5:
                    direction = 'W'
                elif abs(camera_direction3) > 112.5 and abs(camera_direction3) <= 157.5:
                    direction = 'SW'
                elif abs(camera_direction3) > 157.5:
                    direction = 'S' 
        
            
            #print( "Da Yaws", infoDict['Yaw'], direction)
            #print( "Lat", infoDict['GPS Latitude'])

        except:
            direction = 'unknown'
            
        #print(my_image, image_file)

        ##print(dir(my_image))
        #print(my_image.get('flight_yaw'))
##        print('get_thumbnail', my_image.get_thumbnail)
##        print('subject_distance', my_image.subject_distance)
##        print('subject_distance_range', my_image.subject_distance_range)
##        print('focal_length',  my_image.focal_length)
##        print('scene_capture_type', my_image.scene_capture_type)

        try:
            latitude = dms2dd(my_image.gps_latitude[0],my_image.gps_latitude[1],my_image.gps_latitude[2],my_image.gps_latitude_ref)
            longitude = dms2dd(my_image.gps_longitude[0],my_image.gps_longitude[1],my_image.gps_longitude[2],my_image.gps_longitude_ref)

            date = my_image.datetime_original
            time = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
            date2 = time.date()
            
            coords = r'POINT (' + str(longitude) + ' ' + str(latitude) + r')'
            coords_p = coords
            altitude = my_image.gps_altitude



        except:
            print('bork')
            pass
        match_id = 'none'
        match_pole = 'none'
        distance = 99999999
        pLat, pLong = 0,0

    
        
        match_id, match_pole, distance, pLat, pLong = find_poles.get_match(polelist, float(longitude), float(latitude))

        #If we're this close and low then it's probably a pole inspection
        #overwrite the picture's coordinates with the pole's
        if distance < 10 and float(relative_altitude) < 30:
            the_sheet = pole_sheet
            category = 'insp'
            print('altitudes:', altitude, relative_altitude)
            coords = r'POINT (' + str(pLong) + ' ' + str(pLat) + r')'
        else:
            the_sheet = row_sheet
            category = 'view'


        if leftmost_x  is None :
            leftmost_x = longitude 
        elif longitude < leftmost_x :
            leftmost_x = longitude 
        if rightmost_x is None :
            rightmost_x = longitude
        elif longitude > rightmost_x:
            rightmost_x = longitude
        if upmost_y is None :
            upmost_y = latitude
        elif latitude > upmost_y:
            upmost_y = latitude
        if downmost_y is None:
            downmost_y = latitude
        elif latitude < downmost_y:
            downmost_y = latitude
                

        newdirectory = directory+ r'\ '.strip() + match_pole

        if not os.path.exists(newdirectory):
           # os.makedirs(newdirectory)
           pass
        
        newfile = match_pole + '_' +category + '_' + str(date2) + '_' + direction + '_' + str(x) + file_extension # filename
        #newname =  category + newfile
        newname = newfile
        newpath =  directory + newname


        #This copies the file to a folder for unique polenumbers.
        #copy2(candidates[x], newpath)
        #This copies the file to the folder it was already in.
        subd = directory + r'\ '.strip() + 'poleinsp'
        if not os.path.exists(subd):
            os.makedirs(subd)
            pass
        #newentry = candidates[x][:candidates[x].rfind(os.path.basename(candidates[x]))] + 'imp' + newname
        newentry = subd + r'\ '.strip() + newname
        newentry = directory+ r'\ '.strip()  + newname
        print('newentry:', newentry)
        copy2(candidates[x], newentry )
        #os.rename(candidates[x],newentry)


        print('Job: ', job_title, 'Filename: ', filename ,'pole : ', match_pole, 'distance : ', distance)

        #sheet is the line of single picturs
        new_row = [newfile, match_id, match_pole, str(date2), time, job_title, coords,altitude,latitude, longitude, direction,camera_direction3, directory,  newentry, 'unexamined', '']

        if category =='view':
            sheet.append(new_row)
        else:
            

            #Make an entry in the master dictionary (pic_dic) and the current category dictrionary (the_dic)
            #pic_dic should only be used for equipment inspections.
            if str(match_id) in pic_dic:
                pic_dic[str(match_id)].append(newentry)
                #the_dic[str(match_id)].append(newentry)
                pass
            else:
                pic_dic[str(match_id)] = [newfile, match_id, match_pole, str(date2), time, job_title,  coords,altitude,pLat, pLong, direction, camera_direction3, directory, newentry, 'unexamined', ''] + [newentry]
                #the_dic[str(match_id)] = [newfile, match_id, match_pole, str(date2), time, job_title,  coords,altitude,pLat, pLong, direction, camera_direction3, directory, newpath, 'unexamined', ''] + [newentry]
                #pic_dic[str(match_id)] = [newfile, match_id, match_pole, str(date2), time, job_title,  coords,altitude,pLat, pLong, direction, camera_direction3, directory, newentry, 'unexamined', ''] + [newentry]

            


desc = ['file', 'id', 'pole', 'date', 'time', 'job', 'wkt', 'z', 'lat', 'long', 'direction', 'abs_direction', 'folder','path', 'status', 'notes']
with open (directory + r'\inspections.csv', "w", newline = '') as f:
    wr=csv.writer(f)
    wr.writerow(desc)

    for x in sheet:
        wr.writerow(x)

with open (directory + r'\inspections_p.csv', "w", newline = '') as f:
    wr=csv.writer(f)
    wr.writerow(desc + ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10'])

    for x in pic_dic:
    #for x in row_dic:
        #print(pic_dic[x])
        #print(' ')
        wr.writerow(pic_dic[x])
    


with open (directory + r'\job_entry.csv', 'w', newline = '') as f:
    wr=csv.writer(f)
    wr.writerow(['job', 'wkt', 'date'])
    

    #job_title
    #coords
    #date2

    linestring = 'POLYGON(('
    wkt = linestring
    wkt = wkt + str(leftmost_x) + ' ' + str(upmost_y) + ','
    wkt = wkt + str(leftmost_x) + ' ' + str(downmost_y) + ','
    wkt = wkt + str(rightmost_x) + ' ' + str(downmost_y) + ','
    wkt = wkt + str(rightmost_x) + ' ' + str(upmost_y) + ','
    wkt = wkt + str(leftmost_x) + ' ' + str(upmost_y) + '))'

    wr.writerow([job_title, wkt, date2])
    

print("\n\n ============= Done =============")
