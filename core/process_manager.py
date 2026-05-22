import psutil
import threading
import time
from core.logger import add_log

monitoring = False

# =========================
# BLOCK APPS
# =========================

def block_apps(distracting_apps):

    blocked = []

    for process in psutil.process_iter(['pid', 'name']):

        try:

            process_name = process.info['name']

            if process_name.lower() in distracting_apps:

                psutil.Process(process.info['pid']).terminate()

                blocked.append(process_name)
                add_log(f"❌ {process_name} terminated")

        except:
            pass

    return blocked

# =========================
# LIVE MONITOR LOOP
# =========================

def monitor_apps(distracting_apps):

    global monitoring

    monitoring = True

    while monitoring:

        block_apps(distracting_apps)

        time.sleep(2)

# =========================
# START MONITORING
# =========================

def start_monitoring(distracting_apps):

    thread = threading.Thread(
        target=monitor_apps,
        args=(distracting_apps,)
    )

    thread.daemon = True
    thread.start()

# =========================
# STOP MONITORING
# =========================

def stop_monitoring():

    global monitoring

    monitoring = False