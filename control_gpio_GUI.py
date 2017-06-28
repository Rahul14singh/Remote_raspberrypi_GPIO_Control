from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QFormLayout, QPushButton, QHBoxLayout, QApplication, QLabel, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QSize, QRect
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from urllib.request import urlopen
from scp import SCPClient
from json import dumps, JSONEncoder,loads
from base64 import b64encode, b64decode
import httplib2
import base64
import json
import paramiko
import pickle
import errno
import socket
import requests
import sys
import os

apiMethod="http://"
apiVersion="/v21"
apiServer="api.weaved.com"
apiKey="WeavedDemoKey$2015"
userName = "rahulsingh14jan95@gmail.com"
password = "rahul!14singham"
Devicename="Pi_SSH_22"
commandexec=""

def trap_exc_during_debug(*args):
    print(args)

sys.excepthook = trap_exc_during_debug

class workerThread(QThread):

    signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.abort = False
        
    @pyqtSlot()
    def run(self):
        #print("yeah yeah ")
        time.sleep(0.1)
        app.processEvents()
        self.signal.emit('Done')
        
    def __del__(self):
        #print("okay okay")
        self.abort = True
        self.wait()
        
class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}
    
class connection ():
    
    def trySSHConnect(self,host, portNum):
        paramiko.util.log_to_file ('paramiko.log') 
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(host,port=portNum,username="pi", password="raspberry")
            self.ssh.get_transport().window_size = 3 * 1024 * 1024
            command='python /home/pi/Desktop/control_gpio_pi/initial_check.py'
            stdin,stdout,stderr = self.ssh.exec_command(command)
            print('\nstout:',stdout.read())
        except paramiko.AuthenticationException:
            print ("Authentication failed!")
            return -1
        except paramiko.BadHostKeyException:
            print ("BadHostKey Exception!")
            return -1
        except paramiko.SSHException:
            print ("SSH Exception!")
            self.ssh.close()
            return -1
        except socket.error as e:
            print ("Socket error ", e)
            return -1
        except:
            print ("Could not SSH to %s, unhandled exception" % host)
            return -1
        print ("Made connection to " + host + ":" + str(portNum))
        return 0

    def proxyConnect(self,UID, token):
        my_ip = urlopen('http://ip.42.pl/raw').read()
        httplib2.debuglevel     = 0
        http                    = httplib2.Http()
        content_type_header     = "application/json"
        proxyConnectURL = apiMethod + apiServer + apiVersion + "/api/device/connect"

        proxyHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey,
            'token': token
            }

        proxyBody = {
            'deviceaddress': UID,
            'hostip': my_ip,
            'wait': "true"
            }

        response, content = http.request(
            proxyConnectURL,
            'POST',
            headers=proxyHeaders,
            body=dumps(proxyBody,cls=PythonObjectEncoder)
            )
        print ("Response = ", response)
        print ("Content = ", content)
        data = json.loads(content.decode('utf-8'))["connection"]["proxy"]
        print(data)
        URI = data.split(":")[0] + ":" + data.split(":")[1]
        URI = URI.split("://")[1]
        portNum = data.split(":")[2]
        print(URI)
        print(portNum)
        val = self.trySSHConnect(URI,int(portNum))
        if val==0:
            print("Yeah Check that it worked")
            return 1
        else:
            return 0

    def connectioncall(self):
        
        httplib2.debuglevel     = 0
        http                    = httplib2.Http()
        content_type_header     = "application/json"
        loginURL = apiMethod + apiServer + apiVersion + "/api/user/login"
        print ("Login URL = " + loginURL)
        loginHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey
            }
        try:        
            response, content = http.request(
                loginURL + "/" + userName + "/" + password,
                'GET',
                headers=loginHeaders)
        except:
            print ("Server not found.  Possible connection problem!")
            exit()
        try:
            data = json.loads(content.decode('utf-8'))
            if(data["status"] != "true"):
                print ("Can't connect to Weaved server!")
                print (data["reason"])
                exit()
            token = data["token"]
        except KeyError:
            print ("Comnnection failed!")
            exit() 
        print ("Token = " +  token)
        deviceListURL = apiMethod + apiServer + apiVersion + "/api/device/list/all"

        deviceListHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey,
            'token': token,
            }
            
        response, content = http.request(
            deviceListURL,
            'GET',
            headers=deviceListHeaders)
        print ("----------------------------------") 
        deviceData = json.loads(content.decode('utf-8'))
        print (deviceData)
        devices = deviceData['devices']
        for part in devices:
            if part['servicetitle']=='Bulk Service' and part['devicealias']==Devicename:
                BULKaddress=part['deviceaddress']
            elif part['servicetitle']=='HTTP' and part['devicealias']==Devicename:
                HTTPaddress=part['deviceaddress']
            elif part['servicetitle']=='SSH' and part['devicealias']==Devicename:
                SSHaddress=part['deviceaddress']
            elif part['servicetitle']=='VNC' and part['devicealias']==Devicename:
                VNCaddress=part['deviceaddress']
        print(SSHaddress)
        val=self.proxyConnect(SSHaddress,token)
        global success
        if val==1:
            success=1
        else:
            success=0
            
class General (QWidget,connection):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        try:
            self.setWindowState(QtCore.Qt.WindowMaximized)
        except:
            self.setGeometry(10, 30, 1350, 750)
            
        headerfont = QtGui.QFont("Cambria", 13, QtGui.QFont.Bold)
        
        l1 = QLabel("Enter your Account details ( User Name and Password ) and then the Device Name below:")
        l1.setFont(headerfont)
        l1.setMinimumHeight(30)
        l1.setFixedWidth(1000)
        l1.setFont(QtGui.QFont("Cambria", 16, QtGui.QFont.Bold))

        hboxuspass = QHBoxLayout()
        hboxuspass.setSpacing(10)
        l2 = QLabel("User Name: ")
        l2.setFont(headerfont)
        l2.setMinimumHeight(30)
        l2.setFixedWidth(180)
        self.text2 = QLineEdit()
        self.text2.setFixedWidth(300)
        self.text2.setMinimumHeight(30)
        self.text2.setFont(QtGui.QFont("Times", 11))
        self.text2.setText("Enter your User Name here")
        l3 = QLabel("Password: ")
        l3.setFont(headerfont)
        l3.setMinimumHeight(30)
        l3.setFixedWidth(120)
        self.text3 = QLineEdit()
        self.text3.setFixedWidth(300)
        self.text3.setMinimumHeight(30)
        self.text3.setText("Enter your Password here")
        self.text3.setFont(QtGui.QFont("Times", 11))
        hboxuspass.addWidget(l2)
        hboxuspass.addWidget(self.text2)
        hboxuspass.addWidget(l3)
        hboxuspass.addWidget(self.text3)
        hboxuspass.addStretch()

        hboxcheck = QHBoxLayout()
        hboxcheck.setSpacing(10)
        l4 = QLabel("Device Name for SSH: ")
        l4.setFont(headerfont)
        l4.setMinimumHeight(30)
        l4.setFixedWidth(185)
        self.text4 = QLineEdit()
        self.text4.setFixedWidth(300)
        self.text4.setMinimumHeight(30)
        self.text4.setText("Enter the Device Name as in WEAVED")
        self.text4.setFont(QtGui.QFont("Times", 11))
        self.checkbutton= QPushButton("CHECK AUTHENTICATION!", self)
        self.checkbutton.setFont(QtGui.QFont("Calibri", 13))
        self.checkbutton.setMinimumSize(200,30)
        self.checkbutton.clicked.connect(self.checkconnection)
        hboxcheck.addWidget(l4)
        hboxcheck.addWidget(self.text4)
        hboxcheck.addWidget(self.checkbutton)
        hboxcheck.addStretch()
        
        self.l5_1 = QPushButton("GPIO 2  PIN 3 : OFF", self)
        self.l5_1.setFont(QtGui.QFont("Calibri", 13))
        self.l5_1.setMinimumSize(200,30)
        self.l5_1.clicked.connect(self.l51)
        self.l6_1 = QPushButton("GPIO 3  PIN 5 : OFF", self)
        self.l6_1.setFont(QtGui.QFont("Calibri", 13))
        self.l6_1.setMinimumSize(200,30)
        self.l6_1.clicked.connect(self.l61)
        self.l7_1 = QPushButton("GPIO 4  PIN 7 : OFF", self)
        self.l7_1.setFont(QtGui.QFont("Calibri", 13))
        self.l7_1.setMinimumSize(200,30)
        self.l7_1.clicked.connect(self.l71)
        self.l8_1 = QPushButton("GPIO 17  PIN 11 : OFF", self)
        self.l8_1.setFont(QtGui.QFont("Calibri", 13))
        self.l8_1.setMinimumSize(200,30)
        self.l8_1.clicked.connect(self.l81)
        self.l9_1 = QPushButton("GPIO 27  PIN 13 : OFF", self)
        self.l9_1.setFont(QtGui.QFont("Calibri", 13))
        self.l9_1.setMinimumSize(200,30)
        self.l9_1.clicked.connect(self.l91)
        self.l10_1 = QPushButton("GPIO 22  PIN 15 : OFF", self)
        self.l10_1.setFont(QtGui.QFont("Calibri", 13))
        self.l10_1.setMinimumSize(200,30)
        self.l10_1.clicked.connect(self.l101)
        self.l11_1 = QPushButton("GPIO 10  PIN 19 : OFF", self)
        self.l11_1.setFont(QtGui.QFont("Calibri", 13))
        self.l11_1.setMinimumSize(200,30)
        self.l11_1.clicked.connect(self.l111)
        self.l12_1 = QPushButton("GPIO 9  PIN 21 : OFF", self)
        self.l12_1.setFont(QtGui.QFont("Calibri", 13))
        self.l12_1.setMinimumSize(200,30)
        self.l12_1.clicked.connect(self.l121)
        self.l13_1 = QPushButton("GPIO 11  PIN 23 : OFF", self)
        self.l13_1.setFont(QtGui.QFont("Calibri", 13))
        self.l13_1.setMinimumSize(200,30)
        self.l13_1.clicked.connect(self.l131)
        self.l14_1 = QPushButton("GPIO 5  PIN 29 : OFF", self)
        self.l14_1.setFont(QtGui.QFont("Calibri", 13))
        self.l14_1.setMinimumSize(200,30)
        self.l14_1.clicked.connect(self.l141)
        self.l15_1 = QPushButton("GPIO 6  PIN 31 : OFF", self)
        self.l15_1.setFont(QtGui.QFont("Calibri", 13))
        self.l15_1.setMinimumSize(200,30)
        self.l15_1.clicked.connect(self.l151)
        self.l16_1 = QPushButton("GPIO 13  PIN 33 : OFF", self)
        self.l16_1.setFont(QtGui.QFont("Calibri", 13))
        self.l16_1.setMinimumSize(200,30)
        self.l16_1.clicked.connect(self.l161)
        self.l17_1 = QPushButton("GPIO 19  PIN 35 : OFF", self)
        self.l17_1.setFont(QtGui.QFont("Calibri", 13))
        self.l17_1.setMinimumSize(200,30)
        self.l17_1.clicked.connect(self.l171)
        self.l18_1 = QPushButton("GPIO 26  PIN 37 : OFF", self)
        self.l18_1.setFont(QtGui.QFont("Calibri", 13))
        self.l18_1.setMinimumSize(200,30)
        self.l18_1.clicked.connect(self.l181)
        
        self.l5_2 = QPushButton("GPIO 18  PIN 12 : OFF", self)
        self.l5_2.setFont(QtGui.QFont("Calibri", 13))
        self.l5_2.setMinimumSize(200,30)
        self.l5_2.clicked.connect(self.l52)
        self.l6_2 = QPushButton("GPIO 23  PIN 16 : OFF", self)
        self.l6_2.setFont(QtGui.QFont("Calibri", 13))
        self.l6_2.setMinimumSize(200,30)
        self.l6_2.clicked.connect(self.l62)
        self.l7_2 = QPushButton("GPIO 24  PIN 18 : OFF", self)
        self.l7_2.setFont(QtGui.QFont("Calibri", 13))
        self.l7_2.setMinimumSize(200,30)
        self.l7_2.clicked.connect(self.l72)
        self.l8_2 = QPushButton("GPIO 25  PIN 22 : OFF", self)
        self.l8_2.setFont(QtGui.QFont("Calibri", 13))
        self.l8_2.setMinimumSize(200,30)
        self.l8_2.clicked.connect(self.l82)
        self.l9_2 = QPushButton("GPIO 8  PIN 24 : OFF", self)
        self.l9_2.setFont(QtGui.QFont("Calibri", 13))
        self.l9_2.setMinimumSize(200,30)
        self.l9_2.clicked.connect(self.l92)
        self.l10_2 = QPushButton("GPIO 7  PIN 26 : OFF", self)
        self.l10_2.setFont(QtGui.QFont("Calibri", 13))
        self.l10_2.setMinimumSize(200,30)
        self.l10_2.clicked.connect(self.l102)
        self.l11_2 = QPushButton("GPIO 12  PIN 32 : OFF", self)
        self.l11_2.setFont(QtGui.QFont("Calibri", 13))
        self.l11_2.setMinimumSize(200,30)
        self.l11_2.clicked.connect(self.l112)
        self.l12_2 = QPushButton("GPIO 16  PIN 36 : OFF", self)
        self.l12_2.setFont(QtGui.QFont("Calibri", 13))
        self.l12_2.setMinimumSize(200,30)
        self.l12_2.clicked.connect(self.l122)
        self.l13_2 = QPushButton("GPIO 20  PIN 38 : OFF", self)
        self.l13_2.setFont(QtGui.QFont("Calibri", 13))
        self.l13_2.setMinimumSize(200,30)
        self.l13_2.clicked.connect(self.l132)
        self.l14_2 = QPushButton("GPIO 21  PIN 40 : OFF", self)
        self.l14_2.setFont(QtGui.QFont("Calibri", 13))
        self.l14_2.setMinimumSize(200,30)
        self.l14_2.clicked.connect(self.l142)

        hboxl5 = QHBoxLayout()
        hboxl5.setSpacing(10)
        hboxl5.addWidget(self.l5_1)
        hboxl5.addWidget(self.l5_2)
        hboxl5.addStretch()

        hboxl6 = QHBoxLayout()
        hboxl6.setSpacing(10)
        hboxl6.addWidget(self.l6_1)
        hboxl6.addWidget(self.l6_2)
        hboxl6.addStretch()

        hboxl7 = QHBoxLayout()
        hboxl7.setSpacing(10)
        hboxl7.addWidget(self.l7_1)
        hboxl7.addWidget(self.l7_2)
        hboxl7.addStretch()

        hboxl8 = QHBoxLayout()
        hboxl8.setSpacing(10)
        hboxl8.addWidget(self.l8_1)
        hboxl8.addWidget(self.l8_2)
        hboxl8.addStretch()

        hboxl9 = QHBoxLayout()
        hboxl9.setSpacing(10)
        hboxl9.addWidget(self.l9_1)
        hboxl9.addWidget(self.l9_2)
        hboxl9.addStretch()

        hboxl10 = QHBoxLayout()
        hboxl10.setSpacing(10)
        hboxl10.addWidget(self.l10_1)
        hboxl10.addWidget(self.l10_2)
        hboxl10.addStretch()

        hboxl11 = QHBoxLayout()
        hboxl11.setSpacing(10)
        hboxl11.addWidget(self.l11_1)
        hboxl11.addWidget(self.l11_2)
        hboxl11.addStretch()

        hboxl12 = QHBoxLayout()
        hboxl12.setSpacing(10)
        hboxl12.addWidget(self.l12_1)
        hboxl12.addWidget(self.l12_2)
        hboxl12.addStretch()

        hboxl13 = QHBoxLayout()
        hboxl13.setSpacing(10)
        hboxl13.addWidget(self.l13_1)
        hboxl13.addWidget(self.l13_2)
        hboxl13.addStretch()

        hboxl14 = QHBoxLayout()
        hboxl14.setSpacing(10)
        hboxl14.addWidget(self.l14_1)
        hboxl14.addWidget(self.l14_2)
        hboxl14.addStretch()

        hboxl15 = QHBoxLayout()
        hboxl15.setSpacing(10)
        hboxl15.addWidget(self.l15_1)
        hboxl15.addWidget(self.l16_1)
        hboxl15.addStretch()

        hboxl16 = QHBoxLayout()
        hboxl16.setSpacing(10)
        hboxl16.addWidget(self.l17_1)
        hboxl16.addWidget(self.l18_1)
        hboxl16.addStretch()
        
        fbox = QFormLayout()
        fbox.setVerticalSpacing(20)
        fbox.addRow(l1)
        fbox.addRow(hboxuspass)
        fbox.addRow(hboxcheck)
        fbox.addRow(hboxl5)
        fbox.addRow(hboxl6)
        fbox.addRow(hboxl7)
        fbox.addRow(hboxl8)
        fbox.addRow(hboxl9)
        fbox.addRow(hboxl10)
        fbox.addRow(hboxl11)
        fbox.addRow(hboxl12)
        fbox.addRow(hboxl13)
        fbox.addRow(hboxl14)
        fbox.addRow(hboxl15)
        fbox.addRow(hboxl16)
        self.setLayout(fbox)
        self.setWindowTitle('CONTROL GPIO')
        self.setWindowIcon(QIcon('logso.png'))
        oImage = QImage("image2.jpg")
        sImage = oImage.scaled(QSize(1350,750))                   
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.show()
        
    def checkconnection (self):
        if self.text2.text() != "Enter your User Name here":
            userName=self.text2.text()
        if self.text3.text() != "Enter your Password here":
            password=self.text3.text()
        if self.text4.text() != "Enter the Device Name as in WEAVED":
            Devicename=self.text4.text()
        self.Connect=connection()
        self.Connect.connectioncall()
        if success==1:
            self.checkbutton.setText("SUCCESSFUL")
        else:
            self.checkbutton.setText("TRY AGAIN")
        #self.initial()
            
    def initial(self):
        global commandexec
        commandexec=""
        if self.l5_1.text() == "GPIO 2  PIN 3 : OFF":
            commandexec+="0"
        elif self.l5_1.text() == "GPIO 2  PIN 3 : ON":
            commandexec+="1"
        if self.l6_1.text() == "GPIO 3  PIN 5 : OFF":
            commandexec+="0"
        elif self.l6_1.text() == "GPIO 3  PIN 5 : ON":
            commandexec+="1"
        if self.l7_1.text() == "GPIO 4  PIN 7 : OFF":
            commandexec+="0"
        elif self.l7_1.text() == "GPIO 4  PIN 7 : ON":
            commandexec+="1"
        if self.l8_1.text() == "GPIO 17  PIN 11 : OFF":
            commandexec+="0"
        elif self.l8_1.text() == "GPIO 17  PIN 11 : ON":
            commandexec+="1"
        if self.l9_1.text() == "GPIO 27  PIN 13 : OFF":
            commandexec+="0"
        elif self.l9_1.text() == "GPIO 27  PIN 13 : ON":
            commandexec+="1"
        if self.l10_1.text() == "GPIO 22  PIN 15 : OFF":
            commandexec+="0"
        elif self.l10_1.text() == "GPIO 22  PIN 15 : ON":
            commandexec+="1"
        if self.l11_1.text() == "GPIO 10  PIN 19 : OFF":
            commandexec+="0"
        elif self.l11_1.text() == "GPIO 10  PIN 19 : ON":
            commandexec+="1"
        if self.l12_1.text() == "GPIO 9  PIN 21 : OFF":
            commandexec+="0"
        elif self.l12_1.text() == "GPIO 9  PIN 21 : ON":
            commandexec+="1"
        if self.l13_1.text() == "GPIO 11  PIN 23 : OFF":
            commandexec+="0"
        elif self.l13_1.text() == "GPIO 11  PIN 23 : ON":
            commandexec+="1"
        if self.l14_1.text() == "GPIO 5  PIN 29 : OFF":
            commandexec+="0"
        elif self.l14_1.text() == "GPIO 5  PIN 29 : ON":
            commandexec+="1"
        if self.l15_1.text() == "GPIO 6  PIN 31 : OFF":
            commandexec+="0"
        elif self.l15_1.text() == "GPIO 6  PIN 31 : ON":
            commandexec+="1"
        if self.l16_1.text() == "GPIO 13  PIN 33 : OFF":
            commandexec+="0"
        elif self.l16_1.text() == "GPIO 13  PIN 33 : ON":
            commandexec+="1"
        if self.l17_1.text() == "GPIO 19  PIN 35 : OFF":
            commandexec+="0"
        elif self.l17_1.text() == "GPIO 19  PIN 35 : ON":
            commandexec+="1"
        if self.l18_1.text() == "GPIO 26  PIN 37 : OFF":
            commandexec+="0"
        elif self.l18_1.text() == "GPIO 26  PIN 37 : ON":
            commandexec+="1"
        if self.l5_2.text() == "GPIO 18  PIN 12 : OFF":
            commandexec+="0"
        elif self.l5_2.text() == "GPIO 18  PIN 12 : ON":
            commandexec+="1"
        if self.l6_2.text() == "GPIO 23  PIN 16 : OFF":
            commandexec+="0"
        elif self.l6_2.text() == "GPIO 23  PIN 16 : ON":
            commandexec+="1"
        if self.l7_2.text() == "GPIO 24  PIN 18 : OFF":
            commandexec+="0"
        elif self.l7_2.text() == "GPIO 24  PIN 18 : ON":
            commandexec+="1"
        if self.l8_2.text() == "GPIO 25  PIN 22 : OFF":
            commandexec+="0"
        elif self.l8_2.text() == "GPIO 25  PIN 22 : ON":
            commandexec+="1"
        if self.l9_2.text() == "GPIO 8  PIN 24 : OFF":
            commandexec+="0"
        elif self.l9_2.text() == "GPIO 8  PIN 24 : ON":
            commandexec+="1"
        if self.l10_2.text() == "GPIO 7  PIN 26 : OFF":
            commandexec+="0"
        elif self.l10_2.text() == "GPIO 7  PIN 26 : ON":
            commandexec+="1"
        if self.l11_2.text() == "GPIO 12  PIN 32 : OFF":
            commandexec+="0"
        elif self.l11_2.text() == "GPIO 12  PIN 32 : ON":
            commandexec+="1"
        if self.l12_2.text() == "GPIO 16  PIN 36 : OFF":
            commandexec+="0"
        elif self.l12_2.text() == "GPIO 16  PIN 36 : ON":
            commandexec+="1"
        if self.l13_2.text() == "GPIO 20  PIN 38 : OFF":
            commandexec+="0"
        elif self.l13_2.text() == "GPIO 20  PIN 38 : ON":
            commandexec+="1"
        if self.l14_2.text() == "GPIO 21  PIN 40 : OFF":
            commandexec+="0"
        elif self.l14_2.text() == "GPIO 21  PIN 40 : ON":
            commandexec+="1"
        print(commandexec)
        
    def l51(self):
        if self.l5_1.text() == "GPIO 2  PIN 3 : OFF":
            self.l5_1.setText("GPIO 2  PIN 3 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/51high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l5_1.text() == "GPIO 2  PIN 3 : ON":
            self.l5_1.setText("GPIO 2  PIN 3 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/51low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l61(self):
        if self.l6_1.text() == "GPIO 3  PIN 5 : OFF":
            self.l6_1.setText("GPIO 3  PIN 5 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/61high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l6_1.text() == "GPIO 3  PIN 5 : ON":
            self.l6_1.setText("GPIO 3  PIN 5 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/61low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l71(self):
        if self.l7_1.text() == "GPIO 4  PIN 7 : OFF":
            self.l7_1.setText("GPIO 4  PIN 7 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/71high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l7_1.text() == "GPIO 4  PIN 7 : ON":
            self.l7_1.setText("GPIO 4  PIN 7 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/71low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l81(self):
        if self.l8_1.text() == "GPIO 17  PIN 11 : OFF":
            self.l8_1.setText("GPIO 17  PIN 11 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/81high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l8_1.text() == "GPIO 17  PIN 11 : ON":
            self.l8_1.setText("GPIO 17  PIN 11 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/81low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l91(self):
        if self.l9_1.text() == "GPIO 27  PIN 13 : OFF":
            self.l9_1.setText("GPIO 27  PIN 13 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/91high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l9_1.text() == "GPIO 27  PIN 13 : ON":
            self.l9_1.setText("GPIO 27  PIN 13 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/91low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l101(self):
        if self.l10_1.text() == "GPIO 22  PIN 15 : OFF":
            self.l10_1.setText("GPIO 22  PIN 15 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/101high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l10_1.text() == "GPIO 22  PIN 15 : ON":
            self.l10_1.setText("GPIO 22  PIN 15 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/101low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l111(self):
        if self.l11_1.text() == "GPIO 10  PIN 19 : OFF":
            self.l11_1.setText("GPIO 10  PIN 19 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/111high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l11_1.text() == "GPIO 10  PIN 19 : ON":
            self.l11_1.setText("GPIO 10  PIN 19 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/111low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l121(self):
        if self.l12_1.text() == "GPIO 9  PIN 21 : OFF":
            self.l12_1.setText("GPIO 9  PIN 21 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/121high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l12_1.text() == "GPIO 9  PIN 21 : ON":
            self.l12_1.setText("GPIO 9  PIN 21 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/121low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l131(self):
        if self.l13_1.text() == "GPIO 11  PIN 23 : OFF":
            self.l13_1.setText("GPIO 11  PIN 23 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/131high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l13_1.text() == "GPIO 11  PIN 23 : ON":
            self.l13_1.setText("GPIO 11  PIN 23 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/131low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l141(self):
        if self.l14_1.text() == "GPIO 5  PIN 29 : OFF":
            self.l14_1.setText("GPIO 5  PIN 29 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/141high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l14_1.text() == "GPIO 5  PIN 29 : ON":
            self.l14_1.setText("GPIO 5  PIN 29 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/141low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l151(self):
        if self.l15_1.text() == "GPIO 6  PIN 31 : OFF":
            self.l15_1.setText("GPIO 6  PIN 31 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/151high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l15_1.text() == "GPIO 6  PIN 31 : ON":
            self.l15_1.setText("GPIO 6  PIN 31 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/151low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l161(self):
        if self.l16_1.text() == "GPIO 13  PIN 33 : OFF":
            self.l16_1.setText("GPIO 13  PIN 33 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/161high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l16_1.text() == "GPIO 13  PIN 33 : ON":
            self.l16_1.setText("GPIO 13  PIN 33 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/161low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l171(self):
        if self.l17_1.text() == "GPIO 19  PIN 35 : OFF":
            self.l17_1.setText("GPIO 19  PIN 35 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/171high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l17_1.text() == "GPIO 19  PIN 35 : ON":
            self.l17_1.setText("GPIO 19  PIN 35 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/171low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l181(self):
        if self.l18_1.text() == "GPIO 26  PIN 37 : OFF":
            self.l18_1.setText("GPIO 26  PIN 37 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/181high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l18_1.text() == "GPIO 26  PIN 37 : ON":
            self.l18_1.setText("GPIO 26  PIN 37 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/181low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l52(self):
        if self.l5_2.text() == "GPIO 18  PIN 12 : OFF":
            self.l5_2.setText("GPIO 18  PIN 12 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/52high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l5_2.text() == "GPIO 18  PIN 12 : ON":
            self.l5_2.setText("GPIO 18  PIN 12 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/52low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l62(self):
        if self.l6_2.text() == "GPIO 23  PIN 16 : OFF":
            self.l6_2.setText("GPIO 23  PIN 16 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/62high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l6_2.text() == "GPIO 23  PIN 16 : ON":
            self.l6_2.setText("GPIO 23  PIN 16 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/62low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l72(self):
        if self.l7_2.text() == "GPIO 24  PIN 18 : OFF":
            self.l7_2.setText("GPIO 24  PIN 18 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/72high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l7_2.text() == "GPIO 24  PIN 18 : ON":
            self.l7_2.setText("GPIO 24  PIN 18 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/72low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l82(self):
        if self.l8_2.text() == "GPIO 25  PIN 22 : OFF":
            self.l8_2.setText("GPIO 25  PIN 22 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/82high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l8_2.text() == "GPIO 25  PIN 22 : ON":
            self.l8_2.setText("GPIO 25  PIN 22 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/82low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l92(self):
        if self.l9_2.text() == "GPIO 8  PIN 24 : OFF":
            self.l9_2.setText("GPIO 8  PIN 24 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/92high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l9_2.text() == "GPIO 8  PIN 24 : ON":
            self.l9_2.setText("GPIO 8  PIN 24 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/92low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l102(self):
        if self.l10_2.text() == "GPIO 7  PIN 26 : OFF":
            self.l10_2.setText("GPIO 7  PIN 26 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/102high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l10_2.text() == "GPIO 7  PIN 26 : ON":
            self.l10_2.setText("GPIO 7  PIN 26 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/102low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l112(self):
        if self.l11_2.text() == "GPIO 12  PIN 32 : OFF":
            self.l11_2.setText("GPIO 12  PIN 32 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/112high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l11_2.text() == "GPIO 12  PIN 32 : ON":
            self.l11_2.setText("GPIO 12  PIN 32 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/112low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l122(self):
        if self.l12_2.text() == "GPIO 16  PIN 36 : OFF":
            self.l12_2.setText("GPIO 16  PIN 36 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/122high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l12_2.text() == "GPIO 16  PIN 36 : ON":
            self.l12_2.setText("GPIO 16  PIN 36 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/122low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l132(self):
        if self.l13_2.text() == "GPIO 20  PIN 38 : OFF":
            self.l13_2.setText("GPIO 20  PIN 38 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/132high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l13_2.text() == "GPIO 20  PIN 38 : ON":
            self.l13_2.setText("GPIO 20  PIN 38 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/132low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def l142(self):
        if self.l14_2.text() == "GPIO 21  PIN 40 : OFF":
            self.l14_2.setText("GPIO 21  PIN 40 : ON")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/142high.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        elif self.l14_2.text() == "GPIO 21  PIN 40 : ON":
            self.l14_2.setText("GPIO 21  PIN 40 : OFF")
            #self.initial()
            try:
                command='python3 /home/pi/Desktop/control_gpio_pi/142low.py'
                stdin,stdout,stderr = self.Connect.ssh.exec_command(command)
                print('\nstout:',stdout.read())
            except:
                print("Some SSH Error")
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if success==1:
                self.Connect.ssh.close()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = General()
    sys.exit(app.exec_())
