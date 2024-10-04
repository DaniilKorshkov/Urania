import streamlit as st
import os

import GUI_File_Manager
import JSONoperators
from JSONoperators import ReadJSONConfig
import json
import GUI_File_Manager as fm





def display_all_tasks(MainConfig="MainConfig"):

    emergency_task_list = []
    scheduled_task_list = []
    regular_task_list = []
    name_list = []

    handle = open("TaskList","r")
    for line in handle:
        try:
            dictline = json.loads(line)
            if dictline["class"] == "task":
                match dictline["type"]:
                    case "emergency":
                        emergency_task_list.append(dictline)
                    case "scheduled":
                        scheduled_task_list.append(dictline)
                    case "regular":
                        regular_task_list.append(dictline)
                name_list.append(dictline["name"])
            if dictline["class"] == "regular_log":
                metadata = json.loads(line)
        except:
            pass
    handle.close()

    st.write("Emergency Tasks: ")
    st.markdown("")
    for task in emergency_task_list:
        name = task["name"]
        valve = task["valve_position"]
        filename = task["filename"]
        scans = task["scans"]
        execs_left = task["how_much_executions"]
        st.write(f"{name} parameters: valve position:{valve}, spectrum filename: {filename}, scans: {scans}, executions left: {execs_left}")

        delete = st.button(f"delete {name}")

        if delete:
            delete_task(name)

    for i in range(4):
        st.markdown("")


    st.write("Scheduled Tasks: ")
    for task in scheduled_task_list:
        name = task["name"]
        valve = task["valve_position"]
        filename = task["filename"]
        scans = task["scans"]
        freq = task["freq"]
        st.write(f"{name} parameters: valve position:{valve}, spectrum filename: {filename}, scans: {scans}, frequency: {freq}")

        delete = st.button(f"delete {name}")

        if delete:
            delete_task(name)




    for i in range(4):
        st.markdown("")


    task_counter = 0

    st.write("Regular Tasks: ")
    for task in regular_task_list:
        name = task["name"]
        valve = task["valve_position"]
        filename = task["filename"]
        scans = task["scans"]


        st.write(f"{name} parameters: valve position:{valve}, spectrum filename: {filename}, data entries per task: {scans}")
        try:
            file_info = GUI_File_Manager.GUI_File_Info(filename, MainConfig)
            st.write(file_info)
        except:
            pass

        col1,col2,col3=st.columns(3)
        with col1:
            delete = st.button(f"delete {name}")
        with col2:
            move_up = st.button(f"move {name} up")
        with col3:
            move_down = st.button(f"move {name} down")


        if delete:
            delete_task(name)
        if move_up:
            try:
                change_task_position(task_counter,"up",regular_task_list, scheduled_task_list, emergency_task_list, metadata)
            except:
                st.write("Cannot move this task up")
        if move_down:
            try:
                change_task_position(task_counter, "down", regular_task_list, scheduled_task_list, emergency_task_list,
                                 metadata)
            except:
                st.write("Cannot move this task down")









        task_counter += 1


    for i in range(4):
        st.markdown("")

    st.write("Add new task")


# -----------task creation------------------


    task_type = st.radio("Select task type",["regular","emergency","scheduled"])

    name = st.text_input("Enter task name")
    #valve = st.text_input("Enter valve number")
    filename = fm.SpectrumsDropdownMenu()
    minutes_to_scan = st.text_input("How much minutes to scan? ")
    M_per_minute = JSONoperators.ReadJSONConfig("spectrometer_parameters","M_per_minute")


                                #st.text_input("Enter amount of data entries for task")

    match task_type:
        case "emergency":
            executions = st.text_input("How much executions (either integer or 'inf')")
        case "scheduled":
            freq = st.text_input("Enter frequency")
        case "filename":
            pass

    create_task = st.button(f"Create new task")






    if create_task:
        task_is_valid = True
        try:
            assert not(name in name_list)
        except:
            task_is_valid = False
            st.write("Task name already occupied")


        try:
            handle = open(f"{filename}", "r")
            for line in handle:
                dictline = json.loads(line)
                if dictline["class"] == "metadata":
                    M_in_file = int(dictline["amount_of_scans"])

                    break
            handle.close()

            scans = int(int(minutes_to_scan)*M_per_minute/M_in_file)
            if scans < 1:
                scans = 1


        except:
            task_is_valid = False
            st.write("Failed to calculate amount of data entries")



        try:
            scans = int(scans)
            assert scans > 0
        except:
            task_is_valid = False
            st.write("Scans amount is less or equal than zero; or nor an integer")

            #valve = int(valve)
            #assert (valve >=1 and valve <= 16)

        '''try:
            handle = open(filename,"r")
            for line in handle:
                dictline = json.loads(line)
                if dictline["class"] == "metadata":
                    assert dictline["is_a_spectrum"] == "True"
            handle.close()
        except:
            st.write("Filename is not valid")'''

            #scans = int(scans)

        try:
            if task_type == "emergency":
                if executions != "inf":
                    executions = int(executions)
                    assert executions > 0
        except:
            st.write("Invalid amount of executions")
            task_is_valid = False


        try:
            if task_type == "scheduled":

                freq = float(freq)
        except:
            st.write("Invalid freq")
            task_is_valid = False


        if task_is_valid:

            valve = None

            handle = open(filename,"r")
            for line in handle:
                try:
                    dictline = json.loads(line)
                    if dictline["class"] == "metadata":
                        valve = int(dictline["valve_number"])
                        break
                except:
                    pass
            handle.close()

            if valve == None:
                st.write("Failed to extract valve data")
                raise ValueError("Failed to extract valve data")


            new_task_data = {"class": "task","name":name, "type": task_type, "valve_position": valve, "filename": filename,
                             "scans": int(scans)}
            if task_type == "emergency":
                new_task_data["how_much_executions"] = executions
            if task_type == "scheduled":
                new_task_data["freq"] = freq
                new_task_data["last_execution"] = 0


            newfile = []

            handle = open("TaskList", "r")
            for line in handle:
                newfile.append(line+"\n")
            newfile.append(str(json.dumps(new_task_data)+"\n"))

            handle.close()

            handle = open("TaskList", "w")

            for line in newfile:
                handle.write(line)
            handle.close()

















def delete_task(taskname):

    newfile = []

    handle = open("TaskList","r")
    for line in handle:
        try:
            dictline = json.loads(line)
            if dictline["class"] == "task" and dictline["name"] == taskname:
                pass
            else:
                newfile.append(line)
        except:
            pass

    handle.close()

    handle = open("TaskList","w")



    for line in newfile:
        handle.write(line)
        #if i+1 < len(newfile):
            #handle.write("\n")





def change_task_position(current_position,up_or_down,regular_task_list,scheduled_task_list,emergency_task_list,metadata):
    if current_position == 0 and up_or_down == "up":
        raise IndexError("Cannot move this task up")
    if current_position == len(regular_task_list) and up_or_down == "down":
        raise IndexError("Cannot move this task down")


    if_pass = False



    new_regular_task_list = []
    regular_task_list_len = len(regular_task_list)

    i = 0

    while i < regular_task_list_len:
        if up_or_down == "up" and i == current_position-1:
            #st.write(regular_task_list[i])
            new_regular_task_list.append(regular_task_list[i+1])
            new_regular_task_list.append(regular_task_list[i])
            if_pass = True
            i += 2
        if up_or_down == "down" and i == current_position:
            new_regular_task_list.append(regular_task_list[i+1])
            new_regular_task_list.append(regular_task_list[i])
            if_pass = True
            i += 2
        if not if_pass:
            new_regular_task_list.append(regular_task_list[i])
            i += 1
        if if_pass:
            if_pass = False





    handle = open("TaskList","w")
    handle.write(json.dumps(metadata))
    handle.write("\n")
    for line in emergency_task_list:
        handle.write(json.dumps(line))
        handle.write("\n")
    for line in scheduled_task_list:
        handle.write(json.dumps(line))
        handle.write("\n")
    for line in new_regular_task_list:
        handle.write(json.dumps(line))
        handle.write("\n")
    handle.close()


