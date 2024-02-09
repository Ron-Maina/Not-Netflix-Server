# Not-Netflix App
Server for the Not-Netflix App

By Ron Maina

# Description
This is the server side for the Netflix Clone web Application built using Flask and SQLAlchemy

# How to Use
## Requirements
* A computer, tablet or phone
- Access to the internet

## Using the Api
The user can navigate the web app and should be able to: 

* See available endpoints
- Make requests on unprotected endpoints

# Run Locally
## Setup Requirements
To run this app locally, you need a PC with the following:

* Internet Access
* Visual Studio Code
## Installation Process

1. Clone this repository by running the following in your terminal 
```
git clone git@github.com:Ron-Maina/Not-Netflix-Server.git
```
2. Change directory using:
```
cd Not-Netflix-Server
```
and open in visual studio using 
```
code .
```
3. Open a new terminal window in visual studio code and run the folowing commands to run the server
```
pip install -r requirements.txt
``` 
```
flask db init
``` 
```
flask db migrate
``` 
```
flask db upgrade
``` 
```
flask run 
``` 
to start the web app

# Technologies Used
* Flask
* Python
* Flask-RestX
* SQLAlchemy

# License 
MIT License

Copyright (c) 2023 Ron Maina

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE