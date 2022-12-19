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
