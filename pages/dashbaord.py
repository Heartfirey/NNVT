from nicegui import ui
#*------------CustomModule------------*
from component import add_basic_layout, add_resource_card, add_rwd_div, add_page_head_card, add_track_card

@ui.page('/')
def dashboard_page():
    add_basic_layout()
    add_page_head_card(icon_name='dashboard', title_text='Dashboard')
    with add_rwd_div():
        add_resource_card()
    # add_track_card('Tracker #1')