import time
from netmiko.base_connection import BaseConnection


class F5TmshSSH(BaseConnection):
    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self._test_channel_read()
        self.set_base_prompt()
        self.tmsh_mode()
        self.set_base_prompt()
        cmd = 'run /util bash -c "stty cols 255"'
        self.set_terminal_width(command=cmd, pattern="run")
        self.disable_paging(
            command="modify cli preference pager disabled display-threshold 0"
        )
        self.clear_buffer()

    def tmsh_mode(self, delay_factor=1):
        """tmsh command is equivalent to config command on F5."""
        delay_factor = self.select_delay_factor(delay_factor)
        self.clear_buffer()
        command = f"{self.RETURN}tmsh{self.RETURN}"
        self.write_channel(command)
        time.sleep(1 * delay_factor)
        self.clear_buffer()
        return None
    
    def check_config_mode(self, check_string=") #", pattern=""):
        """
        #Checks if the device is in configuration mode or not.
        """
        return super().check_config_mode(check_string=check_string, pattern=pattern)


    def config_mode(self, config_command=""):
        "No config mode for F5 devices."""
        return ""
                                              
    def exit_config_mode(self, exit_config=""):
        """No config mode for F5 devices."""
        return ""

