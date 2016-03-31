from abc import ABCMeta
from abc import abstractmethod


class CliServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_command(self, command, expected_str=None, expected_map=None, timeout=30, retry_count=10,
                     is_need_default_prompt=True):
        pass

    @abstractmethod
    def send_config_command(self, command, expected_str=None, expected_map=None, timeout=30, retry_count=10,
                            is_need_default_prompt=True):
        pass

    @abstractmethod
    def _enter_configuration_mode(self):
        pass

    @abstractmethod
    def _exit_configuration_mode(self):
        pass

    @abstractmethod
    def send_command_list(self, commands_list, send_command_func=send_config_command):
        pass

    @abstractmethod
    def _check_output_for_errors(self, output, error_list=None):
        pass

    @abstractmethod
    def rollback(self):
        pass

