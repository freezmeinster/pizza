import subprocess


def execute_task(task,with_return=False,return_type="list",output=None,input=None):
    if with_return:
        result = subprocess.check_output(task).splitlines()
        if return_type == "list" :
            return result
        else :
            return result[0]
    else :
        if output:
            io_file = open(output,'wb')
            subprocess.call(task,stdout=io_file)
            io_file.close()
        elif input :
            io_file = open(input,'rb')
            subprocess.call(task,stdin=io_file)
            io_file.close()
        else :
            subprocess.call(task)
            return True

def convert_byte(value,to="kb"):
    if to == "kb" :
        return int(value) / 1024
    elif to == 'mb' :
        return int(value) / (1024*1024)
    elif to == 'gb' :
        return int(value) / (1024*1024*1024)
