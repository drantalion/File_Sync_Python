# File_Sync_Python
A little script using os,shutil,time,schedule,logging,argparse modules in Python for syncing a source folder with a replica folder in windows.
Please install a virtual env and pip install schedule for the scheduler module.
A default command arguments run line would look like:
python main.py Source Replica --interval 10 --log sync_file_log.txt
