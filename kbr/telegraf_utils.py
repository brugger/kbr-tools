

def format(measurement:str,tag_sets:dict={}, field_sets:dict={}, timestamp:int=None) -> str:

    line = measurement

    for tag, value in tag_sets.items():
        if tag in ["_field", "_measurement", "time"]:
            raise RuntimeError(f"{tag} is a reserved key")
        line += f",{tag}={value}"
    

    fields = []
    for field, value in field_sets.items():
        fields.append(f"{field}={value}")

    line += " {}".format(",".join(fields))


    if timestamp is not None:
        line += f" {timestamp}"

    
    return line
    