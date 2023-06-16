import gpsd
from bike.models import Bike, Location
import datetime
import time
import sys

#BIKE_NAME = 'Ducati 916' 
BIKE_NAME = "Piaggio MP3 Exclusive 530" 

PORT = 2947
#BIKE_NAME = 'Ducati 916'
#BIKE_NAME = 'Honda Shadow'
DELAY = 30

print(BIKE_NAME)

bike = Bike.objects.get(name=BIKE_NAME) 

class NoFixError(Exception):
    pass

 

def getPositionFromGpsd():
    try:
        gpsd.connect(host=bike.ip_address, port=PORT)
        packet = gpsd.get_current()
        pos = packet.position()
        precision = packet.position_precision()
        time = packet.get_time()
        alt = packet.altitude()
        movement = packet.movement()
        speed, track, climb = movement['speed'], movement['track'], movement['climb']
    except gpsd.NoFixError:
        raise NoFixError("No GPS fix available.")
    except (KeyError, ValueError) as e:
        print("Error retrieving GPS data:", str(e))
        return None
    except Exception as e:
        print("An error occurred while retrieving GPS data:", str(e))
        return None

 

    return {
        'latitude': pos[0],
        'longitude': pos[1],
        'altitude': alt,
        'speed': speed,
        'track': track,
        'climb': climb,
        'time': time,
        'error_horizontal': precision[0],
        'error_vertical': precision[1],
    }

 

# A loop to endlessly ask for bike location
while True:
    try:
        pos = getPositionFromGpsd()
        if pos is not None:
            # Create a location
            try:
                location = Location(
                    bike=bike,
                    latitude=pos['latitude'],
                    longitude=pos['longitude'],
                    altitude=pos['altitude'],
                    speed=pos['speed'],
                    track=pos['track'],
                    climb=pos['climb'],
                    time=pos['time'],
                    error_horizontal=pos['error_horizontal'],
                    error_vertical=pos['error_vertical']
                )
                location.save()
            except Exception as e:
                print("Error creating location:", str(e))
    except NoFixError:
        print("No GPS fix available.")
    except Exception as e:
        print("An error occurred:", str(e))

 

    time.sleep(DELAY)
