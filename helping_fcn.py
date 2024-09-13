import re
import os
import json
import random 
import string 
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


def savecookie(cookies_data,file_name):
    valid_folder = "valid-cookies/"
    os.makedirs(valid_folder, exist_ok=True)
    valid_file_path = os.path.join(valid_folder, file_name)
    with open(valid_file_path, "wb") as f:
        f.write(cookies_data)
    return valid_file_path

def count_user():
    with open("userid.txt", "r") as f:
        lines = f.readlines()
    line_count = len(lines)
    return int(line_count)
    

def sec_key(length=16):
    # Use only alphanumeric characters and a few selected symbols
    safe_characters = string.ascii_letters + string.digits + "-_"
    key = ''.join(random.choice(safe_characters) for _ in range(length))
    return "CRYPTO" + key


def saveid(user_id):
    filename = "userid.txt"
    user_id = str(user_id)
    # Open the file and read all lines into a list
    try:
        with open(filename, "r") as file:
            existing_ids = file.read().splitlines()
    except FileNotFoundError:
        existing_ids = []

    # If the user_id is not already in the file, append it
    if user_id not in existing_ids:
        with open(filename, "a") as file:
            file.write(user_id + "\n")

def check_root(user_id):
    user_id = str(user_id)
    try:
        with open("root.txt","r") as f:#fcn for checking userid in root file to verify user in before using specific commmand 
            lines = f.read().splitlines()
            return user_id in lines 
            
    except FileNotFoundError:
        return False
    
def claiming_key(enterkey, user_id, username):
    current_date = datetime.now().date()
    new_date = None
    duration = None
    time = None

    # Read all lines from the file
    with open("key.txt", "r") as f:
        lines = f.readlines()

    # Open the file in write mode to overwrite it
    with open("key.txt", "w") as f:
        for line in lines:
            line_duration, line_time, key = line.strip().split(",")
            if enterkey == key:
                duration = line_duration
                time = int(line_time)

                # Calculate the new date based on the duration
                if duration == "month":
                    new_date = current_date + relativedelta(months=time)
                elif duration == "year":
                    new_date = current_date + relativedelta(years=time)
                else:
                    return False, None, None, None
                
                # Save the subscription info to paid.txt
                with open("paid.txt", "a") as paid_file:
                    paid_file.write(f"{user_id},{username},{new_date}\n")

                
                continue  # Skip writing this line back to key.txt

            # Write all lines except the claimed one back to the file
            f.write(line)

    # Return True if a key was claimed, otherwise return False
    if duration:
        return True, new_date, duration, time
    else:
        return False, None, None, None



def checking_paid(user_id):
    current_date = datetime.now().date()  # Get the current date
    valid_lines = []  # List to store lines with valid subscriptions
    subscription_valid = False  # Flag to indicate if subscription is valid

    with open("paid.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        try:
            current_id_str, current_username, subs_date_str = line.strip().split(",")
            current_id = int(current_id_str)
            user_id = int(user_id)  # Ensure user_id is also an integer
            
            # Convert subscription date string to date object
            subs_date = datetime.strptime(subs_date_str, '%Y-%m-%d').date()

            if user_id == current_id:
                if subs_date >= current_date:
                    subscription_valid = True
                    valid_lines.append(line)  # Keep the valid subscription
                else:
                    continue
            else:
                valid_lines.append(line)  # Keep other valid subscriptions

        except ValueError as e:

            continue

    # Write valid subscriptions back to the file
    try:
        with open("paid.txt", "w") as file:
            file.writelines(valid_lines)
    except IOError:
        print("Error: Could not write to 'paid.txt' file.")
    
    return subscription_valid

def info(user_id):
    current_date = datetime.now().date()
    
    try:
        with open("paid.txt", "r") as f:
            lines = f.readlines()  # Read all lines from the file
            
        for line in lines:
            usrid, username, sub_date = line.strip().split(',')
            usrid = int(usrid)
            user_id = int(user_id)
            subs_date = datetime.strptime(sub_date, '%Y-%m-%d').date()  # Convert stored date to date object

            if user_id == usrid:
                if subs_date >= current_date:
                    return usrid, username, sub_date, "running"
                else:
                    return usrid, username, sub_date, "expired"
        
        # If the user ID is not found in the file
        return None, None, None, "no"
    
    except FileNotFoundError:
        # Handle the case where the file does not exist
        return None, None, None, "no"
    except Exception as e:
        # Handle other potential exceptions
        print(f"Error reading file: {e}")
        return None, None, None, "error"

def broad():
    idss = []
    with open("userid.txt","r") as f:
        lines = f.readlines()
        for line in lines:
            id = line.strip()
            idss.append(id)
    return idss
        
        
def netflix_checker(cookies_list):
    try:
        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Set cookies from JSON data
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False)
                ))

            # Set headers
            headers = {
                "referer": "https://www.netflix.com/",
                "accept": "*/*",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Send request to Netflix
            req = session.get("https://www.netflix.com", cookies=jar, headers=headers)
            print(req.url)

            # Check if the response redirects to /browse (indicating login success)
            if "/browse" in req.url:
                return True
            else:
                return False

    except Exception as e:
        print(f"Error in netflix_net_checker: {str(e)}")
        return False
    
def gpt_checker(cookies_list):
    user_info_pattern = re.compile(r'"id":"(.*?)","name":"(.*?)","email":"(.*?)"')
    try:
        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Set cookies efficiently
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False)
                ))

            headers = {
                "referer": "https://chatgpt.com/",
                "accept": "*/*",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Make the request
            req = session.get("https://chatgpt.com", cookies=jar, headers=headers)
            print(req.url)
            # Use the pre-compiled regex for matching
            match = user_info_pattern.search(req.text)
            print(req.url)
            if match:
                user_id, user_name, user_email = match.groups()
                if user_id and user_name and user_email:
                    return True
                else:
                    return False
            else:
                return False
    except Exception as e:
        print(f"Error in gpt_checker: {str(e)}")
        return False

def parse_netscape_cookies(cookies_data: str):
    cookies_data = cookies_data.decode('utf-8')
    cookies = []
    lines = cookies_data.splitlines()
    
    for line in lines:
        # Skip comments and empty lines
        if line.startswith('#') and not line.startswith('#HttpOnly_'):
            continue
        
        # Handle "HttpOnly_" cookies by stripping the prefix
        if line.startswith('#HttpOnly_'):
            line = line[len('#HttpOnly_'):]

        # Split by tab, and check if the format matches the Netscape cookie format
        parts = line.split('\t')
        if len(parts) == 7:
            cookie = {
                'domain': parts[0],
                'flag': parts[1],
                'path': parts[2],
                'secure': parts[3] == 'TRUE',
                'expiration': int(parts[4]),
                'name': parts[5],
                'value': parts[6]
            }
            cookies.append(cookie)
    return cookies


def gpt_net_checker(cookies_data):
    user_info_pattern = re.compile(r'"id":"(.*?)","name":"(.*?)","email":"(.*?)"')
    try:
        cookies_list = parse_netscape_cookies(cookies_data)
        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Set cookies efficiently
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False)
                ))

            headers = {
                "referer": "https://chatgpt.com/",
                "accept": "*/*",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Make the request
            req = session.get("https://chatgpt.com", cookies=jar, headers=headers)
            # soup = BeautifulSoup(req.text, "html.parser")
            # data = soup.prettify()
            # with open("response.html", "w") as f:
            #     f.write(data)
            # print(req.url)
            # Use the pre-compiled regex for matching
            match = user_info_pattern.search(req.text)
            if match:
                user_id, user_name, user_email = match.groups()
                if user_id and user_name and user_email:
                    return True
                else:
                    return False
            else:
                return False
    except Exception as e:
        print(f"Error in gpt_checker: {str(e)}")
        return False

def fb_net_checker(cookies_data):
    user_info_pattern = re.compile(r'"NAME":"(.*?)","SHORT_NAME":"(.*?)"')
    try:
        cookies_list = parse_netscape_cookies(cookies_data)
        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Set cookies efficiently
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False)
                ))

            headers = {
                "referer": "https://www.facebook.com/",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Make the request
            req = session.get("https://www.facebook.com/", cookies=jar, headers=headers)

            # Save response for debugging, ensuring utf-8 encoding
            # soup = BeautifulSoup(req.text, "html.parser")
            # data = soup.prettify()
            # with open("response.html", "w", encoding="utf-8") as f:
            #     f.write(data)

            # Check for "NAME" and "SHORT_NAME"
            match = user_info_pattern.search(req.text)
            if match:  # If both fields are found
                name, short_name = match.groups()
                if name and short_name:
                    return True
            return False
    except Exception as e:
        print(f"Error in fb_checker: {str(e)}")
        return False


def fb_checker(cookies_list):
    # Compile regex to find "NAME" field
    user_info_pattern = re.compile(r'"NAME":"(.*?)","SHORT_NAME":"(.*?)"')
    
    try:
        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Set cookies efficiently
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False)
                ))

            headers = {
                "referer": "https://www.facebook.com/",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Make the request
            req = session.get("https://www.facebook.com/", cookies=jar, headers=headers)
            match = user_info_pattern.search(req.text)
            if match:  # If both fields are found
                name, short_name = match.groups()
                if name and short_name:

                    return True
            else:
                return False
    except Exception as e:
        print(f"Error in fb_checker: {str(e)}")
        return False

def crunchy_checker(cookies_list):
    user_info_pattern = re.compile(r'"NAME":"(.*?)"')
    try:
        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Set cookies efficiently
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False)
                ))

            headers = {
                "referer": "https://www.facebook.com/",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Make the request
            req = session.get("https://www.facebook.com/", cookies=jar, headers=headers)

            # Use the pre-compiled regex for matching
            match = user_info_pattern.search(req.text)
            if match:
                user_id, user_name, user_email = match.groups()
                if user_id and user_name and user_email:
                    return True
                else:
                    return False
            else:
                return False
    except Exception as e:
        print(f"Error in fb_checker: {str(e)}")
        return False

def netflix_net_checker(cookies_data):
    try:
        cookies_list = parse_netscape_cookies(cookies_data)

        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()

            # Add cookies to the session
            for cookie in cookies_list:
                jar.set_cookie(requests.cookies.create_cookie(
                    domain=cookie['domain'],
                    name=cookie['name'],
                    value=cookie['value'],
                    path=cookie.get('path', '/'),
                    secure=cookie.get('secure', False),
                    expires=cookie.get('expiry')
                ))

            # Set headers
            headers = {
                "referer": "https://www.netflix.com/",
                "accept": "*/*",
                "sec-ch-ua-platform": "Windows",
                "accept-language": "en-US,en;q=0.5",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Send request to Netflix
            req = session.get("https://www.netflix.com", cookies=jar, headers=headers)
            print(req.url)
            # Write beautified response 
            if  "/browse" in req.url :
                return True
            else:
                return False
    except Exception as e:
        print(f"Error in netflix_net_checker: {str(e)}")


# with open("a.txt","r") as f:
#     cookies_data = f.read()
    
# gpt_net_checker(cookies_data)
