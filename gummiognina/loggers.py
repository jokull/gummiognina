import os.path
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

def configure_logging(app):
    
    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
        'server-error@jl.is', app.config['ADMINS'], 'JL Error', 
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)

    log_dest = os.path.abspath(os.path.join(app.root_path, '..', 'log'))
    log_dest = os.path.exists(log_dest) or '/tmp/log'

    file_handler = RotatingFileHandler(log_dest)
    file_handler.setLevel(logging.WARNING)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(mail_handler)