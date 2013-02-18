# Scans the flair lists of subreddits defined in the database
# Unsets any flairs that do not match the subreddit's regex

import sys, os
import re
import praw
import sqlite3
from ConfigParser import SafeConfigParser

def main():
    containing_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    # load config file
    cfg_file = SafeConfigParser()
    path_to_cfg = os.path.join(containing_dir, 'flair_enforcer.cfg')
    cfg_file.read(path_to_cfg)

    # connect to db and get data
    path_to_db = os.path.join(containing_dir, 'flair_enforcer.db')
    con = sqlite3.connect(path_to_db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM subreddits')
    subreddits = cur.fetchall()

    # log into reddit
    r = praw.Reddit(user_agent=cfg_file.get('reddit', 'user_agent'))
    r.login(cfg_file.get('reddit', 'username'),
            cfg_file.get('reddit', 'password'))

    for sr in subreddits:
        subreddit = r.get_subreddit(sr['name'])

        for flair in subreddit.get_flair_list():
            flags = re.UNICODE
            if not sr['case_sensitive']:
                flags = flags|re.IGNORECASE

            # if their flair text doesn't match the regex, clear their flair
            if (not flair['flair_text']
                    or not re.search(sr['flair_regex'],
                                     flair['flair_text'],
                                     flags)):
                print ('Unsetting flair in /r/{0} for {1} '
                       '(was text="{2}" class="{3}")'
                       .format(sr['name'], flair['user'],
                               flair['flair_text'], flair['flair_css_class']))
                subreddit.set_flair(item=flair['user'])

if __name__ == '__main__':
    main()
