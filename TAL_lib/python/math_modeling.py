#!/usr/bin/env python3
"""This file contains the useful functions to handle modelling problem. 
NOTE: it needs to be placed in the services directory to work properly."""
import subprocess, os, json

class ModellingProblemHelper():
    def __init__(self,
                TAc,
                tmp_path,                                       \
                problem_path,                                   \
                mod_filename      = 'mod',                      \
                dat_filename      = 'dat',                      \
                in_filename       = 'instance',                 \
                sol_filename      = 'solution.txt',             \
                out_filename      = 'output.txt',               \
                err_filename      = 'error.txt',                \
                ef_filename       = 'explicit_formulation.txt', \
                instances_dirname = 'instances_catalogue',      \
                all_instances_subfolder = 'all_instances',      \
                gendict_filename  = 'gen_dictionary.json'):
        self.__TAc = TAc
        #print(f"problem_path={problem_path}")
        #print(f"tmp_path={tmp_path}")
        self.problem_path = problem_path
        self.tmp_path = tmp_path
        self.__mod_path        = os.path.join(tmp_path, mod_filename)
        self.__dat_path        = os.path.join(tmp_path, dat_filename)
        self.__in_path         = os.path.join(tmp_path, in_filename)
        self.__sol_path        = os.path.join(problem_path, sol_filename)
        self.__out_path        = os.path.join(tmp_path, out_filename)
        self.__err_path        = os.path.join(tmp_path, err_filename)
        self.__ef_path         = os.path.join(tmp_path, ef_filename)
        self.__catalogue_path  = os.path.join(problem_path, instances_dirname)
        self.__all_instances_path  = os.path.join(problem_path, instances_dirname, all_instances_subfolder)
        self.__gendict_path    = os.path.join(self.__catalogue_path, gendict_filename)


    def run_ef_GLPSOL(self, ef_format):            
        try:
            with open(self.__out_path, 'w') as out_file:
                try:
                    if ef_format == "math":
                        with open(self.__err_path, 'w') as err_file:
                            # RUN gplsol
                            command = ["glpsol", "--math", self.__ef_path, "-d", self.__dat_path]
                            subprocess.run(command, cwd=self.problem_path, timeout=30.0, stdout=out_file, stderr=err_file)
                    else:
                        with open(self.__err_path, 'w') as err_file:
                            # RUN gplsol
                            command = ["glpsol", f"--{ef_format}", self.__ef_path]
                            subprocess.run(command, cwd=self.problem_path, timeout=30.0, stdout=out_file, stderr=err_file)
                except os.error as err:
                    self.__TAc.print(f"Fail to create stderr file in: {self.__err_path}", "red", ["bold"])
                    exit(0)
                except subprocess.TimeoutExpired as err:
                    self.__TAc.print(f"Too much computing time! Deadline exceeded.", "red", ["bold"])
                    exit(0)
                except subprocess.CalledProcessError as err: 
                    self.__TAc.print(f"The call to glpsol on your .dat file returned error:\n{err}", "red", ["bold"])
                    exit(0)
                except Exception as err:
                    self.__TAc.print(f"Processing returned with error:\n{err}", "red", ["bold"])
                    exit(0)
        except os.error as err:
            self.__TAc.print(f"Fail to create stdout file in: {self.__out_path}", "red", ["bold"])
            exit(0)

    def run_GLPSOL_with_ef(self, ef_format=None, dat_file_fullpath=None):
        if dat_file_fullpath == None:
            dat_file_path = self.__dat_path
        else:
            dat_file_path = dat_file_fullpath
        
        try:
            with open(self.__out_path, 'w') as out_file:
                try:
                    with open(self.__err_path, 'w') as err_file:
                        # RUN gplsol
                        command = ["glpsol", "-m", self.__mod_path, "-d", dat_file_path, f"--w{ef_format}", self.__ef_path]
                        subprocess.run(command, cwd=self.problem_path, timeout=30.0, stdout=out_file, stderr=err_file)
                except os.error as err:
                    self.__TAc.print(f"Fail to create stderr file in: {self.__err_path}", "red", ["bold"])
                    exit(0)
                except subprocess.TimeoutExpired as err:
                    self.__TAc.print(f"Too much computing time! Deadline exceeded.", "red", ["bold"])
                    exit(0)
                except subprocess.CalledProcessError as err: 
                    self.__TAc.print(f"The call to glpsol on your .dat file returned error:\n{err}", "red", ["bold"])
                    exit(0)
                except Exception as err:
                    self.__TAc.print(f"Processing returned with error:\n{err}", "red", ["bold"])
                    exit(0)
        except os.error as err:
            self.__TAc.print(f"Fail to create stdout file in: {self.__out_path}", "red", ["bold"])
            exit(0)

    def run_GLPSOL(self, dat_file_fullpath=None):
        """If  dat_file_path==None  then this procedure launches glpsol on the .mod and .dat files contained in TMP_DIR. Otherwise, the dat file is on the server, in location <dat_file_fullpath>. The stdout, stderr and solution of glpsol are saved in files."""
        if dat_file_fullpath == None:
            dat_file_path = self.__dat_path
        else:
            dat_file_path = dat_file_fullpath
        
        # Get files for stdoutRun GPLSOL
        try:
            with open(self.__out_path, 'w') as out_file:
                try:
                    with open(self.__err_path, 'w') as err_file:
                        # RUN gplsol
                        subprocess.run([
                            "glpsol", 
                            "-m", self.__mod_path, 
                            "-d", dat_file_path,
                        ], cwd=self.problem_path, timeout=30.0, stdout=out_file, stderr=err_file)
                except os.error as err:
                    self.__TAc.print(f"Fail to create stderr file in: {self.__err_path}", "red", ["bold"])
                    exit(0)
                except Exception as err:
                    self.__TAc.print(f"Processing returned with error:\n{err}", "red", ["bold"])
                    exit(0)
                except subprocess.TimeoutExpired as err:
                    self.__TAc.print(f"Too much computing time! Deadline exceeded.", "red", ["bold"])
                    exit(0)
                except subprocess.CalledProcessError as err: 
                    self.__TAc.print(f"The call to glpsol on your .dat file returned error:\n{err}", "red", ["bold"])
                    exit(0)
        except os.error as err:
            self.__TAc.print(f"Fail to create stdout file in: {self.__out_path}", "red", ["bold"])
            exit(0)


    def get_input_str(self):
        """Return a string that contains the input passed with bot"""
        try:
            with open(self.__in_path, 'r') as file:
                return file.read()
        except os.error as err:
            self.__TAc.print(f"Fail to read you input file with the instance.", "red", ["bold"])
            self.__TAc.print(f"Fail to read the input file in {self.__in_path}", "red", ["bold"], file=stderr)
            exit(0)


    def get_out_str(self):
        """Return a string that contains the stdout of GPLSOL."""
        try:
            with open(self.__out_path, 'r') as file:
                return file.read()
        except os.error as err:
            self.__TAc.print(f"Fail to read the stdout file of GPLSOL in {self.__out_path}", "red", ["bold"])
            exit(0)


    def get_err_str(self):
        """Return a string that contains the stderr of GPLSOL."""
        try:
            with open(self.__err_path, 'r') as file:
                return file.read()
        except os.error as err:
            self.__TAc.print(f"Fail to read the stderr file of GPLSOL in {self.__err_path}", "red", ["bold"])
            exit(0)


    def get_ef_str(self):
        """Return a string that contains the explicit formulation of GPLSOL."""
        try:
            with open(self.__ef_path, 'r') as file:
                return file.read()
        except os.error as err:
            self.__TAc.print(f"Fail to read the explicit formulation file of GPLSOL in {self.__ef_path}", "red", ["bold"])
            exit(0)            


    def get_raw_sol(self):
        """Return a list of string that contains the solution produced by GPLSOL. Remember to call a soluion_parsing function."""
        try:
            with open(self.__sol_path, 'r') as file:
                return file.read().splitlines()
        except os.error as err:
            self.__TAc.print(f"Fail to read the solution file of GPLSOL in {self.__sol_path}", "red", ["bold"])
            exit(0)
            

    # MANAGE INPUTS/GENDICT FILES -------------------
    def get_path_from_id(self, id, format_name):
        """Returns the path to the file selected with id."""
        # Read gen-dictionary
        id_as_string = str(id).zfill(3)
        try:
            with open(self.__gendict_path, 'r') as file:
                gendict = json.load(file)
                info = gendict[id_as_string]
        except IOError as ioe:
            self.__TAc.print(f"Fail to open the gen_dictionary .yaml file in: {self.__gendict_path}", "red", ["bold"])
            exit(0)
        except KeyError as err:
            self.__TAc.print(f"The id={id} is invalid.", "red", ["bold"])
            exit(0)
        except os.error as err:
            self.__TAc.print(f"Fail to read/parse the gen_dictionary file in: {self.__gendict_path}", "red", ["bold"])
        # get path from gen-dictionary
        try:
            return os.path.join(self.__all_instances_path, info[format_name])
        except KeyError as err:
            self.__TAc.print(f"The format={format_name} is invalid.", "red", ["bold"])
            exit(0)


    def get_file_str_from_path(self, path):
        """Returns the contents of the file as a string from the selected path."""
        try:
            with open(path, 'r') as file:
                return file.read()
        except IOError as ioe:
            self.__TAc.print(f"Fail to open the file: {path}", "red", ["bold"])
            exit(0)

    def get_file_str_from_id(self, id, format_name):
        """Returns the contents of the file as a string with the selected id."""
        return self.get_file_str_from_path(self.get_path_from_id(id, format_name))

    def get_file_str_from_path_by_alphabet(self, alphabet, format):
        """Returns the contents of the file as a string with the selected alphabet."""
        # read the folders in the file "instances_catalogue"
        folders=[]
        for filename in os.listdir(self.__catalogue_path):
            files_path=filename
            folders.append(files_path)
        # choose the right instance according to the alphabet
        for i in folders:
            if i[10:21]==alphabet[:9]+'_s':
                path=os.path.join(self.__catalogue_path, i)
                instance= os.listdir(os.path.join(self.__catalogue_path, i))
        # choose the right instance according to the format
        for elem in range(len(instance)-1):
            if instance[elem][13:25]==format:
                final_path=os.path.join(path,instance[elem])
                file=self.get_file_str_from_path(final_path)
        return(file)
    
    def get_instances_paths_in(self, dir_name):
        """Returns the list of all file_path in the inputs directory grouped by instance"""
        assert isinstance(dir_name, str)
        try:
            dir_path = os.path.join(self.__catalogue_path, dir_name)
            instances_paths = dict()
            for filename in os.listdir(dir_path):
                tmp_parse = filename.split('.')
                id = tmp_parse[0][len('instance'):]
                format = ".".join(tmp_parse[1:])
                if id not in instances_paths:
                    instances_paths[id] = {format : os.path.join(dir_path, filename)}
                else:
                    instances_paths[id][format] = os.path.join(dir_path, filename)
            return instances_paths
        except os.error as err:
            self.__TAc.print(f"Fail to read the instance file in: {self.__catalogue_path}", "red", ["bold"])
            exit(0)