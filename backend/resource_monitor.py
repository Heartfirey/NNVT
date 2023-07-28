import psutil
import platform
import pynvml


UNIT = 1024 * 1024

def unit_trans(origin, ufrom='KB', uto='MB', round=2):
    UNIT_LIST = { 'B': 1,'KB': 1024, 'MB': 1024 * 1024, 'GB': 1024 * 1024 * 1024}
    unit_origin = UNIT_LIST.get(ufrom, None)
    unit_trans = UNIT_LIST.get(uto, None)
    if unit_origin is None or unit_trans is None:
        raise ValueError('Unit Error! Got unexcepted unit! Unit only show be one of {B, KB, MB, GB}')
    unit_dis = unit_trans / unit_origin
    return origin * unit_dis
    
def get_cpu_states(sample_interval=1):
    cpu_states = {
        'cpu_count': psutil.cpu_count(),
        'cpu_percentage_tot': psutil.cpu_percent(interval=sample_interval, percpu=False),
        'cpu_percentage_pc': psutil.cpu_percent(interval=sample_interval, percpu=True),
    }
    return cpu_states

def get_cpu_info():
    cpu_info = {
        'arch': platform.machine(),
        'details': platform.processor(),
        'cpu_count': psutil.cpu_count(),
    }
    return cpu_info

def get_mem_states():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    mem_states = {
        'mem_total_mb': round(mem.total / UNIT, 2),
        'mem_used_mb': round(mem.used / UNIT, 2),
        'mem_free_mb': round(mem.free / UNIT, 2),
        'swap_total_mb': round(swap.total / UNIT, 2),
        'swap_used_mb': round(swap.used / UNIT, 2),
        'swap_free_mb': round(swap.free / UNIT, 2),
        'mem_percent': mem.percent,
        'swap_percent': swap.percent
    }
    return mem_states

def get_gpu_info():
    pynvml.nvmlInit()
    try:
        zero_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    except Exception as failed_expception:
        print(f'Unable to init pynvml module, got exception: {failed_expception}')
        return (None, str(failed_expception))
    gpu_info = {
        'driver': pynvml.nvmlSystemGetDriverVersion(),
        'cuda': pynvml.nvmlSystemGetCudaDriverVersion(),
        'nvml': pynvml.nvmlSystemGetNVMLVersion(),
        'count': pynvml.nvmlDeviceGetCount()
    }
    pynvml.nvmlShutdown()
    return gpu_info

def get_gpu_states():
    pynvml.nvmlInit()
    gpu_device_count = pynvml.nvmlDeviceGetCount()
    gpu_states = list()
    for gpu_index in range(gpu_device_count):
        current_handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
        gpu_name = pynvml.nvmlDeviceGetName(current_handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(current_handle)
        gpu_temperature = pynvml.nvmlDeviceGetTemperature(current_handle, 0)
        # gpu_fan_speed = pynvml.nvmlDeviceGetFanSpeed(current_handle)
        #### gpu_power_state = pynvml.nvmlDeviceGetPowerState(current_handle)
        gpu_power_limit = pynvml.nvmlDeviceGetPowerManagementLimit(current_handle)
        gpu_power_state = pynvml.nvmlDeviceGetPowerUsage(current_handle)
        gpu_util_info = pynvml.nvmlDeviceGetUtilizationRates(current_handle)
        gpu_states.append({
            'gpu_id': gpu_index,
            'gpu_name': gpu_name,
            'mem_tot_kb': memory_info.total,
            'mem_use_kb': memory_info.used,
            'mem_free_kb': memory_info.free,
            'mem_tot_mb': int(memory_info.total / UNIT),
            'mem_use_mb': int(memory_info.used / UNIT),
            'mem_free_mb': int(memory_info.free / UNIT),
            'mem_used_rate': memory_info.used / memory_info.total,
            'mem_free_rate': memory_info.free / memory_info.total,
            'util_cal_rate': gpu_util_info.gpu,
            'util_mem_rate': gpu_util_info.memory,
            'temperature': gpu_temperature,
            # 'fan_speed': gpu_fan_speed,
            'power_state': gpu_power_state,
            'power_limit': gpu_power_limit
        })
    pynvml.nvmlShutdown()
    return gpu_states

def get_gpu_process(gpu_id: int):
    pynvml.nvmlInit()
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    info_list = pynvml.nvmlDeviceGetComputeRunningProcesses(gpu_handle)
    p_row = list()
    for each_process in info_list:
        pid = each_process.__dict__['pid']
        process = psutil.Process(pid)
        p_row.append({'pid': pid, 'pname': process.name(), 'memuse': each_process.__dict__['usedGpuMemory'] if each_process.__dict__['usedGpuMemory'] is not None else "N/A"})
    pynvml.nvmlShutdown()
    return p_row
    
if __name__ == "__main__":
    # print(get_cpu_states())
    # print(get_cpu_info())
    # print(get_mem_states())
    # print(get_gpu_info())
    # print(get_gpu_states())
    print(get_gpu_process(0))
