from nicegui import ui
import plotly.express as px
#*------------CustomModule------------*
from .global_com import add_rwd_div
from backend import PlotlyObj

def add_track_card(card_title: str) -> None:
    with add_rwd_div():
        with ui.card().classes('row q-mx-sm w-full background="grey-12" q-px-none').style('width: 1471.2px;'):
            # with ui.card_section().classes('q-py-sm'):
            with ui.element('div').classes('w-full'):
                with ui.tabs().classes('q-mr-md').props('dense align="left" narrow-indicator no-caps inline-label') as tabs:
                    with ui.element('div').classes('row items-center q-ma-none q-gutter-x-md q-pl-md'):
                        ui.icon('troubleshoot').classes('text-h5')
                        ui.label(card_title).classes('text-lg text-weight-bolder')
                        ui.badge('test')
                    ui.element('q-space')
                    progress_track_pannel = ui.tab(name='Progress Track', icon='description')
                    scalar_track_pannel = ui.tab(name='Scalar Track', icon="timeline").classes('')
                # ui.separator()
            def add_tab_head(title: str, icon: str, badge_list: list):
                with ui.element('div').classes('row w-full items-center q-gutter-x-md q-mb-md'):
                    ui.icon(icon).classes('text-h4')
                    ui.label(title).classes('text-h5')
                    for each_badge in badge_list:
                        if type(each_badge) == tuple:
                            with ui.badge(color=each_badge[2]):
                                ui.icon(each_badge[1]).classes('q-mr-xs')
                                ui.label(each_badge[0])
                ui.separator()
                    
            with ui.element('div').classes('w-full q-px-md'):
                with ui.tab_panels(tabs, value=scalar_track_pannel).classes('w-full'):
                    with ui.tab_panel(progress_track_pannel):
                        with ui.scroll_area().style('height: 740px;'):
                            with ui.element('div').classes('q-py-none q-gutter-y-md'):
                                add_tab_head(title='Progress Track', icon='description', badge_list=[])
                                add_track_line_progress()
                                add_track_circular_progress()
                                add_stepper_card()
                    with ui.tab_panel(scalar_track_pannel):
                        with ui.scroll_area().style('height: 740px;'):
                            with ui.element('div').classes('q-py-none q-gutter-y-md'):
                                add_tab_head(title='Scalar Track', icon='timeline', badge_list=[('Directory', 'folder', 'amber-14')])
                                add_scalar_track()


#! WARINING! this function only used for test!
# TODO: Remove this function!
def add_text_track(text: str, icon: str = 'analytics', with_back_sep: bool = True):
    ui.icon(icon).classes('text-amber-14 text-xl')
    ui.label(f'{text}:').classes('text-amber-14 text-weight-bold text-md')
    track_text = ui.label('-- : -- : --').classes('text-grey-9 text-weight-medium text-md')
    if with_back_sep:
        ui.separator().props('vertical')
    return track_text

#! WARINING! this function only used for test!
# TODO: Remove this function!
def add_track_line_progress():
    with ui.element('div').classes('row w-full'):
        with ui.card().props('flat bordered').classes('w-full q-px-none q-pt-none'):
            with ui.element('div').classes('row w-full'):
                ui.button(text='TrackItemName', icon="track_changes").props('flat no-caps text-xl')
                ui.element('q-space')
                ui.spinner(type='hourglass', size='1.5rem', color='orange-14').classes('q-ma-sm')
                ui.separator().classes('q-ma-none')
            with ui.element('div').classes('w-full q-px-md q-gutter-y-md'):
                with ui.linear_progress().props('stripe rounded') as p_bar:
                    with ui.element('div').classes('absolute-full flex flex-center'):
                        ui.badge(color='white', text_color='green-14', text='50%').bind_text_from(p_bar, 'value', lambda x: f'{round(x * 100, 2)}%')
                with ui.element('q-banner').classes('bg-grey-3 q-pa-md').props('rounded'):
                    with ui.element('div').classes('row items-center q-gutter-sm q-mb-md'):
                        add_text_track(text='IterRound', icon='task_alt')
                        add_text_track(text='TimeUsage', icon='timer')
                        add_text_track(text='TimeLeft', icon='schedule')
                        add_text_track(text='Speed', icon='speed', with_back_sep=False)
                        ui.element('q-space')
                        ui.spinner(type='bars', size='1.5rem', color='amber-14')
                    ui.separator().classes('q-mb-md')
                    with ui.element('div').classes('row items-center q-gutter-sm'):
                        # ui.icon('timer').classes('text-amber-14 text-xl')
                        add_text_track(text='SelfTrack') 

#! WARINING! this function only used for test!
# TODO: Remove this function!
def add_track_circular_progress():
    with ui.element('div').classes('row w-full'):
        with ui.card().props('flat bordered').classes('w-full q-px-none q-pt-none'):
            with ui.element('div').classes('row w-full'):
                ui.button(text='TrackItemName', icon="track_changes").props('flat no-caps text-xl')
                ui.element('q-space')
                ui.spinner(type='ball', size='1.5rem', color='orange-14').classes('q-ma-sm')
                ui.separator().classes('q-ma-none')
            with ui.element('div').classes('row w-full q-py-md q-px-md q-gutter-y-md'):
                with ui.element('div').classes('col-14'):
                    ui.circular_progress(size='128px').props('rounded indeterminate')
                with ui.element('div').classes('col'):
                    with ui.element('q-banner').classes('bg-grey-3 q-ml-lg h-full').props('rounded'):
                        with ui.element('div').classes('row items-center q-gutter-sm q-mb-md'):
                            add_text_track(text='IterRound', icon='task_alt')
                            add_text_track(text='TimeUsage', icon='timer')
                            add_text_track(text='TimeLeft', icon='schedule')
                            add_text_track(text='Speed', icon='speed', with_back_sep=False)
                            ui.element('q-space')
                            ui.spinner(type='bars', size='1.5rem', color='amber-14')
                        ui.separator().classes('q-mb-md')
                        with ui.element('div').classes('row items-center q-gutter-sm'):
                            # ui.icon('timer').classes('text-amber-14 text-xl')
                            add_text_track(text='SelfTrack') 

#! WARINING! this function only used for test!
# TODO: Remove this function!             
def add_stepper_card():
    with ui.element('div').classes('row w-full'):
        with ui.card().props('flat bordered').classes('w-full q-px-none q-py-none q-gutter-y-none').style('border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;'):
            with ui.element('div').classes('row w-full'):
                ui.button(text='Global Step Track', icon="track_changes").props('flat no-caps text-xl')
                ui.element('q-space')
                ui.spinner(type='clock', size='1.5rem', color='orange-14').classes('q-ma-sm')
        with ui.stepper().props('animated flat bordered').classes('w-full q-mt-none').style('border-top-width: 0px; border-top-right-radius: 0px; border-top-left-radius: 0px;') as stepper:
            with ui.step(name='First Step'):
                ui.label('Preheat the oven to 350 degrees')
            ui.step(name='Second Step')
            ui.step(name='Third Step')
            
#! WARINING! this function only used for test!
# TODO: Remove this function!
def add_scalar_track():
    # Initialize the ployly control object
    # TODO: Remove this currently data read field!
    from backend.event_processing.tf_events_converter import parse_tfevents_file
    from backend.event_processing.event_handler import get_scalars_groups, get_scalars_data

    parsed_data = parse_tfevents_file(file_path='events.out.tfevents.1680438328.ubuntu.741332.0')
    scalars_groups = get_scalars_groups(parsed_data)
    scalars_data = get_scalars_data(parsed_data, scalars_groups[0])
    plotly_obj = PlotlyObj(plotly_type='line', title=scalars_groups[0], data=scalars_data, default_fields={'x': 'step', 'y': 'value'})
    
    
    # Select component
    def add_dense_select(name : str, icon: str, options: list, default_value: str, on_change: any = None):
        selector = ui.select(options=options, label=name, value=default_value, on_change=on_change).props('outlined dense options-dense')
        with selector.add_slot('before'):
            ui.icon(name=icon, color='grey-14')
        return selector
    # Left pannel layout
    def add_left_pannel():
        available_templates = plotly_obj.get_available_templates()
        current_templates = plotly_obj.get_current_templates()
        available_colorscale = plotly_obj.get_available_colorscale()
        current_colorscale = plotly_obj.get_current_colorscale()
        with ui.element('q-list').classes('q-gutter-y-md'):
            # Graph style control
            with ui.element('div').classes('row items-center'):
                ui.label('STYLE').classes('text-grey-8 text-weight-medium')
                ui.element('q-space')
                with ui.button(icon='question_mark', color='grey-14').props('unelevated round size="xs"'):
                    ui.tooltip('need helps?').props('anchor="top middle" self="bottom middle"')
                    with ui.menu().props('anchor="bottom middle" self="top middle"') as menu:
                        ui.menu_item('About plotly templates', lambda: ui.open('https://plotly.com/python/templates/')).props('dense')
                        ui.menu_item('About builtin-colorscales', lambda: ui.open('https://plotly.com/python/builtin-colorscales/')).props('dense')
            style_select = add_dense_select(name='Style Template', icon='edit_square', options=available_templates, default_value=current_templates)
            color_select = add_dense_select(name='Color Scale', icon='palette', options=available_colorscale, default_value=current_colorscale)
            
            # style_select.on_value_change(lambda obj=plotly_obj: obj.set_templates(style_select.value))
            style_select.on('update:model-value', lambda obj=plotly_obj: obj.set_templates(style_select.value))
            color_select.on('update:model-value', lambda obj=plotly_obj: obj.set_colorscale(color_select.value))
            ui.separator()
            # Running data control
            ui.label('RUNS').classes('text-grey-8 text-weight-medium')
            
            with ui.input(placeholder='Write a regex to filter runs').props('dense outlined').classes('col').add_slot('after'):
                with ui.button(icon='send', color='grey-14').props('round dense flat'):
                    ui.tooltip(text='run regex filter')
            columns = [# {'name': 'class', 'label': 'Class', 'field': 'class', 'required': True, 'align': 'left', 'sortable': True},
                       {'name': 'label', 'label': 'Label', 'field': 'label', 'align': 'left', 'sortable': True},
                       {'name': 'color', 'label': 'Color', 'field': 'color', 'align': 'left', 'sortable': True}]
            data_source_list = ui.table(columns=columns, rows=[], row_key='class', selection='multiple').props('flat bordered dense virtual-scroll')
            
    # Middle pannel layout
    def add_mid_pannel():
        plotly_obj.get_plotly_ui()
        
        
    # Right pannel layout
    def add_right_pannel():
        # ui.label('come soon')
        
        with ui.element('q-list').classes('q-gutter-y-md'):
            # General pannel
            with ui.element('div').classes('row items-center'):
                ui.label('GENERAL').classes('text-grey-8 text-weight-medium w-full q-mb-xs')
                # Horizontal Axis
                axis_options = ['Step', 'Relative', 'Wall']
                ui.label('Horizontal Axis').classes('text-grey-6 w-full q-mb-sm')
                ui.select(options=axis_options, value='Step').props('dense outlined options-dense').classes('w-full q-mb-sm')
                # Refreshing interval
                ui.label('Refresh Interval').classes('text-grey-6 w-full q-mb-sm')
                with ui.number(min=2.0, step=0.1, suffix='seconds', format='%.01f', value=2.0).props('dense outlined label-slot').classes('w-full').add_slot('label'):
                    with ui.element('div').classes('row items-center all-pointer-events'):
                        ui.icon('update').classes('q-mr-xs')
                        ui.label('No less than 2s')
            ui.separator()
            
            # Scalar pannel
            with ui.element('div').classes('row items-center'):
                ui.label('SCALARS').classes('text-grey-8 text-weight-medium w-full q-mb-xs')
                # Smoothing control
                ui.label('Smoothing').classes('text-grey-6 w-full q-mb-sm')
                with ui.element('div').classes('row w-full items-center q-mb-md'):
                    smooth_slider = ui.slider(min=0, max=0.99, step=0.01, value=0.00).props('label switch-label-side').classes('col q-mr-sm')
                    smooth_input = ui.number(max=0.99, min=0.00, step=0.01, format='%.2f').props('dense outlined').classes('col-4 text-xs')
                    smooth_slider.bind_value_to(smooth_input)
                    smooth_slider.bind_value_from(smooth_input)
                # Y-axis scale
                ui.label('Y-axis scale').classes('text-grey-6 w-full q-mb-sm')
                with ui.element('div').classes('row w-full items-center q-mb-sm'):
                    ui.number().props('dense outlined').classes('col')
                    ui.label('-').classes('q-mx-sm')
                    ui.number().props('dense outlined').classes('col')
                ui.button('Set Axis').props('dense unelevated').classes('w-full q-mb-md')   
                # Ignore outliers
                ui.checkbox(text='Ignore outliers in chart scaling').classes('text-grey-6 text-xs q-mb-sm').props('dense')
                # Partion non-monotonic X axis
                ui.checkbox(text='Partion non-monotonic X axis').classes('text-grey-6 text-xs q-mb-sm').props('dense')
                # Show scalar markers in graph
                ui.checkbox(text='Show scalar markers').classes('text-grey-6 text-xs').props('dense')
            ui.separator()
            
            # Download pannel
            with ui.element('div').classes('row items-center'):
                ui.label('OTHER').classes('text-grey-8 text-weight-medium w-full q-mb-xs')
                # Export graph
                support_format = plotly_obj.get_available_export_format()
                ui.label('File Export').classes('text-grey-6 w-full q-mb-sm')
                with ui.select(label='export as', options=support_format, multiple=True, value=support_format[0]).classes('w-full text-xs q-mb-sm').props('outlined dense options-dense use-chips stack-label').add_slot('before') as selector:
                    ui.icon('image')
                ui.button('Export as image').props('dense unelevated').classes('w-full q-mb-md')              
    # Card layout
    with ui.element('q-list').classes('w-full rounded-borders').props('bordered'):
        with ui.expansion('Card Name', icon='multiline_chart', value=True).classes('w-full overflow-hidden'):
            with ui.element('div').classes('row no-wrap w-full h-full q-px-none q-ma-none'):
                with ui.element('div').classes('col-2 q-ma-none q-pa-md'):
                    add_left_pannel()
                ui.separator().props('vertical')
                with ui.element('div').classes('col q-ma-none q-pa-md'):
                    add_mid_pannel()
                ui.separator().props('vertical')
                with ui.element('div').classes('col-2 q-ma-none q-pa-md'):
                    add_right_pannel()