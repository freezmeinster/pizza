import platform
from utils import convert_byte, execute_task

class Pizza(object):

    def __init__(self):
        if platform.system() != "Linux":
            print "sorry, for now we only support ZFS on Linux"
            exit()
        else :
            pass

    def __list_pool(self):
        result = execute_task(
                    ['zpool','list','-Ho','name'],
                    with_return=True,
                    spliter="new_line"
                )
        result.pop()
        return result

    def list_pool(self,detail=False,unit="kb"):
        if detail :
            list_pool = self.__list_pool()
            result = {}
            for pool in list_pool:
                result[pool] = self.__get_capacity(pool,unit)
            return result
            
        else :
            return self.__list_pool()
    
    def __get_capacity(self,pool,unit):
        used = execute_task(
            ["zfs", "list", "-Hp -o", "used" ,pool],
            with_return=True,
        )
        
        free = execute_task(
            ["zfs", "list", "-Hp -o", "available" ,pool],
            with_return=True,
        )
        
        resutl = {
            'used' : convert_byte(used,unit),
            'free' : convert_byte(free,unit),
            'total' : convert_byte(used,unit) +
                      convert_byte(free,unit)
        }
        return result
        
