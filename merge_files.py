from shutil import copy2
import csv
#from os import walk, path, makedirs

existingfile  = r'X:\Engineering\GIS\Images\DroneCollected\Roam3.0.6\projects\_data\inspections_p.csv'
existingfile = r'X:\Engineering\GIS\Images\DroneCollected\Roam3.0.6\projects\_data\videos.csv'

newfile = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_14_wilhite_east\inspections_p.csv'
newfile = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\22\4\2020_10_16_weejo_ct\inspections_p.csv'
newfile = r'X:\Engineering\GIS\Images\DroneCollected\SUBSTATIONS\45\2\2020_10_22_bell_rd\video\flightline.csv'

result = r'X:\Engineering\GIS\Images\DroneCollected\Roam3.0.6\projects\_data\result.csv'
#result = existingfile

products = {}
desc = []

alldata = []

copy2(existingfile, existingfile + r'_back')

keyfield = 'id'     #Use an appropriate keyfield for poles
keyfield = 'wkt'    #Use a unique field when you want to copy every record

with open( existingfile, "r" ) as source:
    rdr = csv.DictReader( source )
    for row in rdr:
        if len(row[keyfield]) > 1:
            products[row[keyfield]] = row # or maybe some rearrangement

        alldata.append(row)

    for x in next(iter(products.values())):
        print(x)
        desc.append(x)

##    for name in products:
##        print(name, products[name])
##        #print(products[name])
####        for x in products[name]:
####            print(x)


with open( newfile, 'r' ) as source:
    rdr = csv.DictReader( source )
    for row in rdr:
        if row[keyfield] in products:
            # maybe update?
            print('exists', row[keyfield])
        else:
            print('doesnt exist')
            if len(row[keyfield]) > 1:
                products[row[keyfield]] = row # or maybe some rearrangement
        alldata.append(row)

with open( result, 'w', newline='' ) as target:
    wtr = csv.writer( target ) 
    wtr.writerow( desc )
    #for name in sorted( products ):
    for name in products :
        row =[]        
        for z in products[name]:
            row.append(products[name][z])
            
        #wtr.writerow( products[name] )
        wtr.writerow( row )
