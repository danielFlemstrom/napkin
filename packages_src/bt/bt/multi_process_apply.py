

import subprocess as sp
import json
import os
import pandas
import multiprocessing as mp
import time
import datetime
import sys
# ---------------------------------------------------------------------------------
# ------------------------   Parameters and Globals ------------------------------
# ---------------------------------------------------------------------------------
if __name__ == '__main__':
    from bt.global_defaults import default_main_defs, \
        default_ga_motor,  \
        default_main_defs, \
        default_log_dir,   \
        default_ga_dir
else:
    from .global_defaults import default_main_defs, \
        default_ga_motor,  \
        default_main_defs, \
        default_log_dir,   \
        default_ga_dir


# ---------------------------------------------------------------------------------
# ------------------------    Command Line Escape   ------------------------------
# ---------------------------------------------------------------------------------

def escape_cmd_line_args(s):
    return s  # .replace('\\','\\\\').replace('"','\\"').replace(" ","\ ")


# ---------------------------------------------------------------------------------
# ------------------------    Evaluate G/As on Logfile(s)   ----------------------
# ---------------------------------------------------------------------------------
'''
    argball containing:
    ix         # job nr
    ga_files,  # list of fullpaths
    log_file,   # fullpath
    main_defs,   # fullpath
    out_queue,   #  out_queue.put(result)When in run in anoter process, return value here
    ga_motor     # SAGA Evaluation Core 
'''


def run_one_log_eval(argball):

    # try:
    arglist = ["/usr/local/bin/node",
               f"{argball['ga_motor']}",
               f"ga_files={escape_cmd_line_args(json.dumps(argball['ga_files']))}",
               f"log_file={escape_cmd_line_args(argball['log_file'])}",
               f"main_defs={escape_cmd_line_args(argball['main_defs'])}"]

    p = sp.run(arglist,  # text=True,
               universal_newlines=True,
               shell=False,
               # capture_output=True,
               stdout=sp.PIPE,
               stderr=sp.PIPE,
               check=True)

    result = {'ix': argball['ix'],
              'row': json.loads(p.stdout)}
    '''
    except Exception as e:
        print("run_one_log_eval::Exception",e)
        result =[]
        for ga_file in ga_files:
            result.append({
                            'ga_file':ga_file,
                            'log_file':log_file,
                            'status':"Exception",
                            'err_msg':str(e)
                        })
        result = {'ix':argball['ix'],
                 'row':result}
    finally:
    '''
    return result
# -----------------------------------------------------------------------------------------------------------------
#                                   test_run_one_log_eval
# -----------------------------------------------------------------------------------------------------------------


def test_run_one_log_eval():
    print("-----------------------------")
    print(default_ga_dir)
    print(os.listdir(default_ga_dir))
    gafiles = [default_ga_dir +
               f for f in os.listdir(default_ga_dir) if ".txt" in f][:1]

    logfile = [default_log_dir +
               f for f in os.listdir(default_log_dir) if ".TXT" in f][0]
    argball = {
        'ix': 1,
        'ga_files': gafiles,
        'log_file': logfile,
        'main_defs': default_main_defs,
        'ga_motor': default_ga_motor
    }
    print("Running one evaluation with the following arguments:")
    print(argball)
    res = run_one_log_eval(argball)
    print(res)


# ---------------------------------------------------------------------------------
# ------------------------    Evaluate G/As on ONE Logfile   ---------------------
# ---------------------------------------------------------------------------------
'''
    ga_files,  # list of fullpaths
    log_file,   # fullpath
    main_defs,   # fullpath
    out_queue,   #  out_queue.put(result)When in run in anoter process, return value here
    ga_motor     # SAGA Evaluation Core 
'''


def mass_eval(logs=None, logdir=default_log_dir, gadir=default_ga_dir):

    if logs is None:
        logs = os.listdir(logdir)
        log_files = [logdir + "/" +
                     x for x in logs if "LOGDATA" in x and "TXT" in x]
    else:
        log_files = logs

    gas = os.listdir(gadir)
    ga_files = [gadir + "/" + x for x in gas if "txt" in x]

    print(
        f"Processing {len(ga_files)} G/A files over {len(log_files)} log files:")

    results = []

    tasks = []
    ix = 0
    for log_file in log_files:
        t = {'ix': ix,
             'ga_files': ga_files,
             'log_file': log_file,
             'main_defs': default_main_defs,
             'ga_motor': default_ga_motor}
        tasks.append(t)
        ix += 1

    with mp.Pool(5) as p:
        results = (p.map(run_one_log_eval, tasks))

    return results


if __name__ == '__main__':
    ts = datetime.datetime.now()
    test_run_one_log_eval()
    exit()
    res = mass_eval()

    for r in res:
        print("-------------------------------------------------------------------------------------------------")
        print(r['ix'], len(r['row']))

    te = datetime.datetime.now()
    print(f"Time {(te-ts).total_seconds()}")
