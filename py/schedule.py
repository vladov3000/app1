import yaml

def readConfig(cfg_file):
    with open(cfg_file, 'r') as stream:
        try:
            return (yaml.load(stream))
        except yaml.YAMLError as exc:
            logger.error('Failed to load yaml file:'+str(exc))
            raise exc


d=readConfig("interlake.yml")
print(d)