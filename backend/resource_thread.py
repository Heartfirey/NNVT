import time
from threading import Thread
#*------------CustomModule------------*
from . import resource_monitor

def add_obj_indeterminate(cpu_obj, mem_obj, gpu_obj):
    pass

def remove_obj_indeterminate(cpu_obj, mem_obj, gpu_obj):
    pass

def cpu_obj_refresh(cpu_obj: dict):
    def color_rule(value) -> str:
        if value > 75: return 'negative'
        elif value > 50: return 'warning'
        else: return 'positive'
    # Get current state
    cpu_states = resource_monitor.get_cpu_states()
    tot_percentage = cpu_states['cpu_percentage_tot']
    # Refresh total rate
    cpu_obj['tot'].set_value(round(tot_percentage / 100, 2))
    cpu_obj['tot'].props(add=f'color="{color_rule(value=tot_percentage)}"', remove='color')
    # Refresh all core
    for core_id in range(cpu_states['cpu_count']):
        current_core_percentage = cpu_states['cpu_percentage_pc'][core_id]
        cpu_obj['core'][core_id].set_value(current_core_percentage)
        cpu_obj['core'][core_id].props(add=f'color={color_rule(value=current_core_percentage)}', remove='color')
        
def gpu_obj_refresh(gpu_obj):
    def util_color_rule(value) -> str:
        if value > 75: return 'negative'
        elif value > 50: return 'warning'
        else: return 'positive'
    def mem_color_rule(value) -> str:
        if value > 85: return 'negative'
        elif value > 60: return 'warning'
        else: return 'positive'
    def temperature_color_rule(value) -> str:
        if value > 75: return 'negative'
        elif value > 55: return 'warning'
        else: return 'positive'
    def power_color_rule(value, tot) -> str:
        if value > tot * 0.85: return 'negative'
        elif value > tot * 0.6: return 'warning'
        else: return 'positive'
    gpu_states = resource_monitor.get_gpu_states()
    for each_gpu_id in range(len(gpu_states)):
        cur_gpu_obj = gpu_obj[f'gpu_{each_gpu_id}']
        cur_gpu_states = gpu_states[each_gpu_id]
        # Refresh util bar
        cur_gpu_obj['util_bar'].set_value(round(cur_gpu_states['util_cal_rate'] / 100, 2))
        cur_gpu_obj['util_bar'].props(add=f"color={util_color_rule(value=cur_gpu_states['util_cal_rate'])}", remove='color')
        # Refresh memory bar
        cur_mem_rate = cur_gpu_states['mem_use_kb'] / cur_gpu_states['mem_tot_kb']
        cur_gpu_obj['mem_bar'].set_value(round(cur_mem_rate, 2))
        cur_gpu_obj['mem_bar'].props(add=f"color={mem_color_rule(value=cur_mem_rate * 100)}", remove='color')
        # Refresh memory info label
        cur_gpu_obj['mem_label'].set_text(f"{cur_gpu_states['mem_use_mb']}MB (Used) / {cur_gpu_states['mem_free_mb']}MB (Free) / {cur_gpu_states['mem_tot_mb']}MB (Total)")
        # Refresh util memory io rate
        cur_gpu_obj['util_mem'].set_value(cur_gpu_states['util_mem_rate'])
        cur_gpu_obj['util_mem'].props(add=f"color={mem_color_rule(value=cur_gpu_states['util_mem_rate'])}", remove='color')
        # Refresh temperature
        cur_gpu_obj['temperature'].set_value(cur_gpu_states['temperature'])
        cur_gpu_obj['temperature'].props(add=f"color={temperature_color_rule(value=cur_gpu_states['temperature'])}", remove='color')
        # Refresh power state
        cur_power_state = (cur_gpu_states['power_state'] // 1000)
        tot_power_limit = (cur_gpu_states['power_limit'] // 1000)
        cur_gpu_obj['power'].set_value(cur_power_state)
        cur_gpu_obj['power'].props(add=f"color={power_color_rule(value=cur_power_state, tot=tot_power_limit)}", remove='color')
        # Refresh processes table
        # cur_gpu_obj['proc_rows'] = resource_monitor.get_gpu_process(gpu_id=each_gpu_id)
        
        # cur_gpu_obj['proc_watcher'].update()
        cur_gpu_obj['proc_watcher'].clear()
        cur_proc_list = resource_monitor.get_gpu_process(gpu_id=each_gpu_id)
        for each_proc in cur_proc_list:
            cur_gpu_obj['proc_watcher'].add_rows(each_proc)
        # cur_gpu_obj['proc_watcher'].add_rows(resource_monitor.get_gpu_process(gpu_id=each_gpu_id))
        # print(resource_monitor.get_gpu_process(gpu_id=each_gpu_id))
        
        
def memory_obj_refresh(mem_obj: str):
    def color_rule(value) -> str:
        if value > 85: return 'negative'
        elif value > 60: return 'warning'
        else: return 'positive'
    # Get current state
    mem_states = resource_monitor.get_mem_states()
    mem_usage_rate = mem_states['mem_percent']
    swap_usage_rate = mem_states['swap_percent']
    # Refresh physical memory
    mem_obj['mem_bar'].set_value(round(mem_usage_rate / 100, 2))
    mem_obj['mem_bar'].props(add=f'color="{color_rule(value=mem_usage_rate)}"', remove='color')
    mem_obj['mem_info']['total'].set_text(f"{round(mem_states['mem_total_mb'] / 1024, 2)}GB")
    mem_obj['mem_info']['used'].set_text(f"{round(mem_states['mem_used_mb'] / 1024, 2)}GB")
    mem_obj['mem_info']['free'].set_text(f"{round(mem_states['mem_free_mb'] / 1024, 2)}GB")
    # Refresh swap memory
    mem_obj['swap_bar'].set_value(round(swap_usage_rate / 100, 2))
    mem_obj['swap_bar'].props(add=f'color="{color_rule(value=swap_usage_rate)}"', remove='color')
    mem_obj['swap_info']['total'].set_text(f"{round(mem_states['swap_total_mb'] / 1024, 2)}GB")
    mem_obj['swap_info']['used'].set_text(f"{round(mem_states['swap_used_mb'] / 1024, 2)}GB")
    mem_obj['swap_info']['free'].set_text(f"{round(mem_states['swap_free_mb'] / 1024, 2)}GB")
    
class ResourceWatcher(Thread):
    def __init__(self, cpu_obj: dict, mem_obj: dict, gpu_obj: dict):
        super().__init__()
        self.cpu_obj = cpu_obj
        self.mem_obj = mem_obj
        self.gpu_obj = gpu_obj
    def run(self, ):
        while True:
            cpu_obj_refresh(self.cpu_obj)
            memory_obj_refresh(self.mem_obj)
            gpu_obj_refresh(self.gpu_obj)
            time.sleep(1)