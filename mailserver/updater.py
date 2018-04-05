import socket
import time
import threading
import sendmail
import sqlite3
soc=socket.socket()
port=2000
ip="192.168.43.49"
soc.bind((ip,port))
soc.listen(20)
locas=time.localtime()
tyear=locas[0]
tmonth=locas[1]
tday=locas[2]
presen=[]
absen=[]
present_period=1
calen=dict()
calen[1]="jan"
calen[2]="feb"
calen[3]="mar"
calen[4]="apr"
calen[5]="may"
calen[6]="jun"
calen[7]="jul"
calen[8]="aug"
calen[9]="sep"
calen[10]="oct"
calen[11]="nov"
calen[12]="dec"

idss=[]
conn=sqlite3.connect("database/attendance")
c=conn.cursor()
c.execute("select id from contacts")
k=c.fetchall()
for data in k:
	hmd=data[0]
	hmd=int(hmd)
	idss.append(hmd)
c.close()
conn.close()



def informabsence():
	global presen
	global absen
	global idss
	global names
	for i in idss:
		if i not in presen:
			absen.append(i)
	sendmail.sendmail(absen)
def emailalarm(h,m):
	print("informing absence")
	loca=time.localtime()
	hdiff=abs(h-loca[3])
	mdiff=abs(m-loca[4])
	print(hdiff)
	print(mdiff)
	sleepTime=(hdiff*60*60)+(mdiff*60)+loca[5]
	time.sleep(sleepTime)
	informabsence()

def updateattendance(sec,num):
	global tmonth
	global tyear
	global tday
	global present_period
	database="database/"+sec+str(calen[tmonth])
	print(database)
	conn=sqlite3.connect(database)
	c=conn.cursor()
	table=calen[tmonth]+str(tday)
	para="P"+str(present_period)
	tquery="update "+table+" set "+para+"=1 where id = "+str(num)
	print(tquery)
	c.execute(tquery)
	conn.commit()
	c.close()
	conn.close()
def listUpdation(h,m):
	global present_period
	loca=time.localtime()
	hdiff=abs(h-loca[3])
	mdiff=abs(m-loca[4])
	print(hdiff)
	print(mdiff)
	sleepTime=(hdiff*60*60)+(mdiff*60)+loca[5]
	print(str(sleepTime))
	time.sleep(sleepTime)
	presen=[]
	present_period=present_period+1
	print("updated"+str(present_period))
def packet(data0,data1,data2):
	global presen
	if data0=="atten":
		if data2 not in presen:
			presen.append(int(data2))
		print(presen)
		updateattendance(data1,data2)
#pers=threading.Thread(target=listUpdation,args=(19,57))
#pers.start()
#pers1=threading.Thread(target=listUpdation,args=(19,58))
#pers1.start()
ems=threading.Thread(target=emailalarm,args=(20,44))
ems.start()
while True:
	c,addr=soc.accept()
	print(str(addr))
	k=c.recv(1024)
	k=k.decode('utf-8')
	print(k)
	data=k.split("\r\n")
	print(data)
	thre=threading.Thread(target=packet,args=(data[0],data[1],data[2]))
	thre.start()