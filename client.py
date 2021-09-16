from os import close
import socket
import argparse
import ssl

INI_INFO = 'ex_string'
PORT = 27993       
HELLOMESSAGE = 'HELLO'
FINDMESS = 'FIND'
BYEMESS = 'BYE'
COUNTMESS = 'COUNT'

# handle the bye situation
def bye_handle(all_data,server):
    encrypted = all_data[2]
    print(encrypted)
    server.close()
    
    

# handle the find situation
def find_handle(all_data,server):
    result = all_data[3].count(all_data[2])
    server.sendall("{0} {1} {2}\n".format(INI_INFO,COUNTMESS,result).encode('UTF-8'))
    result = server.recv(8192).decode('UTF-8')
    
    while 1:
        if not result.endswith("\n"):
            temp = server.recv(8192).decode('UTF-8')
            result += temp
        else:
            break
    return result
    
    

if __name__ == "__main__":
    # parse the argument.
    pars = argparse.ArgumentParser(description='command line')
    # parse the port, default is 27993.
    pars.add_argument('-p',dest='port',type=int,default=PORT,help='port')
    # parse the optional flag.
    pars.add_argument('-s',dest='encrypted',action='store_true',help='optional flag')
    # parse the hostname.
    pars.add_argument('hostname',type=str,help='hostname')
    # parse the neuid.
    pars.add_argument('NEU_ID',help='NEU_ID')
    # the result parsing result.
    args = pars.parse_args()
    
    # initial a socket.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    if args.encrypted:
        args.port = 27994
        server = ssl.wrap_socket(server)

    # try connect it.
    try:
        server.connect((args.hostname,args.port))
    except:
        server.close()
        print('error connecting to the server') 
        exit()

    server.sendall(("{0} {1} {2}\n".format(INI_INFO,HELLOMESSAGE, args.NEU_ID)).encode('UTF-8'))
    # get all the back data
    back = server.recv(8192).decode('UTF-8')
    # complete the data
    while 1: 
        if not back.endswith("\n"):
            temp = server.recv(8192).decode('UTF-8')
            back += temp
        else:
            break

    all_data = back.split()
    # handle the find message
    back2 = find_handle(all_data,server)
    # deal with the loop message between find and bye
    while 1:   
        all_data2 = back2.split()
        if all_data2[1] == FINDMESS:
            back2 = find_handle(all_data2,server)
        if all_data2[1] == BYEMESS:
            bye_handle(all_data2,server)
            break




