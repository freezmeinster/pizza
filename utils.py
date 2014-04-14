import subprocess


def execute_task(task,with_return=False,return_type="list"):
    if with_return:
        result = subprocess.check_output(task).splitlines()
        if return_type == "list" :
            return result
        else :
            return result[0]
    else :
        return subprocess.call(task)

def convert_byte(value,to="kb"):
    if to == "kb" :
        return int(value) / 1024
    elif to == 'mb' :
        return int(value) / (1024*1024)
    elif to == 'gb' :
        return int(value) / (1024*1024*1024)
