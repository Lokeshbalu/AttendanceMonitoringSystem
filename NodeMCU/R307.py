#copyrights reserved by adorein
#author	: R.Lokesh
#email	: lokeshbalaji68@gmail.com
def genImage(uart):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x03)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x05)
	uart.write(buf)
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	return k[9]
def image2Tz(uart,x):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x04)
	buf.append(0x02)
	buf.append(x)
	buf.append(0x00)
	buf.append(0x07+x)
	uart.write(buf)
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	return k[9]
def regModel(uart):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x03)
	buf.append(0x05)
	buf.append(0x00)
	buf.append(0x09)
	uart.write(buf)
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	return k[9]

def storeModel(uart,location):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x06)
	buf.append(0x06)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(location)
	buf.append(0x00)
	buf.append(0x0e+location)
	uart.write(buf)
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	return k[9]

def verifyModel(uart):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x08)
	buf.append(0x04)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x00)
	buf.append(0x00)
	buf.append(0x10)
	buf.append(0x00)
	buf.append(0x1e)
	uart.write(buf)
	da=[]
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	da.append(k[9])
	da.append(k[10])
	da.append(k[11])
	return da
def empty(uart):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x03)
	buf.append(0x0d)
	buf.append(0x00)
	buf.append(0x11)
	uart.write(buf)
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	return k[9]
def delete(uart,ids):
	buf=bytearray()
	buf.append(0xef)
	buf.append(0x01)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0xff)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x07)
	buf.append(0x0c)
	buf.append(0x00)
	buf.append(ids)
	buf.append(0x00)
	buf.append(0x01)
	buf.append(0x00)
	buf.append(0x15+ids)
	uart.write(buf)
	print("waiting")
	while not (uart.any()>0):
		pass
	print("count is "+str(uart.any()))
	k=uart.read(22)
	for data in k:
		print(data)
	return k[9]