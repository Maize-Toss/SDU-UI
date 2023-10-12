import socket, bluetooth

# Define the RFCOMM channel number
channel = 0

# Replace this with the device address you bound to
device_address = "00:21:10:30:16:91"

# Create a socket
sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)


try:
    # Connect to the device
    sock.connect((device_address, channel))
    print("Connected to the device")

    while True:
        message = input("Enter a message to send (or 'q' to quit): ")
        if message == 'q':
            break

        # Send the message
        sock.send(message)

        # Receive a response
        data = sock.recv(1024)
        print("Received:", data.decode())

except bluetooth.btcommon.BluetoothError as e:
    print("Error:", e)

finally:
    sock.close()
