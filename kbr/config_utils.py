from munch import Munch, munchify
import json



def readin_config_file( filename: str) -> Munch:

    if ".yaml" in filename or ".yml" in filename:
        return readin_yaml_file( filename )
    elif  ".json" in filename:
        return readin_json_file( filename )
    else:
        raise NotImplementedError("Cannot use {} as config file".format( filename))



def readin_json_file(filename:str) -> Munch:
    
    with open( filename ) as json_file:
        data = json.load(json_file)
        json_file.close(  )
    return munchify(data)


def readin_yaml_file(config_file:str) -> Munch:
    """ reads in and checks the config file

    Args:
      config_file: yaml formatted config files

    Returns:
      config ( munch )

    Raises:
      None
    """

    with open(config_file, 'r') as stream:
        config = Munch.fromYAML(stream)
        stream.close()

    return config


