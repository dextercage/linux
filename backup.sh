#!/bin/bash

DATE=$(date +%Y-%m-%d-%H-%M)
FILE_NAME="GALERA_BACKUP_CRON_$DATE.sql"
mysqldump -u wpuser --password=1975kjKJ1975 wordpressDB > /tmp/$FILE_NAME
rsync -az /tmp/$FILE_NAME ubuntu@54.93.167.130:/home/ubuntu/db_backup/

