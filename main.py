import os
import shutil
import time
import argparse
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def calculate_file_hash(file_path):
    # Calculate MD5 hash of a file
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


class SyncEventHandler(FileSystemEventHandler):
    def __init__(self, source, replica, log_file):
        super().__init__()
        self.source = source
        self.replica = replica
        self.log_file = log_file

    def on_any_event(self, event):
        if not event.is_directory:
            source_path = event.src_path
            replica_path = os.path.join(self.replica, os.path.relpath(source_path, self.source))
            if event.event_type == 'created':
                shutil.copy2(source_path, replica_path)
                log_to_file(self.log_file, f"Created/Copied: {source_path} to {replica_path}")
                print(f"Created/Copied: {source_path} to {replica_path}")
            elif event.event_type == 'deleted':
                os.remove(replica_path)
                log_to_file(self.log_file, f"Removed: {replica_path}")
                print(f"Removed: {replica_path}")
            elif event.event_type == 'modified':
                shutil.copy2(source_path, replica_path)
                log_to_file(self.log_file, f"Updated/Copied: {source_path} to {replica_path}")
                print(f"Updated/Copied: {source_path} to {replica_path}")



def log_to_file(log_file, message):
    with open(log_file, 'a') as f:
        f.write(f"{time.ctime()}: {message}\n")
    print(message)


def main():
    parser = argparse.ArgumentParser(description='Sync folders')
    parser.add_argument('source', type=str, help='Source folder path')
    parser.add_argument('replica', type=str, help='Replica folder path')
    parser.add_argument('interval', type=int, help='Sync interval in seconds')
    parser.add_argument('log_file', type=str, help='Log file path')
    args = parser.parse_args()

    print(f'Syncing folders {args.source} to {args.replica} every {args.interval} seconds...')

    # Initialize event handler and observer
    event_handler = SyncEventHandler(args.source, args.replica, args.log_file)
    observer = Observer()
    observer.schedule(event_handler, args.source, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(args.interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
