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


def path_finder(i):
    process = subprocess.Popen(f"grep -rin --include=indexes.conf '{i}' . ",
                               shell=True,
                               stdout=subprocess.PIPE,
                               )
    list_path=process.communicate()[0].decode("utf-8").split('\n')
    final_paths=[]
    for k in list_path:
        final_paths.append(k.split(':')[0])
    final_paths.remove('')
    final_paths=set(final_paths)
    for j in final_paths:
        print(GREEN+f"Index definition present at = {j}"+ENDC)

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
    DDAA_flag=True
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
                print(GREEN+"Recomended config change Path for bulk change = /opt/splunk/etc/slave-apps/_cluster_admin/local/indexes.conf"+ENDC)
            else :
                print("current path =", paths)
                print(GREEN+"config change Path = /opt/splunk/etc/slave-apps/_cluster_admin/local/indexes.conf"+ENDC)
            if "1" in data_req or "15" in data_req:
                try:
                    result = list_files[list_files.index("archiver.enableDataArchive") + 2].split('\\n')[0]
                    if result == 'false':
                        DDAA_flag = False
                        print(RED + "DDAA Enabled =", result + ENDC)
                    else:
                        print("DDAA Enabled =", GREEN,result,ENDC)
                except:
                    print(YELL + 'DDAA parameter has not been set' + ENDC)
            if "2" in data_req or "15" in data_req :
                try:
                    if DDAA_flag == False:
                        print(RED+"maxDataArchiveRetentionPeriod is not available as DDAA is disabled"+ENDC)
                    else:
                        print("DDAA RetentionPeriod =",
                          list_files[list_files.index('archiver.maxDataArchiveRetentionPeriod') + 2].split('\\n')[0])
                except:
                    print(YELL + 'maxDataArchiveRetentionPeriod parameter has not been set' + ENDC)
            if "3" in data_req or "15" in data_req:
                try:
                    if list_files[list_files.index('disabled') + 2].split('\\n')[0] == 'true':
                        print(RED+"Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0]+ENDC)
                    else:
                        print("Disabled =", list_files[list_files.index('disabled') + 2].split('\\n')[0])
                except:
                    print(GREEN + 'Index is not disabled' + ENDC)
            if "4" in data_req or "15" in data_req:
                try:
                    print("frozenTimePeriodInSecs =",
                          list_files[list_files.index('frozenTimePeriodInSecs') + 2].split('\\n')[0])
                except:
                    print(YELL + "frozenTimePeriodInSecs parameter has not been set" + ENDC)
            if "5" in data_req or "15" in data_req:
                try:
                    print("maxGlobalDataSizeMB =", list_files[list_files.index('maxGlobalDataSizeMB') + 2].split('\\n')[0])
                except:
                    print(YELL + "maxGlobalDataSizeMB parameter has not been set" + ENDC)
            if "6" in data_req or "15" in data_req:
                try:
                    print("maxTotalDataSizeMB =", list_files[list_files.index('maxTotalDataSizeMB') + 2].split('\\n')[0])
                except:
                    print(YELL + "maxTotalDataSizeMB parameter has not been set" + ENDC)
            if "7" in data_req or "15" in data_req:
                try:
                    print("homePath =", list_files[list_files.index('homePath') + 2].split('\\n')[0])
                except:
                    print(YELL + "homePath parameter has not been set" + ENDC)
            if "8" in data_req or "15" in data_req:
                try:
                    print("thawedPath =", list_files[list_files.index('thawedPath') + 2].split('\\n')[0])
                except:
                    print(YELL + "thawedPath parameter has not been set" + ENDC)
            if "9" in data_req or "15" in data_req:
                try:
                    if DDAA_flag == False:
                        print(RED+"coldStorageRetentionPeriod is not availale as DDAA is disabled"+ENDC)
                    else:
                        print("coldStorageRetentionPeriod =",
                      list_files[list_files.index('archiver.coldStorageRetentionPeriod') + 2].split('\\n')[0])
                except:
                    print(YELL + "coldStorageRetentionPeriod parameter has not been set" + ENDC)
            if "10" in data_req or "15" in data_req:
                try:
                    if DDAA_flag==False:
                        print(RED+"coldStorageProvider is not available as DDAA is not enable"+ENDC)
                    else:
                        print("coldStorageProvider =",
                          list_files[list_files.index('archiver.coldStorageProvider') + 2].split('\\n')[0])
                except:
                    print(YELL + "coldStorageProvidere has not been set" + ENDC)
            if "11" in data_req or "15" in data_req:
                try:
                    print("coldPath =", list_files[list_files.index('coldPath') + 2].split('\\n')[0])
                except:
                    print(YELL + "coldPath parameter not set" + ENDC)
            if "12" in data_req or "15" in data_req:
                try:
                    print("repFactor =", list_files[list_files.index('repFactor') + 2].split('\\n')[0])
                except:
                    print(YELL + "repFactor parameter has not been set" + ENDC)
            if "13" in data_req or "15" in data_req:
                try:
                    path_finder(i)
                except:
                    print(YELL + "Path function failed" + ENDC)
            if "14" in data_req or "15" in data_req:
                try:
                    print("DDSS selfStorageBucket =", list_files[list_files.index('archiver.selfStorageBucket') + 2].split('\\n')[0])
                except:
                    print(YELL + "selfStorageBucket parameter has not been set" + ENDC)
                try:
                    print("DDSS selfStorageBucketFolder =", list_files[list_files.index('archiver.selfStorageBucketFolder') + 2].split('\\n')[0])
                except:
                    print(YELL + "selfStorageBucketFolder parameter has not been set" + ENDC)
                try:
                    print("DDSS selfStorageProvider = ", list_files[list_files.index('archiver.archiver.selfStorageProvider') + 2].split('\\n')[0], "\n")
                except:
                    print(YELL + "selfStorageProvider  parameter has not been set" + ENDC)



def index_fetch():
    try:
        print("\n1. DDAA\n2. DDAA RetentionPeriod\n3. Index Disabled\n4. frozenTimePeriodInSecs\n5. maxGlobalDataSizeMB\n6. maxTotalDataSizeMB\n7. homePath\n8. thawedPath\n9. coldStorageRetentionPeriod\n10. coldStorageProvidere\n11. coldPath \n12. repFactor\n13. Index locations\n14. DDSS Parameters\n15. All")
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
    print("1. List All indexes\n2. List all indexes & create index.txt file\n3. Fetch index’s different parameters")
    choice = str(input())
    if choice == '1':
        list_all_indexes()
    elif choice == '2':
        list_all_indexes_write()
    elif choice == '3':
        index_fetch()
    else:
        print(RED+"Invalid Choice"+ENDC)