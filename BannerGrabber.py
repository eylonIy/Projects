import socket
def GrabTheBan():
    sock = socket.socket()
    ip=input("what ip to banner grab \n ")
    portMin=int(input("Enter the first port in the range \n"))
    portMax=int(input("Enter the last port in the range \n"))
    for x in range(portMin,portMax):
        sock = socket.socket()
        try:
            sock.connect((ip,x))
            sock.settimeout(0.3)
            print(f"The port {x} is open")
            sock.send("test \r\n".encode())
            banner = sock.recv(10000).decode()
            print(f"The banner is {banner}")
            sock.close()
        except:
            print(f"the port {x} is closed")
            sock.close()

GrabTheBan()