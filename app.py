from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from extract_food import extract_food_data


app = Flask(__name__)


def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)


@app.route("/summary", methods=['GET', 'POST'])
def incoming_sms():
    user_input = request.form.get('NumMedia')
    if user_input == '1':
        pic_url = request.form.get('MediaUrl0')
        nutritional_value = extract_food_data(pic_url)
        respond("hello!")
        return respond(f"{nutritional_value}")
    else:
        return respond("Please send a picture containing text!")


if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=8080)
