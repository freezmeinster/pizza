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
                )
        return result
    
    
    
    def __get_capacity(self,datasheet,unit):
        used = execute_task(
            ["zfs", "list", "-Hp" ,"-o", "used" ,datasheet],
            with_return=True,
            return_type="value"
        )
        
        free = execute_task(
            ["zfs", "list", "-Hp", "-o", "available" ,datasheet],
            with_return=True,
            return_type="value"
        )
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
        )
        if pool == raw :
            return []
        else :
            del raw[0]
            return raw
    
    def __get_datasheet_attribute(self,datasheet,attribute,unit):
        if attribute == 'all' :
            result = {}
            cmd = execute_task(
                ['zfs', 'get', '-Hp', 'all', '-o', 'property,value' ,datasheet],
                with_return=True,
            )
            for line in cmd :
                item = line.split("\t")
                if item[1].isdigit() :
                    value = convert_byte(int(item[1]),unit)
                elif item[1] == "-":
                    value = None
                else :
                    value = item[1]
                result[item[0]] = value
            return result
        else :
            cmd = execute_task(
                ['zfs', 'get', '-Hp', attribute, '-o', 'property,value' ,datasheet],
                with_return=True,
                return_type="value"
            )
            item = cmd.split("\t")
            if item[1].isdigit() :
                value = convert_byte(int(item[1]),unit)
            elif item[1] == "-":
                value = None
            else :
                value = item[1]
            return { item[0]: value}
    
    
    def __check_datasheet(self,pool,datasheet):
        list_datasheet = self.__get_datasheet(pool)
        if datasheet not in list_datasheet :
            return False
        else :
            return True
    
    def list_pool(self,detail=False,unit="gb"):
        """Return information about pool
        
        Keyword arguments :
        detail -- detail output with capacity and datasheet list ( default True)
        unit   -- return will formated in: kb,mb,gb (default kb)
        """
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
    
    def get_datasheet(self,pool):
        """Return list of datasheet in a pool
        
        Arguments :
        pool  --  Pool name
        """
        return self.__get_datasheet(pool)
    
    def get_datasheet_attribute(self,datasheet,attribute="all",unit="kb"):
        """Return information about attribute of datasheet
        
        Arguments :
        datasheet  -- datasheet you want
        
        Keyword arguments :
        attribute  -- test
        unit       -- test
        """
        return self.__get_datasheet_attribute(datasheet,attribute,unit)
    
    def create_datasheet(self,pool,name,attribute=None):
        if self.__check_datasheet(pool,name):
            print "udah ada"
        else :
            if attribute :
                args = ""
                for item in attribute :
                    args += "%s=%s" %(item,arg.get(item))
                args = args[:-1]
    
    def create_zvol(self,pool,name,capacity,attribute=None):
        pass
    
    def alter_datasheet_attribute(self,name,attribute,value):
        pass
    
    def alter_zvol_attribute(self,name,attribute,value):
        pass