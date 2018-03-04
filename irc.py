raw_server_messages = False
raw_client_messages = False

# ----------------------------------------------------------------------------
#TODO Improve/unify repl reporting/debugging code
import socket
import ure
from gc import collect

sock=None
channel=""
nick=""

def join():
    global sock, nick, channel # FIXME?
    sock.send(b"NICK %s\r\n" % nick)
    sock.send(b"USER %s 8 * :%s\r\n" % (nick,nick))
    #for ch in c:
    sock.send(b"JOIN %s\r\n" % channel)
    print("joining channel " + str(channel))

def send_msg_to_channel(chan, msg, use_notice):
    global sock # FIXME?
    tosend = b"%s %s :%s\r\n" % ("NOTICE" if use_notice else "PRIVMSG",chan,msg)
    sock.send(tosend)
    if raw_client_messages: print("Client sent: [%s]" % tosend)

def do_server():
    global sock,nick
    collect()
    line = sock.readline()
    if line != None:
        if len(line) < 3: print("Unexpected short line length (%d characters)" % len(line))
        if not (line[-2]==13 and line[-1]==10): # Assume all IRC messages should end in \r\n
            print("Invalid message from server; ignoring message"); return
        if raw_server_messages and len(line)>1: print("Server sent: [%s]" % line)
        if line.find(b"PING :") == 0:
            _ = sock.send(b"PONG :%s" % line[6:])
            if raw_client_messages: print("Client sent: [%s]" % (b"PONG :%s" % line[6:]))
        elif line.find(b"PRIVMSG " + str(channel)) != -1:
            print("msg received")
            return 1
        elif line.find(b":Nickname is already in use") != -1:
            print("Nickname '%s' is already in use" % nick)
            nick = nick + "_"
            join()
        elif line.find(b"Welcome to HackINT") != -1:
            print("Connected, joining channel")
            join()
        else:
            pass

def connect(server,port,channel_,nick_):#,suffixes_,actions_,responses_):
    global sock,channel,nick
    channel=channel_
    nick=nick_

    sock = socket.socket()
    addr = socket.getaddrinfo(server, port)
    sock.connect(addr[0][-1])
    sock.setblocking(False)
    join()
