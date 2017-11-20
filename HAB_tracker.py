import serial #imports the serial module 
import time #imports the time module

ser = serial.Serial('/dev/cu.usbserial-A906NC0Z', 57600)
time.sleep(2) # pauses for a second and allows the radio time to start recieving a signal

ser.readline() #serial is used to go through first lines of inputs
ser.readline()
ser.readline()

count = 0

ser.flushInput()

while True: #starts an infinite while loop


    if count <= 0: #this if loop runs only on the first iteration of the while loop i.e when count = 0
        count=count+1 #after this if is run through once count becomes 1 and this section of code is never entered again

        longitude = ser.readline() # reads the longitude data from serial
        latitude = ser.readline() # reads the latitude data from serial
        altitude = ser.readline() # reads the altitude data from serial
        ser.flushInput() #flushs the serial moniter

        strLongitude = longitude.replace(" ", "")
        strLatitude = latitude.replace(" ", "")

        floatLong = float(strLongitude)
        floatLat= float(strLatitude)

        lastLong = floatLong
        lastLat = floatLat


        
        #open the file to be written
        f = open('entirePath.kml', 'w')

        f.write("<?xml version='1.0' encoding='UTF-8'?>\n") #begins writing the KML file line by line in the correct format
        f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        f.write("<Document>\n")
        f.write("<Style id='yellowPoly'>\n")
        f.write("<LineStyle>\n")
        f.write("<color>7f00ffff</color>\n")
        f.write("<width>15</width>\n")
        f.write("</LineStyle>\n")
        f.write("<PolyStyle>\n")
        f.write("<color>7f00ff00</color>\n")
        f.write("</PolyStyle>\n")
        f.write("</Style>\n")
        f.write("<Placemark><styleUrl>#yellowPoly</styleUrl>\n")
        f.write("<LineString>\n")
        f.write("<extrude>1</extrude>\n")
        f.write("<tesselate>1</tesselate>\n")
        f.write("<altitudeMode>absolute</altitudeMode>\n")
        f.write("<coordinates>\n")
        f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude)))  #This line inputs the first set of coordinates into the KML file
        f.write("\n</coordinates>\n")
        f.write("</LineString></Placemark>\n\n")
        f.write("</Document></kml>")

        f.close() #Closes the files 

        f = open('currentLocation.kml', 'w') # creates another file in write mode that displays only the current location

        f.write("<?xml version='1.0' encoding='UTF-8'?>\n") #begins writing the KML file line by line in the correct format
        f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        f.write("<Document>\n")
        f.write("<Style id='yellowPoly'>\n")
        f.write("<LineStyle>\n")
        f.write("<color>7f00ffff</color>\n")
        f.write("<width>15</width>\n")
        f.write("</LineStyle>\n")
        f.write("<PolyStyle>\n")
        f.write("<color>7f00ff00</color>\n")
        f.write("</PolyStyle>\n")
        f.write("</Style>\n")
        f.write("<Placemark><styleUrl>#yellowPoly</styleUrl>\n")
        f.write("<LineString>\n")
        f.write("<extrude>1</extrude>\n")
        f.write("<tesselate>1</tesselate>\n")
        f.write("<altitudeMode>absolute</altitudeMode>\n")
        f.write("<coordinates> \n")
        f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude))) 
        f.write("\n</coordinates>\n")
        f.write("</LineString></Placemark>\n\n")
        f.write("</Document></kml>")

        f.close() #closes the file

    else:
        longitude = ser.readline() # reads the longitude data from serial
        latitude = ser.readline() # reads the latitude data from serial
        altitude = ser.readline() # reads the altitude data from serial
        
        ser.flushInput() #flushs the serial moniter

        #counts the number of - symbols in the string longitude and latitude
        countLong = longitude.count('-') 
        countLat = latitude.count('-')

        #sets the index lat to zero so that data can be stored as long as all if statements are met
        indexLat = 0
        indexLong = 0


        if countLong == 1:
            indexLong = longitude.index('-') 

        if countLat == 1:
            indexLat = latitude.index('-')

        if countLong <= 1:  
            if indexLong <= 0:
                if countLat <= 1:
                    if indexLat <= 0:

                        strLongitude = longitude.replace(" ", "")
                        strLatitude = latitude.replace(" ", "")

                        floatLong = float(strLongitude)
                        floatLat= float(strLatitude)

                        if isinstance(floatLong, float) == True: #this is meant to prevent corrupted data from coming through the serial moniter. Sometimes corrupted data would have multiple - and would therefore not be a valid float  
                            if isinstance(floatLat, float) == True: #same
                                changeLong = floatLong - lastLong #calculates the changes in latitude and longitude
                                changeLat = floatLat - lastLat
            
                                if -1 < changeLong < 1: #ensures that the longitude and latitude have changed only reasonable amounts also meant to stop corrupted data                               
                                    if -1 < changeLat < 1:
                                        f = open('entirePath.kml','r+')
                                        f.seek(-59,2)
                                        f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude))) 
                                        f.seek(-27,2)
                                        f.write("\n</coordinates>\n")
                                        f.write("</LineString></Placemark>\n\n")
                                        f.write("</Document></kml>")

                                        f.close()

                                        f = open ('currentLocation.kml','r+')
                                        f.seek(-92,2)
                                        f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude)))
                                        f.write("\n</coordinates>\n")
                                        f.write("</LineString></Placemark>\n\n")
                                        f.write("</Document></kml>")

                                        f.close()
                                    
                                        lastLong=floatLong
                                        lastLat=floatLat
