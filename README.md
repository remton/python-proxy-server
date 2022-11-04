# python-proxy-server
Simple proxy server made in python. Routes requests to webserver and handles response. Will add files to cache as needed.

Author: Remington Ward

Date: 11/04/2022

This project was made for a class CS 4390 Networking with professor Kresman

The proxy server will process requests and respond in turn.
After starting the proxy in a web browser you should connext to it like, localhost:44551/webserver.com
If you areusing the mock webserver included in this project connect like, localhost:44551/localhost:55441/File1.txt

The proxy server is a python .py file. 
It should be run in a compatible IDE or using the python3 command via command line.
EX: Python3 proxy.py

There are no command line arguments. By default the proxy server runs on port 44551. This can be changed near the top of proxy.py file
Access a webserver by appending localhost:44551/ to the domain

In the same directory as the .py file the proxy server will create a directory “/proxy_cache” to add cached files

There is also a very simple mock webserver I made to test the proxy.
It runs on local machine with default port 55441.
It checks “/webserver_files” directory relative to its own directory for files to fullfill GET requests

