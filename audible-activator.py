#!/usr/bin/env python2

from __future__ import print_function
from getpass import getpass
import time
from selenium import webdriver
from urllib import urlencode
from urlparse import urlparse, parse_qsl
import hashlib
import base64
import requests
import os
import common
import sys

def fetch_activation_bytes(username, password):
    if os.getenv("DEBUG"):
        print("[!] Running in DEBUG mode. You will need to login in a semi-automatic way, wait for the login screen to show up ;)")
    base_url = 'https://www.audible.com/'
    base_url_license = 'https://www.audible.com/'
    lang = 'us'

    is_de = False
    if len(sys.argv) > 1 and sys.argv[1] == "de":
        print("using audible.de")
        base_url = 'https://www.audible.de/'
        lang = 'de'
        is_de = True

    # Step 0
    opts = webdriver.ChromeOptions()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko")

    # Step 1
    if '@' in username:  # Amazon login using email address
        login_url = "https://www.amazon.com/ap/signin?"
    else:  # Audible member login using username (untested!)
        login_url = "https://www.audible.com/sign-in/ref=ap_to_private?forcePrivateSignIn=true&rdPath=https%3A%2F%2Fwww.audible.com%2F%3F"
    player_id = base64.encodestring(hashlib.sha1("").digest()).rstrip()
    payload = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.mode': 'logout',
        'openid.assoc_handle': 'amzn_audible_' + lang,
        'openid.return_to': base_url + 'player-auth-token?playerType=software&playerId=%s=&bp_ua=y&playerModel=Desktop&playerManufacturer=Audible' % (player_id)
    }
    if is_de:
        login_url = login_url.replace('.com', '.de')

    driver = webdriver.Chrome(chrome_options=opts, executable_path="./chromedriver")

    query_string = urlencode(payload)
    url = login_url + query_string
    driver.get(base_url + '?ipRedirectOverride=true')
    driver.get(url)
    search_box = driver.find_element_by_id('ap_email')
    search_box.send_keys(username)
    search_box = driver.find_element_by_id('ap_password')
    search_box.send_keys(password)
    if os.getenv("DEBUG"):  # enable if you hit CAPTCHA (or other "security" screens)
        time.sleep(32)
    else:
        search_box.submit()

    # Step 2
    driver.get(base_url + 'player-auth-token?playerType=software&bp_ua=y&playerModel=Desktop&playerId=%s&playerManufacturer=Audible&serial=' % (player_id))
    current_url = driver.current_url
    o = urlparse(current_url)
    data = dict(parse_qsl(o.query))

    # Step 2.5, switch User-Agent to "Audible Download Manager"
    headers = {
        'User-Agent': "Audible Download Manager",
    }
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    # Step 3, de-register first, in order to stop hogging all activation slots (there are 8 of them!)
    durl = base_url_license + 'license/licenseForCustomerToken?' + 'customer_token=' + data["playerToken"] + "&action=de-register"
    s.get(durl, headers=headers)

    # Step 4
    url = base_url_license + 'license/licenseForCustomerToken?' + 'customer_token=' + data["playerToken"]
    response = s.get(url, headers=headers)
    common.extract_activation_bytes(response.content)

    # Step 5 (de-register again to stop filling activation slots)
    s.get(durl, headers=headers)

    # driver.get(url)
    time.sleep(8)
    driver.quit()


if __name__ == "__main__":
    username = raw_input("Username: ")
    password = getpass("Password: ")

    fetch_activation_bytes(username, password)
