# Source: https://python.hotexamples.com/examples/gpsd/-/connect/python-connect-function-examples.html?utm_content=cmp-true

import gpsd
from bike.models import Bike, Location
import datetime
import time

HOST="172.16.7.2"
PORT=2947
BIKE_NAME='Ducati 916'
DELAY=30 

class NoFixError(Exception):
	pass

def getPositionFromGpsd():
	gpsd.connect(host=HOST, port=PORT)
	try:
		packet = gpsd.get_current()
	except KeyError as e:
		return

	try:
		pos = packet.position()
	except gpsd.NoFixError:
		#raise NoFixError
		print("position failed")
	else:
		precision = packet.position_precision()
		time = packet.get_time()
	try:
		alt = packet.altitude()
		movement = packet.movement()
	except gpsd.NoFixError:
		alt, speed, track, climb = ['n/a'] * 4
	else:
		speed, track, climb = movement['speed'], movement['track'], movement['climb']

#            print(time)
#            print(pos)
#            print(alt)
#            print(speed)
#            print(track)
#            print(climb)
#            print(precision)

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

# a loop to endlesly ask bike location
while True:
	pos = getPositionFromGpsd()
	if (pos is not None):
		# create a location
		try:
			location = Location(bike=Bike.objects.get(name=BIKE_NAME), latitude=pos['latitude'], longitude=pos['longitude'], \
					altitude=pos['altitude'], speed=pos['speed'], track=pos['track'], climb=pos['climb'], \
					time=pos['time'], error_horizontal=pos['error_horizontal'], error_vertical=pos['error_vertical'])
			location.save()
		except Exception as e:
			print(e)
	time.sleep(DELAY)

