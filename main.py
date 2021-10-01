import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, request
import smtplib, ssl

app = Flask("Ebay Tracker")

app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form['url']

        def get_price():
            source = requests.get(url).text
            html = BeautifulSoup(source, 'lxml')

            price = html.find(id="prcIsum").text
            price = price.split("$")
            return price

        def write_price(price):
            with open('price.json', 'w') as f:
                f.write(price[1])

        def send_mail(msg):
            password = "Sid4!adv"
            email = "siddheshadsv@gmail.com"
            to = "siddheshadsv@icloud.com"

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, password)
                server.sendmail(email, to, msg)        

        price = get_price()
        write_price(price)

        while True:
            with open('price.json') as f:
                price = f.read()
                price = float(price)

            curr_price = get_price()
            with open('price.json', 'w') as f:
                f.write(curr_price[1])

            curr_price = float(curr_price[1])

            if curr_price < price:
                message = f"THE PRICE HAS DROPPED FROM {price} to {curr_price}"
                send_mail(message)

            if curr_price > price:
                message = f"THE PRICE HAS GONE UP FROM {price} to {curr_price}"
                send_mail(message)

            else:
                print(f"Current: {curr_price}, Price: {price}")

            time.sleep(10)

        return render_template('index.html')

    else:
        return render_template('index.html')

app.run() # HAHA Nice 69 lines