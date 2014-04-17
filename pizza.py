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
    
    
    
    def __get_capacity(self,dataset,unit):
        if self.__get_dataset_attribute(
            dataset,attribute='type',unit=unit).get('type') == 'filesystem' :
            used = execute_task(
                ["zfs", "list", "-Hp" ,"-o", "used" ,dataset],
                with_return=True,
                return_type="value"
            )
            
            free = execute_task(
                ["zfs", "list", "-Hp", "-o", "available" ,dataset],
                with_return=True,
                return_type="value"
            )
            
            result = {
            'used' : convert_byte(used,unit),
            'free' : convert_byte(free,unit),
            'total' : convert_byte(used,unit) +
                      convert_byte(free,unit)
            }
        elif self.__get_dataset_attribute(
            dataset,attribute='type',unit=unit).get('type') == 'volume' :
            used = execute_task(
                ["zfs", "list", "-Hp" ,"-o", "usedbydataset" ,dataset],
                with_return=True,
                return_type="value"
            )
            
            total = execute_task(
                ["zfs", "list", "-Hp", "-o", "volsize" ,dataset],
                with_return=True,
                return_type="value"
            )
            result = {
                'used' : convert_byte(used,unit),
                'free' : convert_byte(total,unit) -
                         convert_byte(used,unit),
                'total' : convert_byte(total,unit)
            }
        else :
            result = {}
        return result
    
    def __get_dataset(self,pool):
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
    
    def __get_dataset_attribute(self,dataset,attribute,unit):
        if attribute == 'all' :
            result = {}
            cmd = execute_task(
                ['zfs', 'get', '-Hp', 'all', '-o', 'property,value' ,dataset],
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
                ['zfs', 'get', '-Hp', attribute, '-o', 'property,value' ,dataset],
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
    
    
    def __check_dataset(self,pool,dataset):
        list_dataset = self.__get_dataset(pool)
        dataset = "%s/%s" % (pool,dataset)
        if dataset not in list_dataset :
            return False
        else :
            return True
        
    def __alter_attribute(self,name,attribute,value):
        agr = "%s=%s" % (attribute,value)
        execute_task(
            ['zfs','set',agr, name]
        )
        
    def __destroy_zfs(self,name):
        execute_task(
            ['zfs','destroy', '-R', name]
        )
    
    def __send_zfs(self,dataset,target):
        zfs_type = self.__get_dataset_attribute(
            dataset,attribute='type',unit='kb').get('type')
        if zfs_type == 'snapshot' :
            execute_task(
               ['zfs','send',dataset],
               output=target
            )
        else :
            raise ValueError("Source not snapshot")
    
    def __receive_zfs(self,source,target):
        execute_task(
           ['zfs','receive','-F',target],
           input=source
        )
    
    def __snapshot_zfs(self,target,snapshot_name):
        execute_task(
            ['zfs','snapshot','%s@%s' % (target,snapshot_name)]
        )
    
    def __clone_zfs(self,zfs_source,target):
        execute_task(
            ['zfs','clone','-p',zfs_source, target]
        )
        
    def __resize_zfs(self,dataset,new_size):
        dataset_type = self.__get_dataset_attribute(
            dataset,attribute="type",unit='kb').get('type')
        if dataset_type == "volume" :
            execute_task(
                ['zfs','set','volsize=%s' % new_size,dataset]
            )
        elif dataset_type == "filesystem" :
            execute_task(
                ['zfs','set','quota=%' % new_size, dataset]
            )
    
    def list_pool(self,detail=False,unit="gb"):
        """Return information about pool
        
        Keyword arguments :
        detail -- detail output with capacity and dataset list ( default True)
        unit   -- return will formated in: kb,mb,gb (default kb)
        """
        if detail :
            list_pool = self.__list_pool()
            result = {}
            for pool in list_pool:
                result[pool] = {
                    'capacity' : self.__get_capacity(pool,unit),
                    'dataset' : self.__get_dataset(pool)
                }
            return result
            
        else :
            return self.__list_pool()
    
    def get_dataset(self,pool):
        """Return list of dataset in a pool
        
        Arguments :
        pool  --  Pool name
        """
        return self.__get_dataset(pool)
    
    def get_dataset_attribute(self,dataset,attribute="all",unit="kb"):
        """Return information about attribute of dataset
        
        Arguments :
        dataset  -- dataset you want
        
        Keyword arguments :
        attribute  -- test
        unit       -- test
        """
        return self.__get_dataset_attribute(dataset,attribute,unit)
    
    def create_dataset(self,pool,name,attribute=None):
        if self.__check_dataset(pool,name):
            raise ValueError("Dataset already exists")
        else :
            if attribute :
                task = ['zfs', 'create']
                for item in attribute :
                    task.append("-o")
                    task.append("%s=%s" %(item,attribute.get(item)))
                task.append('%s/%s' % (pool,name))
                execute_task(
                    task
                )
            else :
                execute_task(
                    ['zfs', 'create','%s/%s' % (pool,name)],
                )
        return "Dataset succesfuly created"
    
    def create_zvol(self,pool,name,capacity,attribute=None):
        if self.__check_dataset(pool,name):
            raise ValueError("Zvol already exists")
        else :
            if attribute :
                task = ['zfs', 'create' ,'-V', capacity]
                for item in attribute :
                    task.append("-o")
                    task.append("%s=%s" %(item,attribute.get(item)))
                task.append('%s/%s' % (pool,name))
                execute_task(
                    task
                )
            else :
                execute_task(
                    ['zfs', 'create','-V', capacity ,'%s/%s' % (pool,name)],
                )
        return "Zvol succesfuly created"
    
    def alter_dataset_attribute(self,name,attribute,value):    
        self.__alter_attribute(name,attribute,value)
        
    def alter_zvol_attribute(self,name,attribute,value):
        self.__alter_attribute(name,attribute,value)
        
    def destroy_zfs(self,name):
        self.__destroy_zfs(name)
        
    def send_zfs(self,dataset,target):
        self.__send_zfs(dataset,target)
    
    def receive_zfs(self,source,target):
        self.__receive_zfs(source,target)
        
    def resize_zfs(self,dataset,new_size):
        self.__resize_zfs(dataset,new_size)
    
    def snapshot_zfs(self,target,snapshot_name):
        self.__snapshot_zfs(target,snapshot_name)
    
    def clone_zfs(self,zfs_source,target):
        self.__clone_zfs(zfs_source,target)