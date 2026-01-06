# Tracing the T2 BCE with qemu

(partially)



Make QEMU trace events to a file and make it not map the io memory for the bce (so read/writes are caught and traced):
```xml
<qemu:commandline>
    <qemu:arg value="-trace"/>
    <qemu:arg value="events=/path/to/events.txt,file=/tmp/vfiotrace.log"/>
  </qemu:commandline>



<qemu:override>
    <qemu:device alias="ua-bce">
      <qemu:frontend>
        <qemu:property name="x-no-mmap" type="bool" value="true"/>
      </qemu:frontend>
    </qemu:device>
  </qemu:override>
```

This traces some of the windows driver's activity, with `vfio_region_write` and `vfio_region_read` events, however once the driver starts mapping memory and using that to communicate with bce, we can't see what its doing.

For example, the log file made by qemu can then be processed by `./analyse.py boot-hybernate.log` and you can see everything with the mailbox and doorbell, however the actual data and queue creation is not traced with this simple method.

```
mb send ('SET_FW_PROTOCOL_VERSION', '0x20001')
non zero read(0x81c, 0010f000)
mb recv ('SET_FW_PROTOCOL_VERSION', '0x20001')
mb send ('REGISTER_COMMAND_CQ', '0x1428222d8')
non zero read(0x81c, 00100100)
mb recv ('REGISTER_COMMAND_QUEUE_REPLY', '0x0')
mb send ('REGISTER_COMMAND_SQ', '0x1428222f0')
non zero read(0x81c, 00101200)
mb recv ('REGISTER_COMMAND_QUEUE_REPLY', '0x0')
timestamp inital start
write doorbell qid=1, tail=1
write doorbell qid=0, tail=1
write doorbell qid=1, tail=2
...
write doorbell qid=1, tail=30
write doorbell qid=0, tail=30
timestamp stop
mb send ('SAVE_STATE_AND_SLEEP', '0x141dc0002')
non zero read(0x81c, 00102300)
mb recv ('SAVE_RESTORE_STATE_COMPLETE', '0x0')
```
