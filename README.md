#  Automated YouTube Video Link Archiving for Andrew Kibe Comedy Show

## Description

I loved [the Andrew Kibe Comedy Show](https://twitter.com/KibeAndy) on YouTube.
It was hosted daily before he was cancelled and all his videos deleted from the platform.

In order to encourage people to watch the live show and also monetize on Patreon, the host unlisted the videos as soon the show was done.
So, if you did not have the link you could not re-watch the show unless you were subscribed to his Patreon.

To overcome this limitation, I leveraged my server infrastructure and programming skills to ensure convenient access to the shows at my own pace.

I developed a Python script that retrieves the YouTube RSS feed and stores the links in a dedicated Google Sheet. This script is orchestrated by a scheduled task using CRON, executing every three hours.

Over the course of a year, I successfully compiled and stored all links to Andrew Kibe's videos in a dedicated [Google Sheet](https://docs.google.com/spreadsheets/d/1yQFIRC1dF9rWpXaQYxT78-WwO_egei7xJFye--rtBts)
