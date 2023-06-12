import struct
import asyncio
from bleak import BleakScanner, BleakClient

uuid_service = "00002a6e-0000-1000-8000-00805f9b34fb"

async def main():
	address = "02:91:52:01:1A:A6"
	async with BleakClient(address) as client:
		print("Connected")
		svcs = await client.get_services()
		print("Services:")
		for service in svcs:
			print(service)
		
		while True: 
			data = await client.read_gatt_char(uuid_service)
			#print(int.from_bytes(data, byteorder='big'))
			data_unpacked = struct.unpack("<h", data)
			x = data_unpacked[0]
			print(x)
			
			text_file = open("shared_2.txt", "w")
			if x == 0:
				text_file.write("00")
			elif x == 1:
				text_file.write("10")
			elif x == 2:
				text_file.write("02")
			elif x == 3:
				text_file.write("12") 
			text_file.close()		
				
asyncio.run(main())
