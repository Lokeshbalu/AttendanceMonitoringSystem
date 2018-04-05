import socket
import time
import network
from machine import UART
from machine import Pin
from machine import I2C
import R307
import lcd16x2
#intilising the uart 0
uart=UART(0,57600)
uart.init(baudrate=57600,bits=8,parity=None,stop=1)


#count of students
iner=[]
ins=0
gid=0
d_id=0
tot=10
#initlising the I2C line for LCD  display
i2c = I2C(scl=Pin(5), sda=Pin(4))
devices=i2c.scan()
if len(devices)==0:
	print("no LCD display attached")
for data in devices:
	print("device address found: "+str(data))
time.sleep(1)
lcd=lcd16x2.lcd(i2c)

#connects to wifi
try:
	lcd.lcd_clear()
	lcd.lcd_display_string("Connecting WiFi",1)
except Exception as e:
	print("no lcd found")
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
time.sleep(2)
while not sta_if.isconnected():
	sta_if.connect('new','RVLBlokesh')
	time.sleep(2)
	try:
		lcd.lcd_clear()
		lcd.lcd_display_string("Connecting..",1)
	except Exception as e:
		print("no lcd found")
try:
	lcd.lcd_clear()
	lcd.lcd_display_string("Connected",1)
except Exception as e:
	print("no lcd found")

#initilising sensing pin
finger_sense=Pin(2,Pin.IN)
time.sleep(2)

#Making connection to the server
try:
	lcd.lcd_clear()
	lcd.lcd_display_string("fetch server..",1)
except Exception as e:
	print("no lcd found")
soc=socket.socket()
soc3=socket.socket()
ip="192.168.43.49"
port=3000
port3=2000
check=True
while check:
	try:
		soc.connect((ip,port))
		time.sleep(2)
		soc3.connect((ip,port3))
		time.sleep(2)
		check = False
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("fetched",1)
		except Exception as e:
			print("no lcd found")
	except Exception as e:
		time.sleep(5)
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("No server",1)
		except Exception as e:
			print("no lcd found")

#LCD default screen
def lcdDefault():
	global lcd
	global ins
	global iner
	global tot
	ins=len(iner)
	try:
		lcd.lcd_clear()
		tex="present: "+str(ins)
		lcd.lcd_display_string(tex,1)
		tex2="persent %:"+str((ins/tot)*100)
		lcd.lcd_display_string(tex2,2)
	except Exception as e:
		print("no lcd found")

#The function the verifies the person
def Fingercheck(x):
	global iner
	global soc3
	global uart
	global lcd
	print("entered the mode")
	#soc2.send("Entered".encode('utf-8'))
	try:
		lcd.lcd_clear()
		lcd.lcd_display_string("place firmly",1)
		time.sleep(2)
		lcd.lcd_clear()
		lcd.lcd_display_string("verifing...",1)
	except Exception as e:
		print("no lcd found")
	k=R307.genImage(uart)
	if k==0:
		#soc2.send("imaged".encode('utf-8'))
		res=R307.image2Tz(uart,0x01)
		if res==0:
			#soc2.send("Templated".encode('utf-8'))
			res=R307.verifyModel(uart)
			if res[0]==0:
				dd=str(res[1])+str(res[2])
				#soc2.send(dd.encode("utf-8"))
				solo=int(dd)
				if solo not in iner:
					if solo>0:
						iner.append(solo)
				sed="atten"+"\r\n"+"C"+"\r\n"+dd
				soc3.send(sed.encode("utf-8"))
				time.sleep(2)
				rep=soc3.recv(1024)
				rep=rep.decode('utf-8')
				reps=rep.split("\r\n")
				pers="per%: "+reps[1]
				try:
					lcd.lcd_clear()
					lcd.lcd_display_string(reps[0],1)
					lcd.lcd_display_string(pers,2)
				except Exception as e:
					print("no lcd found")
			else:
				try:
					lcd.lcd_clear()
					lcd.lcd_display_string("verification",1)
					lcd.lcd_display_string("failed",2)
				except Exception as e:
					print("no lcd found")
		else:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("Templating",1)
				lcd.lcd_display_string("failed",2)
			except Exception as e:
				print("no lcd found")
	else:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("Generation",1)
			lcd.lcd_display_string("failed",2)
		except Exception as e:
			print("no lcd found")
	

#initiating the trigger for every finger sense
finger_sense.irq(trigger=Pin.IRQ_FALLING , handler=Fingercheck)

#The code that executes when enrollment is called
def enroll(x):
	global uart
	global lcd
	global gid
	errs=0
	try:
		lcd.lcd_clear()
		lcd.lcd_display_string("Enrolling",1)
	except Exception as e:
		print("no lcd found")
	time.sleep(2)
	try:
		lcd.lcd_clear()
		lcd.lcd_display_string("generating temp1",1)
	except Exception as e:
		print("no lcd found")
	k=R307.genImage(uart)
	if k==0:
		res=R307.image2Tz(uart,0x01)
		if res==0:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("Templated",1)
			except Exception as e:
				print("no lcd found")
		else:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("generation",1)
				lcd.lcd_display_string("failed",2)
				errs=1
			except Exception as e:
				print("no lcd found")
	else:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("generation error",1)
			errs=1
		except Exception as e:
			print("no lcd found")
	time.sleep(3)
	if errs==1:
		finger_sense=Pin(2,Pin.IN)
		finger_sense.irq(trigger=Pin.IRQ_FALLING , handler=Fingercheck)
		return
	try:
		lcd.lcd_clear()
		lcd.lcd_display_string("generating temp2",1)
	except Exception as e:
		print("no lcd found")
	k=R307.genImage(uart)
	if k==0:
		res=R307.image2Tz(uart,0x02)
		if res==0:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("Templated",1)
			except Exception as e:
				print("no lcd found")
		else:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("generation error",1)
				errs=1
			except Exception as e:
				print("no lcd found")
	else:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("generation error",1)
			errs=1
		except Exception as e:
			print("no lcd found")
	time.sleep(2)
	if errs==1:
		finger_sense=Pin(2,Pin.IN)
		finger_sense.irq(trigger=Pin.IRQ_FALLING , handler=Fingercheck)
		return
	try:
		lcd.lcd_clear()
		lcd.lcd_display_string("registering",1)
	except Exception as e:
		print("no lcd found")
	k=R307.regModel(uart)
	if k==0:
		res=R307.storeModel(uart,ids)
		if res==0:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("Registered.",1)
			except Exception as e:
				print("no lcd found")
		else:
			try:
				lcd.lcd_clear()
				lcd.lcd_display_string("store error",1)
			except Exception as e:
				print("no lcd found")
	else:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("reg error",1)
		except Exception as e:
			print("no lcd found")
	time.sleep(2)
	finger_sense=Pin(2,Pin.IN)
	finger_sense.irq(trigger=Pin.IRQ_FALLING , handler=Fingercheck)
	lcdDefault()
#code that empties the entire templates stored on the device
def empty():
	global uart
	global lcd
	res=R307.empty(uart)
	if res==0:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("Emptied",1)
			lcd.lcd_display_string("successfully",2)
		except Exception as e:
			print("no lcd found")
	else:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("Process",1)
			lcd.lcd_display_string("failed",2)
		except Exception as e:
			print("no lcd found")
	time.sleep(2)
	finger_sense=Pin(2,Pin.IN)
	finger_sense.irq(trigger=Pin.IRQ_FALLING , handler=Fingercheck)
	lcdDefault()
#code that deletes a template
def delet(x):
	global uart
	global lcd
	global d_id
	res=R307.delete(uart,d_id)
	if res==0:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("Deleted",1)
			lcd.lcd_display_string("successfully",2)
		except Exception as e:
			print("no lcd found")
	else:
		try:
			lcd.lcd_clear()
			lcd.lcd_display_string("Deleting",1)
			lcd.lcd_display_string("failed",2)
		except Exception as e:
			print("no lcd found")
	time.sleep(2)
	finger_sense=Pin(2,Pin.IN)
	finger_sense.irq(trigger=Pin.IRQ_FALLING , handler=Fingercheck)
	lcdDefault()

#.....................code that loops executes all time.............
while  True:

#Receving command from user
	cmd=soc.recv(1024)
	cmd=cmd.decode("utf-8")
#carrying out actions according to the command
	if cmd=="enroll":
		soc.send("Enter the id of the student :".encode('utf-8'))
		k=soc.recv(1024)
		k=k.decode('utf-8')
		gid=int(k)
		finger_enroll=Pin(2,Pin.IN)
		finger_enroll.irq(trigger=Pin.IRQ_FALLING , handler=enroll)
		time.sleep(2)
	if cmd=="empty":
		soc.send("Are you sure to empty database(yes/no):".encode('utf-8'))
		k=soc.recv(1024)
		k=k.decode('utf-8')
		if k="yes":
			empty()
		else:
			pass
	if cmd=="delet":
		soc.send("Enter the id to delete:".encode('utf-8'))
		k=soc.recv(1024)
		k=k.decode('utf-8')
		d_id=int(k)
		finger_delete=Pin(2,Pin.IN)
		finger_delete.irq(trigger=Pin.IRQ_FALLING , handler=delet)























