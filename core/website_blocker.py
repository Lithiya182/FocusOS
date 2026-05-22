HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT = "127.0.0.1"

blocked_sites = [
    "www.youtube.com",
    "youtube.com",
    "www.instagram.com",
    "instagram.com",
    "www.facebook.com",
    "facebook.com"
]

# =========================
# BLOCK WEBSITES
# =========================

def block_websites():

    with open(HOSTS_PATH, "r+") as file:

        content = file.read()

        for site in blocked_sites:

            if site not in content:

                file.write(f"{REDIRECT} {site}\n")

# =========================
# UNBLOCK WEBSITES
# =========================

def unblock_websites():

    with open(HOSTS_PATH, "r+") as file:

        lines = file.readlines()

        file.seek(0)

        for line in lines:

            if not any(site in line for site in blocked_sites):

                file.write(line)

        file.truncate()