import logging
from collections.abc import Callable, Generator
from typing import Union

from metaknowledge.storage.base_storage import BaseStorage
from metaknowledge.storage.storage_type import StorageType


logger = logging.getLogger(__name__)


class Storage:
    def __init__(self,config:dict):
        self.config = config
        storage_factory = self.get_storage_factory(self.config["STORAGE_TYPE"])
        self.storage_runner = storage_factory()

    def get_storage_factory(self,storage_type: str) -> Callable[[], BaseStorage]:
        match storage_type:
            case StorageType.S3:
                from metaknowledge.storage.aws_s3_storage import AwsS3Storage

                return AwsS3Storage(self.config)
            case StorageType.LOCAL:
                from metaknowledge.storage.opendal_storage import OpenDALStorage

                return lambda: OpenDALStorage(scheme="fs", root=self.config["STORAGE_LOCAL_PATH"])
            case StorageType.ALIYUN_OSS:
                from metaknowledge.storage.aliyun_oss_storage import AliyunOssStorage

                return AliyunOssStorage(self.config)
            case _:
                raise ValueError(f"unsupported storage type {storage_type}")

    def save(self, filename, data):
        try:
            self.storage_runner.save(filename, data)
        except Exception as e:
            logger.exception(f"Failed to save file {filename}")
            raise e

    def load(self, filename: str, /, *, stream: bool = False) -> Union[bytes, Generator]:
        try:
            if stream:
                return self.load_stream(filename)
            else:
                return self.load_once(filename)
        except Exception as e:
            logger.exception(f"Failed to load file {filename}")
            raise e

    def load_once(self, filename: str) -> bytes:
        try:
            return self.storage_runner.load_once(filename)
        except Exception as e:
            logger.exception(f"Failed to load_once file {filename}")
            raise e

    def load_stream(self, filename: str) -> Generator:
        try:
            return self.storage_runner.load_stream(filename)
        except Exception as e:
            logger.exception(f"Failed to load_stream file {filename}")
            raise e

    def download(self, filename, target_filepath):
        try:
            self.storage_runner.download(filename, target_filepath)
        except Exception as e:
            logger.exception(f"Failed to download file {filename}")
            raise e

    def exists(self, filename):
        try:
            return self.storage_runner.exists(filename)
        except Exception as e:
            logger.exception(f"Failed to check file exists {filename}")
            raise e

    def delete(self, filename):
        try:
            return self.storage_runner.delete(filename)
        except Exception as e:
            logger.exception(f"Failed to delete file {filename}")
            raise e
