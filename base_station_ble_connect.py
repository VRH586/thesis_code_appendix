from bleak import BleakClient, BleakScanner
import asyncio
import struct

def encode_to_binary(integer):
	binary = format(integer, '03b')
	binary_list = [int(bit) for bit in binary]
	return binary_list
	
def convert_to_string(lst):
	char_list = [str(num) for num in lst]
	string = ''.join(char_list)
	return string

async def connect_to_devices(device0_address, device1_address, device2_address):
	uuid_service = "00002a6e-0000-1000-8000-00805f9b34fb"
	
	# Create client instances, numbering changes to match physical devices
	device0_client = BleakClient(device0_address)
	device1_client = BleakClient(device1_address)
	device2_client = BleakClient(device2_address)

	try:
	# Connect to devices
		await device0_client.connect()
		await device1_client.connect()
		await device2_client.connect()

		# Print connection message
		print("Connected to all devices!")

		# Perform operations on the devices
		while True: 
			data_0 = await device0_client.read_gatt_char(uuid_service)
			data_1 = await device1_client.read_gatt_char(uuid_service)
			data_2 = await device2_client.read_gatt_char(uuid_service)
			data_unpacked_0 = struct.unpack("<h", data_0)[0]
			data_unpacked_1 = struct.unpack("<h", data_1)[0]
			data_unpacked_2 = struct.unpack("<h", data_2)[0]
			b0 = encode_to_binary(data_unpacked_0) #OK
			b1 = encode_to_binary(data_unpacked_1) #OK
			b2 = encode_to_binary(data_unpacked_2) #OK
			print("Badge#0: ", data_unpacked_0, b0)
			print("Badge#1: ", data_unpacked_1, b1)
			print("Badge#2: ", data_unpacked_2, b2)
			print()
			
			
			##Badge0 OK
			text_file = open("shared_badge_0.txt", "w")
			for x in range(3):
				if b0[x] == 1:
					b0[x] = x+1  
			print("b0 converted: ", b0)	
			b0 = convert_to_string(b0)
			print("b0 string: ", b0)
			text_file.write(b0)
			text_file.close()
			
			##Badge1
			text_file = open("shared_badge_1.txt", "w")
			if b1[0] == 1:
				b1[0] = 0
			else:
				b1[0] = 1	
			
			if b1[1] == 1:
				b1[1] = 2
			else:
				b1[1] = 1	
			
			if b1[2] == 1:
				b1[2] = 3
			else:
				b1[2] = 1	
			print("b1 converted: ", b1)	
			b1 = convert_to_string(b1)
			print("b1 string: ", b1)
			text_file.write(b1)
			text_file.close()
			
			##Badge2
			text_file = open("shared_badge_2.txt", "w")
			if b2[0] == 1:
				b2[0] = 0
			else:
				b2[0] = 2	
			
			if b2[1] == 1:
				b2[1] = 1
			else:
				b2[1] = 2	
			
			if b2[2] == 1:
				b2[2] = 3
			else:
				b2[2] = 2	
			print("b2 converted: ", b2)	
			b2 = convert_to_string(b2)
			print("b2 string: ", b2)
			text_file.write(b2)
			text_file.close()

	except Exception as e:
		await device0_client.disconnect()
		await device1_client.disconnect()
		await device2_client.disconnect()
		print(f"Error: {e}")

	finally:
		# Disconnect from devices
		await device0_client.disconnect()
		await device1_client.disconnect()
		await device2_client.disconnect()

		# Print disconnection message
		print("Disconnected from all devices.")

async def main():
	# Scan for devices
	#scanner = BleakScanner()
	#devices = await scanner.discover()

	# Find the addresses of the two devices you want to connect to
	device0_address = "02:91:52:01:45:FE"
	device1_address = "02:91:52:01:1A:A6"
	device2_address = "02:91:52:01:26:FE"

	if True:
		await connect_to_devices(device0_address, device1_address, device2_address)
	#else:
	#	print("Could not find all devices.")

# Run the program
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
