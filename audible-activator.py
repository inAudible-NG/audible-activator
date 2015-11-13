#!/usr/bin/env python

from __future__ import print_function
import time
from selenium import webdriver
from urllib import urlencode
from urlparse import urlparse, parse_qsl
import hashlib
import base64
import traceback
import binascii
import sys
import requests
import os


def fetch_activation_bytes(username, password):
    if os.getenv("DEBUG"):
        print("[!] Running in DEBUG mode. You will need to login in a semi-automatic way, wait for the login screen to show up ;)")

    # Step 0
    opts = webdriver.ChromeOptions()
    # opts.add_argument("user-agent=Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko")
    driver = webdriver.Chrome(chrome_options=opts, executable_path="./chromedriver")

    # Step 1
    if '@' in username:  # Amazon login using email address
        base_url = "https://www.amazon.com/ap/signin?"
    else:  # Audible member login using username (untested!)
        base_url = "https://www.audible.com/sign-in/ref=ap_to_private?forcePrivateSignIn=true&rdPath=https%3A%2F%2Fwww.audible.com%2F%3F"
    # fake_hash = hashlib.sha1(os.urandom(128)).digest()
    # playerId = base64.encodestring(fake_hash).rstrip()  # generate base64 digest of a random 20 byte string ;)
    playerId = base64.encodestring(hashlib.sha1("").digest()).rstrip()
    payload = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.mode': 'logout',
        'openid.assoc_handle': 'amzn_audible_us',
        'openid.return_to': 'https://www.audible.com/player-auth-token?playerType=software&playerId=%s=&bp_ua=y&playerModel=Desktop&playerManufacturer=Audible' % (playerId)
    }
    query_string = urlencode(payload)
    url = base_url + query_string
    # print(url, file=sys.stderr)
    # http://chromedriver.storage.googleapis.com/index.html?path=2.19/
    driver.get('https://www.audible.com/')
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
    driver.get('https://www.audible.com/player-auth-token?playerType=software&bp_ua=y&playerModel=Desktop&playerId=%s&playerManufacturer=Audible&serial=' % (playerId))
    current_url = driver.current_url
    o = urlparse(current_url)
    data = dict(parse_qsl(o.query))
    # print(data, file=sys.stderr)

    # Step 2.5, switch User-Agent to "Audible Download Manager"
    headers = {
        'User-Agent': "Audible Download Manager",
    }
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    # Step 3, de-register first, in order to stop hogging all activation slots (there are 8 of them!)
    durl = 'https://www.audible.com/license/licenseForCustomerToken?' + 'customer_token=' + data["playerToken"] + "&action=de-register"
    # print(durl, file=sys.stderr)
    response = s.get(durl, headers=headers)
    # driver.get(durl)
    # extract_activation_bytes(response.content)

    # Step 4
    # url = 'https://www.audible.com/license/licenseForCustomerToken?' + 'customer_token=' + data["playerToken"] + "&action=register"
    url = 'https://www.audible.com/license/licenseForCustomerToken?' + 'customer_token=' + data["playerToken"]
    # print(url, file=sys.stderr)
    response = s.get(url, headers=headers)
    # driver.get(durl)
    # print(response.content)
    extract_activation_bytes(response.content)

    # Step 5 (de-register again to stop filling activation slots)
    # print(durl, file=sys.stderr)
    # driver.get(durl)
    response = s.get(durl, headers=headers)

    # driver.get(url)
    time.sleep(8)
    driver.quit()


def extract_activation_bytes(data):
    try:
        if (b"BAD_LOGIN" in data or b"Whoops" in data) or \
                b"group_id" not in data:
            print(data)
            print("\nActivation failed! ;(")
            sys.exit(-1)
        k = data.rfind(b"group_id")
        l = data[k:].find(b")")
        keys = data[k + l + 1 + 1:]
        output_keys = []
        # each key is of 70 bytes
        for i in range(0, 8):
            key = keys[i * 70 + i:(i + 1) * 70 + i]
            h = binascii.hexlify(bytes(key))
            h = [h[i:i+2] for i in range(0, len(h), 2)]
            h = b",".join(h)
            output_keys.append(h)
    except SystemExit as e:
        sys.exit(e)
    except:
        traceback.print_exc()

    # only 4 bytes of output_keys[0] are necessary for decryption! ;)
    activation_bytes = output_keys[0].replace(b",", b"")[0:8]
    # get the endianness right (reverse string in pairs of 2)
    activation_bytes = "".join(reversed([activation_bytes[i:i+2] for i in
                                         range(0, len(activation_bytes), 2)]))
    print(activation_bytes)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s <username> <password>" % sys.argv[0])
        sys.exit(1)

    fetch_activation_bytes(sys.argv[1], sys.argv[2])
