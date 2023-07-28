
# TODO: Implement event handler

def get_scalars_groups(raw_data: any) -> list:
    if type(raw_data) is dict:
        # print (raw_data)
        return [key for key in raw_data.keys()]
    
def get_scalars_data(raw_data: any, tag: str) -> list:
    if type(raw_data) is dict:
        return raw_data[tag]