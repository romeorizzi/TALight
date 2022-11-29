import subprocess as sp
import unittest
from typing import List

SERVER_CMD_LINE = "rtald -d example_problems/tutorial".split()


def request(service: str, args: List[str]) -> List[str]:
    """Build the command line for the invocation of a service"""
    
    return []


class ClientServerIntegration(unittest.TestCase):

    def test_server_and_client_startup(self):
        cmd = "rtal".split()
        with sp.Popen(SERVER_CMD_LINE, shell=True) as server:
            with sp.Popen(cmd, shell=True) as client:
                pass

    def test_connect_to_problem(self):
        cmd = "rtal connect RO_robot".split()
        with sp.Popen(SERVER_CMD_LINE, shell=True) as server:
            sp.check_call(cmd, shell=True)

    @unittest.skip("Not yet implemented")
    def test_synopsis_service(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_check_service(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_oracle_service(self):
        cmd = "rtal connect RO_robot".split()
        arg = "-a pwd=?".split()
        with sp.Popen(SERVER_CMD_LINE, shell=True) as server:
            sp.check_call(cmd + arg, shell=True)



class CheckServiceIntegration(unittest.TestCase):

    @unittest.skip("Not yet implemented")
    def test_check_output(self):
        pass


class OracleServiceIntegration(unittest.TestCase):

    @unittest.skip("Not yet implemented")
    def test_oracle_output(self):
        pass

if __name__ == "__main__":
    unittest.main()
