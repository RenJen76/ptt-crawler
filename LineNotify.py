import configparser
import requests

class LineNotify:

    def __init__(self):

        config  = configparser.ConfigParser()
        config.read('config/config.ini')
        self.token = config['LINE_NOTIFY']['token']

    def NotifyMessage(self, message):

        payload = {'message': message}
        headers = {
            "Authorization": "Bearer " + self.token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }

        NotifyRequest = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return NotifyRequest