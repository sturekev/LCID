from detector1 import qr_scanner
from send_data1 import send_data1

while True:
    token = qr_scanner()
    noti = send_data1(token)
    if noti:
        print(noti)
        break

