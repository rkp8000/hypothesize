from __future__ import division, print_function, unicode_literals
from datetime import datetime
import os
import re
from shutil import copyfile

from django.conf import settings

DB_BACKUP_TIME_PATTERN = 'db_backup_([\d_]+).sqlite3'
DATETIME_FORMAT = '%Y_%m_%d_%H_%M_%S_%f'


def most_recent_db_backup():
    """
    Return the path to the most recent database backup.
    """

    files_in_backup_dir = os.listdir(settings.DATABASE_BACKUPS_DIRECTORY)

    backups = [f for f in files_in_backup_dir if f.startswith('db_backup_')]

    return os.path.join(settings.DATABASE_BACKUPS_DIRECTORY, sorted(backups)[-1])


def back_up_db():
    """
    Back up the database.
    :return: True if successful. False otherwise.
    """

    original_db_path = settings.DATABASES['default']['NAME']

    # create db backup directory if it doesn't exist

    if not os.path.exists(settings.DATABASE_BACKUP_DIRECTORY):

        os.makedirs(settings.DATABASE_BACKUP_DIRECTORY)

    # get path for new backup file

    timestamp = datetime.now().strftime(DATETIME_FORMAT)

    backup_filename = 'db_backup_{}.sqlite3'.format(timestamp)

    backup_path = os.path.join(settings.DATABASE_BACKUP_DIRECTORY, backup_filename)

    copyfile(original_db_path, backup_path)

    return backup_path


def attempt_db_backup():
    """
    Attempt to backup the database.
    :return: path to backed up database, or False if database not backed up
    """

    db_path = settings.DATABASES['default']['NAME']

    # get time of last database modification

    last_db_mod_time = datetime.fromtimestamp(os.path.getmtime(db_path))

    # get datetime of last backup

    last_backup_filename = os.path.basename(most_recent_db_backup())

    last_backup_time_str = re.search(DB_BACKUP_TIME_PATTERN, last_backup_filename).group(1)

    last_backup_time = datetime.strptime(last_backup_time_str, DATETIME_FORMAT)

    # return False if database has not been modified since last backup

    if (last_db_mod_time - last_backup_time).total_seconds() < 2:

        return False

    # return False if not enough time has passed since last backup

    if (datetime.now() - last_backup_time) < settings.DATABASE_BACKUP_INTERVAL_SECONDS:

        return False

    # back up database

    return back_up_db()