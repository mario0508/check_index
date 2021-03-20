import subprocess

YELL = '\033[93m'
ENDC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'


def find_path(string1):
    list_path = []
    for i in string1:
        if "indexes.conf" in i:
            list_path.append(i)
    list_path[0] = list_path[0].split("'")[1]

    for i in range(1, len(list_path)):
        list_path[i] = list_path[i].split('\\n')[1]
    list_path = list(set(list_path))
    return list_path



def index_Btool(index):
    for i in index:
        list_files = subprocess.run(['splunk', 'btool', 'indexes', 'list', '{}'.format(i), '--debug'],
                                    capture_output=True)
        if list_files.stdout == b'':
            print(RED + "\n index {} might be removed or does not exist \n".format(i) + ENDC)
            continue
        else:
            list_files = str(list_files.stdout).split()
            paths=find_path(list_files)
            print("\ndetails of index {}".format(i))
            print("==============================","\n")
            for i in range(len(paths)):
                if i==0:
                    print(GREEN+'Path (Highest priority conf) = ', paths[i]+ENDC)
                else:
                    print('other available paths = ', paths[i])
            try:
                result = list_files[list_files.index("archiver.enableDataArchive") + 2].split('\\n')[0]
                if result == 'false':
                    print(RED + "DDAA Enabled =", result + ENDC)
                else:
                    print("DDAA Enabled =", GREEN,result,ENDC)
            except:
                print(YELL + ' DDAA parameter not found check manually' + ENDC)
            try:
                print("RetentionPeriod =",
                      list_files[list_files.index('archiver.maxDataArchiveRetentionPeriod') + 2].split('\\n')[0])
            except:
                print(YELL + 'parameter not found check manually' + ENDC)
            try:
                if list_files[list_files.index('disabled') + 2].split('\\n')[0] == 'true':
                    print(RED+"Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0]+ENDC)
                else:
                    print("Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0])
            except:
                print(YELL + 'Disabled parameter not found check manually' + ENDC)
            try:
                print("frozenTimePeriodInSecs =",
                      list_files[list_files.index('frozenTimePeriodInSecs') + 2].split('\\n')[0])
            except:
                print(YELL + " frozenTimePeriodInSecs parameter not found check manually" + ENDC)
            try:
                print("maxGlobalDataSizeMB =", list_files[list_files.index('maxGlobalDataSizeMB') + 2].split('\\n')[0])
            except:
                print(YELL + " maxGlobalDataSizeMB parameter not found check manually" + ENDC)
            try:
                print("maxTotalDataSizeMB =", list_files[list_files.index('maxTotalDataSizeMB') + 2].split('\\n')[0])
            except:
                print(YELL + "maxTotalDataSizeMB parameter not found check manually" + ENDC)
            try:
                print("homePath =", list_files[list_files.index('homePath') + 2].split('\\n')[0])
            except:
                print(YELL + "homePath parameter not found check manually" + ENDC)
            try:
                print("thawedPath =", list_files[list_files.index('thawedPath') + 2].split('\\n')[0])
            except:
                print(YELL + "thawedPath parameter not found check manually" + ENDC)
            try:
                print("coldStorageRetentionPeriod =",
                      list_files[list_files.index('archiver.coldStorageRetentionPeriod') + 2].split('\\n')[0])
            except:
                print(YELL + "coldStorageRetentionPeriod parameter not found check manually" + ENDC)
            try:
                print("coldStorageProvider =",
                      list_files[list_files.index('archiver.coldStorageProvider') + 2].split('\\n')[0])
            except:
                print(YELL + "coldStorageProvidere parameter not found check manually" + ENDC)
            try:
                print("coldPath =", list_files[list_files.index('coldPath') + 2].split('\\n')[0], "\n")
            except:
                print(YELL + "coldPath parameter not found check manually" + ENDC)

if __name__=='__main__':
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
