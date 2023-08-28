import csv
from subprocess import Popen



up_to_date_poles = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\poles.csv'

pole_list = []




def get_poles(polefile=r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\poles.csv'):
    with open(up_to_date_poles) as polefile:
        reader = csv.DictReader(polefile)
        for row in reader:
            pole_list.append([row['id'],row['label'],float(row['Lat']), float(row['Long']), float(row['X']), float(row['Y'])])
        

    return(pole_list)

def get_match(pole_list, longitude, latitude):
    distance = 999999
    pLat, pLong = 0,0

    for z in pole_list:
        dist =  ( (latitude - z[2]) **2 + (longitude - z[3]) **2  ) ** 0.5
        if dist < distance:
            distance = dist
            match_id = z[0]
            match_label = z[1]
            pLat = z[2]
            pLong = z[3]

    return match_id, match_label, distance, pLat, pLong
            
def update_poles(polefile=r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\poles.csv', bat=r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\update_poles.bat'):
    p = Popen(bat, cwd=r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS')
    stdout, stderr = p.communicate()
    
    
