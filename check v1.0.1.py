import subprocess
def index_Btool(index):
    for i in index:
        list_files = subprocess.run(['splunk', 'btool', 'indexes', 'list', '{}'.format(i), '--debug'],
                                    capture_output=True)
        if list_files.stdout == b'':
            print("\n index {} might be removed or does not exist \n".format(i))
            continue
        else:
            list_files = str(list_files.stdout).split()
            print("\ndetails of index {}".format(i))
            print("==============================\n")
            print('Path (Highest priority conf) = ', list_files[0].split("'")[1])
            try:
                print("DDAA Enabled =", list_files[list_files.index("archiver.enableDataArchive") + 2].split('\\n')[0])
            except:
                print('check DDAA status manually')
            try:
                print("RetentionPeriod =",
                      list_files[list_files.index('archiver.maxDataArchiveRetentionPeriod') + 2].split('\\n')[0])
            except:
                print('check RetentionPeriod  manually')
            try:
                print("Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0])
            except:
                print('Disabled parameter is not present')
            try:
                print("frozenTimePeriodInSecs =",
                      list_files[list_files.index('frozenTimePeriodInSecs') + 2].split('\\n')[0])
            except:
                print("check frozenTimePeriodInSecs manually")
            try:
                print("maxGlobalDataSizeMB =", list_files[list_files.index('maxGlobalDataSizeMB') + 2].split('\\n')[0])
            except:
                print("check maxGlobalDataSizeMB manually")
            try:
                print("maxTotalDataSizeMB =", list_files[list_files.index('maxTotalDataSizeMB') + 2].split('\\n')[0])
            except:
                print("check maxTotalDataSizeMB manually", "\n")
            try:
                print("homePath =", list_files[list_files.index('homePath') + 2].split('\\n')[0])
            except:
                print("check homePath manually", "\n")
            try:
                print("thawedPath =", list_files[list_files.index('thawedPath') + 2].split('\\n')[0])
            except:
                print("check thawedPath manually", "\n")
            try:
                print("archiver.coldStorageRetentionPeriod =", list_files[list_files.index('archiver.coldStorageRetentionPeriod') + 2].split('\\n')[0])
            except:
                print("check archiver.coldStorageRetentionPeriod manually", "\n")
            try:
                print("archiver.coldStorageProvider =", list_files[list_files.index('archiver.coldStorageProvider') + 2].split('\\n')[0])
            except:
                print("check archiver.coldStorageProvidere manually", "\n")
            try:
                print("coldPath =", list_files[list_files.index('coldPath') + 2].split('\\n')[0],"\n")
            except:
                print("check coldPath manually", "\n")


try:
    print("\nenter 1 if you want to enter indexes with through CLI ")
    print("enter 2 if you have created index.txt ")
    choice=str(input("Please enter your option : "))
    if choice=='1':
        index=input("enter index name separated by ',' in single line : ").split(',')
        index_Btool(index)
    elif choice=='2':
        try:
            file_indexes = open("index.txt", "r")
        except:
            print("index.txt doesn't exist")

        index=file_indexes.read()
        index=index.split()
        index_Btool(index)
    else:
        print("invalid choice")
except:
    print("Something went wrong.")

