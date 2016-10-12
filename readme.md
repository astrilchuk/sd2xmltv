# sd2xmltv

sd2xmltv is an application written in Python to convert Schedules Direct (schedulesdirect.org) TV schedules JSON feed into an xmltv format.  This application was written primarily to facilitate importing TV schedules into tvheadend with Kodi (XBMC) as a frontend.  While the primary target is tvheadend, the output file should work in any application which can parse xmltv.xml files.

Show descriptions are massaged to display like so:

Series; New; S27E21; TVPG • Homer embarrasses himself while trying to read a speech at work, then turns to improv comedy to regain his confidence for public speaking; Marge decides to rebuild Bart's treehouse.

Series; 2014-05-15; S7E24; TVPG • Faced with an uncertain future, Sheldon considers a major change; Emily and Raj decide to take things to the next level.

Feature Film; 1988; PG; ***½ • After a wish turns 12-year-old Josh Baskin (David Moscow) into a 30-year-old man (Tom Hanks), he heads to New York City and gets a low-level job at MacMillen Toy Company. A chance encounter with the owner (Robert Loggia) of the company leads to a promotion testing new toys. Soon a fellow employee, Susan Lawrence (Elizabeth Perkins), takes a romantic interest in Josh. However, the pressure of living as an adult begins to overwhelm him, and he longs to return to his simple, former life as a boy. •  See also: Elf, 13 Going on 30, Freaky Friday

Sports event; Live; E5578 • Alex Ovechkin and the Captials look to keep their playoff hopes alive against the Penguins in game 5 action. In game 4, Patric Hornqvist scored the overtime winner and Pittsburgh defeated Washington 3-2, the Pens first playoff OT win since 2013.

## Installation

For Kodi addon instructions, see README in the /kodi folder.

### Installation for TVHeadend

These instructions are specific for TVHeadend users, but hopefully can help out other users as well.

1. Configure TVHeadend to listen on a socket for xmltv (typically stored in `/home/hts/.hts/tvheadend/epggrab/xmltv.sock`)
2. Unzip or `git clone {url}` into folder accessible to the `hts` user.
3. `chmod +x sd2xmltv.py`
4. (optional) Manage lineups using sd2xmltv --manage ...:
 
 ```
./sd2xmltv.py -u {USERNAME} -p {PASSWORD} -m
 ```
5. Create script which runs listings update regularly:
 ```
!/bin/bash
SRC=/home/hts/sd2xmltv/xmltv.xml
SOCKET=/home/hts/.hts/tvheadend/epggrab/xmltv.sock
EMAIL={EMAILADDR}
USERNAME={USERNAME}
PASSWORD={PASSWORD}

echo "Updating listings" | mail -s "PVR updating" $EMAIL

cd /home/hts/sd2xmltv/
OUTPUT=$(./sd2xmltv.py -u $USERNAME -p $PASSWORD -i 2>&1)

if [ -s $SRC ];
then
	cat $SRC | socat stdin UNIX-CONNECT:$SOCKET
fi

echo $OUTPUT | mail -s "PVR updated" $EMAIL
 ```
6. Make script executable `chmod +x {SCRIPT}`
7. Install this script in the `hts` user's crontab `crontab -e`
8. Execute script and ensure output is as expected

## Usage

For Kodi addon instructions, see README in the /kodi folder.

To create an xmltv.xml file with your current Schedules Direct lineup:

```
./sd2xmltv.py --username sdusername --password sdpassword [--output ./xmltv.xml] [--days 14] [--hdhomerun discover|ip]
```

As a crontab job (twice a day, everyday at 6:45 and 18:45 in this example):

```
45 6,18 * * * cd ~/sdxmltv && sudo python sd2xmltv.py -u sdusername -p sdpassword -o ./xmltv.xml.gz >> sd2xmltv.log 2>&1 && gzip -c -d xmltv.xml.gz | sudo socat - unix-connect:/home/hts/.hts/tvheadend/epggrab/xmltv.sock
```

or, alternatively, write directly to xmltv.sock (sd2xmltv assumes a Unix socket if the filename ends with .sock):

```
45 6,18 * * * cd ~/sd2xmltv && sudo python sd2xmltv.py -u sdusername -p sdpassword -o /home/hts/.hts/tvheadend/epggrab/xmltv.sock >> sd2xmltv.log 2>&1
```



To manage your Schedules Direct lineup(s):

```
./sd2xmltv.py --username sdusername --password sdpassword --manage
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

See [LICENSE](https://github.com/astrilchuk/sd2xmltv/blob/master/LICENSE)
file.
