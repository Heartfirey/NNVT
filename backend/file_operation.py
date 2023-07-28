import struct

def parse_tfevents_file(file_path):
    with open(file_path, 'rb') as file:
        while True:
            header_data = file.read(8)
            if not header_data:
                break
            # Parase the length of the event
            event_length = struct.unpack('Q', header_data)[0]
            print('wtf', event_length)
            # Read the whole event
            event_data = file.read(event_length)
            print('ed', event_data)
            # Parse the event
            pos = 0
            while pos < event_length:
                # Parse the length information of the event
                tag_bytes = event_data[pos:pos + 4]
                pos += 4
                tag = int.from_bytes(tag_bytes, byteorder='little')
                
                length_bytes = event_data[pos:pos + 4]
                pos += 4
                length = int.from_bytes(length_bytes, byteorder='little')
                
                # Get the value of the event
                value_bytes = event_data[pos:pos + length]
                pos += length
                
                # Process the abstract data
                if tag == 2:
                    step, wall_time = struct.unpack('Qd', value_bytes[:12])
                    value = value_bytes[12:]
                    print(f"step: {step}, wall_time: {wall_time}, value: {value}")
                    
if __name__ == "__main__":
    event_file_path = './events.out.tfevents.1680438328.ubuntu.741332.0'
    parse_tfevents_file(event_file_path)