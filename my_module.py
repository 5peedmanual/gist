def write_to_file(name, data):
    text_file = open(name, "w")
    text_file.write(str(data))
    text_file.close()
