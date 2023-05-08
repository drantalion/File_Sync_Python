import os # Module for interacting with the operating system
import shutil # Module for high-level operations with files
import time # Module for various time-related functions
import schedule # Third party api job scheduler
import logging # Module for exporting statements to a log file
import argparse # Module for proccesing command line instructions

# Get the current working directory path:
print("SYNC ON. Current path is:\n",os.getcwdb())

# Command line info
print("Please run using the following arguments:")
print("default: python main.py /path/to/source/folder /path/to/replica/folder --interval 10 --log /path/to/log/file")

# Create parsing command line arguments
parser = argparse.ArgumentParser(description='File sync.')
parser.add_argument('source_folder', type=str, help='Path to source folder.')
parser.add_argument('replica_folder', type=str, help='Path to replica folder.')
parser.add_argument('--interval', type=int, default=10, help='Sync interval in seconds (default: 10)')
parser.add_argument('--log', type=str, default='sync_log_file.txt', help='path to log file (default: sync_long_file.txt)')
args = parser.parse_args()

# Create logger object
logger = logging.getLogger('sync_logger')
logger.setLevel(logging.DEBUG)

# Create file handler for the log file
file_handler = logging.FileHandler('sync_log_file.txt')

# Create formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def sync_folders():
    # Define the folder path:
    source_path = args.source_folder
    replica_path = args.replica_folder

    # Create and verify if the folders do exist:
    if not os.path.exists(source_path) and not os.path.exists(replica_path):
        os.makedirs(source_path)
        os.makedirs(replica_path)
        print("Source and Replica folders had been created.")
        logger.info("Source and Replica folders had been created.")

    elif os.path.exists(source_path) and os.path.exists(replica_path):
        print("Source and Replica folders already exist.")
        logger.info("Source and Replica folders already exist.")
    
    elif os.path.exists(source_path):
        os.makedirs(replica_path)
        print("Replica folder not found, a new one has been created.")
        logger.info("Replica folder not found, a new one has been created.")

    elif not os.path.exists(source_path) and os.path.exists(replica_path):
        os.makedirs(source_path)
        print("Source folder not found, a new one has been created.")
        logger.info("Source folder not found, a new one has been created.")
    
    else:
        print("Unknown error, cannot create folder!")
        logger.info("Unknown error, cannot create folder!")

    # Get files, folders from the source folder (does not cover the hidden files)
    files = []
    folders = []

    for item in os.listdir(source_path):
        item_path = os.path.join(source_path, item)
        replica_item_path = os.path.join(replica_path, item)

        # Check if item exists in replica folder:
        if not os.path.exists(replica_item_path):
            
            # Copy the file/folder to the replica folder if it doesn't exist
            if os.path.isfile(item_path):
                shutil.copy2(item_path, replica_item_path)
                print(f"Copied file {item} to replica folder.")
                logger.info("Copied file %s to replica folder.", item)

            elif os.path.isdir(item_path):
                shutil.copytree(item_path, replica_item_path)
                print(f"Copied folder {item} to replica folder.")
                logger.info("Copied folder %s to replica folder.", item)

        # Check timestamps and update the replica file/folder if necessary:
        source_time = os.stat(item_path).st_mtime
        replica_time = os.stat(replica_item_path).st_mtime

        if source_time > replica_time:

            if os.path.isfile(item_path):
                shutil.copy2(item_path, replica_item_path)
                print(f"Updated file {item} in replica folder.")
                logger.info("Updated file %s in replica folder.", item)
            
            elif os.path.isdir(item_path):
                shutil.rmtree(replica_item_path)
                shutil.copytree(item_path, replica_item_path)
                print(f"Updated folder {item} in replica folder.")
                logger.info("Updated folder %s in replica folder.", item)
        else:
            print(f"{item} is up-to-date in replica folder.")
            logger.info("%s is up-to-date in replica folder.", item)

        # Read files/folders in the source folder:
        if os.path.isfile(item_path):
            files.append(item)

        elif os.path.isdir(item_path):
            folders.append(item)

    # Check if there are any files/folders in the replica folder
    # that don't exist in the source folder
    for item in os.listdir(replica_path):
        item_path = os.path.join(replica_path, item)
        source_item_path = os.path.join(source_path, item)

        if not os.path.exists(source_item_path):
            
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file {item} from replica folder.")
                logger.info("Deleted file %s from replica folder.", item)
            
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted folder {item} from replica folder.")
                logger.info("Deleted folder %s from replica folder.", item)

    # Print the list of files and folders in the source folder.
    print("Source folder contains:")
    print("Files:", files)
    print("Folders:", folders)
    logger.info("Source folder contains: Files: %s Folders: %s", files, folders)


# Schedule the synchronization to run every 10 seconds:
schedule.every(10).seconds.do(sync_folders)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(args.interval)