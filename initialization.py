# The script initializes database of the project BIKE
# How it works:
# rm db.sqlite3
# python manage.py migrate
# python manage.py shell < initialization.p


from pathlib import Path
from bike.models import Group, User, Bike, Category, Reservation, Complaint, Comment
# pip install -U get-video-properties
#import time
import datetime
from django.template.defaultfilters import slugify


#PATH='videos/2023.name/'

# create groups of users
worker = Group(name='worker')
worker.save()
mechanic = Group(name='mechanic')
mechanic.save()

print('Groups created:')
for gr in Group.objects.all():
    print(f'\t{gr}')

# add users
admin=User.objects.create_user('admin', password='123', is_superuser='True', is_staff='True', email='admin@admin.org')
nick=User.objects.create_user('nick', password='123qwe', first_name='Nikolai', last_name='Nevedomskii', is_superuser='True', is_staff='True', email='nick@n.org')
nick_worker=User.objects.create_user('nick_worker', password='123qwe', first_name='Nikolai', last_name='Nevedomskii', is_superuser='False', is_staff='False', email='nick_worker@n.org')
nick_mechanic=User.objects.create_user('nick_mechanic', password='123qwe', first_name='Nikolai', last_name='Nevedomskii', is_superuser='False', is_staff='False', email='nds@n.org')

print('Users created:')
for user in User.objects.all():
    print(f'\t{user}')

# add users in groups
nick_worker = User.objects.get(username='nick_worker')
worker = Group.objects.get(name='worker')
worker.user_set.add(nick_worker)
worker.save()
nick_mechanic = User.objects.get(username='nick_mechanic')
mechanic = Group.objects.get(name='mechanic')
mechanic.user_set.add(nick_mechanic)
mechanic.save()

for group in Group.objects.all():
    print(f'Group {group.name}:')
    for user in User.objects.filter(groups=group):
        print(f'\t {user}')


# add bike categories
standard = Category(name='Sports Bike', slug='sports-bikes')
standard.save()
cruiser = Category(name='Cruiser Bikes', slug='cruiser-bikes')
cruiser.save()
chopper = Category(name='Electric Bikes', slug='electric-bikes')
chopper.save()
scooter = Category(name='Scooters', slug='scooters')
scooter.save()
off_road = Category(name='Dirt Bikes', slug='dirt-bikes')
off_road.save()

print('Categories created:')
for cat in Category.objects.all():
    print(f'\t{cat}')

# add bikes
fireblade = Bike(name='Fireblade', description='Super fast and super powerful', price=99.00, year=2020, image='bikes/fb_r.jpg', category=Category.objects.get(name='Sport'))
fireblade.slug = slugify(fireblade.name)
fireblade.save()

print('Bikes created:')
for bike in Bike.objects.all():
    print(f'\t{bike}')


