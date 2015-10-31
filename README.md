# web_snoop

## About

Utility for checking web-resource for certain changes and reporting it by email.

As a matter of fact it was made, because I had troubles to make an appointment to a doctor. My medical center has a web service which one can use to register an appointment to the doctor. But it's really hard to make it, because available time can appear at random time and I constantly missed it. So, I decided to write a small script, that will inform me, when there is an available time.

One can use this script as the base for it's own, that can inform about a web-resource changes (but be aware, not to DDOS it ;-)).

##Requirements

- Python v2.7
- job-scheduler like cron, that can execute script from time to time
- email address to send and receive messages

## Installing

1. Place your settings in *settings.py* (use *settings_example.py)*.

2. Edit *parse_data()* function, to match your needs.

3. Add *main.py* as job for job-scheduler.

- **In Linux** (Mac OS too, I guess) you can use cron:
`sudo crontab -e`
Add line to the end of the file, like this:
`*/10 * * * * /usr/bin/python /home/pi/Documents/web_snoop/main.py`
This will launch job every 10 minutes.

- **In Windows** there is a command *taskschd.msc* to launch task-scheduler GUI.

## License

The MIT License