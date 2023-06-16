from django.core.management.base import BaseCommand, CommandError
from bike.models import Bike, BikeStatus
import requests

PORT = 89
TIMEOUT = 3 # seconds
#BIKE_NAME = 'Ducati 916'
BIKE_NAME = 'Honda Shadow'

# api-endpoint
URI = '/api/'
# api method
METHOD = 'unlock'

bike = Bike.objects.get(name=BIKE_NAME)


class Command(BaseCommand):
	help = 'Lock a bike'
	
	# get argument (name of a bike)
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

		def unlock():
			try:
				# sending get request and saving the response as response object
				r = requests.get(url = 'http://' + IP_ADDRESS + ':' + str(PORT) + URI + METHOD, timeout = TIMEOUT)
				r.raise_for_status()
			except requests.exceptions.HTTPError as errh:
				print ("Http Error:",errh)
				return None
			except requests.exceptions.ConnectionError as errc:
				print ("Error Connecting:",errc)
				return None
			except requests.exceptions.Timeout as errt:
				print ("Timeout Error:",errt)
				return None
			except requests.exceptions.RequestException as err:
				print ("OOps: Something Else",err)
				return None
			else:
				# extracting data in json format
				data = r.json()
				if data[IP_ADDRESS] == 'OK':
					return 1
				elif data[IP_ADDRESS] == 'FAIL':
					return 0
			return 0
		
		try:
			unlock()
			# unlock a bike
			try:
				bikeStatus = BikeStatus(bike = bike, is_online = True, is_locked = True)
				bike.is_online = True
				bike.is_locked = False
				bikeStatus.save()
				bike.save()
			except Exception as e:
				print("Error creating BikeStatus:", str(e))
		except Exception as e:
			try:
				bikeStatus = BikeStatus(bike = bike, is_online = False, is_locked = None)
				bike.is_online = False
				bike.is_locked = None
				bikeStatus.save()
				bik.save()
			except Exception as e:
				print("rror creating BikeStatus", str(e))
			print("An error occurred:", str(e))

		
