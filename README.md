# web_snoop

## About

Utility that checks if a particular web-resource has certain changes and reports about it by email.

As a matter of fact it was written, because I had troubles to make an appointment to a doctor. My medical center has a web service where one can register an appointment to the doctor. But it's really hard to register it, because available time can appear at a random time and I always miss it. So, I decided to write a small script, that will inform me, when there is an available time.

One can use this script as the base for it's own, that can inform about a web-resource changes (but be aware, not to DDOS it ;-)).

##Requirements

- Python v2.7 (not yet tested with 3+)
- job-scheduler like cron, that can execute script from time to time
- email address to send and receive messages

##License

The MIT License