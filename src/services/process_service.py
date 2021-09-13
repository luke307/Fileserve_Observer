import subprocess


class ProcessService:

    def start(self):
        DETACHED_PROCESS = 8
        proc = subprocess.Popen('C:\\Users\\Lukas\\Desktop\\ftp\\dist\\ftp_service.exe', creationflags=DETACHED_PROCESS, close_fds=True)


    def kill(self):
        subprocess.Popen(f'taskkill /IM "ftp_service.exe" /F')


if __name__ == '__main__':
    process_service = ProcessService()
    #process_service.start()
    process_service.kill()
