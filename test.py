from pizza import Pizza
from utils import execute_task


p = Pizza()

print "======================= zpool list test==================================="
print p.list_pool()
print "=========================================================================="
print "\n\n"

print "======================= zpool list (detail) test=========================="
print p.list_pool(detail=True)
print "=========================================================================="
print "\n\n"

print "======================= zfs dataset test=========================="
print p.get_dataset("tank")
print "=========================================================================="
print "\n\n"

print "======================= dataset attribute test=========================="
print p.get_dataset_attribute("tank/test",attribute="type")
print "=========================================================================="
print "\n\n"

print "======================= Create Dataset without attribute =========================="
try :
    print p.create_dataset('vstorage','centos01')
except ValueError as e:
    print e
print "=========================================================================="
print "\n\n"

print "======================= Create Dataset with attribute =========================="
try :
    attr = {'mountpoint':'/centos02','quota':'1G'}
    print p.create_dataset('vstorage','centos02',attribute=attr)
except ValueError as e:
    print e
print "=========================================================================="
print "\n\n"

print "======================= Create Zvol =========================="
try :
    print p.create_zvol('vstorage','zvol01',capacity='1G')
except ValueError as e:
    print e
print "=========================================================================="
print "\n\n"

print "======================= dataset attribute change =========================="
print p.alter_dataset_attribute('vstorage/centos02',attribute='mountpoint',value='/nguk02')
print "=========================================================================="
print "\n\n"

print "=======================  resize ZFS  ===================================="
print p.resize_zfs('vstorage/zvol01','3G')
print "=========================================================================="
print "\n\n"

print "======================= destroy ZFS  ===================================="
print p.destroy_zfs('vstorage/centos02')
print p.destroy_zfs('vstorage/zvol01')
print "=========================================================================="
print "\n\n"

print "======================= send ZFS  ===================================="
print p.send_zfs('vstorage/centos01@01','/tmp/01.img')
print "=========================================================================="
print "\n\n"

print "======================= receive ZFS  ===================================="
print p.receive_zfs('/tmp/01.img','vstorage/centos03')
print "=========================================================================="
print "\n\n"

print "======================= snapshot ZFS  ===================================="
print p.snapshot_zfs('vstorage/centos01','datapenting')
print "=========================================================================="
print "\n\n"

print "=======================  clone ZFS  ===================================="
print p.clone_zfs('vstorage/centos01@datapenting','vstorage/datapenting')
print "=========================================================================="
print "\n\n"

