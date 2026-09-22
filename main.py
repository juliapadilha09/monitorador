import dht
from machine import Pin
import network
import time
import urequests


# ==========================================
# CONFIGURAÇÕES
# ==========================================

SSID = "SENAI-IoT"
PASSWORD = "sua_senha_aqui"

# IP DO COMPUTADOR QUE ESTÁ RODANDO O XAMPP
API_URL = "http://192.168.0.200/api/leituras.php"

DISPOSITIVO_ID = "ESP32-01"

DHT_PIN = 4

INTERVALO_ENVIO = 5


# ==========================================
# SENSOR
# ==========================================

sensor = dht.DHT11(Pin(DHT_PIN))


# ==========================================
# CONECTAR AO WI-FI
# ==========================================

def conectar_wifi():

    print("Inicializando ESP32...")

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    if wlan.isconnected():

        print("Wi-Fi já conectado!")

        print("IP:", wlan.ifconfig()[0])

        return wlan


    print("Conectando ao Wi-Fi...")
    print("SSID:", SSID)

    wlan.connect(SSID, PASSWORD)

    tentativas = 0

    while not wlan.isconnected():

        time.sleep(0.5)

        print(".", end="")

        tentativas += 1

        if tentativas >= 30:

            print("\nNão foi possível conectar ao Wi-Fi.")

            return None


    print("\nWi-Fi conectado!")

    print("IP:", wlan.ifconfig()[0])

    print("Iniciando monitoramento...\n")

    return wlan


# ==========================================
# ENVIAR DADOS
# ==========================================

def enviar_dados(temperatura, umidade):

    dados = {

        "temperatura": temperatura,

        "umidade": umidade,

        "dispositivo": DISPOSITIVO_ID

    }


    headers = {

        "Content-Type": "application/json"

    }


    resposta = None


    try:

        print("Enviando dados...")

        print(dados)

        resposta = urequests.post(

            API_URL,

            json=dados,

            headers=headers

        )


        print(
            "Resposta da API:",
            resposta.status_code
        )


        if resposta.status_code in [200, 201]:

            print("Dados enviados com sucesso!")

        else:

            print(
                "Erro ao enviar dados."
            )


    except Exception as erro:

        print(
            "Erro na comunicação com a API:",
            erro
        )


    finally:

        if resposta is not None:

            resposta.close()


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def principal():

    wlan = conectar_wifi()


    if wlan is None:

        print("Sistema não iniciou.")

        return


    while True:

        try:

            # Verifica se o Wi-Fi continua conectado

            if not wlan.isconnected():

                print(
                    "Wi-Fi desconectado."
                )

                wlan = conectar_wifi()


                if wlan is None:

                    time.sleep(5)

                    continue


            # ------------------------------
            # LEITURA DO DHT11
            # ------------------------------

            sensor.measure()

            temperatura = sensor.temperature()

            umidade = sensor.humidity()


            print("------------------------------")

            print(
                "Temperatura:",
                temperatura,
                "°C"
            )

            print(
                "Umidade:",
                umidade,
                "%"
            )


            # ------------------------------
            # ENVIO PARA API
            # ------------------------------

            enviar_dados(
                temperatura,
                umidade
            )


            print(
                "Próxima leitura em",
                INTERVALO_ENVIO,
                "segundos..."
            )


        except OSError as erro:

            print(
                "Erro no sensor ou Wi-Fi:",
                erro
            )


        except Exception as erro:

            print(
                "Erro inesperado:",
                erro
            )


        time.sleep(
            INTERVALO_ENVIO
        )


# ==========================================
# INICIAR
# ==========================================

principal()