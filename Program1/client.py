import socket
import struct
import sys

#getting command line arguments
for args in sys.argv:
    if args == '-s':
        server = sys.argv[sys.argv.index(args)+1]
    elif args == '-p':
        port = int(sys.argv[sys.argv.index(args)+1])
    elif args == '-l':
        logfile = sys.argv[sys.argv.index(args)+1]

#creating socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connecting to client
server_address = (server, port)
sock.connect(server_address)

print("Received connection from (IP, PORT): ", server_address)

#variables for the hello message
msg = 'HELLO'
msgLength = len(msg)
version = 17
msgType = 1

#method for packing the variables into a struct
def packing(fversion, fmsgType, fmsgLength, fmsg):
    return struct.pack(f'! 3i {fmsgLength}s', fversion, fmsgType, fmsgLength, fmsg.encode())

#packing
packed = packing(version, msgType, msgLength, msg)

print("Sending HELLO packet")
#sending
sock.send(packed)




serverReceived = sock.recv(struct.calcsize('! 3i 5s'))
sversion, smsgType, smsgLength, smsg = struct.unpack('! 3i 5s', serverReceived)
print("Received Data: version: ", sversion," message_type: ", smsgType, " length: ", smsgLength)

File_object = open(logfile, "w")

if sversion == 17:
    print("VERSION ACCEPTED")
    File_object.write("VERSION ACCEPTED")
    print("Received Message Hello")

    #variables for the command packet
    msg2 = "LIGHTON"
    msgLength2 = len(msg2)
    verison2 = 17
    msgType2 = 1

        #packing
    packed2 = packing(verison2, msgType2, msgLength2, msg2)

    print("Sending command")
        #sending
    sock.sendall(packed2)

    serverReceived2 = sock.recv(struct.calcsize('! 3i 7s'))
    sversion2, smsgType2, smsgLength2, smsg2 = struct.unpack('! 3i 7s', serverReceived2)
    File_object.write(f"Server response: {smsg2}")
    print("Command Successful")

else:
    print("VERSION MISMATCH")
    File_object.write("VERSION MISMATCH")

print("Closing socket")  
sock.close()

