import subprocess

YELL = '\033[93m'
ENDC = '\033[0m'
RED = '\033[91m'


def index_Btool(index):
    for i in index:
        list_files = subprocess.run(['splunk', 'btool', 'indexes', 'list', '{}'.format(i), '--debug'],
                                    capture_output=True)
        print(list_files)
        if list_files.stdout == b'':
            print(RED + "\n index {} might be removed or does not exist \n".format(i) + ENDC)
            continue
        else:
            list_files = str(list_files.stdout).split()
            print("\ndetails of index {}".format(i))
            print("==============================\n")
            print('Path (Highest priority conf) = ', list_files[0].split("'")[1])
            try:
                result = list_files[list_files.index("archiver.enableDataArchive") + 2].split('\\n')[0]
                if result == 'false':
                    print(RED + "DDAA Enabled =", result + ENDC)
                else:
                    print("DDAA Enabled =", result)
            except:
                print(YELL + 'check DDAA status manually' + ENDC)
            try:
                print("RetentionPeriod =",
                      list_files[list_files.index('archiver.maxDataArchiveRetentionPeriod') + 2].split('\\n')[0])
            except:
                print(YELL + 'check RetentionPeriod  manually' + ENDC)
            try:
                print("Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0])
            except:
                print(YELL + 'Disabled parameter is not present' + ENDC)
            try:
                print("frozenTimePeriodInSecs =",
                      list_files[list_files.index('frozenTimePeriodInSecs') + 2].split('\\n')[0])
            except:
                print(YELL + "check frozenTimePeriodInSecs manually" + ENDC)
            try:
                print("maxGlobalDataSizeMB =", list_files[list_files.index('maxGlobalDataSizeMB') + 2].split('\\n')[0])
            except:
                print(YELL + "check maxGlobalDataSizeMB manually" + ENDC)
            try:
                print("maxTotalDataSizeMB =", list_files[list_files.index('maxTotalDataSizeMB') + 2].split('\\n')[0])
            except:
                print(YELL + "check maxTotalDataSizeMB manually" + ENDC)
            try:
                print("homePath =", list_files[list_files.index('homePath') + 2].split('\\n')[0])
            except:
                print(YELL + "check homePath manually" + ENDC)
            try:
                print("thawedPath =", list_files[list_files.index('thawedPath') + 2].split('\\n')[0])
            except:
                print(YELL + "check thawedPath manually" + ENDC)
            try:
                print("archiver.coldStorageRetentionPeriod =",
                      list_files[list_files.index('archiver.coldStorageRetentionPeriod') + 2].split('\\n')[0])
            except:
                print(YELL + "check archiver.coldStorageRetentionPeriod manually" + ENDC)
            try:
                print("archiver.coldStorageProvider =",
                      list_files[list_files.index('archiver.coldStorageProvider') + 2].split('\\n')[0])
            except:
                print(YELL + "check archiver.coldStorageProvidere manually" + ENDC)
            try:
                print("coldPath =", list_files[list_files.index('coldPath') + 2].split('\\n')[0], "\n")
            except:
                print(YELL + "check coldPath manually" + ENDC)


try:
    print("\nenter 1 if you want to enter indexes with through CLI ")
    print("enter 2 if you have created index.txt ")
    choice = str(input("Please enter your option : "))
    if choice == '1':
        index = input("enter index name separated by ',' in single line : ").split(',')
        index_Btool(index)
    elif choice == '2':
        try:
            file_indexes = open("index.txt", "r")
        except:
            print("index.txt doesn't exist")

        index = file_indexes.read()
        index = index.split()
        index_Btool(index)
    else:
        print(RED + "invalid choice" + ENDC)
except:
    print(RED + "Something went wrong." + ENDC)