import time
import signal
import socket

def run_server_C():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.2.1', 12345))
    print('Waiting for user to connect.')
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print("User is now connected!")
        sock_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(0.0001)
        sock_remote.connect(('137.110.38.247', 12345)) # TODO: replace with Ramin's IPv4 addr thru VPN
        while True:
            time.sleep(0.0001)
            data = conn.recv(1024)
            data = data.decode()
            if (data == 'disconnect'):
                print("Disconnecting Connors' Server from Ramin's Remote Server")
                sock_remote.sendall(bytes('disconnect', 'utf-8'))
                break
            elif (len(data) == 4):
                sock_remote.sendall(bytes(data, 'utf-8'))
                data = list(data)
                print("Sent the following list to Ramin's Remote Server: ",data)
        sock_remote.close()
    print("Connors' Pynq has disconnected from Server")

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit)
    run_server_C()
