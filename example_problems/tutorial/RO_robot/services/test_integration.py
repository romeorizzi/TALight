import os
import subprocess as sp
import unittest
from typing import List

os.environ["PATH"] += os.pathsep + "./rtal/target/release/"


SERVER_CMD_LINE = "rtald -d example_problems/tutorial".split()

SERVER = "./rtal/target/release/rtald.exe"
CLIENT = "./rtal/target/release/rtal.exe"


def request(service: str, args: List[str] = []) -> List[str]:
    """Build the command line for the invocation of a service"""
    cmd = ["rtal", "connect", service]
    for arg in args:
        cmd.extend(["-a", arg])
    return cmd


# NOTE: both 'rtald' and 'rtal' should ideally be in PATH
@unittest.skip("Not yet finalized, must handle resource cleanup after the tests")
class ShellAliasesTest(unittest.TestCase):
    def test_run_server_from_shell(self):
        # assert "./rtal/target/release" in os.environ["PATH"].split(";")
        sp.call(executable=SERVER, args=["--help"])
        sp.call(["rtald", "--help"], shell=True)

    def test_run_client_from_shell(self):
        # assert "./rtal/target/release" in os.environ["PATH"].split(";")
        sp.call(executable=CLIENT, args=["--help"])
        sp.check_call("rtal --help", shell=True)


@unittest.skip("Not yet finalized, must handle resource cleanup after the tests")
class ClientServerIntegration(unittest.TestCase):

    def test_server_and_client_startup(self):
        cmd = "rtal".split()
        with sp.Popen(SERVER_CMD_LINE, shell=True) as server:
            with sp.Popen(cmd, shell=True) as client:
                pass

    def test_connect_to_problem(self):
        cmd = "rtal connect RO_robot".split()
        with sp.Popen(SERVER_CMD_LINE, shell=True) as _:
            sp.check_call(cmd, shell=True)

    def test_synopsis_service(self):
        cmd = request(service="synopsis")
        with sp.Popen(SERVER_CMD_LINE, shell=True) as _:
            sp.check_call(cmd, shell=True)

    def test_check_service(self):
        cmd = request(service="check")
        with sp.Popen(SERVER_CMD_LINE, shell=True) as _:
            sp.check_call(cmd, shell=True)

    def test_oracle_service(self):
        cmd = request(service="oracle", args=["pwd=?"])
        with sp.Popen(SERVER_CMD_LINE, shell=True) as _:
            sp.check_call(cmd, shell=True)


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
