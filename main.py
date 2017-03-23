from PyQt5.Qt import *
import sys
import mainwindow
import settings


class settings(QDialog, settings.Ui_SettingDialog):
    sendSettingsInfo = pyqtSignal(list)
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)
        self.baudrate = 115200
        self.name = ""
        self.databits = 8
        self.flowcontrol = 0
        self.parity = 0
        self.stopbits = 0
        self.initUI()
        self.updatePortName()

    def initUI(self):
        self.initPortInfo()
        self.accepted.connect(self.acceptSettings)
    def initPortInfo(self):
        serialPortSettings = QSettings("GEOSAT", "BATHYSAT.PY")
        if str(serialPortSettings.value("name")) != "":
            self.baudrate = serialPortSettings.value("baudrate")
            self.comboBox_baudrate.setCurrentText(serialPortSettings.value("baudrate"))

            self.name = serialPortSettings.value("name")
            self.comboBox_portname.setCurrentText(serialPortSettings.value("name"))

            self.databits = serialPortSettings.value("databits")
            self.comboBox_databits.setCurrentText(str(serialPortSettings.value("databits")))
            flowcontrol=""
            self.flowcontrol=serialPortSettings.value("flowcontrol")
            if serialPortSettings.value("flowcontrol") == 0:
                flowcontrol="NoFlowControl"
            elif serialPortSettings.value("flowcontrol") == 1:
                flowcontrol = "HardwareControl"
            elif serialPortSettings.value("flowcontrol") == 2:
                flowcontrol = "SoftwareControl"
            self.comboBox_flowcontrol.setCurrentText(flowcontrol)

            self.parity = serialPortSettings.value("parity")
            if serialPortSettings.value("parity") == 0:
                self.comboBox_parity.setCurrentText("NoParity")
            elif serialPortSettings.value("parity") == 2:
                self.comboBox_parity.setCurrentText("EvenParity")
            elif serialPortSettings.value("parity") == 5:
                self.comboBox_parity.setCurrentText("MarkParity")
            elif serialPortSettings.value("parity") == 3:
                self.comboBox_parity.setCurrentText("OddParity")
            elif serialPortSettings.value("parity") == 4:
                self.comboBox_parity.setCurrentText("SpaceParity")


            self.stopbits = serialPortSettings.value("stopbits")
            if serialPortSettings.value("stopbits") == 2:
                self.comboBox_stopbits.setCurrentText("TwoStop")
            elif serialPortSettings.value("stopbits") == 1:
                self.comboBox_stopbits.setCurrentText("OneStop")
            elif serialPortSettings.value("stopbits") == 3:
                self.comboBox_stopbits.setCurrentText("OneAndHalfStop")
    def acceptSettings(self):
        serialPortSettings = QSettings("GEOSAT", "BATHYSAT.PY")

        self.name = self.comboBox_portname.currentText()
        self.baudrate= self.comboBox_baudrate.currentText()
        self.databits=self.comboBox_databits.currentText()
        if self.comboBox_stopbits.currentText()=="TwoStop":
            self.stopbits=2
        elif self.comboBox_stopbits.currentText()=="OneStop":
            self.stopbits=1
        elif self.comboBox_stopbits.currentText()=="OneAndHalfStop":
            self.stopbits=3

        if self.comboBox_flowcontrol.currentText()=="NoFlowControl":
            self.flowcontrol=0
        elif self.comboBox_flowcontrol.currentText()=="HardwareControl":
            self.flowcontrol=1
        elif self.comboBox_flowcontrol.currentText()=="SoftwareControl":
            self.flowcontrol=2

        if self.comboBox_parity.currentText()=="NoParity":
            self.parity=0
        elif self.comboBox_parity.currentText()=="EvenParity":
            self.parity=2
        elif self.comboBox_parity.currentText()=="MarkParity":
            self.parity=5
        elif self.comboBox_parity.currentText()=="OddParity":
            self.parity=3
        elif self.comboBox_parity.currentText()=="SpaceParity":
            self.parity=4

        serialPortSettings.setValue("name", self.name)
        serialPortSettings.setValue("databits", self.databits)
        serialPortSettings.setValue("baudrate", self.baudrate)
        serialPortSettings.setValue("parity", self.parity)
        serialPortSettings.setValue("stopbits", self.stopbits)
        serialPortSettings.setValue("flowcontrol", self.flowcontrol)
        self.sendSettingsInfo.emit([self.name, self.databits, self.baudrate, self.parity,self.stopbits,self.flowcontrol])
    def rejectSettings(self):
        self.initPortInfo()
        self.sendSettingsInfo.emit([self.name, self.databits, self.baudrate, self.parity,self.stopbits,self.flowcontrol])
    def updatePortName(self):
        infos=QSerialPortInfo.availablePorts()
        for info in infos:
            self.comboBox_portname.clear()
            self.comboBox_portname.addItem(info.portName())




class mainwindow(QMainWindow,mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.settingsDialog = settings()
        self.baudrate=115200
        self.databits=8
        self.name=""
        self.stopbits=0
        self.parity=0
        self.flowcontrol=0
        self.serialport=QSerialPort()
        self.currentTime=""
        self.initUI()
    def initUI(self):
        self.actionSettings.triggered.connect(self.openSettingsDialog)
        self.settingsDialog.accepted.connect(self.saveSettings)
        self.settingsDialog.rejected.connect(self.rejectSettings)
        self.actionConnect.triggered.connect(self.connect)
        self.settingsDialog.sendSettingsInfo.connect(self.updateSettings)
        self.serialport.readyRead.connect(self.readData)
        self.actionSave.triggered.connect(self.saveFile)

        serialPortSettings=QSettings("GEOSAT", "BATHYSAT.PY")
        if serialPortSettings.value("name")!="":
            self.name=serialPortSettings.value("name")
            self.databits=serialPortSettings.value("databits")
            self.baudrate=serialPortSettings.value("baudrate")
            self.parity=serialPortSettings.value("parity")
            self.flowcontrol=serialPortSettings.value("flowcontrol")
            self.stopbits=serialPortSettings.value("stopbits")

    def openSettingsDialog(self):
        self.settingsDialog.show()
        self.settingsDialog.updatePortName()
        self.setHidden(True)
    def saveSettings(self):
        self.setHidden(False)
    def rejectSettings(self):
        self.setHidden(False)
    def connect(self):
        self.serialport.setBaudRate(int(self.baudrate))
        self.serialport.setDataBits(int(self.databits))
        self.serialport.setPortName(self.name)
        self.serialport.setFlowControl(int(self.flowcontrol))
        self.serialport.setParity(int(self.parity))
        self.serialport.setStopBits(int(self.stopbits))
        if self.serialport.open(QIODevice.ReadWrite):
            self.actionDisconnect.setEnabled(False)
            self.actionConnect.setEnabled(False)
            self.actionSettings.setEnabled(False)
            self.actionSave.setEnabled(False)
            self.textEdit_new.setEnabled(False)
            print("open")
    def disconnect(self):
        self.actionConnect.setChecked(False)
        self.actionDisconnect.setEnabled(False)
        self.actionConnect.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionSettings.setEnabled(False)
        self.textEdit_new.setEnabled(True)
        self.serialport.close()
    def updateSettings(self,infoList):
        self.name=infoList[0]
        self.baudrate=infoList[2]
        self.databits=infoList[1]
        self.flowcontrol=infoList[5]
        self.parity=infoList[3]
        self.stopbits=infoList[4]
    def saveData(self,data):
        file=open("~/Desktop/saving.log",'a')
        file.write(data)
    def readData(self):
        currentTime = QDateTime.currentDateTime().toString("hh:mm:ss,yyyy-MM-dd")
        if self.currentTime != currentTime:

            if self.currentTime != "":
                self.saveData("<DateTime/>")
                self.textEdit.append("<DateTime/>\n")
            self.currentTime=currentTime
            self.saveData("<DateTime"+currentTime+">")
            self.textEdit.append("<DateTime"+currentTime+">")
        data=self.serialport.readAll()
        self.saveData(data)
        self.textEdit.append(data)
        self.saveData(data)
    def saveFile(self):
        fileName=QFileDialog.getSaveFileName(self,self,"Save Data","./","Text(*.txt);;All(*.*)")
        file=open(fileName,'w')
        file.write(self.textEdit_new.toPlainText())
        file.close()
    def formatData(self,getDepth=True):
        text = self.textEdit.toPlainText()
        dataList = text.split("<DateTime/>")
        for data in dataList:
            result=data[0,32]
            elementList=data.split(",")
            if len(elementList)>0:
                if getDepth==True:
                    posM=elementList.index("M")
                    if posM>1:
                        depth=elementList[posM-1]
                        result=result+"\n Depth : " + depth
            self.textEdit_new.append(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = mainwindow()
    form.show()
    app.exec_()