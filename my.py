import socket
import sys
import time
import threading

host, port = 'localhost',801
file_route = 'main'
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_server():
    try:
        print("Starting web server on {host}:{port}.....".format(host=host, port=port))
        soc.bind((host,port))            # binding socket with network interface and port
        print("Server started on port {port}.".format(port=port))
    except Exception as e:
        print("Error: Could not bind to port {port}".format(port=port))
        # shutdown()
        print(e)
        sys.exit(1)       # exit from the program
    connect()

def connect():
    while True:
        soc.listen(4)     # listening for connctions from client , 4 is number of invalid connections before terminate
        client_connection,client_address = soc.accept()
        # print("connection : ", client_connection)
        # print("address : " , client_address)
        t = threading.Thread(target = controlling, args=(client_connection,))
        t.start()

def controlling(connection):
    while True:
        try:
            data = connection.recv(1024)
            str_data = bytes.decode(data)  # string converted data
            if not str_data:
                break
        except Exception as e:
            print("Request timeout {e}").format(e=e)
            break
        print(str_data)

        fileName = str_data.split(' ')[1].split('?')[0]
        try:


            if (fileName == '/'):
                fileName = '/index.html'
            file_path = file_route + fileName

            file = open(file_path,'rb')    # read bytes
            response_data = file.read()
            file.close()



            content_type =''
            if fileName.endswith('.html'):
                content_type += 'Content-Type: text/html\n'
            elif fileName.endswith('.jpg') or fileName.endswith('.jpeg'):
                content_type += 'Content-Type: image/jpeg\n'
            elif fileName.endswith('.png'):
                content_type += 'Content-Type: image/png\n'
            elif fileName.endswith('.css'):
                content_type += 'Content-Type: text/css\n'
            header = "HTTP/1.1 200 OK\n"
            # if type == 'htm' or type == 'html':
            #     header += 'Content-Type: text/html\n'
            # elif type == 'jpg' or type == 'jpeg':
            #     header += 'Content-Type: image/jpeg\n'
            # elif type == 'png':
            #     header += 'Content-Type: image/png\n'
            # elif type == 'css':
            #     header += 'Content-Type: text/css\n'

            header += content_type
            header += 'Connection Close \n\n'
            print(header)
        except IndexError as e:
            print(e)
            header = makeHeader(400,'')
            response_data = b"<h1>malformed syntax<h1>"

        except UnboundLocalError as e:
            print(e)
            #header = makeHeader(400,'')
            header = 'HTTP/1.1 400 Bad Request\n'
            response_data = b"Malformed requested"
        

        except FileNotFoundError as e :
            print(e)
            #header = makeHeader(404,'')
            header = 'HTTP/1.1 404 Not Found\n'
            response_data =b"<h1>File not found<h1>"


        response = header.encode()
        response += response_data
        connection.send(response)
        connection.close()
        break

# def makeHeader(code, type):
#     print(type)
#     header =''
#     if code == 200:
#         header +="HTTP/1.1 200 OK\n"
#     elif code == 404:
#         header += 'HTTP/1.1 404 Not Found\n'
#     elif code == 400:
#         header += 'HTTP/1.1 400 Bad Request\n'
#
#     if type == 'jpg' or type == 'jpeg':
#         header += 'Content-Type: image/jpeg\n'
#     elif type == 'htm' or type == 'html':
#         header += 'Content-Type: text/html\n'
#     elif type == 'png':
#         header += 'Content-Type: image/png\n'
#     elif type == 'css':
#         header += 'Content-Type: text/css\n'
#
#     header += 'Connection: close\n\n'
#     return header

start_server()
