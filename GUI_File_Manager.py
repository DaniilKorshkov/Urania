import os

import streamlit as st
import subprocess

import JSONoperators
from JSONoperators import ReadJSONConfig
import json
import stat
import datetime as dt




def if_file_is_spectrum(filename):
    try:
        handle = open(f"{filename}","r")
        for line in handle:
            dictline = json.loads(line)
            if dictline["class"] == "metadata" and dictline["is_a_spectrum"] == "True":
                return True
                break
        handle.close()
        return False

    except:
        return False



def FindAllSpectrums(MainConfig="MainConfig"):
    

    ret = str((subprocess.run(f"ls",capture_output=True)).stdout)

    ret = ret.strip("b")
    ret = ret.strip("'")

    files_list = ret.split("\\n")
    final_files_list = []

    for file in files_list:
        if if_file_is_spectrum(file):
            final_files_list.append(file)

    return final_files_list


def SpectrumsDropdownMenu(MainConfig="MainConfig"):
    final_files_list = FindAllSpectrums(MainConfig)
    ret = st.selectbox("Spectrum file selection menu",final_files_list)
    return ret







def GUI_File_Info(filename,MainConfig="MainConfig"):
    handle = open(filename,"r")
    for line in handle:
        dictline = json.loads(line)
        if dictline["class"] == "metadata":
            valve = dictline["valve_number"]
            init_scan = dictline["initial_value"]
            amt_of_scans = dictline["amount_of_scans"]
            step = dictline["step"]
            accuracy = dictline["accuracy"]
            purge_cycles = dictline["purge_cycles"]

            try:
                #purging_time = dictline["purging_time"]
                #calmdown_time = dictline["calmdown_time"]
                #purging_mfc = dictline["purging_mfc"]
                #calmdown_mfc = dictline["calmdown_mfc"]
                return f"{str(filename)} parameters: \nValve:{valve}; Initial M:{init_scan}, amount of scans:{amt_of_scans}, step:{step}, accuracy:{accuracy}, amount of purge cycles:{purge_cycles}"
            except:
                return f"{str(filename)} parameters: \nValve:{valve}; Initial M:{init_scan}, amount of scans:{amt_of_scans}, step:{step}"


def CreateSpectrum(filelist, MainConfig="MainConfig"):

    first_line = {"class":"metadata","is_a_spectrum":"True"}

    name = st.text_input(label="Type new spectrum name")

    current_date = dt.datetime.now()
    datetime_label = current_date.strftime("%d_%m_%Y")

    name = f"{name}-{datetime_label}"

    valve = st.text_input(label="Type multi inlet valve position")
    init_m = st.text_input(label="Type initial molar mass")
    final_m = st.text_input(label="Type final molar mass")
    step = st.text_input(label="Type step")
    accuracy = st.text_input(label="Enter scan accuracy from 1 to 8 (default - 5)")
    purge_cycles = st.text_input(label="Enter amount of purge cycles (default - 5)")
    minutes_of_scan = st.text_input("How much minutes data is recorded? (for 16 files at a time creation only, otherwise it is specified in TaskManager)")
    M_per_minute = JSONoperators.ReadJSONConfig("spectrometer_parameters","M_per_minute")
    #spectrum_scans = int((M_per_minute*minutes_of_scan)/)

    #purging_time = st.text_input("Type purging time in seconds")
    #calmdown_time = st.text_input("Type calmdown time in seconds")
    #purging_mfc = st.text_input("Type MFC behaviour for purging (open,close or number from 20 to 1000)")
    #purging_mfc = purging_mfc.lower()
    #calmdown_mfc = st.text_input("Type MFC behaviour for calmdown (open,close or number from 20 to 1000)")
    #calmdown_mfc = calmdown_mfc.lower()





    #scans = st.text_input(label="Type amount of scans")




    create_new_spectrum = st.button("Create spectrum")

    if create_new_spectrum:
        spectrum_is_valid = True
        try:
            valve = int(valve)
            assert valve >=1 and valve <= 16
        except:
            spectrum_is_valid = False
            st.write("Valve position is invalid")

        try:
            assert not(name in filelist)
        except:
            spectrum_is_valid = False
            st.write("Spectrum name already exists")

        try:

            init_m = float(init_m)
            step = float(step)
            final_m = float(final_m)
        except:
            spectrum_is_valid = False
            st.write("Not a valid numbers inputed")


        try:
            assert init_m >= 1
        except:
            spectrum_is_valid = False
            st.write("Initial M is less than 1")

        try:
            assert final_m <= 200
        except:
            spectrum_is_valid = False
            st.write("Final M is greater than 200")


        try:
            assert final_m > init_m
        except:
            spectrum_is_valid = False
            st.write("Final M is lesser or equal than initial M")



        try:
            assert step > 0
        except:
            spectrum_is_valid = False
            st.write("Step is less or equal than zero")




        try:
            scans = int((final_m-init_m)/step) + 1
            if scans < 1:
                scans = 1
        except:
            spectrum_is_valid = False
            st.write("Failed to calculate scan amount")





        try:
            if accuracy == None or accuracy == "":
                accuracy = 5
            accuracy = int(accuracy)

            accuracy_is_int = True

        except:
            spectrum_is_valid = False
            st.write("Provided accuracy is not a valid number")
            accuracy_is_int = False

        if accuracy_is_int:
            try:

                assert accuracy >= 1

            except:
                spectrum_is_valid = False
                st.write("Provided accuracy is less than one")

            try:

                assert accuracy <= 8

            except:
                spectrum_is_valid = False
                st.write("Provided accuracy is greater than eight")



        try:
            if purge_cycles == None or purge_cycles == "":
                purge_cycles = 5
            purge_cycles = int(purge_cycles)

            if purge_cycles < 1:
                purge_cycles = 1


        except:
            spectrum_is_valid = False
            st.write("Provided amount of purge cycles is not an integer")








        #try:
         #   calmdown_time = int(calmdown_time)
          #  if calmdown_time < 1:
          #      calmdown_time = 1
          #      st.write("Calmdown time set to 1")
        #except:
         #   spectrum_is_valid = False
         #   st.write("Invalid calmdown time")

        #try:
         #   purging_time = int(purging_time)
          #  if purging_time < 1:
        #        purging_time = 1
         #       st.write("Purging time set to 1")
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid calmdown time")



        #try:


         #   if not ( (calmdown_mfc == "open") or (calmdown_mfc == "close")):
          #      calmdown_mfc = int(calmdown_mfc)
           #     assert calmdown_mfc > 19
            #    assert  calmdown_mfc < 1001
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid calmdown MFC behaviour")

        #try:
         #   if not ((purging_mfc == "open") or (purging_mfc == "close")):
          #      purging_mfc = int(purging_mfc)
           #     assert purging_mfc > 19
            #    assert  purging_mfc < 1001
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid purging MFC behaviour")





        if spectrum_is_valid:

            first_line["valve_number"] = valve
            first_line["initial_value"] = init_m
            first_line["amount_of_scans"] = scans
            first_line["step"] = step
            first_line["accuracy"] = accuracy
            first_line["purge_cycles"] = purge_cycles

            #first_line["purging_time"] = purging_time
            #first_line["calmdown_time"] = calmdown_time
            #first_line["purging_mfc"] = purging_mfc
            #first_line["calmdown_mfc"] = calmdown_mfc

            line = json.dumps(first_line)


            handle = open(name,"w")
            handle.close()

            os.system(f"sudo chmod 777 {name}")

            '''ret = str((subprocess.run(f"whoami", capture_output=True)).stdout)
            ret = ret.strip("b")
            ret = ret.strip("'")

            os.system(f"sudo chown {ret}")'''

            handle = open(name, "w")
            handle.write(line)
            handle.close()

            os.system(f"sudo chmod 777 {name}")



    create_16_spectrums = st.button("Create 16 equivalent spectrums and corresponding tasks")

    if create_16_spectrums:
        spectrum_is_valid = True


        try:
            for i in range(16):
                assert not(f"{i+1}_{name}" in filelist)
        except:
            spectrum_is_valid = False
            st.write("Spectrum name already exists")

        try:

            init_m = float(init_m)
            step = float(step)
            final_m = float(final_m)
        except:
            spectrum_is_valid = False
            st.write("Not a valid numbers inputed")


        try:
            assert init_m >= 1
        except:
            spectrum_is_valid = False
            st.write("Initial M is less than 1")

        try:
            assert final_m <= 200
        except:
            spectrum_is_valid = False
            st.write("Final M is greater than 200")


        try:
            assert final_m > init_m
        except:
            spectrum_is_valid = False
            st.write("Final M is lesser or equal than initial M")



        try:
            assert step > 0
        except:
            spectrum_is_valid = False
            st.write("Step is less or equal than zero")




        try:
            scans = int((final_m-init_m)/step) + 1
            if scans < 1:
                scans = 1
        except:
            spectrum_is_valid = False
            st.write("Failed to calculate scan amount")


        try:


            spectrum_scans = int(minutes_of_scan)*60
            if spectrum_scans == 0:
                spectrum_scans = 1
        except:
            spectrum_is_valid = False
            st.write("Failed to calculate required amount of scans")





        try:
            if accuracy == None or accuracy == "":
                accuracy = 5
            accuracy = int(accuracy)

            accuracy_is_int = True

        except:
            spectrum_is_valid = False
            st.write("Provided accuracy is not a valid number")
            accuracy_is_int = False



        if accuracy_is_int:
            try:

                assert accuracy >= 1

            except:
                spectrum_is_valid = False
                st.write("Provided accuracy is less than one")



            try:

                assert accuracy <= 8

            except:
                spectrum_is_valid = False
                st.write("Provided accuracy is greater than eight")



        try:
            if purge_cycles == None or purge_cycles == "":
                purge_cycles = 5
            purge_cycles = int(purge_cycles)

            if purge_cycles < 1:
                purge_cycles = 1


        except:
            spectrum_is_valid = False
            st.write("Provided amount of purge cycles is not an integer")





        #try:
         #   calmdown_time = int(calmdown_time)
          #  if calmdown_time < 1:
         #       calmdown_time = 1
          #      st.write("Calmdown time set to 1")
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid calmdown time")

        #try:
        #    purging_time = int(purging_time)
        #    if purging_time < 1:
         #       purging_time = 1
         #       st.write("Purging time set to 1")
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid calmdown time")


        #try:

         #   if not ((calmdown_mfc == "open") or (calmdown_mfc == "close")):
          #      calmdown_mfc = int(calmdown_mfc)
           #     assert calmdown_mfc > 19
            #    assert  calmdown_mfc < 1001
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid calmdown MFC behaviour")

        #try:
         #   if not ((purging_mfc == "open") or (purging_mfc == "close")):
          #      purging_mfc = int(purging_mfc)
           #     assert purging_mfc > 19
            #    assert  purging_mfc < 1001
        #except:
         #   spectrum_is_valid = False
          #  st.write("Invalid purging MFC behaviour")





        if spectrum_is_valid:

            filename_list = []

            for i in range(16):

                first_line["valve_number"] = i+1
                first_line["initial_value"] = init_m
                first_line["amount_of_scans"] = scans
                first_line["step"] = step

                first_line["accuracy"] = accuracy
                first_line["purge_cycles"] = purge_cycles

                #first_line["purging_time"] = purging_time
                #first_line["calmdown_time"] = calmdown_time
                #first_line["purging_mfc"] = purging_mfc
                #first_line["calmdown_mfc"] = calmdown_mfc

                newname = f"{i+1}_{name}"

                line = json.dumps(first_line)

                handle = open(newname, "w")
                handle.close()

                os.system(f"sudo chmod 777 {newname}")

                '''ret = str((subprocess.run(f"whoami", capture_output=True)).stdout)
                ret = ret.strip("b")
                ret = ret.strip("'")

                os.system(f"sudo chown {ret}")'''

                handle = open(newname, "w")
                handle.write(line)
                handle.close()

                os.system(f"sudo chmod 777 {newname}")

                filename = newname
                filename_list.append(newname)





                new_task_data = {"class": "task", "name": newname, "type": "regular", "valve_position": i+1,
                                 "filename": filename,
                                 "scans": spectrum_scans}




                newfile = []

                handle = open("TaskList", "r")
                for line in handle:
                    newfile.append(line)
                newfile.append(str(json.dumps(new_task_data) + "\n"))

                handle.close()

                handle = open("TaskList", "w")

                for line in newfile:
                    handle.write(line)
                handle.close()


















def SpectrumFileManager(MainConfig="MainConfig"):
    filelist = FindAllSpectrums(MainConfig)
    st.write("Parameters of all spectrum files:")
    st.markdown("")
    for file in filelist:
        try:
            line = GUI_File_Info(file,MainConfig)
            st.write(line)
        except:
            pass


    for i in range(4):
        st.markdown("")

    st.write("Create new spectrum file:")
    CreateSpectrum(filelist,MainConfig)






