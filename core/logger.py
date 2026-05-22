logs = []

# =========================
# ADD LOG
# =========================

def add_log(message):

    logs.append(message)

# =========================
# GET LOGS
# =========================

def get_logs():

    return logs[-20:]