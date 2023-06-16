from bike.models import Bike, BikeStatus
import requests
import datetime
import time

PORT = 89
TIMEOUT = 3 # seconds
#BIKE_NAME = 'Ducati 916'
BIKE_NAME = 'Honda Shadow'
DELAY = 30

# api-endpoint
URI = '/api/'

bike = Bike.objects.get(name=BIKE_NAME) 

IP_ADDRESS = bike.ip_address

# sending get request and saving the response as response object
#r = requests.get(url = 'http://' + IP_ADDRESS + ':' + str(PORT) + URI + 'is_locked')

# extracting data in json format
#data = r.json()

#print(data[IP_ADDRESS])

#if data[IP_ADDRESS] == 'OK':
#	BikeStatus(bike=bike, is_online = True, is_locked = )

def getStatus():
    try:
        print('1')
        # sending get request and saving the response as response object
        r = requests.get(url = 'http://' + IP_ADDRESS + ':' + str(PORT) + URI + 'is_locked', timeout = TIMEOUT)
        is_online = True
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        is_online = False
        is_locked = None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        is_online = False
        is_locked = None
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        return None
    else:
        # extracting data in json format
        data = r.json()
        if data[IP_ADDRESS] == 'True':
            is_locked = True
        elif data[IP_ADDRESS] == 'False':
            is_locked = False

    return {
        'is_online' : is_online,
        'is_locked' : is_locked
    } 
    

try:
    status = getStatus()
    # Create a BikeStatus
    try:
        bikeStatus = BikeStatus(bike = bike, is_online = status['is_online'], is_locked = status['is_locked'])
        bikeStatus.save()
    except Exception as e:
        print("Error creating BikeStatus:", str(e))
except Exception as e:
        print("An error occurred:", str(e))


