import yaml


def parse_yaml(file):
    """ Parse a yaml file """

    with open(file, 'r') as stream:
        parsed_obj = yaml.safe_load(stream)

    return parsed_obj


if __name__ == "__main__":
    # retrieve reverse proxy configuration file
    config = parse_yaml('proxy.yaml')
