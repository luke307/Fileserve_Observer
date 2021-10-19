import subprocess
import os

class ProcessService:

    def start(self) -> None:
        path = os.getcwd()
        service_path = os.path.join(path, 'dist\\ftp_service.exe')
        DETACHED_PROCESS = 8
        proc = subprocess.Popen(service_path, creationflags=DETACHED_PROCESS, close_fds=True)


    def kill(self) -> None:
        subprocess.Popen(f'taskkill /IM "ftp_service.exe" /F')


if __name__ == '__main__':
    process_service = ProcessService()
    process_service.start()
    #process_service.kill()
