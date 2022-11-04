#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Remington Ward
# 10/25/2022
# CS 4390 HW 4 Task 1
# Instructor: Kresman
# This file is meant to be a simple web server for the purpose of testing the proxy server for task 1
# We process GET requests and respond with the requested file or a 404 Not Found 
#
# The server is created on the local machine at port 5544 which can be changed below


# In[2]:


port = 55441


# In[3]:


def multi_threaded_client(connection):
    while True:
        #Recieve request
        data = connection.recv(2048)
        request = data.decode('utf-8')
        print("--- Received Request from Client ---")
        print(request)
        
        #If we recieve a different request just end connection
        if(not "GET" in request[0:3]):
            print("--- Only GET requests supported ---")
            response = "HTTP/1.1 501 Not Implemented\r\n\r\n"
            connection.sendall(str.encode(response))
            print("\n--- Sent Response to Client ---")
            print(response)
            connection.close()
            return
        
        requestLines = request.split('\n')
        filepath = requestLines[0].split(' ')[1]
        if(os.path.exists('webserver_files/' + filepath)):
            file = open('webserver_files/' + filepath, 'r', encoding='utf-8')
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + file.read()
        else:
            file = open('webserver_files/NotFound.html')
            response = "HTTP/1.1 404 Not Found\r\n\r\n" + file.read()
        print("--- SENDING RESPONSE TO CLIENT ---")
        print(response)
        connection.sendall(str.encode(response))
    connection.close()


# In[ ]:


#Modified version of instructor Kresman's example code
import socket
import os
from _thread import *
ServerSideSocket = socket.socket()
host = '127.0.0.1'
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
    ServerSideSocket.listen(5)
    print('Socket is listening on port: ' + str(port))
except socket.error as e:
    print(str(e))
    ServerSideSocket.close()

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()


# In[ ]:




