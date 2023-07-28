import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
from nicegui import ui
from enum import Enum

BUILTIN_FUNCTION_LIST = ['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']

def color_list_filter(data: list) -> list:
    del_list = []
    for each_item in data:
        if each_item in BUILTIN_FUNCTION_LIST or each_item[0] == '_':
            del_list.append(each_item)
    for each_del in del_list:
        data.remove(each_del)
    return data

def add_prefix(data : list, prefix : str) -> list:
    for index in range(len(data)):
        data[index] = f'{prefix}-{data[index]}'
    return data

class PlotlyDataFormat(Enum):
    temoplate_line_2d = {
        'dim' : 2,
        'template': {
            'x': list(),
            'y': list(),
            'z': list()
        }
    }

class PlotlyObj(object):
    def __init__(self, plotly_type: str, title: str, data: any, default_fields: dict):
        self.plotly_type = plotly_type
        self.templates = 'none'
        self.color_scale = px.colors.qualitative.Plotly
        self.color_scale_name = 'qualitative-Plotly'
        self.legend_name = ''
        self.plotly_graph = None
        self.plotly_ui = None
        self.horiznontal_axis = 'step'
        
        
        self.support_format = ['SVG', 'PNG', 'JPG']
        self.data_format = {
            'dim': 2,
            'template': {
                'x': list(),
                'y': list()
            }
        }
        self.data = data
        self.title = title
        self.fields = default_fields
        self.generate_plotly_graph()
        
    
    def _generate_line_plotly_graph(self) -> None:
        field_x = self.fields['x']
        field_y = self.fields['y']
        self.plotly_graph = px.line(title=self.title, 
                                    x=[subdata[field_x] for subdata in self.data], 
                                    y=[subdata[field_y] for subdata in self.data],
                                    template=self.templates,
                                    color_discrete_sequence=self.color_scale,)
    
    def generate_plotly_graph(self) -> None:
        if self.plotly_type == 'line':
            self._generate_line_plotly_graph()
        pass
    
    def get_plotly_ui(self, classes: str='w-full h-120') -> go.Figure:
        self.plotly_ui = ui.plotly(self.plotly_graph).classes(classes)
        return self.plotly_ui
    
    def get_available_templates(self) -> list:
        templates_list = list(pio.templates)
        return templates_list
    
    def get_current_templates(self) -> str:
        return self.templates
    
    def get_available_colorscale(self) -> list:
        color_scale_list = []
        color_scale_list += add_prefix(color_list_filter(dir(px.colors.qualitative)), 'qualitative')
        color_scale_list += add_prefix(color_list_filter(dir(px.colors.sequential)), 'sequential')
        color_scale_list += add_prefix(color_list_filter(dir(px.colors.diverging)), 'diverging')
        color_scale_list += add_prefix(color_list_filter(dir(px.colors.cyclical)), 'cyclical')
        return color_scale_list
    
    def get_current_colorscale(self) -> str:
        return self.color_scale_name
    
    def get_available_export_format(self) -> list:
        return self.support_format
    
    def set_templates(self, templates_name: str = 'none') -> None:
        assert templates_name in list(pio.templates)
        self.templates = templates_name
        self.plotly_graph.update_layout(template=self.templates)
        self.update()
    
    def set_colorscale(self, color_scale: str) -> None:
        self.color_scale_name = f'{color_scale}'
        color_class, color_scale = color_scale.split('-')
        self.color_scale = getattr(getattr(px.colors, color_class), color_scale)
        self.generate_plotly_graph()
        self.update(overwrite=True)
    
    def set_legend_name(self, name: str) -> None:
        self.legend_name = name
        self.update()

    def set_data_fields(self, field: str, val: str) -> None:
        self.fileds[field] = val
        self.update()
    
    def update(self, overwrite: bool = False):
        print('Update!')
        # self.generate_plotly_graph()
        if overwrite is True:
            self.plotly_ui.update_figure(self.plotly_graph)
        else:    
            self.plotly_ui.update()
        

if __name__ == "__main__":
    # plt = PlotlyObj()
    # print(plt.get_available_colorscale())
    import operator
    # named_colorscales = px.colors.sequential
    
    all_name = dir(px.colors.sequential)
    # print(add_prefix(color_list_filter(all_name), 'test'))
    # print(operator.attrgetter('ice_r')(px.colors.sequential))
    
    # print(getattr(px.colors.sequential, 'haline'))
    # print(getattr(getattr(px.colors, 'sequential'), 'haline'))
    print(px.colors.sequential.haline)