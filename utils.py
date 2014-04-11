import subprocess

split = {
    "tab" : "\t",
    "new_line" : "\n",
    "space" : " "
}

def execute_task(task,with_return=False,spliter="space",field=None):
    if with_return:
        result = subprocess.check_output(task)
        if field :
            return result.split(split.get(spliter))[field]
        else :
            return result.split(split.get(spliter))
    else :
        return subprocess.call(task)

def convert_byte(value,to="kb"):
    if to == "kb" :
        return int(value) / 1024
    elif to == 'mb' :
        return int(value) / (1024*1024)
    elif to == 'gb' :
        return int(value) / (1024*1024*1024)
