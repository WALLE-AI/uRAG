import loguru
import yaml
def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("加载yaml文件:", yaml_file)
    with open(yaml_file, encoding="utf-8") as f:
        data = yaml.full_load(f.read())
    return data

def init_config():
    config_path = "config/config.yaml"
    config = get_yaml_data(config_path)
    for key in config:
        loguru.logger.info(f"{key}: {config[key]}")
    return config