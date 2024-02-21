# mqtt_app/views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import paho.mqtt.client as mqtt
from keras.models import load_model
import json
from django.views.decorators.http import require_http_methods
from sklearn.preprocessing import StandardScaler
import numpy as np

scaler = StandardScaler()

# MQTT Settings
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
mqtt_username = "Hello"
mqtt_password = ""
mqtt_subscribe_topic = "hello1"
mqtt_publish_topic = "hello2"

# Load the pre-trained machine learning model
model1 = load_model("model.h5")
model2 = load_model("voltage_model.h5")

# Set up MQTT client
mqtt_client = mqtt.Client()

# Function to preprocess input data for prediction
def preprocess_input_data(voltage):

    lag_features = []
    for i in range(1, 7):
        lag_features.append(1 if voltage <= 11.5 else 0)
    return np.array([lag_features]).reshape(1, 1, 6)

def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode("utf-8"))
        print(f"Received message: {message}")

        # Future Voltage Prediction
        scaler = StandardScaler()
        scaler.mean_ = np.load('scaler_mean.npy')  
        scaler.scale_ = np.load('scaler_scale.npy')  

        # Make predictions using the loaded model
        input_data = np.array([[ message["voltage"]]])

        voltage = scaler.transform(input_data)
        prediction = model2.predict(voltage)
        forcast_prediction =  scaler.inverse_transform(prediction)[0]
        print(forcast_prediction)

        # predict the probabiliy to clean or not

        voltage_ = preprocess_input_data(message['voltage'])
        prediction_prob = model1.predict(voltage_)[0, 0]
        probability = 1 if prediction_prob >= 0.5 else 0

        if probability <= 0.5 :
            message = "You Should Clear the Solar Surface Before Date"
        else :
            message = "No forecasted threshold crossing in the upcoming year"

        prediction_json = {'forcast_voltage': str(forcast_prediction), 'message': message}

        client.publish(mqtt_publish_topic, json.dumps(prediction_json))
        print(f"Sent prediction: {prediction_json}")

    except Exception as e:
        print(f"Error processing message: {e}")



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

