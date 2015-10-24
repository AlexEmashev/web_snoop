# -*- coding: utf-8 -*-
from datetime import datetime
import os
import urllib2
import json
import smtplib
import logging
import logging.handlers
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Import settings
from settings import SETTINGS


# Returns absolute path to file (used for names from settings)
def abs_path(path):
    return os.path.join(os.path.dirname(__file__), path)


# Setup log
def log_setup():
    rotate_handler = logging.handlers.RotatingFileHandler(abs_path(SETTINGS['log_file_name']), maxBytes=2048, backupCount=1)
    formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno) d]# %(levelname)-8s [%(asctime)s] %(message)s')
    rotate_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(rotate_handler)
    logger.setLevel(logging.DEBUG)


# Get data from web resource
def get_data():
    try:
        logging.info(u'Requesting ' + SETTINGS['url'] + u'...')
        response = urllib2.urlopen(SETTINGS['url']).read()
        data = json.loads(response)
        return data
    except Exceptiona as exc:
        logging.error(u'Exception during web request ' + exc.message)
    raise


# Parse received data, search for certain criteria
def parse_data(data):
    logging.info(u'Parsing data...')

    results = []
    # Provide your own code for this
    for planning in data['planning']:
        if not planning['disabled']:
            for interval in planning['intervals']:
                if interval["free"]:
                    results.append(interval["formattedDate"])

    if len(results) == 0:
        logging.info(u'There are no results')

    return results


# Format  message with results
def format_message(data):
    try:
        logging.info(u'Formatting message...')

        if len(data) == 0:
            return u''

        mail_template = open(abs_path(SETTINGS['mail_template'])).read()
        results_list = u'<ul>'
        for item in data:
            results_list += u'<li>' + item + u'</li>'
        results_list += u'</ul>'

        mail_template = mail_template.replace(u'{{date}}', datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        mail_template = mail_template.replace(u'{{results}}', results_list)
        mail_template = mail_template.replace(u'{{visit_url}}', SETTINGS['mail_msg_info'])

        return mail_template

    except Exceptiona as exc:
        logging.error(u'Exception while formatting ' + exc.message)
        raise


# Send mail with notification
def send_mail(message):
    try:
        logging.info('Sending email...')
        from_ = SETTINGS['mail_sender_address']
        to_ = SETTINGS['mail_receiver_address']

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SETTINGS['mail_subject']
        msg['From'] = from_
        msg['To'] = to_

        # Create the body of the message (a plain-text and an HTML version).
        text = u'See HTML message for more info'
        html1 = message

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html1, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        mail = smtplib.SMTP(SETTINGS['mail_smtp_address'], SETTINGS['mail_smtp_port'])

        mail.ehlo()

        mail.starttls()

        # Note, if you're using Gmail, you should allow unsafe apps to send emails in Google account.
        mail.login(SETTINGS['mail_sender_address'], SETTINGS['mail_sender_password'])
        mail.sendmail(from_, to_, msg.as_string())
        mail.quit()

        logging.info('Email sent')
        return True

    except Exception as exc:
        logging.error(u'Exception during mail sending ' + exc.message)
        raise


# Function that run all job, if previous doesn't create file with results.
def run_task():
    # If result file is exist, it means that script has already ran successfully
    if os.path.isfile(abs_path(SETTINGS['result_file_name'])):
        print 'Check result here ' + os.path.abspath(abs_path((SETTINGS['result_file_name'])))
        logging.info('Task completed, check results file here ' +
                     os.path.abspath(abs_path((SETTINGS['result_file_name']))))
        return
    else:
        try:
            log_setup()
            data = get_data()
            parsed_data = parse_data(data)
            # If there are results, format them and send by email
            if len(parsed_data) > 0:
                formatted_message = format_message(parsed_data)
                send_mail(formatted_message)
                print 'Mail sent'
                # Create file with results
                file_result = open(abs_path(SETTINGS['result_file_name']), 'w+')
                file_result.write('Data parsed and sent successfully at ' + datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
                file_result.close()

        except Exception as exc:
            logging.error(u'Exception ' + exc.message)

# Run the script
run_task()
