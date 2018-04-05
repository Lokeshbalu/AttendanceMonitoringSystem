import sqlite3
import time
sec='C'
names=["Raushan","Mubasheer","Lokesh","Keerthana","Divya"]
ids=[1,2,3,4,5]
Rolls=["14751A04B4","14751A04C2","14751A04A9","14751A04C0","14751A04D4"]
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
loca=time.localtime()
tyear=loca[0]
tmonth=loca[1]
tday=loca[2]
database="database/"+sec+str(calen[tmonth])
table=calen[tmonth]+str(tday)
conn=sqlite3.connect(database)
c=conn.cursor()
c.execute("create table "+table+" (id Integer,Name Text,RollNo Text,P1 Integer,P2 Integer,P3 Integer,P4 Integer,P5 Integer,P6 Integer,P7 Integer)")
conn.commit()
i=0
for data in names:
	print("Enter")
	c.execute("insert into "+table+" values ("+str(ids[i])+",'"+data+"','"+Rolls[i]+"',0,0,0,0,0,0,0)")
	conn.commit()
	i=i+1
c.close()
conn.close()