import subprocess
import re

def get_wifi_profiles():
    result = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
    profiles = re.findall(r"All User Profile\s*:\s(.*)", result)
    return [profile.strip() for profile in profiles]

def get_wifi_password(profile_name):
    try:
        result = subprocess.check_output(
            f'netsh wlan show profile name="{profile_name}" key=clear',
            shell=True, text=True)
        password_search = re.search(r"Key Content\s*:\s(.*)", result)
        if password_search:
            return password_search.group(1).strip()
        else:
            return "(No password found)"
    except subprocess.CalledProcessError:
        return "(Error retrieving password)"

def main():
    profiles = get_wifi_profiles()
    if not profiles:
        print("No Wi-Fi profiles found.")
        return

    print("\nSaved Wi-Fi Networks and Passwords:\n")
    for profile in profiles:
        password = get_wifi_password(profile)
        print(f"SSID: {profile}\nPassword: {password}\n{'-'*40}")

if __name__ == "__main__":
    main()

