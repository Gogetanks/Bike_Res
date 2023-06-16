from django.core.management.base import BaseCommand, CommandError
from bike.models import Bike, Location
import datetime
import sys

BIKE_NAME = 'Honda Shadow'

#bike = Bike.objects.get(name=BIKE_NAME) 

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
