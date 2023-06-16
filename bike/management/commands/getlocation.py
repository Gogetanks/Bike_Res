from django.core.management.base import BaseCommand
import gpsd
from bike.models import Bike, Location
import datetime
import sys

#BIKE_NAME = 'Ducati 916'

# cheching if an argument (name of a bike) was passed
#if len(sys.argv) == 2:
#	print("First if")
#	if Bike.objects.get(name=sys.argv[1]):
#		print("second if")
#		BIKE_NAME = sys.argv[1]
 
PORT = 2947
#BIKE_NAME = 'Ducati 916'
BIKE_NAME = 'Honda Shadow'

bike = Bike.objects.get(name=BIKE_NAME) 

class Command(BaseCommand):
	help = 'Get location of a bike'
	
	def add_arguments(self , parser):
		parser.add_argument('bike_name', nargs='+', type=str)

	def handle(self, **options):
		BIKE_NAME = options['bike_name'][0]
		print(BIKE_NAME)

		try:
			bike = Bike.objects.get(name=BIKE_NAME)
		except Bike.DoesNotExist:
			raise CommandError('Bike "%s" does not exist' % BIKE_NAME)
		print(bike.price)
		self.stdout.write(
			self.style.SUCCESS('Successfully found bike "%s"' % BIKE_NAME)
		)

		if bike.ip_address == None:
			raise CommandError('Bike "%s" does not have an IP address' % BIKE_NAME)

		IP_ADDRESS = bike.ip_address
		
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

		 

		# Asking for bike location
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
					bike.latitude = pos['latitude']
					bike.longitude = pos['longitude']
					location.save()
					bike.save()
				except Exception as e:
					print("Error creating location:", str(e))
		except NoFixError:
			print("No GPS fix available.")
		except Exception as e:
			print("An error occurred:", str(e))


