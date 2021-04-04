import subprocess

YELL = '\033[93m'
ENDC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'


# def find_path(string1):
#     print(string1)
#     list_path = []
#     for i in string1:
#         if "indexes.conf" in i:
#             list_path.append(i)
#     list_path[0] = list_path[0].split("'")[1]
#
#     for i in range(1, len(list_path)):
#         list_path[i] = list_path[i].split('\\n')[1]
#     list_path = list(set(list_path))
#     return list_path


def list_all_indexes():
    # indexes = subprocess.Popen(['splunk','btool','indexes','list','|','grep','"\[*\]"'],
    #                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process = subprocess.Popen("splunk btool indexes list | grep '\[*\]'",
                               shell=True,
                               stdout=subprocess.PIPE,
                               )
    stdout_list = process.communicate()[0].decode("utf-8").replace("vix.splunk.search.recordreader.csv.regex = \.([tc]sv)(?:\.(?:gz|bz2|snappy))?$",'').replace('[','').replace(']','')
    print(stdout_list)

def list_all_indexes_write():
    process = subprocess.Popen("splunk btool indexes list | grep '\[*\]'",
                               shell=True,
                               stdout=subprocess.PIPE,
                               )
    stdout_list = process.communicate()[0].decode("utf-8").replace("vix.splunk.search.recordreader.csv.regex = \.([tc]sv)(?:\.(?:gz|bz2|snappy))?$",'').replace('[','').replace(']','')
    print(stdout_list)
    try:
        file = open("index.txt", 'w')
        file.write(stdout_list)
        print(GREEN+"File written succesfully"+ENDC)
    except:
        print(RED+"something went wrong!"+ENDC)
def index_Btool(index,data_req):
    for i in index:
        list_files = subprocess.run(['splunk', 'btool', 'indexes', 'list', '{}'.format(i), '--debug'],
                                    capture_output=True)
        if list_files.stdout == b'':
            print(RED + "\n index {} might be removed or does not exist \n".format(i) + ENDC)
            continue
        else:
            list_files = str(list_files.stdout).split()
            paths=list_files[0].replace("b'","")
            print("\ndetails of index {}".format(i))
            print("==============================","\n")
            P_l=paths.split('/')
            if 'local' in P_l and '_cluster_admin' in P_l:
                print("current path =",paths)
                print(GREEN+"config change path =",paths+ENDC)
            elif 'local' in P_l:
                print("current path =",paths)
                print(GREEN+"config change path =", paths+ENDC)
                print(GREEN+"Recomended config change Path = /opt/splunk/etc/slave-apps/_cluster_admin/local/indexes.conf"+ENDC)
            else :
                print("current path =", paths)
                print(GREEN+"config change Path = /opt/splunk/etc/slave-apps/_cluster_admin/local/indexes.conf"+ENDC)
            if "1" or '12'in data_req:
                try:
                    result = list_files[list_files.index("archiver.enableDataArchive") + 2].split('\\n')[0]
                    if result == 'false':
                        print(RED + "DDAA Enabled =", result + ENDC)
                    else:
                        print("DDAA Enabled =", GREEN,result,ENDC)
                except:
                    print(YELL + 'DDAA parameter not found check manually' + ENDC)
            if "2" or '12' in data_req:
                try:
                    print("RetentionPeriod =",
                          list_files[list_files.index('archiver.maxDataArchiveRetentionPeriod') + 2].split('\\n')[0])
                except:
                    print(YELL + 'parameter not found check manually' + ENDC)
            if "3" or '12' in data_req:
                try:
                    if list_files[list_files.index('disabled') + 2].split('\\n')[0] == 'true':
                        print(RED+"Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0]+ENDC)
                    else:
                        print("Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0])
                except:
                    print(YELL + 'Disabled parameter not found check manually' + ENDC)
            if "4" or '12' in data_req:
                try:
                    print("frozenTimePeriodInSecs =",
                          list_files[list_files.index('frozenTimePeriodInSecs') + 2].split('\\n')[0])
                except:
                    print(YELL + "frozenTimePeriodInSecs parameter not found check manually" + ENDC)
            if "5" or '12' in data_req:
                try:
                    print("maxGlobalDataSizeMB =", list_files[list_files.index('maxGlobalDataSizeMB') + 2].split('\\n')[0])
                except:
                    print(YELL + "maxGlobalDataSizeMB parameter not found check manually" + ENDC)
            if "6" or '12' in data_req:
                try:
                    print("maxTotalDataSizeMB =", list_files[list_files.index('maxTotalDataSizeMB') + 2].split('\\n')[0])
                except:
                    print(YELL + "maxTotalDataSizeMB parameter not found check manually" + ENDC)
            if "7" or '12' in data_req:
                try:
                    print("homePath =", list_files[list_files.index('homePath') + 2].split('\\n')[0])
                except:
                    print(YELL + "homePath parameter not found check manually" + ENDC)
            if "8" or '12' in data_req:
                try:
                    print("thawedPath =", list_files[list_files.index('thawedPath') + 2].split('\\n')[0])
                except:
                    print(YELL + "thawedPath parameter not found check manually" + ENDC)
            if "9" or '12' in data_req:
                try:
                    print("coldStorageRetentionPeriod =",
                      list_files[list_files.index('archiver.coldStorageRetentionPeriod') + 2].split('\\n')[0])
                except:
                    print(YELL + "coldStorageRetentionPeriod parameter not found check manually" + ENDC)
            if "10" or '12' in data_req:
                try:
                    print("coldStorageProvider =",
                          list_files[list_files.index('archiver.coldStorageProvider') + 2].split('\\n')[0])
                except:
                    print(YELL + "coldStorageProvidere parameter not found check manually" + ENDC)
            if "11" or '12' in data_req:
                try:
                    print("coldPath =", list_files[list_files.index('coldPath') + 2].split('\\n')[0], "\n")
                except:
                    print(YELL + "coldPath parameter not found check manually" + ENDC)

def index_fetch():
    try:
        print("\n1. DDAA\n2. RetentionPeriod\n3. Index Disabled\n4. frozenTimePeriodInSecs\n5. maxGlobalDataSizeMB\n6. maxTotalDataSizeMB\n7. homePath\n8. thawedPath\n9. coldStorageRetentionPeriod\n10. coldStorageProvidere\n11. coldPath \n12. All")
        print("example input : 1,2,3\n")
        print("Select parameters that you want to get in output:")
        data_req=input().split(',')
        print("\nenter 1 if you want to enter indexes with through CLI ")
        print("enter 2 if you have created index.txt ")
        choice = str(input("Please enter your option : "))
        if choice == '1':
            index = input("enter index name separated by ',' in single line : ").split(',')
            index_Btool(index,data_req)
        elif choice == '2':
            try:
                file_indexes = open("index.txt", "r")
            except:
                print("index.txt doesn't exist")

            index = file_indexes.read()
            index = index.split()
            index_Btool(index,data_req)
        else:
            print(RED + "invalid choice" + ENDC)
    except:
        print(RED + "Something went wrong." + ENDC)


if __name__=='__main__':
    print("select option from below:")
    print("1. List All indexes\n2. List all indexes & create index.txt file\n3. Fetch index details")
    choice = str(input())
    if choice == '1':
        list_all_indexes()
    elif choice == '2':
        list_all_indexes_write()
    elif choice == '3':
        index_fetch()
    else:
        print(RED+"Invalid Choice"+ENDC)