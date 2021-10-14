#!/usr/bin/env python3
"""This file contains the useful functions to handle modelling problem. 
NOTE: it needs to be placed in the services directory to work properly."""
import subprocess, os

from bot_interface import service_server_requires_and_gets_file_of_handle


def get_archive_path_from(you_service_file_path):
    """Call this with: get_archive_path_from(__file__)"""
    service_dir_path = os.path.abspath(os.path.dirname(you_service_file_path))
    return os.path.join(service_dir_path, '../archive')


class ModellingProblemHelper():
    def __init__(self,
                archive_path  = None,           \
                tmp_dirname   = '../tmp97815',  \
                mod_filename  = 'model.mod',    \
                dat_filename  = 'instance.dat', \
                sol_filename  = 'solution.txt', \
                out_filename  = 'output.txt',   \
                err_filename  = 'error.txt'     ):
        self.__archive_path = archive_path
        self.__tmp_dirname = tmp_dirname
        self.__mod_filename  = mod_filename
        self.__dat_filename  = dat_filename
        self.__sol_filename  = sol_filename
        self.__out_filename  = out_filename
        self.__err_filename  = err_filename
        self.__tmp_path = None
        self.__mod_path = None
        self.__dat_path = None
        self.__sol_path = None
        self.__out_path = None
        self.__err_path = None


    # TODO: fix PermissionError:
    def __del__(self):
        """Remove TMP_DIR"""
        # os.remove(self.__get_tmp_path())


    def __get_tmp_path(self):
        """Returns the path of the tmp directory."""
        if not self.__tmp_path:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            self.__tmp_path = os.path.join(current_dir, self.__tmp_dirname)
        return self.__tmp_path
    

    def get_dat_path(self):
        """Returns the path of the dat file."""
        if not self.__dat_path:
            self.__dat_path = os.path.join(self.__get_tmp_path(), self.__dat_filename)
        return self.__dat_path
    

    def get_mod_path(self):
        """Returns the path of the mod file."""
        if not self.__mod_path:
            self.__mod_path = os.path.join(self.__get_tmp_path(), self.__mod_filename)
        return self.__mod_path
    

    def get_out_path(self):
        """Returns the path of the stdout of GPLSOL."""
        if not self.__out_path:
            self.__out_path = os.path.join(self.__get_tmp_path(), self.__out_filename)
        return self.__out_path
    

    def get_err_path(self):
        """Returns the path of the stderror of GPLSOL."""
        if not self.__err_path:
            self.__err_path = os.path.join(self.__get_tmp_path(), self.__err_filename)
        return self.__err_path


    def get_sol_path(self):
        """Returns the path of the GPLSOL solution file."""
        if not self.__sol_path:
            self.__sol_path = os.path.join(self.__get_tmp_path(), self.__sol_filename)
        return self.__sol_path


    def __init_tmp_dir(self):
        """Creates a folder where to store the temporary files needed by the service. Our goal is that this should work whether the service is run in local or on a server."""
        if not os.path.exists(self.__get_tmp_path()):
            os.makedirs(self.__get_tmp_path())


    def receive_files(self, mod=False, dat=False, input=False):
        """Enable the service to recive the files selected. If input=True then return the input in a string form."""
        # Initialize TMP_DIR
        self.__init_tmp_dir()

        # Manage mod file
        if mod:
            mod = service_server_requires_and_gets_file_of_handle('mod').decode()
            try:
                with open(self.get_mod_path(), 'w') as mod_file:
                    mod_file.write(mod)
            except os.error as err:
                raise RuntimeError('write-error', self.__mod_filename, err)

        # Manage dat file
        if dat:
            dat = service_server_requires_and_gets_file_of_handle('dat').decode()
            try:
                with open(self.get_dat_path(), 'w') as dat_file:
                    dat_file.write(dat)
            except os.error as err:
                raise RuntimeError('write-error', self.__dat_filename, err)
        
        # Manage input file
        if input:
            input = service_server_requires_and_gets_file_of_handle('input').decode()
            return input


    def run_GPLSOL(self, file_dat_path='tmp_path'):
        """launches glpsol on the .mod and .dat files contained in TMP_DIR. The stdout, stderr and solution of glpsol are saved in files."""
        # Get file dat path
        if file_dat_path == 'tmp_path':
            file_dat_path = self.get_dat_path()
        # Get files for stdoutRun GPLSOL
        try:
            with open(self.get_out_path(), 'w') as out_file:
                try:
                    with open(self.get_err_path(), 'w') as err_file:
                        # RUN gplsol
                        subprocess.run([
                            "glpsol", 
                            "-m", self.get_mod_path(), 
                            "-d", file_dat_path,
                        ], cwd=self.__get_tmp_path(), timeout=30.0, stdout=out_file, stderr=err_file)
                except os.error as err:
                    raise RuntimeError('write-error', self.__err_filename, err)
                except Exception as err:
                    raise RuntimeError('process-exception', err)
                except subprocess.TimeoutExpired as err:
                    raise RuntimeError('process-timeout', err)
                except subprocess.CalledProcessError as err: 
                    raise RuntimeError('process-call', err)
        except os.error as err:
            raise RuntimeError('write-error', self.__out_filename, err)


    def get_out_str(self):
        """Return a string that contents the stdout of GPLSOL."""
        try:
            with open(self.get_out_path(), 'r') as file:
                return file.read()
        except os.error as err:
            raise RuntimeError('stdout-read-error', err)


    def get_err_str(self):
        """Return a string that contents the stderr of GPLSOL."""
        try:
            with open(self.get_err_path(), 'r') as file:
                return file.read()
        except os.error as err:
            raise RuntimeError('stderr-read-error', err)


    def get_raw_solution(self):
        """Return a list of string that contents the solution produced by GPLSOL. Remember to call a soluion_parsing function."""
        try:
            with open(self.get_sol_path(), 'r') as file:
                return file.read().splitlines()
        except os.error as err:
            raise RuntimeError('solution-read-error', err)


    def get_input_from_archive(self, dir_name):
        """Returns a string that contents the input of the dir_selected."""
        assert isinstance(dir_name, str)
        assert self.__archive_path, '"archive_path" must be initialized when create the ModellingProblemHelper object'
        try:
            dir_path = os.path.join(self.__archive_path, dir_name)
            input_path = os.path.join(dir_path, 'input.txt')
            with open(input_path, 'r') as file:
                return file.read()
        except os.error as err:
            raise RuntimeError('input-read-error', input_path)
        except Exception as err:
            raise RuntimeError('dir-not-exist', dir_name)


    def get_dat_paths_from_archive(self, dir_name):
        """Returns the list of all dat_files_path in this directory in archive"""
        assert isinstance(dir_name, str)
        assert self.__archive_path, '"archive_path" must be initialized when create the ModellingProblemHelper object'
        try:
            dir_path = os.path.join(self.__archive_path, dir_name)
            paths_list = list()
            for filename in os.listdir(dir_path):
                # Filter only .dat file
                if filename[-4:] == '.dat':
                    # Get full path and add it if is a file
                    file_path = os.path.join(dir_path, filename)
                    if os.path.isfile(file_path):
                        paths_list.append(file_path)
            return paths_list

        except Exception as err:
            raise RuntimeError('dir-not-exist', dir_name)


