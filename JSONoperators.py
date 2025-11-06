import json
import Functions as fn
import os
import streamlit as st
import datetime
#from EmailNotificationSystem import NotifyUser
#from ArduinoComms import FillingActClose

'''def file_selector(folder_path='.'):
    filename = st.file_uploader(label="Select a spectrum file", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None,
                     kwargs=None, disabled=False)
    return filename'''


def read_spectrum_json(filename):   #function to read array of spectrums from JSON files

    metadata = {}
    spectrum_list = {}            #array of spectrums is presented as dictionaty with time used as key and list of PPM's for each mass used as respective value
    oxygen_list = {}
    custom_names_list = {}
    solutions_list = {}


    handle = open(filename, "r")

    for line in handle:
        if line == "" or line == "\n" or line[0] == "#":
            continue
        #print(line)
        tempdict = json.loads(line)
        match tempdict["class"]:
            case "metadata":
                metadata = tempdict
                assert metadata["is_a_spectrum"] == "True"
            case "spectrum":
                time = tempdict["time"]
                spectrum_array = tempdict["array"]
                try:
                    oxygen = tempdict["oxygen"]
                except:
                    oxygen = 0

                
                try:
                    custom_line_name = tempdict["custom_line_name"]
                    custom_names_list[str(time)] = custom_line_name
                    
                except:
                    pass
                
                try:
                    interpreted_spectrum = tempdict["interpreted_spectrum"]
                    error_factors = tempdict["error_factors"]
                    stdev = tempdict["stdev"]

                    solutions_list[str(time)] = { "interpreted_spectrum":interpreted_spectrum, "error_factors":error_factors, "stdev":stdev  }
                except:
                    solutions_list[str(time)] = None
                    

                spectrum_list[str(time)] = spectrum_array
                oxygen_list[str(time)] = oxygen

    handle.close()
    return metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list



def read_last_spectrums(filename, howmuchspectrums):   # function to get X most recent spectrums from full array


    metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = read_spectrum_json(filename)
    time_list = fn.get_time_list(spectrum_list)  # list of all time moments of spectrums in full array of spectrums
    lng = len(spectrum_list)



    if howmuchspectrums > lng:
        howmuchspectrums = lng


    new_spectrum_list = {}
    new_oxygen_list = {} # only spectrums corresponding to X latest moments of time are appended to new_spectrum_list
    new_custom_names_list = {}
    new_solutions_list = {}
    for i in range(howmuchspectrums):
        new_spectrum_list[str(time_list[lng-i-1])] = spectrum_list[str(time_list[lng-i-1])]
        new_oxygen_list[str(time_list[lng-i-1])] = oxygen_list[str(time_list[lng-i-1])]
        try:
            new_solutions_list[str(time_list[lng-i-1])] = solutions_list[str(time_list[lng-i-1])]
        except:
            new_solutions_list[str(time_list[lng-i-1])] = None

        try:
            new_custom_names_list[str(time_list[lng-i-1])] = custom_names_list[str(time_list[lng-i-1])]
        except:
            pass

    return metadata, new_spectrum_list, new_oxygen_list, new_custom_names_list, new_solutions_list      #new_spectrum_list is returned

def read_last_spectrums_for_time(filename, time_interval):   # function to get X most recent spectrums from full array


    metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = read_spectrum_json(filename)
    time_list = fn.get_time_list(spectrum_list)  # list of all time moments of spectrums in full array of spectrums
    lng = len(spectrum_list)




    new_spectrum_list = {}
    new_oxygen_list = {}
    new_custom_names_list = {}
    new_solutions_list = {}

    i = 0

    while i+1 <= lng:
        new_spectrum_list[str(time_list[lng-i-1])] = spectrum_list[str(time_list[lng-i-1])]
        new_oxygen_list[str(time_list[lng-i-1])] = oxygen_list[str(time_list[lng-i-1])]
        try:
            new_custom_names_list[str(time_list[lng-i-1])] = custom_names_list[str(time_list[lng-i-1])]
        except:
            pass
        try:
            new_solutions_list[str(time_list[lng-i-1])] = solutions_list[str(time_list[lng-i-1])]
        except:
            new_solutions_list[str(time_list[lng-i-1])] = None

        if (time_list[lng-i-1]) < (datetime.datetime.now().timestamp() - time_interval):
            break

        i += 1

    return metadata, new_spectrum_list, new_oxygen_list, new_custom_names_list, new_solutions_list     #new_spectrum_list is returned



def read_GUI_page_settings(filename, self_name):   #function to read settings for given page for GUI from JSON format

    GUI_page_settings = {}

    handle = open(filename, "r")

    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        try:
            tempdict = json.loads(line)
            if tempdict["page_name"] == self_name:  #if page_name in JSON config equals the desired name, settings are returned
                GUI_page_settings = tempdict
        except:
            pass

    handle.close()
    return GUI_page_settings


def read_period_of_time(filename, howmuchspectrums, desired_time):  #function to read X spectrums starting from given moment of time

    metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = read_spectrum_json(filename)
    time_list = fn.get_time_list(spectrum_list)  # list of all time moments of spectrums in full array of spectrums


    lng = len(spectrum_list)
    #time_list.sort()

    t = 0  # counter for finding desired time

    time_found = False #error handler if desired time is bigger than last measurement

    for element in time_list:
        if element >= desired_time: #ineffective search algorithm, fix later?
            time_found = True # finding closest match to desired time
            break
        else:
            t += 1


    if time_found:
        new_spectrum_list = {}
        new_oxygen_list = {} # only spectrums corresponding to desired time boundaries are added to new_spectrum_list
        new_custom_names_list = {}
        for i in range(howmuchspectrums):
                try:
                    new_spectrum_list[str(time_list[t+i])] = spectrum_list[str(time_list[t+i])]
                    new_oxygen_list[str(time_list[t + i])] = oxygen_list[str(time_list[t + i])]
                    try:
                        new_custom_names_list[str(time_list[t + i])] = custom_names_list[str(time_list[t + i])]
                    except:
                        pass
                    
                    try:
                        new_solutions_list[str(time_list[t+i])] = solutions_list[str(time_list[t+i])]
                    except:
                        new_solutions_list[str(time_list[t+i])] = None

                except:
                    pass
    else: # in desired time is bigger than most recent spectrum, only single last spectrum is added to new_spectrum_list
        new_spectrum_list = {}
        new_oxygen_list = {}
        new_custom_names_list = {}
        new_spectrum_list[str(time_list[t-1])] = spectrum_list[str(time_list[t-1])]
        new_oxygen_list[str(time_list[t - 1])] = oxygen_list[str(time_list[t - 1])]
        new_solutions_list = {}
        try:
            new_custom_names_list[str(time_list[t-1])] = custom_names_list[str(time_list[t-1])]
        except:
            pass
        try:
            new_solutions_list[str(time_list[t-1])] = solutions_list[str(time_list[t-1])]
        except:
            new_solutions_list[str(time_list[t-1])] = None


    return metadata, new_spectrum_list, new_oxygen_list, new_custom_names_list, new_solutions_list



def read_period_of_time_wrt_time(filename, time_interval, initial_time):  #function to read X spectrums starting from given moment of time

    metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = read_spectrum_json(filename)
    time_list = fn.get_time_list(spectrum_list)  # list of all time moments of spectrums in full array of spectrums


    lng = len(spectrum_list)
    #time_list.sort()

    t = 0  # counter for finding desired time

    time_found = False #error handler if desired initial time is bigger than last measurement

    for element in time_list:
        if element >= initial_time: #ineffective search algorithm, fix later?
            time_found = True # finding closest match to desired time
            break
        else:
            t += 1


    if time_found:
        new_spectrum_list = {}
        new_oxygen_list = {} # only spectrums corresponding to desired time boundaries are added to new_spectrum_list
        new_custom_names_list = {}
        new_solutions_list = {}

        i=0

        while i+1 <= lng:
            try:
                new_spectrum_list[str(time_list[t + i])] = spectrum_list[str(time_list[t + i])]
                new_oxygen_list[str(time_list[t + i])] = oxygen_list[str(time_list[t + i])]
                try:
                    new_custom_names_list[str(time_list[t + i])] = custom_names_list[str(time_list[t + i])]
                except:
                    pass
                
                try:
                    new_solutions_list[str(time_list[t+i])] = solutions_list[str(time_list[t+i])]
                except:
                    new_solutions_list[str(time_list[t+i])] = None

                if (time_list[lng - i - 1]) < (datetime.datetime.now().timestamp() - time_interval):
                    break

                i += 1


            except:
                pass



    else: # in desired time is bigger than most recent spectrum, only single last spectrum is added to new_spectrum_list
        new_spectrum_list = {}
        new_oxygen_list = {}
        new_custom_names_list = {}
        new_solutions_list = {}
        new_solutions_list = {}

        if len(time_list) > 0:

            new_spectrum_list[str(time_list[t - 1])] = spectrum_list[str(time_list[t-1])]
            new_oxygen_list[str(time_list[t - 1])] = oxygen_list[str(time_list[t - 1])]
            try:
                    new_custom_names_list[str(time_list[t -1])] = custom_names_list[str(time_list[t -1])]
            except:
                    pass
            
            try:
                    new_solutions_list[t-1] = solutions_list[t-1]
            except:
                    new_solutions_list[t-1] = None


    return metadata, new_spectrum_list, new_oxygen_list, new_custom_names_list, new_solutions_list





def read_all_page_numbers(filename):   # function to read all page numbers from JSON config

    page_numbers = []

    handle = open(filename, "r")

    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        tempdict = json.loads(line)
        page_numbers.append(tempdict["page_name"])

    handle.close()

    return page_numbers


def assert_file_exists(filename,default_image_filename=None):
    try:
        handle = open(filename,"r")
        handle.close()
    except:
        os.system(f"touch {filename}")

        if default_image_filename != None:

            handle = open(default_image_filename,"r")
            copy = []
            for line in handle:
                copy.append(line)
            handle.close()

            handle = open(filename,"w")
            for line in copy:
                handle.write(line)
            handle.close()



def MergeJSONConfigs(MainConfig="MainConfig",DefaultMainConfig="DefaultMainConfig"):
    MergedConfig = dict()
    LinesList = []

    #print(123)

    try:
        handle = open(MainConfig,"r")
        MainConfigExist = True
    except:
        MainConfigExist = False

    if MainConfigExist:

        handle = open(MainConfig,"r")
        for line in handle:
            dictline = json.loads(line)
            MergedConfig[dictline["class"]] = dictline
            LinesList.append(dictline["class"])
        handle.close()


        handle = open(DefaultMainConfig,"r")
        for line in handle:
            dictline = json.loads(line)
            if not (dictline["class"] in LinesList):
                MergedConfig[dictline["class"]] = dictline
            else:
                for key in MergedConfig:
                    if (MergedConfig[key])["class"] == dictline["class"]:
                        for entry_key in dictline:
                            try:
                                void = (MergedConfig[key])[entry_key]
                            except:
                                (MergedConfig[key])[entry_key] = dictline[entry_key]


        handle.close()



        handle = open(MainConfig,"w")
        for key in MergedConfig:
            handle.write(  json.dumps(MergedConfig[key])  )
            handle.write("\n")
        handle.close()

    else:
        NewConfig = []
        handle = open(DefaultMainConfig, "r")
        for line in handle:
            NewConfig.append(line)
        handle.close()

        handle = open(MainConfig, "w")
        for line in NewConfig:
            handle.write(line)
        handle.close()









def ReadJSONConfig(linename,entryname=None,config="MainConfig",DefaultMainConfig="DefaultMainConfig"): #function to read a specific entry from specified line in config
    entry = None
    handle = open(config, "r")
    for line in handle:

        if line == "" or line == "\n" or line[0] == "#" or line == None:
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == linename:
            if entryname == None:
                entry = dict_line
                break
            else:
                entry = dict_line[entryname]
                break
    handle.close()

    if entry ==  None:

        handle = open(DefaultMainConfig, "r")
        for line in handle:

            if line == "" or line == "\n" or line[0] == "#" or line == None:
                continue

            dict_line = json.loads(line)
            if dict_line["class"] == linename:
                if entryname == None:
                    entry = dict_line
                    break
                else:
                    entry = dict_line[entryname]
                    break
        handle.close()
    
    if entry == None:
        #NotifyUser("0015", f"Default Config Entry Missing: {linename}, {entryname} (0015)",True)

        #try:
         #   FillingActClose()
        #except:
         #   NotifyUser("0014", f"Default Config Entry Missing; and filling actuator is not responsive (0014)",True)

        raise LookupError(f"{entryname} entry was not found in {linename} line in {config} config")
        

    return entry







def EditJSONConfig(linename,new_string,MainConfig="MainConfig"):
        handle = open(MainConfig,"r")
        newconfig = []
        for line in handle:
                    try:
                        dictline = json.loads(line)
                        if dictline["class"] == linename:
                            newconfig.append((new_string.strip("\n"))+"\n")
                        else:
                            newconfig.append(line)
                    except:
                        pass
        handle.close()

        handle = open(MainConfig,"w")
        for line in newconfig:
                    handle.write(line)
        handle.close()












def read_vsc_log(filename="VSC_log"):   #function to read vaccuum system log from file

    log_dictionary = {}  # log is presented as dictionary w. time used as key

    handle = open(filename, "r")

    for line in handle:
        if line == "" or line == "\n" or line[0] == "#":
            continue
        #print(line)
        tempdict = json.loads(line)
        time = tempdict["time"]
        log_array = tempdict
                

        log_dictionary[str(time)] = log_array

    handle.close()
    return log_dictionary

def read_last_vsc_entries(howmuchspectrums, filename="VSC_log"):   # function to get X most recent spectrums from full array


    log_dictionary = read_vsc_log(filename)
    time_list = fn.get_time_list(log_dictionary)  # list of all time moments of spectrums in full array of spectrums
    lng = len(log_dictionary)
    #time_list.sort()


    if howmuchspectrums > lng:
        howmuchspectrums = lng


    new_log_dictionary = {}
     # only spectrums corresponding to X latest moments of time are appended to new_spectrum_list
    for i in range(howmuchspectrums):
        new_log_dictionary[str(time_list[lng-i-1])] = log_dictionary[str(time_list[lng-i-1])]
        

    return new_log_dictionary      #new_spectrum_list is returned


def read_last_vsc_entries_wrt_time(time_interval,filename="VSC_log"):  # function to get X most recent spectrums from full array

    log_dictionary = read_vsc_log(filename)
    time_list = fn.get_time_list(log_dictionary)  # list of all time moments of spectrums in full array of spectrums
    lng = len(log_dictionary)
    # time_list.sort()

    i = 0

    new_log_dictionary = {}

    while i + 1 <= lng:
        new_log_dictionary[str(time_list[lng - i - 1])] = log_dictionary[str(time_list[lng - i - 1])]

        if (time_list[lng - i - 1]) < (datetime.datetime.now().timestamp() - time_interval):
            break

        i += 1



    return new_log_dictionary  # new_spectrum_list is returned







def read_vsc_period_of_time(howmuchspectrums, desired_time, filename="VSC_log"):  #function to read X spectrums starting from given moment of time

    log_dictionary = read_vsc_log(filename)
    time_list = fn.get_time_list(log_dictionary)  # list of all time moments of spectrums in full array of spectrums


    lng = len(log_dictionary)
    #time_list.sort()

    t = 0  # counter for finding desired time

    time_found = False #error handler if desired time is bigger than last measurement

    for element in time_list:
        if element >= desired_time: #ineffective search algorithm, fix later?
            time_found = True # finding closest match to desired time
            break
        else:
            t += 1


    if time_found:
        new_log_dictionary = {}

        i = 0

        for i in range(howmuchspectrums):
                try:
                    new_log_dictionary[str(time_list[t+i])] = log_dictionary[str(time_list[t+i])]

                except:
                    pass


    else: # in desired time is bigger than most recent spectrum, only single last spectrum is added to new_spectrum_list
        new_log_dictionary = {}
        new_log_dictionary[str(time_list[t-1])] = log_dictionary[str(time_list[t-1])]
        


    return new_log_dictionary


def read_vsc_period_of_time_wrt_time(time_interval, desired_time,
                            filename="VSC_log"):  # function to read X spectrums starting from given moment of time

    log_dictionary = read_vsc_log(filename)
    time_list = fn.get_time_list(log_dictionary)  # list of all time moments of spectrums in full array of spectrums

    lng = len(log_dictionary)
    # time_list.sort()

    t = 0  # counter for finding desired time

    time_found = False  # error handler if desired time is bigger than last measurement

    for element in time_list:
        if element >= desired_time:  # ineffective search algorithm, fix later?
            time_found = True  # finding closest match to desired time
            break
        else:
            t += 1

    if time_found:
        new_log_dictionary = {}
        i = 0

        while i+1 <= lng:
            try:
                new_log_dictionary[str(time_list[t + i])] = log_dictionary[str(time_list[t + i])]

                if (time_list[lng - i - 1]) < (datetime.datetime.now().timestamp() - time_interval):
                    break

                i += 1


            except:
                pass



    else:  # in desired time is bigger than most recent spectrum, only single last spectrum is added to new_spectrum_list

        new_log_dictionary = {}
        if len(time_list) > 0:
            new_log_dictionary[str(time_list[t - 1])] = log_dictionary[str(time_list[t - 1])]

    return new_log_dictionary


def filling_numerical_integration(initial_time, final_time, filename="VSC_log"):  # returns flow in liters
    if (final_time < initial_time):
        return 0

    else:


        log_dictionary = read_vsc_log(filename)

        #print(log_dictionary)
        time_list = fn.get_time_list(log_dictionary)
        #print(type(time_list))

        new_time_list = []

        for element in time_list:
            if (element >= initial_time) and (element <= final_time):
                new_time_list.append(element)


        if len(new_time_list) == 0:
            return 0

        else:

            #print(new_time_list)

            integral = (float((log_dictionary[str(new_time_list[0])])["filling_mfm_flow"]))*(int(new_time_list[0])-initial_time)

            #print(integral)

            integral += (float((log_dictionary[str(new_time_list[len(new_time_list)-1])])["filling_mfm_flow"]))*(final_time - int(new_time_list[len(new_time_list)-1]))

            #print(integral)

            for i in range(len(new_time_list)-1):
                integral += float((log_dictionary[str(new_time_list[i])]["filling_mfm_flow"]))*(int(new_time_list[i+1])-int(new_time_list[i]))
                #print(integral)

            integral = integral/60000  # convert cm3/min * seconds to liters
            return (integral)


if __name__ == "__main__":
    print(filling_numerical_integration(1,20))