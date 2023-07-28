from nicegui import ui
#*------------CustomModule------------*
from component import add_basic_layout

@ui.page('/models')
def models_page() -> None:
    add_basic_layout()
    ui.label('Just for test')