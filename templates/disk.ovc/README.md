# template: disk.ovc

## Description:

This actor template represents a disk in ovc to be used later on by other services.

## Schema:
 - size: disk size in GB.
 - type: type of disk boot or normal.
 - description: description of disk.
 - maxIOPS: max inputs outputs per second (same as totalIopsSec).
 - devicename: device name (leave empty).
 - ssdSize: ssd size always available , will default to 10
 - location: location of the resource on cloud (i.e du-conv-2)
 - totalBytesSec: The optional total_bytes_sec element is the total throughput limit in bytes per second. This cannot appear with read_bytes_sec or write_bytes_sec.
 - readBytesSec: The optional read_bytes_sec element is the read throughput limit in bytes per second.
 - writeBytesSec: The optional write_bytes_sec element is the write throughput limit in bytes per second.
 - totalIopsSec: The optional total_iops_sec element is the total I/O operations per second. This cannot appear with read_iops_sec or write_iops_sec (same as maxIOPS).
 - readIopsSec: The optional read_iops_sec element is the read I/O operations per second.
 - writeIopsSec: The optional write_iops_sec element is the write I/O operations per second.
 - totalBytesSecMax: The optional total_bytes_sec_max element is the maximum total throughput limit in bytes per second.
 - readBytesSecMax: The optional read_bytes_sec_max element is the maximum read throughput limit in bytes per second.
 - writeBytesSecMax: The optional write_bytes_sec_max element is the maximum write throughput limit in bytes per second.
 - totalIopsSecMax: The optional total_iops_sec_max element is the maximum total I/O operations per second. This cannot appear with read_iops_sec_max or write_iops_sec_max.
 - readIopsSecMax: The optional read_iops_sec_max element is the maximum read I/O operations per second.
 - writeIopsSecMax: The optional write_iops_sec_max element is the maximum write I/O operations per second.
 - sizeIopsSec: The optional size_iops_sec element is the size of I/O operations per second.
 - diskId: Id of disk.

Disk name will be service name.

## Example for creating disks
```yaml
g8client__env:
    url: '<env_url>'
    login: '<login>'
    password: '<password>'
    account: '<account>'

disk.ovc__disk1:
    size: <disk size>
    g8client: 'env'
    description: '<Description of the disk>'
    type: '<B or D. B for Boot and D for Data>'
    location: '<location of the disk>'

actions:

  - action: install
    actor: g8client
    service: env

  - action: create
    actor: disk.ovc
    service: disk1
```

## Example for deleting disks
```yaml
g8client__env:
    url: '<env_url>'
    login: '<login>'
    password: '<password>'
    account: '<account>'

disk.ovc__disk1:

actions:

  - action: install
    actor: g8client
    service: env

  - action: delete
    actor: disk.ovc
    service: disk1
```

## Example for limit IO for disks you can only limit disks that are attached to a vm, which is done using node.ovc service.
(note that the disk MUST be attached to a machine)
```yaml
g8client__env:
    url: '<env_url>'
    login: '<login>'
    password: '<password>'
    account: '<account>'

disk.ovc__disk1:
    maxIOPS: 100
    readBytesSec: 6500000
    writeBytesSec: 6500000

actions:

  - action: install
    actor: g8client
    service: env

  - action: limit_io
    actor: disk.ovc
    service: disk1
```

## Example for using disk with other services:

```yaml
sshkey__demo:

g8client__env1:
    # url: 'du-conv-3.demo.greenitglobe.com'
    url: '<env url>'
    login: '<login>'
    password: '<password>'
    account: '<account name>'

vdcfarm__vdcfarm1:

vdc__scality:
    vdcfarm: 'vdcfarm1'
    g8client: 'env1'
    location: '<location>'

disk.ovc__disk1:
  size: 1000

s3__demo:
    vdc: 'scality'
    disk:
      - 'disk1'
    domain: 'mystorage.com'
```
