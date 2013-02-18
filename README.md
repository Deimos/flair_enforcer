# Flair Enforcer
This is a script for [reddit](http://www.reddit.com) that can scan the user flair lists of subreddits that it moderates and remove flair from any users with flair that doesn't match a defined regex.

By using this, subreddits can allow users to set their own flair, but ensure that they stay inside particular guidelines. For example, some subreddits allow users to set their flair to point to their profiles on specific other sites (Steam profiles, etc.).

### Setup / Configuration

1. Rename `flair_enforcer.cfg.example` to `flair_enforcer.cfg` and `flair_enforcer.db.example` to `flair_enforcer.db`.
2. Edit `flair_enforcer.cfg` and set the `username` and `password` lines accordingly for the user account that you want to run the script under
3. Using a SQLite client, insert a row into the `subreddits` table in `flair_enforcer.db` for each subreddit you want to enforce flair inside. There are three columns:

* `name` = The subreddit's name. If it's /r/example, insert `'example'`.
* `flair_regex` = Each user in the subreddit's flair text will be checked against this regex. If their flair text does **not** match, their flair will be removed.
* `case_sensitive` = If true, the regex check will be case-sensitive.

### Example

As an example, imagine that we have a subreddit /r/reddit, where users are only allowed to set their flair as the URL of their reddit overview. The row in the database for this subreddit should look as follows:

* `name` = `reddit`
* `flair_regex` = `^http://www\.reddit\.com/user/[a-z0-9_-]+$`
* `case_sensitive` = false
