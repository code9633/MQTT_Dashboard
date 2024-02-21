from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import paho.mqtt.client as mqtt
from keras.models import load_model
import json
from django.views.decorators.http import require_http_methods
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta


scaler = StandardScaler()

# MQTT Settings
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
mqtt_username = "helo123"
mqtt_password = ""
mqtt_subscribe_topic = "hello2"
mqtt_publish_topic = "test/topic"

# Load the pre-trained machine learning model
model = joblib.load("model_ARIMA.pkl")


# Set up MQTT client
mqtt_client = mqtt.Client()

# Function to preprocess input data for prediction
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        print(f"Received data: {data}")

        # Future Voltage Prediction

        input_data = [data['temperature'], data['humidity']]
        prediction = model.forecast(steps=1, exog=[input_data])[0]
        

        prediction_json = {
                "ForcastVoltage" : round(prediction, 2),
                "CurrentVoltage" : data['voltage'],
                "date" : datetime.now().strftime("%M:%S")
             }

        send_email(prediction, data)

        client.publish(mqtt_publish_topic, json.dumps(prediction_json))
        print(f"Sent prediction: {prediction_json}")

    except Exception as e:
        print(f"Error processing data: {e}")


def send_email(prediction, data):
    if prediction < 11.5:
        subject = 'Cleaning Alert'
        next_week_date = datetime.now() + timedelta(days=7)
        message = render_to_string('email_template.html', {
            'prediction': round(prediction, 2),
            'temperature': data['temperature'],
            'humidity': data['humidity'],
            'date': next_week_date.strftime('%Y-%m-%d')  
        })
        recipient_list = ['shashikaudara6@gmail.com']  # You can add list of email address which you want to receive emails.
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=message)
    
# Configure MQTT client
mqtt_client.on_message = on_message
mqtt_client.username_pw_set(username=mqtt_username, password=mqtt_password)
# Connect to the MQTT broker and subscribe
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.subscribe(mqtt_subscribe_topic)
mqtt_client.loop_start()


def check_connection(request):
    if mqtt_client.is_connected():
        return JsonResponse({"status": "Connected"})
    else:
        return JsonResponse({"status": "Not connected"})

def index(request):
     return HttpResponse("<p>Welcome! Please send a JSON object with \"voltage\" key</p>")