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
        
    def list_pool(self,detail=False,unit="gb"):
        if detail :
            list_pool = self.__list_pool()
            result = {}
            for pool in list_pool:
                result[pool] = {
                    'capacity' : self.__get_capacity(pool,unit),
                    'datasheet' : self.__get_datasheet(pool)
                }
            return result
            
        else :
            return self.__list_pool()
    
    def __get_capacity(self,datasheet,unit):
        used = execute_task(
            ["zfs", "list", "-Hp" ,"-o", "used" ,datasheet],
            with_return=True,
        ).pop()
        
        free = execute_task(
            ["zfs", "list", "-Hp", "-o", "available" ,datasheet],
            with_return=True,
        ).pop()
        
        result = {
            'used' : convert_byte(used,unit),
            'free' : convert_byte(free,unit),
            'total' : convert_byte(used,unit) +
                      convert_byte(free,unit)
        }
        return result
    
    def __get_datasheet(self,pool):
        result = {}
        raw = execute_task(
            ['zfs', 'list','-Hp', '-o' ,'name' ,'-r', pool],
            with_return=True,
            spliter="new_line"
        )
        del raw[0]
        del raw[-1]
        return raw
    
    def __get_datasheet_attribute(self,datasheet,atrribute=all):
        pass
