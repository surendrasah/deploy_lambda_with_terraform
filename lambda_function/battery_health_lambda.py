import binascii
def decode_payload(payload):
    # Convert the hexadecimal string to a bytes object
    payload_bytes = binascii.unhexlify(payload)

    # Extract the different fields from the payload
    time = int.from_bytes(payload_bytes[0:4], 'little')
    time = (time << 4) + (payload_bytes[4] & 0b00001111)

    state = (payload_bytes[4] & 0b11110000) >> 4
    state_of_charge = payload_bytes[5]
    temperature = int.from_bytes(payload_bytes[6:8], 'little')


    # Convert the state to a string
    if state == 0:
        state_str = "power off"
    elif state == 1:
        state_str = "power on"
    elif state == 2:
        state_str = "discharge"
    elif state == 3:
        state_str = "charge"
    elif state == 4:
        state_str = "charge complete"
    elif state == 5:
        state_str = "host mode"
    elif state == 6:
        state_str = "shutdown"
    elif state == 7:
        state_str = "error"
    else:
        state_str = "undefined"

    # Convert the state of charge and temperature to floats
    state_of_charge = state_of_charge / 2
    temperature = (temperature / 2) - 20

    return {
        "time": time,
        "state": state_str,
        "state_of_charge": state_of_charge,
        "temperature": temperature
    }

def lambda_handler(event, context):
    device = event["device"]
    payload = event["payload"]

    data = decode_payload(payload)

    print({
        "time": data["time"],
        "state": data["state"],
        "state_of_charge": data["state_of_charge"],
        "temperature": data["temperature"]
    })
