# twitter2mewe

This script will use Twitter API to read user's timeline, then post to MeWe.

## Initializing sqlite3 database

    $ sqlite3 ~/.config/twitter2plurk/entry.sqlite3
    sqlite> CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

## License

See [LICENSE](LICENSE).
