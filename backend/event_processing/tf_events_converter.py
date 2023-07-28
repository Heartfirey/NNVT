from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


def parse_tfevents_file(file_path, convert_type: str='scalars'):
    """Parse the tfevents file and convert data
    To use this function, you have to install the tensorboard package first!
    Args:
        file_path (_type_): The path of the tfevents file
        convert_type (str, optional): (Noted that the 'scalars' type is the only supported type for now.) Must be scalars, audios, images, histograms or tensors. Defaults to 'scalars'. 
    """
    event_data = EventAccumulator(file_path, size_guidance={'tensors': 0})
    event_data.Reload()
    convert_data = dict()
    for tag in event_data.Tags()[convert_type]:
        convert_data.update({tag: list()})
        tensor_events = event_data.Scalars(tag)
        for tensor_event in tensor_events:
            fields = tensor_event._fields
            convert_dict = dict()
            for each_field in fields:
                convert_dict.update({each_field: getattr(tensor_event, each_field)})
            convert_data[tag].append(convert_dict)

    return convert_data
            




if __name__ == "__main__":
    file_path = "events.out.tfevents.1680438328.ubuntu.741332.0"  # Replace with the actual file path
    parse_tfevents_file(file_path)
