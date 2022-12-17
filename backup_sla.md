## Backup SLA

### Backup coverage
- MySQL: Dump of the database.
- InfluxDb: Dump of the database.

### RPO:
- Incremental backup: Every day at 2:00.
- Full backup: Every Sunday at: 0:00
- Acceptable data loss: 1 day

### Versioning and retention:
Backups are stored for 30 days, so 30 versions are held \
Backups will simultaneously be created on the local server and on the backup server

### Usability checks:
Usability check will be done weekly with the full backup on a temporary test server

### Restoration criteria
A backup should be restored when data loss has occurred that can be fixed with the backup, when
the data on server has become unusable or when the data has been modified by an unauthorized entity.

### RTO
System can be recovered in 1 hour

### Storage
Two copies are stored locally on servers
One copy is on an off-site server

For MySQL we backup SQL dump in two ways. One way is local storage and other is in cloud. 
Local storage is copied to two HDD storage mediums to minimize any damage done by one HDD going bad.

InfluxDB we back up the data in two ways. One way is local storage and other is in cloud.
Local storage is copied to two HDD storage mediums to minimize any damage done by one HDD going bad.


RPO: Backup dumps will be done every night at 01:25, which makes RPO 24 hours.
Backing up dump files starts 5minutes later at 01:30.


Versioning and retention: We are backing up data for 30 days (configured as 31 days) and we keep 31 versions of backups.


Usability checks: Done once every two weeks, we build two VMs and recreate a working system using one random version of a backup. We restore data from that backup version and run ansible playbook. After the VMs are restored we check data from grafana, check if all mandatory services are running, manually check InfluxDB database to see if additional data is still created, manually check mysql databases and add more info to it to verify system as operational. 


Restoration criteria: Restoration is needed if multiple services are down and no new data is being created and all tries to restore the system manually have failed.

RTO: Is set as 2 hours. Right now it is more likely lower than that, but we expect the time to recover to slowly increase with bigger databases. 