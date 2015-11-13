# audible-activator

Retrieves your activation data (activation_bytes) from Audible servers.

## Usage

```
$ ./audible-activator.py <username> <password>

$ mpv --demuxer-lavf-o=activation_bytes=CAFED00D sample.aax
```

## Quick Setup

Python 2 is required.

```
pip install requests  # use "easy_install" if pip is missing

pip install selenium
```

### Install ChromeDriver

```
Extract correct zip file from the http://chromedriver.storage.googleapis.com/index.html?path=2.20/ page, to this folder.

```

Ryan reports that the 32-bit Mac ChromeDriver works fine under a 64-bit Mac
environment.

## Notes

``xhost local:root``

## Anti-Piracy Notice

Note that this project does NOT ‘crack’ the DRM. It simplys allows the user to
use their own encryption key (fetched from Audible servers) to decrypt the
audiobook in the same manner that the official audiobook playing software does.

Please only use this application for gaining full access to your own audiobooks
for archiving/converson/convenience. DeDRMed audiobooks should not be uploaded
to open servers, torrents, or other methods of mass distribution. No help will
be given to people doing such things. Authors, retailers, and publishers all
need to make a living, so that they can continue to produce audiobooks for us to
hear, and enjoy. Don’t be a parasite.

This blurb is borrowed from the https://apprenticealf.wordpress.com/ page.

## Debugging

If you see an error message like "audible_error=Internal service error has
occured while processing the request, please contact service admin" during the
activation process, then contact Audible customer care and they will clear up
your activation slots (there are 8 such slots).

If you see an "activation loop" in the official software (e.g. Audible Download
Manager), then you are seeing the same exact problem (you activation slots are
all used).
