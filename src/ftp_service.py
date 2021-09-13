from services.monitor_service import MonitorService

def service():
    monitor_service = MonitorService()
    monitor_service.monitor()

if __name__ == '__main__':
    service()
