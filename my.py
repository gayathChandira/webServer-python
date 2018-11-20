import socket
import sys
import threading
import subprocess

host, port = 'localhost',8080
file_route = 'main'
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_server():

    try:
        print("Starting server on {host}:{port}.....".format(host=host, port=port))
        soc.bind((host,port))            # binding socket with network interface and port
        print("Server started on port {port}.".format(port=port))

    except Exception as e:
        print(e)            # if port is not available
        print("Error: Could not bind to port {port}".format(port=port))
        shutdown()
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
        print(fileName)

        try:
            if (fileName == '/'):
                fileName = '/index.html'
            if "." not in fileName:
                raise IndexError

            file_path = file_route + fileName
            file = open(file_path,'rb')    # read bytes
            response_data = file.read()
            file.close()
            try:
                if (fileName.split('.')[1] == "php"):
                    result = subprocess.run(
                        ['php', file_path],        # program and arguments
                        stdout=subprocess.PIPE,     # capture stdout
                        check=True                # raise exception if program fails
                    )
                    response_data = result.stdout
                    print(response_data)
            except:
                pass

            content_type =''
            if fileName.endswith('.html') or fileName.endswith('.php'):
                content_type += 'Content-Type: text/html\n'
            elif fileName.endswith('.jpg') or fileName.endswith('.jpeg'):
                content_type += 'Content-Type: image/jpeg\n'
            elif fileName.endswith('.png'):
                content_type += 'Content-Type: image/png\n'
            elif fileName.endswith('.css'):
                content_type += 'Content-Type: text/css\n'
            elif fileName.endswith('.pdf'):
                content_type += 'Content-Type: application\pdf\n'
            elif fileName.endswith('.js'):
                content_type += 'Content-Type: application\javascript\n'
            elif fileName.endswith('.mp4'):
                content_type += 'Content-Type: video\mp4\n'

            if "." not in fileName:
                raise IndexError

            header = "HTTP/1.1 200 OK\n"

            header += content_type
            header += 'Connection Close \n\n'
            print(header)

        except IndexError as e:    # if user not defined file type correctly
            print(e)
            header = 'HTTP/1.1 400 Bad Request\n\n'
            response_data = b"<h1>malformed syntax</h1><p>No file type defined!</p>"

        except FileNotFoundError as e :
            print(e)
            header = 'HTTP/1.1 404 Not Found\n\n'
            fileName = '/404error.html'
            file_path = file_route + fileName
            file = open(file_path,'rb')
            response_data = file.read()
            file.close()
            print(file_path)


        response = header.encode()
        response += response_data
        connection.send(response)
        connection.close()
        break

def shutdown():
    soc.shutdown(socket.SHUT_RDWR) # shut down the read and write

start_server()
