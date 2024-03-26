# SocketPwn

SocketPwn is a modular tool used for running automated tools through websockets. 

# Usage

pip install -r requirements.txt

python SocketPwn.py -u ws://yourwebsocketurl --sqlmap --payload your_payload_or_payload_file

python SocketPwn.py -u "ws://localhost:8156/ws" --sqlmap --payload payload.json

# Payloads 

Just grab the payload from burp:

![image](https://github.com/Themaim/SocketPwn/assets/141221448/814f6d78-849c-4407-9bd5-a02bdad5e632)

copy and paste this into a file in the dir

should format it to this:

{"employeeID":"1"}

Replace the injection point you want with %s

{"employeeID":"%s"}

# Example

![image](https://github.com/Themaim/SocketPwn/assets/141221448/af18aa20-017b-443f-9305-975c3dd85890)


# ToDo
•	Make sql command more dynamic
•	add more support for automated tools

