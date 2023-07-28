from nicegui import ui
from backend import resource_monitor
from backend import resource_thread

def add_resource_card():
    with ui.element('div').classes('row q-gutter-md'):
        with ui.element('div').classes('col'):
            cpu_obj = add_cpu_card()
        with ui.element('div').classes('col'):
            mem_obj = add_mem_card()
        with ui.element('div').classes('col'):
            gpu_obj = add_gpu_card()
    watcher_thread_test = resource_thread.ResourceWatcher(cpu_obj=cpu_obj, mem_obj=mem_obj, gpu_obj=gpu_obj)
    watcher_thread_test.setDaemon(True)
    watcher_thread_test.start()
        

def add_cpu_card() -> dict:
    # CPU Info Table
    cpu_info = resource_monitor.get_cpu_info()
    cpu_card_columns = [{'name': 'properties', 'label': 'Properties', 'field': 'properties', 'align': 'left'}, 
                        {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'left'}]
    cpu_card_rows = [{'properties': 'Architecture', 'value': cpu_info['arch']}, 
                     {'properties': 'Platform', 'value': cpu_info['details']}, 
                     {'properties': 'Core Nums', 'value': cpu_info['cpu_count']}]
    cpu_obj = dict()
    cpu_core_rate_list = list()
    # Single Core Monitor
    def add_cpu_core(core_id):
        with ui.element('div').classes('col-md q-gutter-y-sm'):
            with ui.element('div').classes('row flex-center'):
                progress = ui.circular_progress(size='xl', min=0, max=100, value=50).props('rounded')
            with ui.element('div').classes('row flex-center'):
                ui.badge(f'Core #{core_id}')
        return progress
    with ui.card().classes('max-w-lg h-full').style('width: 30rem;'):
        with ui.card_section():
            ui.label('CPU States Monitor').classes('col text-lg text-weight-bolder')
        with ui.scroll_area().style('height: 494px;'):
            with ui.card().classes('q-pa-none'):
                for core_row in range(cpu_info['cpu_count'] // 4):
                    with ui.element('div').classes('row w-full').style('min-width: 28rem;'):
                        for i in range(4):
                            cpu_core_rate_list.append(add_cpu_core(core_id=core_row * 4 + i))
                with ui.element('div').classes('w-full'):
                    with ui.linear_progress(value=0.5, color='green-14').props('stripe rounded') as tot_usage:
                        cpu_obj['tot'] = tot_usage
                        with ui.element('div').classes('absolute-full flex flex-center'):
                            ui.badge(color='white', text_color='green-14', text='NAN% (Total Usage)').bind_text_from(tot_usage, 'value', lambda x: f'{round(x * 100, 2)}% (Total Usage)')
                with ui.row().classes('w-full'):
                    ui.table(cpu_card_columns, cpu_card_rows).props('flat bordered').classes('w-full q-mb-sm')
    cpu_obj['core'] = cpu_core_rate_list
    return cpu_obj

def add_none_info(text: str, exp_msg: str):
    with ui.element('div').classes('column w-full h-full flex-center'):
        ui.icon('cancel', color='red').classes('col-5 text-9xl flex-center')
        ui.label(text).classes('col-2 flex-center text-xl')
        with ui.element('div').classes('col w-full'):     
            with ui.card().classes('flat w-full').props('flat bordered'):
                with ui.card().classes('w-full h-24 q-pa-xs').props('no-shadow'):
                    with ui.scroll_area():
                        ui.label(text=exp_msg)
                with ui.element('div').classes('h-4 w-full'): 
                    ui.badge(text="Exception Message", color='orange-14').classes('text-md').props('outline')
                    
def add_subgpu_card(gpu_id: int, gpu_info: dict) -> dict:
    subgpu_obj = dict()
    with ui.card().classes('w-full').props('flat bordered'):
        with ui.element('div').classes('h-4 w-full q-gutter-md q-mb-md'): 
            with ui.badge(text=f"GPU #{gpu_id}", color='blue-14').classes('text-md'):
                ui.icon(name='developer_board').classes('q-ml-sm')
            ui.badge(text=f"{gpu_info['gpu_name']}", color='deep-purple-14').classes('text-md').props('outline')
        def add_progress_bar(text: str):
            with ui.element('div').classes('row w-full'): 
                ui.label(text=text).classes('text-right col-2 q-mr-md')    
                with ui.linear_progress(value=0.5, color='green-14').classes('col').props('stripe rounded') as bar:
                    with ui.element('div').classes('absolute-full flex flex-center'):
                        ui.badge(color='white', text_color='green-14', text='50%').bind_text_from(bar, 'value', lambda x: f'{round(x * 100, 2)}%')
            return bar
        subgpu_obj['util_bar'] = add_progress_bar('GPU-Util')
        subgpu_obj['mem_bar'] = add_progress_bar('MemUsed')
        with ui.element('div').classes('row w-full flex-center'):
            with ui.element('q-chip').props('square'):
                ui.avatar(icon='memory', color='indigo-14', text_color="white", square=True, font_size='lg')
                subgpu_obj['mem_label'] = ui.label(f"{gpu_info['mem_use_mb']}MB (Used) / {gpu_info['mem_free_mb']}MB (Free) / {gpu_info['mem_tot_mb']}MB (Total)")
        def add_watcher(name: str, min_val: int = 0, max_val: int = 100, props: str = "rounded", init_val: int = 0):
            with ui.element('div').classes('col-md'):
                with ui.element('div').classes('row flex-center'):
                    progress = ui.circular_progress(size='xl', min=min_val, max=max_val, value=init_val).props(props)
                ui.label(name).classes('row flex-center').classes('q-mt-sm')
            return progress
        with ui.element('div').classes('row w-full'):
            subgpu_obj['util_mem'] = add_watcher('UtilMemoryIO')
            subgpu_obj['temperature'] = add_watcher('Tempature')
            subgpu_obj['power'] = add_watcher('PowerState', max_val=int(gpu_info['power_limit']//1000))
            subgpu_obj['fanspeed'] = add_watcher('FanSpeed', props="indeterminate", init_val=0)
            
        columns = [{'name': 'pid', 'label': 'PID', 'field': 'pid', 'required': True, 'align': 'left', 'sortable': True},
                   {'name': 'pname', 'label': 'ProcessName', 'field': 'pname', 'align': 'left', 'sortable': True},
                   {'name': 'memuse', 'label': 'GPUMemUsage', 'field': 'memuse', 'align': 'left', 'sortable': True}]
        with ui.row().classes('w-full'):
            subgpu_obj['proc_watcher'] = ui.table(title='GPU Compute Processes', columns=columns, rows=[] , row_key='memuse') \
                                            .props('flat bordered dense virtual-scroll').classes('w-full').style("height: 160px")
    
    return subgpu_obj  
        

def add_gpu_card():
    gpu_obj = dict()
    gpu_info = resource_monitor.get_gpu_info()
    with ui.card().classes('column max-w-lg h-full').style('width: 30rem;'):
        with ui.card_section():
            ui.label('GPU States Monitor (Nvidia)').classes('text-lg text-weight-bolder')
        if type(gpu_info) is tuple and gpu_info[0] is None:
            with ui.element('div').classes('col w-full h-auto'):
                add_none_info('GPU Monitor Loaded Failed!', gpu_info[-1])
        else: 
            with ui.element('div').classes('row w-full flex-center'):
                with ui.element('q-chip').props('square').classes('q-pl-none'):
                    with ui.element('q-chip').props('square color="teal-14" text-color="white"').classes('q-ml-none'):
                        ui.label(text="Driver")
                    ui.label(f"{gpu_info['driver']}").classes('q-ml-sm')
                with ui.element('q-chip').props('square').classes('q-pl-none'):
                    with ui.element('q-chip').props('square color="deep-purple-14" text-color="white"').classes('q-ml-none'):
                        ui.label(text="CUDA")
                    ui.label(f"{gpu_info['cuda']}").classes('q-ml-sm')
                with ui.element('q-chip').props('square').classes('q-pl-none'):
                    with ui.element('q-chip').props('square color="indigo-14" text-color="white"').classes('q-ml-none'):
                        ui.label(text="NVML")
                    ui.label(f"{gpu_info['nvml']}").classes('q-ml-sm')
            current_state = resource_monitor.get_gpu_states()
            with ui.scroll_area().style('height: 442px;'):
                for each_gpu_id in range(gpu_info['count']):
                    with ui.element('div').classes('col w-full'): 
                        gpu_obj[f'gpu_{each_gpu_id}'] = add_subgpu_card(each_gpu_id, current_state[0])
                    
    return gpu_obj               
            
def add_mem_card() -> dict:
    mem_obj = dict()
    with ui.card().classes('max-w-lg h-full').style('width: 30rem;'):
        with ui.card_section():
            ui.label('Memory States Monitor').classes('text-lg text-weight-bolder')
        # Progress Bar
        def add_progress_bar(text: str) -> dict:
            with ui.element('div').classes('row w-full'): 
                ui.label(text=text).classes('text-right text-no-wrap col-2 q-mr-md')    
                with ui.linear_progress(value=0.5, color='green-14').classes('col').props('stripe rounded') as bar:
                    with ui.element('div').classes('absolute-full flex flex-center'):
                        ui.badge(color='white', text_color='green-14', text='50%').bind_text_from(bar, 'value', lambda x: f'{round(x * 100, 2)}%')
            return bar
        # Memory data info badge
        def add_mem_info() -> dict:
            info_obj = dict()
            with ui.element('div').classes('row w-full flex-center q-gutter-xs'):
                with ui.element('q-chip').props('square').classes('q-pl-none').style('width: 128px;'):
                    with ui.element('q-chip').props('square color="cyan-14" text-color="white"').classes('q-ml-none'):
                        ui.label(text="Total")
                    info_obj['total'] = ui.label("NAN").classes('q-ml-xs')
                with ui.element('q-chip').props('square').classes('q-pl-none').style('width: 128px;'):
                    with ui.element('q-chip').props('square color="amber-10" text-color="white"').classes('q-ml-none'):
                        ui.label(text="Used")
                    info_obj['used'] = ui.label("NAN").classes('q-ml-xs')
                with ui.element('q-chip').props('square').classes('q-pl-none').style('width: 128px;'):
                    with ui.element('q-chip').props('square color="teal" text-color="white"').classes('q-ml-none'):
                        ui.label(text="Free")
                    info_obj['free'] = ui.label("NAN").classes('q-ml-xs')
            return info_obj
        with ui.scroll_area().style('height: 494px;'):
            with ui.element('div').classes('w-full q-mb-md'): 
                with ui.card().classes('w-full').props('flat bordered'):
                    with ui.element('div').classes('h-4 w-full q-gutter-md q-mb-md'): 
                        with ui.badge(text="Physical Memory", color='blue-14').classes('text-md'):
                            ui.icon(name='memory').classes('q-ml-sm')
                    mem_obj['mem_bar'] = add_progress_bar('Total Used')
                    mem_obj['mem_info'] = add_mem_info()

            with ui.element('div').classes('w-full'): 
                with ui.card().classes('w-full').props('flat bordered'):
                    with ui.element('div').classes('h-4 w-full q-gutter-md q-mb-md'): 
                        with ui.badge(text="Swap Memory", color='blue-14').classes('text-md'):
                            ui.icon(name='memory').classes('q-ml-sm')
                    mem_obj['swap_bar'] = add_progress_bar('Swap Used')
                    mem_obj['swap_info'] = add_mem_info()
    return mem_obj