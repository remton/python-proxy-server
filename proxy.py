#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Remington Ward
# 10/25/2022
# CS 4390 HW 4 Task 1
# Instructor: Kresman
# This file is a simple proxy server
# We process Get requests and check if the requested file is in the cache
# If its in the cache we send that file to client
# If not in cache we create a GET request and send to Web Server
# We add to cache when a file is recieved from Web Server
# 
# Cache will be created at /prixy_cache in the same directory as this file
# The server is created on the local machine with a port assigned by the OS
# The port will be output to the console when this is ran


# In[2]:


import socket
import os
import select
from _thread import *
port = 44551
timeout = 15


# In[3]:


#This is the function run when a client connects
def multi_threaded_client(connection):
    while True:
        #Recieve request
        data = connection.recv(2048)
        request = data.decode('utf-8')
        print("\n--- Recieved Request from Client ---")
        print(request)

        #Request in form like "GET webserver.com/folder/file.html"
        #If we recieve a different request send not implemented
        if(not "GET" in request[0:3]):
            response = "HTTP/1.1 501 Not Implemented\r\n\r\n"
            connection.sendall(str.encode(response))
            print("\n--- Sent Response to Client ---")
            print(response)
            connection.close()
            break
        
        #parse request for the web address, host ip, port number, and requested file name
        requestLines = request.split('\n')
        webfilepath = requestLines[0].split(' ')[1] # 2nd "word" in first line GET '/webserver.com/dir.file.txt' HTTP/1.1
        webAddress = webfilepath.split('/',2)[1] # 1st part of filepath is the web address /'webserver.com'/dir/file.txt
        if(len(webfilepath.split('/',2)) > 2):
            filename = webfilepath.split('/',2)[2]
        else:
            filename = '/'
        if('localhost:' in webAddress):
            webfilepath = webfilepath.replace(":", "")
            webport = int(webAddress.split(':')[1].split('/')[0])
            webAddress = 'localhost'
            webhost = socket.gethostbyname(webAddress)
        else:
            webport = 80 #default port for http
            webhost = socket.gethostbyname(webAddress)
        
        #Look for file in cache
        print("\n--- Looking for file: " + filename + " at " + webAddress + " ---")
        #the file is in the cache
        if(os.path.exists('proxy_cache/' + webfilepath)):
            print("\n--- File found in cache! ---")
            file = open('proxy_cache/' + webfilepath, 'r', encoding='utf-8')
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + file.read()
        #the file is not in the cache
        else:
            print("\n--- Did not find file in cache ---")
            
            #create a socket to ask the web server for the page
            websocket = socket.socket()
            try:
                websocket.connect((webhost, webport))
            #We failed to create socket so we send bad request to client
            except socket.error as e:
                print("\n--- Could not create socket ---")
                print(str(e))
                response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
                connection.sendall(str.encode(response))
                print("\n--- Sent Response to Client ---")
                print(response)
                connection.close()
                return
            
            #Make a GET request
            webRequest = "GET " + filename + " HTTP/1.0\r\n\r\n"
            websocket.sendall(str.encode(webRequest))
            print("\n--- Sent GET Request to Web Server ---")
            print(webRequest)

            #read response into webdata
            try:
                BUFFERSIZE = 2048
                data = websocket.recv(BUFFERSIZE)
                webData = data
                if(not len(data) < BUFFERSIZE):
                    data = websocket.recv(BUFFERSIZE)
                    webData+=data
                    while(not len(data) < BUFFERSIZE):
                        data = websocket.recv(BUFFERSIZE)
                        webData+=data
            except (ConnectionError) as e:
                print("\n--- Could not get response from web server ---")
                print(str(e))
                response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
                connection.sendall(str.encode(response))
                print("\n--- Sent Response to Client ---")
                print(response)
                connection.close()
                return
            #decode response      
            webResponse = webData.decode('utf-8')
            print("\n--- Recieved Response from Web Server ---")
            print(webResponse)
            webHeader = webResponse.split('\r\n\r\n', 1)[0]

            #We recieved the file OK
            if("HTTP/1.1 200 OK" in webHeader):
                webMessage = webResponse.split('\r\n\r\n', 1)[1]
                #Add file to cache
                os.makedirs(os.path.dirname("proxy_cache" + webfilepath), exist_ok=True)
                cachefile = open("proxy_cache" + webfilepath, 'w')
                cachefile.write(webMessage)
                cachefile.close()
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + webMessage

            #The content is deleted. Remove from cache if it is there
            elif("HTTP/1.1 410 Gone" in webHeader):
                if os.path.exists("proxy_cache" + webfilepath):
                    os.remove("proxy_cache" + webfilepath)
                response = webResponse

            #Something else went wrong. Send the servers respnse to client
            else:
                response = webResponse

        #Send response to client
        connection.sendall(str.encode(response))
        print("\n--- Sent Response to Client ---")
        print(response)
    connection.close()


# In[4]:


#Modified version of instructor Kresman's example code
ServerSideSocket = socket.socket()
host = '127.0.0.1'
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
    print('Socket is listening on port: ' + str(port))
    ServerSideSocket.listen(5)
    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
except socket.error as e:
    print(str(e))
    
ServerSideSocket.close()

