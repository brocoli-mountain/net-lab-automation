#!/usr/bin/env python

import json
import requests
from collections import OrderedDict

raw_data = requests.get("http://10.0.50.20/api/dcim/devices/")
js_data = json.loads(raw_data.text)

lab_devices = { device['name'] : OrderedDict([('id', device['id'])])
	for device in js_data['results'] if device['tenant'] is not None 
		and device['tenant']['name'] == 'Lab' 
		and device['device_role']['slug'] == "router"
	}


int_mapping = OrderedDict([('fxp0', 0),
	('ge-0/0/0' , 1),
	('ge-0/0/1' , 2),
	('ge-0/0/2' , 3),
	('ge-0/0/3' , 4),
	('ge-0/0/4' , 5),
])

for k,v in lab_devices.items():
	# k = router name
	# v = the child dictionary
	device_id = v['id']
	lab_devices[k]['interfaces'] = []
	url = "http://10.0.50.20/api/dcim/interfaces/?device_id=%s" % device_id
	raw_data = requests.get(url)
	interfaces = json.loads(raw_data.text)
	for name,order in int_mapping.items():
		for intf in interfaces['results']:
			
			if name == intf['name']:
				if intf['description']:
					lab_devices[k]['interfaces'].append({'name':intf['description'], 'device_type' : 'vmxnet3'})
				else:
					lab_devices[k]['interfaces'].append({'name':"un-used adapters" , 'device_type' : 'vmxnet3'})	
print(json.dumps(wrapper))