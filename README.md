A program that synchronizes two folders: source and replica.
The program maintains a complete, identical copy of the source folder in the replica folder. 
Synchronization is one-way (after synchronization, the contents of the replica folder are changed so that they exactly match the contents of the original folder)
Synchronization is performed periodically.
File creation/copy/deletion operations are recorded in the file and on the console output;
Folder paths, sync interval, and log file path are provided via command line arguments. 
Test example (python main.py /path/to/source /path/to/replica --interval 10 --log /path/to/LogFile.log) 
This code does not use third-party libraries that implement folder synchronization. But the external watchdog library is used.
