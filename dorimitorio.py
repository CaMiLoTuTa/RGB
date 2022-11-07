
# ?------------------------------[ IMPORT ]------------------------------------
import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# ?---------------------------[ OBJETOS ]---------------------------------------
# * LED RGB
colorRojo = PWM(Pin(5), 500)
colorVerde = PWM(Pin(18), 500)
colorAzul = PWM(Pin(19), 500)

# * SERVOMOTOR 180°
servo = PWM(Pin(21), freq=50)

# * MQTT Server Parameters
MQTT_CLIENT_ID = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
topic_sub = 'negro/diego'
topic_pub = 'negro/diego'

# ?----------------------[ CONECTAR WIFI ]---------------------------------------------------------#
print("Conectando al WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Q60', 'minumero')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# ?----------------------[ FUNCION RECEPCIÓN EN EL SUB ]---------------------------------------------------------#


def sub_cb(topic, msg):
    # print(f"llego el topic: {topic} con el valor {msg}")
    if topic == 'negro/diego':
        fun = msg.decode()
    fun = msg.decode()

    lista = str(fun)

    lista = lista.replace("[", "")
    lista = lista.replace("]", "")
    lista = lista.replace(" ", "")
    lista = list(lista.split(','))

    valorR = int(lista[0])
    valorG = int(lista[1])
    valorB = int(lista[2])
    valorS = int(lista[3])

    valorRealR = (valorR-255)*4
    if valorRealR < 0:
        valorRealR *= -1
    colorRojo.duty(valorRealR)

    valorRealG = (valorG-255)*4
    if valorRealG < 0:
        valorRealG *= -1
    colorVerde.duty(valorRealG)

    valorRealB = (valorB-255)*4
    if valorRealB < 0:
        valorRealB *= -1
    colorAzul.duty(valorRealB)

    valorRealS = int((valorS/2)+10)
    if valorRealS > 180:
        valorRealS = 180
    if valorRealS < 0:
        valorRealS = 0
    servo.duty(valorRealS)
    print(valorRealS)


# ?----------------------[ CONECTAR BROKER ]---------------------------------------------------------#
print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER,
                    user=MQTT_USER, password=MQTT_PASSWORD)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)
print('Connected to %s MQTT broker, subscribed to %s topic' %
      (MQTT_BROKER, topic_sub))
print("Connected!")

# ?----------------------[ CICLO INFINITO ]---------------------------------------------------------#
while True:
    print("esperando")
    client.wait_msg()
