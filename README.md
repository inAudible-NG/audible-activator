# audible-activator

A script to retrieve your activation data (activation_bytes) from Audible
servers.

Last tested on Ubuntu 20.04 + Chromium 83.x + chromium-chromedriver (83.0.x) +
Python 3.8.x in July 2020.

July-2020 update: https://github.com/openaudible/openaudible folks have stolen
this `central principal component` code + "IP" and have created a
non-100%-free-source commercial product with it.


## Usage

```
$ ./audible-activator.py -h
Usage: audible-activator.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d, --debug           run program in debug mode, enable this for 2FA enabled
                        accounts or for authentication debugging
  -f, --firefox         use this option to use firefox instead of chrome
  -l LANG, --lang=LANG  us (default) / au / in / de / fr / jp / uk (untested)
  -p PLAYER_ID          Player ID in hex (for debugging, not for end users)
  --username=USERNAME   Audible username, use along with the --password option
  --password=PASSWORD   Audible password
...

$ ./audible-activator.py
<enter username and password>

$ ./audible-activator.py -l de  # for "de" users
<enter username and password>

$ mpv --demuxer-lavf-o=activation_bytes=CAFED00D sample.aax

$ echo -e "\ndemuxer-lavf-o=activation_bytes=CAFED00D" >> ~/.config/mpv/mpv.conf  # for convenience

$ ffplay -activation_bytes CAFED00D sample.aax
```

## Quick Setup

Python 2 (or Python >= 3.6) is required along with Selenium, Requests,
ChromeDriver, and Google Chrome.

```
pip install --user requests  # use "easy_install" if pip is missing

pip install --user selenium
```

Download and extract the correct ChromeDriver zip file [from
here](https://sites.google.com/a/chromium.org/chromedriver/downloads) to this
folder.

Download Google Chrome from https://www.google.com/chrome/ and install it on
your computer.

Ryan reports that the 32-bit Mac ChromeDriver works fine under a 64-bit Mac
environment.

## Anti-Piracy Notice

Note that this project does NOT 'crack' the DRM. It simplys allows the user to
use their own encryption key (fetched from Audible servers) to decrypt the
audiobook in the same manner that the official audiobook playing software does.

Please only use this application for gaining full access to your own audiobooks
for archiving/converson/convenience. DeDRMed audiobooks should not be uploaded
to open servers, torrents, or other methods of mass distribution. No help will
be given to people doing such things. Authors, retailers, and publishers all
need to make a living, so that they can continue to produce audiobooks for us to
hear, and enjoy. Don't be a parasite.

This message is borrowed from the https://apprenticealf.wordpress.com/ page.

## Debugging Tips

* If you see an error message like "audible_error=Internal service error has
occured while processing the request, please contact service admin" during the
activation process, then contact Audible customer care and they will clear up
your activation slots (there are 8 such slots).

* If you see an "activation loop" in the official software (e.g. Audible Download
Manager), then you are seeing the same exact problem (you activation slots are
all used up).

* Too many authentication attempts result in a temporary 30 minutes ban!

* Use the following command to extract the SHA1 checksum from .aax files.

  ```
  $ ffprobe test.aax  # extract SHA1 checksum
  ...
  ...
  [mov,mp4,m4a,3gp,3g2,mj2 @ 0x1dde580] [aax] file checksum == 999a6a...
  [mov,mp4,m4a,3gp,3g2,mj2 @ 0x1dde580] [aax] activation_bytes option is missing!
  ```

* In case of login problems use the `./audible-activator.py -d` command  to run
the program in debugging mode and to login manually.

* If you get an error in your terminal about selenium (such as
`selenium.common.exceptions.WebDriverException: Message: unknown error: call
function result missing 'value'`), make sure you have the most recent
*compatible* chromedriver version. You may need to uninstall and reinstall it.

* This program is pretty short and easy to debug. I cannot provide end-user
support but I would be very happy to accept patches.

* If this program does not work for you and all the debugging steps fail, then
use the https://github.com/inAudible-NG/tables project to recover your
"activation_bytes" in an offline manner. The good news is that you need to
retrieve your "activation_bytes" only once.

* Running `wine AudibleGeneratePCPlayerID.exe` multiple times under Linux can
result in different outputs (different Player ID values). To get stable output
run `wine AudibleGeneratePCPlayerID.exe` after running the "Audible Manager"
program (Manager.exe) under Wine once.

## Notes

* It is possible to extract the "activation_bytes" from an existing
'AudibleActivation.sys' file.

  ```
  $ ./AAS-parser.py AudibleActivation.sys
  CAFED00D
  ```

  You can grab the 'AudibleActivation.sys' file from various already-activated
  devices like Android phones, and Sansa music players.

* If you have an Audible username (not an email address), please help in
testing and fixing this program.

* ``xhost local:root``

## Credits

* sfgasdfsafggfgg (spindoctors_mix <none@none.com>)

* kidburglar

* Jason Peper (jasontrublu, for "de" support and cleaner code)

* Braden (braden337, add Google Chrome as a requirement)

* Fernando Paladini (non-interactive credentials input)

* wolfi101 (Firefox support)

* corbolais (chromedriver autodetection)

* Thies Mueller (td00, Python 3 support)

* Ziyuan Guo (shadowmourne, Audible JP support)

* Ryan Connors (ryanpconnors, Python 3 fixes)

* Savio Sebastian (savioseb) - Support for Audible India

* Rod Vagg (rvagg) - Support for Audible Australia

* Jason (JasonMFry) - ChromeDriver debugging tip

* Stefan Gränitz (weliveindetail) - Make authentication reliable

* See https://github.com/inAudible-NG/audible-activator/pulls.
