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

print "======================= zfs datasheet test=========================="
print p.get_datasheet("tank")
print "=========================================================================="
print "\n\n"

print "======================= datasheet attribute test=========================="
print p.get_datasheet_attribute("tank/test",attribute="mountpoint")
print "=========================================================================="
print "\n\n"