import time
import signal
import socket

def run_remote_server_R():
    sock_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_remote.bind(('137.110.38.247', 12345)) # TODO: replace with Ramin's IPv4 addr thru VPN
    sock_remote.listen()
    conn_remote, addr_remote = sock_remote.accept()
    with conn_remote:
        print("Connected to Connors' Server!")
        sock_pynq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(0.0001)
        sock_pynq.connect(('192.168.2.99', 12345))
        print("Now connected to Ramin's pynq board!")
        while True:
            time.sleep(0.0001)
            data_remote = conn_remote.recv(1024)
            data_remote = data_remote.decode()
            if (data_remote == 'disconnect'):
                print("Disconnecting Ramin's Remote Server from Connors' Server")
                sock_pynq.sendall(bytes('disconnect', 'utf-8'))
                break
            elif (len(data_remote) == 4):
                sock_pynq.sendall(bytes(data_remote, 'utf-8'))
                data_remote = list(data_remote)
                print("Sent the following list to Ramin's Pynq Board: ",data_remote)
        sock_pynq.close()
    print("Connors has terminated the program.")

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit)
    run_remote_server_R()
