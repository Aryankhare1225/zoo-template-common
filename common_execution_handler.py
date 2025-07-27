# common/common_execution_handler.py

import os
import json
import yaml
from loguru import logger
from pystac.stac_io import StacIO
from urllib.parse import urlparse
from pystac.item_collection import ItemCollection

#from common.custom_stac_io import CustomStacIO


class CommonExecutionHandler:
    def __init__(self, conf):
        self.conf = conf
        self.job_id = None
        self.feature_collection = None
        self.results = None

        # Set the STAC I/O to our custom one
        # StacIO.set_default(CustomStacIO)

    def pre_execution_hook(self):
        """Hook to run before execution — override if needed."""
        logger.info("Default pre_execution_hook: no operation")

    def post_execution_hook(self, log, output, usage_report, tool_logs):
        """Hook to run after execution — override if needed."""
        logger.info("Default post_execution_hook: no operation")

    
    def get_pod_env_vars(self):
        logger.info("get_pod_env_vars")
        return self.conf.get("pod_env_vars", {})

    def get_pod_node_selector(self):
        logger.info("get_pod_node_selector")
        return self.conf.get("pod_node_selector", {})

    def get_additional_parameters(self):
        logger.info("get_additional_parameters")
        return self.conf.get("additional_parameters", {})

    def local_get_file(self, file_name):
        try:
            with open(file_name, "r") as file:
                return yaml.safe_load(file)
        except Exception:
            return {}

    def get_secrets(self):
        logger.info("get_secrets")
        return self.local_get_file("/assets/pod_imagePullSecrets.yaml")

    def handle_outputs(self, log, output, usage_report, tool_logs):
        try:
            logger.info("handle_outputs")

            self.conf["main"]["tmpUrl"] = self.conf["main"]["tmpUrl"].replace(
                "temp/", self.conf["auth_env"]["user"] + "/temp/"
            )

            services_logs = [
                {
                    "url": os.path.join(
                        self.conf["main"]["tmpUrl"],
                        f"{self.conf['lenv']['Identifier']}-{self.conf['lenv']['usid']}",
                        os.path.basename(tool_log),
                    ),
                    "title": f"Tool log {os.path.basename(tool_log)}",
                    "rel": "related",
                }
                for tool_log in tool_logs
            ]

            for idx, log_entry in enumerate(services_logs):
                for key in ["url", "title", "rel"]:
                    log_key = key if idx == 0 else f"{key}_{idx}"
                    self.conf.setdefault("service_logs", {})[log_key] = log_entry[key]

            self.conf["service_logs"]["length"] = str(len(services_logs))

        except Exception as e:
            logger.error("ERROR in handle_outputs")
            raise e

