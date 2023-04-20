import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = ''
password = ''

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    max_tries = 20
    try_count = 0
    while wlan.isconnected() == False\
          and try_count < max_tries\
          and wlan.status() > 0:
        try_count = try_count + 1
        print(f'{try_count}: Waiting for connection... {wlan.status()}')
        sleep(1)
        
    print(f'wlan.isconnected():{wlan.isconnected()} wlan.status(): {wlan.status()}')
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection


global num
num = 0
def serve(connection,ip):
    global num
    
    state = 'ON'
    color = 'green'
    pico_led.on()
    temperature = 0
    




    while(True):
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
            color = 'green'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
            color = 'red'
        temperature = pico_temp_sensor.temp
        
        html = f"""
        <!DOCTYPE html>
        <html>
         <meta http-equiv="refresh" content="2; URL=http://{ip}/">

            <title>Ella's test page</title>
            <body>
                <p style="font-size:70px">
                    Hi Ella {num}!
                </p>
                <form action="./lighton">
                    <input type="submit" value="Light on" style="height:50px; width:200px; font-size:20px"/>
                </form>
                <form action="./lightoff">
                    <input type="submit" value="Light off" style="height:50px; width:200px; font-size:20px"/>
                </form>
                <hr/>
                <p style="font-size:70px;color:{color}">
                    LED is {state}
                </p>f
                <p style="font-size:70px">
                    Temperature is {temperature}
                </p>
            </body>
        </html>
        """
        num += 1
        client.send(html)
        client.close()

try:
    ip = connect()
    print(ip)
    connection = open_socket(ip)
    serve(connection,ip)
except KeyboardInterrupt:
    machine.reset()
