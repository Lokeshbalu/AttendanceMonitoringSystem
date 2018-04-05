import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def sendmail(contacts):
	tolist=[]
	for data in contacts:
		conn=sqlite3.connect("database/attendance")
		c=conn.cursor()
		c.execute("select email from contacts where id="+str(data))
		k=c.fetchall()
		l=k[0][0]
		l=str(l)
		print(l)
		tolist.append(l)
		conn.commit()
		c.close()
		conn.close()
	for data in tolist:
		print("connecting to smtp")
		#for tls the port number is 587 and host for gmail is smtp.gmail.com
		s = smtplib.SMTP(host="smtp.gmail.com", port=587)
		print("ok")
		s.starttls()
		s.login("lokeshbalaji68@gmail.com", "RVLB@loke=family")
		msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
		message = "You bloody I am SITAMS. Why are absent today??"

    # setup the parameters of the message
		msg['From']="lokeshbalaji68@gmail.com"
		print("sending mail to "+str(data))
		msg['To']=data
		msg['Subject']="This is TEST"

    # add in the message body
		msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
		s.sendmail("lokeshbalaji68@gmail.com",data,msg.as_string())
    	