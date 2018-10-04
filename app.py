from flask import Flask, render_template, request
from pymessenger.bot import Bot
from random import randint
import os
import csv

app = Flask(__name__)
bot = Bot (os.environ['ACCESS_TOKEN'])


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == os.environ['VERIFY_TOKEN']:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'
    if request.method == 'POST':
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for x in messaging:
            recipient_id = x['sender']['id']

            if x.get('message'):

                msg = "Hi, How are you?"
                a = bot.send_text_message(recipient_id, msg)
                return "success"

                if x['message'].get('text'):
                    msg = "Hi, How are you?"
                    a = bot.send_text_message(recipient_id, msg)
                    print(a)
                    print(x['message'].get('text'))
                if x['message'].get('attachments'):
                    with open('./magic_csv/blackgirlmagicCSV.csv', 'r') as csvfile:
                        magiccsv = list(csv.reader(csvfile)) 
                    lengthofcsv = len(magiccsv)
                    position = randint(0, lengthofcsv)
                    response = magiccsv[position][0]
                    try:
                        a = bot.send_image_url(recipient_id, response)
                        if "error" in a:
                            b = bot.send_text_message(recipient_id, response)
                    except:
                        c = bot.send_text_message(recipient_id, response)
                    return "success"
            else:
                pass
    return "success"


@app.route("/privacypolicy", methods=['GET', 'POST'])
def privacy():
    return render_template('privacy.html')


if __name__ == "__main__":
    app.run(port=6550)