import psutil

def is_process_running(keyword):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if keyword in " ".join(proc.info['cmdline']):
                return True
        except Exception:
            continue
    return False 