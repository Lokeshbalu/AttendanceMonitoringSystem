import socket
soc=socket.socket()
port=3000
ip="192.168.43.49"
soc.bind((ip,port))
soc.listen(20)
c,addr=soc.accept()
print(str(addr))
while True:
	cmd=raw_input("Enter your command.....;-)")
	print(cmd)
	c.send("enroll".encode('utf-8'))
	rec=c.recv(1024)
	rec=rec.decode('utf-8')
	print(rec)
	cmd=raw_input()
	cmd=str(cmd)
	c.send(cmd.encode('utf-8'))


	