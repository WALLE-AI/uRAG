from typing import Dict
from xml.dom.minidom import Document
import loguru
import yaml

from error.error import ValidaionException
def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("加载yaml文件:", yaml_file)
    with open(yaml_file, encoding="utf-8") as f:
        data = yaml.full_load(f.read())
    return data

def init_config():
    config_path = "config/config.yaml"
    parsed_dict = yaml_to_dict(config_path)
    return parsed_dict


def yaml_to_dict(file_path: str) -> Dict:
    with open(file_path,"r",encoding="utf-8") as yaml_file:
        yaml_string = yaml_file.read()

        try:
            # convert yaml string to dict
            parsed_dict = yaml.safe_load(yaml_string)
        except yaml.scanner.ScannerError as e:
            raise ValidaionException(f"There could be some syntax error in yaml written in {file_path}", e)

    return parsed_dict


def yaml_to_class(yaml_file_path: str, cls: type, default_yaml_file_path: str = None):
    """
    Read yaml file present at path `yaml_file_path`, convert it to dictionary using pyyaml's standard methods.
    Then convert this dictionary to class object of class given as `cls`. Further check if user has provided all
    the required fields in `yaml_file_path`. Fields that are missing in `yaml_file_path`, set them with defaults.

    :param yaml_file_path: str
    :param cls: type
    :param default_yaml_file_path: str
    :return:
    """
    if not yaml_file_path:
        yaml_file_path = default_yaml_file_path
    custom_args = yaml_to_dict(yaml_file_path)

    if default_yaml_file_path:
        # If user has not provided all the required arguments, fill them with defaults
        default_args = yaml_to_dict(default_yaml_file_path)
        missing_args = set(default_args) - set(custom_args)
        for key in list(missing_args):
            custom_args[key] = default_args[key]

    try:
        yaml_as_class = cls(**custom_args)
    except TypeError as e:
        raise ValidaionException(f"Exception while converting yaml file at {yaml_file_path} "
                                     f"to class {cls.__name__}: ", e)

    return yaml_as_class

