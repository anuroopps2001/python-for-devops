def update_server_configuration(file_path, key, value):
    # Read the server_configuration file content
    with open(file_path, "r") as reading:
        original_content = reading.readlines()  # # This creates a LIST of lines

    with open(file_path, "w") as writing:
        for each_line in original_content:
            if key in each_line:
                writing.write(key + "=" + value + "\n")
            else:
                writing.write(each_line)

server_config_file = "server.conf"


key_to_update = "MAX_CONNECTIONS"


new_value = "400"

update_server_configuration(server_config_file, key_to_update, new_value)