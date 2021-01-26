# twitter2mewe

Sync Twitter timeline to MeWe without API.

# Pre-installation

Install these packages first:

* chromium-browser
* chromium-chromedriver

And create symbolic link for chromedriver:

    sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

Then login MeWe and keep cookies.

# Workaround on Chromium

Chromium cannot use cookies in headless mode with latest version (now it's 87), so you need the workaround to install old version, and avoid from upgrading:

    apt-cache showpkg chromium-browser
    sudo apt install \
        chromium-browser=65.0.3325.181-0ubuntu1 \
        chromium-chromedriver=65.0.3325.181-0ubuntu1 \
        chromium-codecs-ffmpeg=65.0.3325.181-0ubuntu1
    sudo apt-mark hold chromium-browser chromium-chromedriver chromium-codecs-ffmpeg

Since this chromium is old, I suggest that just use it for twitter2mewe (so it will only access MeWe site), and not to use it regularly, for security reason.

## Installation

Install Python 3 first (I used `pyenv` to run it), then use `pip` to install dependencies:

    pip install -r requirements.txt

Setup Twitter's key & secret in `~/.config/twitter2mewe/config.ini`:

    [default]
    mewe_token = x
    twitter_access_token = x
    twitter_access_token_secret = x
    twitter_consumer_key = x
    twitter_consumer_secret = x
    twitter_username = x

Use `sqlite3` to create table schema in `~/.config/twitter2mewe/entry.sqlite3`:

    $ sqlite3 ~/.config/twitter2mewe/entry.sqlite3
    sqlite> CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

# Crontab

When using pyenv, you might need to specify pyenv to run this script:

    LANG=en_US.UTF-8 ~/.pyenv/shims/python3 /path/twitter2facebook/twitter2mewe.py

## License

See [LICENSE](LICENSE).
