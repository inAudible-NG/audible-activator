#!/usr/bin/env python2

from __future__ import print_function
from getpass import getpass
from optparse import OptionParser
import sys
import time
from selenium import webdriver
from urllib import urlencode
from urlparse import urlparse, parse_qsl
import hashlib
import base64
import requests
import os
import common
import binascii


def fetch_activation_bytes(username, password, options):
    base_url = 'https://www.audible.com/'
    base_url_license = 'https://www.audible.com/'
    lang = options.lang

    # Step 0
    opts = webdriver.ChromeOptions()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko")

    # Step 1
    if '@' in username:  # Amazon login using email address
        login_url = "https://www.amazon.com/ap/signin?"
    else:  # Audible member login using username (untested!)
        login_url = "https://www.audible.com/sign-in/ref=ap_to_private?forcePrivateSignIn=true&rdPath=https%3A%2F%2Fwww.audible.com%2F%3F"
    if lang != "us":  # something more clever might be needed
        login_url = login_url.replace('.com', "." + lang)
        base_url = base_url.replace('.com', "." + lang)

    player_id = base64.encodestring(hashlib.sha1("").digest()).rstrip()  # keep this same to avoid hogging activation slots
    if options.player_id:
        player_id = base64.encodestring(binascii.unhexlify(options.player_id)).rstrip()
    print("[*] Player ID is %s" % player_id)

    payload = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.mode': 'logout',
        'openid.assoc_handle': 'amzn_audible_' + lang,
        'openid.return_to': base_url + 'player-auth-token?playerType=software&playerId=%s=&bp_ua=y&playerModel=Desktop&playerManufacturer=Audible' % (player_id)
    }

    if sys.platform == 'win32':
        chromedriver_path = "chromedriver.exe"
    else:
        chromedriver_path = "./chromedriver"

    driver = webdriver.Chrome(chrome_options=opts,
                              executable_path=chromedriver_path)

    query_string = urlencode(payload)
    url = login_url + query_string
    driver.get(base_url + '?ipRedirectOverride=true')
    driver.get(url)
    if os.getenv("DEBUG") or options.debug:  # enable if you hit CAPTCHA or 2FA or other "security" screens
        print("[!] Running in DEBUG mode. You will need to login in a semi-automatic way, wait for the login screen to show up ;)")
        time.sleep(32)
    else:
        search_box = driver.find_element_by_id('ap_email')
        search_box.send_keys(username)
        search_box = driver.find_element_by_id('ap_password')
        search_box.send_keys(password)
        search_box.submit()
        if options.two_factor:
            search_box = driver.find_element_by_id('auth-mfa-otpcode')
            search_box.send_keys(raw_input("Enter Two-Step Verification Code: "))
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

    # Step 3, de-register first, in order to stop hogging all activation slots
    # (there are 8 of them!)
    durl = base_url_license + 'license/licenseForCustomerToken?' \
        + 'customer_token=' + data["playerToken"] + "&action=de-register"
    s.get(durl, headers=headers)

    # Step 4
    url = base_url_license + 'license/licenseForCustomerToken?' \
        + 'customer_token=' + data["playerToken"]
    response = s.get(url, headers=headers)

    with open("activation.blob", "wb") as f:
        f.write(response.content)
    activation_bytes, _ = common.extract_activation_bytes(response.content)
    print(activation_bytes)

    # Step 5 (de-register again to stop filling activation slots)
    s.get(durl, headers=headers)

    # driver.get(url)
    time.sleep(8)
    driver.quit()


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]", version="%prog 0.2")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="run program in debug mode, enable this for 2FA enabled accounts or for authentication debugging")
    parser.add_option("-l", "--lang",
                      action="store",
                      dest="lang",
                      default="us",
                      help="us (default) / de / fr",)
    parser.add_option("-p",
                      action="store",
                      dest="player_id",
                      default=None,
                      help="Player ID in hex (for debugging, not for end users)",)
    parser.add_option("--username",
                      action="store",
                      dest="username",
                      default=False,
                      help="Audible username, use along with the --password option")
    parser.add_option("--password",
                      action="store",
                      dest="password",
                      default=False,
                      help="Audible password")
    parser.add_option("-t", "--two-factor",
                      action="store_true",
                      dest="two_factor",
                      default=False,
                      help="Use this option to enable two factor authentication",)
    (options, args) = parser.parse_args()

    username = raw_input("Username: ")
    password = getpass("Password: ")

    fetch_activation_bytes(username, password, options)
