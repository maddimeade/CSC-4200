import socket
import struct
import sys

#getting command line arguments
for args in sys.argv:
    if args == '-p':
        port = int(sys.argv[sys.argv.index(args)+1])
    if args == '-l':
        logfile = sys.argv[sys.argv.index(args)+1]
    if args == "-p":
        url = sys.argv[sys.argv.index(args)+1]

#setting server
server = 'localhost'
#server = socket.gethostbyname(socket.gethostname())

#creating socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#specify where the server should listen on, IP and PORT
server_address_object = (server, port)
print("Address = ", server_address_object)
sock.bind(server_address_object)

#listening
sock.listen(1)

#connecting to client
connection_object, client_address = sock.accept()
print("Received connection from (IP, PORT): ", client_address)

#writing to file
File_object = open(logfile, "w")
File_object.write(f"Received connection from {client_address}")

#receiving data
byte_received = connection_object.recv(struct.calcsize('! 3i 5s'))
version, msgType, msgLength, msg = struct.unpack('! 3i 5s', byte_received)

print("Received Data: version: ", version," message_type: ", msgType, " length: ", msgLength)

#writing to file and sending output based on version and message type
if version == 17:
    File_object.write("VERSION ACCEPTED")
    print("VERSION ACCEPTED")

else:
    File_object.write("VERSION MISMATCH")
    print("VERSION MISMATCH")




#sending hello to client
serverMsg = 'HELLO'
serverMsgLength = len(serverMsg)
serverVerison = 17
serverMsgType = 1

#method for packing the variables into a struct
def packing(fversion, fmsgType, fmsgLength, fmsg):
    return struct.pack(f'! 3i {fmsgLength}s', fversion, fmsgType, fmsgLength, fmsg.encode())

#packing
serverPacket = packing(serverVerison, serverMsgType, serverMsgLength, serverMsg)

#sending
connection_object.sendall(serverPacket)




#receiving and unpacking
while True:

    byte_received2 = connection_object.recv(struct.calcsize('! 3i 7s'))
    version2, msgType2, msgLength2, msg2 = struct.unpack('! 3i 7s', byte_received2)

    print("Received Data: version: ", version2," message_type: ", msgType2, " length: ", msgLength2)

    #writing to file and sending output based on version and message type
    if version2 == 17:
        print("VERSION ACCEPTED")

        if msgType == 1:
            File_object.write(f"EXECUTING SUPPORTED COMMAND: {msg2}")
            print(f"EXECUTING SUPPORTED COMMAND: {msg2}")

        elif msgType == 2:
            File_object.write(f"EXECUTING SUPPORTED COMMAND: {msg2}")
            print(f"EXECUTING SUPPORTED COMMAND: {msg2}")

        else:
            File_object.write(f"IGNORING UNKNOWN COMMAND: {msg2}")
            print(f"IGNORING UNKNOWN COMMAND: {msg2}")

    else:
        File_object.write("VERSION MISMATCH")
        print("VERSION MISMATCH")



    #sending hello to client
    serverMsg2 = 'SUCCESS'
    serverMsgLength2 = len(serverMsg2)
    serverVerison2 = 17
    serverMsgType2 = 1

    #packing
    serverPacket2 = packing(serverVerison2, serverMsgType2, serverMsgLength2, serverMsg2)

    #sending
    connection_object.sendall(serverPacket2)

    if msgLength2 != 0:
        break