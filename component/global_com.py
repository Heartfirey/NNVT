from nicegui import ui
from pathlib import Path
from typing import Awaitable, Callable, Optional
#*------------CustomModule------------*

def add_head_html() -> None:
    ui.add_head_html((Path(__file__).parent.parent / 'static' / 'header.html').read_text())
    ui.add_head_html(f"<style>{(Path(__file__).parent.parent / 'static' / 'style.css').read_text()}</style>")

def add_header(menu: Optional[ui.left_drawer] = None) -> None:
    menu_items = {
        'Installation': '/#installation',
        'Features': '/#features',
    }
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        if menu:
            ui.button(on_click=menu.toggle, icon='menu').props('flat color=white round')

        with ui.element('div').classes('nicegui-link row gap-4 items-center no-wrap mr-auto'):
            with ui.element('div').classes('w-8 stroke-white stroke-2 max-[550px]:hidden'):
                ui.icon('hub', color='white').classes('text-3xl')
            ui.label('Neural Network Training Toolbox').classes('text-2xl')
        
        with ui.row().classes('max-[1050px]:hidden'):
            for title, target in menu_items.items():
                ui.link(title, target).classes(replace='text-lg text-white')

        with ui.row().classes('min-[1051px]:hidden'):
            with ui.button(icon='more_vert').props('flat color=white round'):
                with ui.menu().classes('bg-primary text-white text-lg'):
                    for title, target in menu_items.items():
                        ui.menu_item(title, on_click=lambda target=target: ui.open(target))
                        
def add_drawer() -> None:
    drawer_items = {
        'DashBoard': ('dashboard', '/'),
        'sepline': (),
        'Models': ('model_training', '/models'),
        'Schedule': ('edit_calendar', 'link3'),
    }
    miniState = True
    def toggle_miniState(miniState):
        miniState = not miniState
        return miniState
    with ui.left_drawer().props(f'show-if-above :mini=True bordered :width="200" :breakpoint="1600"').classes('q-pa-none') as drawer:
        drawer.on('mouseover', lambda obj=drawer: obj.props(remove=':mini=True'))
        with ui.scroll_area().classes('fit'):
            with ui.element('q-list').props('padding').classes('menu-list'):
                for item_text, props in drawer_items.items():
                    if item_text == "sepline":
                        ui.element('q-separator')
                    else:
                        with ui.menu_item(on_click=lambda target=props[1]: ui.open(target)):
                            with ui.element('q-item-section').props('avatar'):
                                ui.icon(name=props[0])
                            with ui.element('q-item-section'):
                                ui.label(text=item_text)
        with ui.element('div').classes('q-mini-drawer-hide absolute').style('top: 15px; right: -17px'):
            ui.button(on_click=lambda obj=drawer: obj.props(add=':mini=True')).props('dense round unelevated color="accent" icon="chevron_left"')
    return drawer

def add_basic_layout() -> None:
    add_head_html()
    drawer = add_drawer()
    add_header(drawer)
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')

def add_rwd_div():
    div_box = ui.element('div').classes('row w-full flex-center q-px-none')
    return div_box

def add_page_head_card(icon_name, title_text):
    with add_rwd_div():
        with ui.card().classes('row q-mx-sm w-full background="grey-12"').style('width: 1471.2px;'):
            with ui.element('div').classes('row w-full items-center q-ma-md'):
                ui.icon(f'{icon_name}').classes('text-h3 q-mr-md')
                ui.label(f'{title_text}').classes('text-h4')

