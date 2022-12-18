#### Restore all services:
Run this command locally

    ansible-playbook infra.yaml

#### Restore MySQL data from a backup:
Run commands as user `ubuntu` on the machine with the master mysql database
the `Operation not permitted` errors from the duplicity command can be ignored

    sudo su - backup -c "duplicity --no-encryption --force restore rsync://Hattyot@backup//home/Hattyot/mysql/ /home/backup/restore/"
    sudo mysql agama < /home/backup/restore/$(ls /home/backup/restore/ | grep "agama-" | tail -n 1) 
    sudo rm -R /home/backup/restore/

###### Confirm that the restore worked
    
    sudo mysql -e 'SELECT * FROM agama.item';

#### Restore influxdb telegraf data from a backup:
Run commands as user `ubuntu` on the machine with the influxdb database
the `Operation not permitted` errors from the duplicity command can be ignored

    sudo su - backup -c "duplicity --no-encryption --force restore rsync://Hattyot@backup//home/Hattyot/influxdb/telegraf/ /home/backup/restore/"

    sudo systemctl stop telegraf
    sudo influx -execute 'DROP DATABASE telegraf' -port $(grep -P -oh ":\d+" /etc/influxdb/influxdb.conf | cut -d ":" -f 2)
    sudo su - backup -c 'influxd restore -portable -database telegraf /home/backup/restore/telegraf'
    sudo systemctl start telegraf
    sudo rm -R /home/backup/restore/

#### Restore influxdb latency data from a backup:
Run commands as user `ubuntu` on the machine with the influxdb database
the `Operation not permitted` errors from the duplicity command can be ignored

    sudo su - backup -c "duplicity --no-encryption --force restore rsync://Hattyot@backup//home/Hattyot/influxdb/latency/ /home/backup/restore/"

    sudo systemctl stop pinger.service
    sudo influx -execute 'DROP DATABASE latency' -port $(grep -P -oh ":\d+" /etc/influxdb/influxdb.conf | cut -d ":" -f 2)
    sudo influxd restore -portable -database latency /home/backup/restore/latency/
    sudo systemctl start pinger.service
    sudo rm -R /home/backup/restore/