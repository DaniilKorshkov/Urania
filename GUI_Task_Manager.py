import streamlit as st
import os
from JSONoperators import ReadJSONConfig
import json





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




    st.write("Regular Tasks: ")
    for task in regular_task_list:
        name = task["name"]
        valve = task["valve_position"]
        filename = task["filename"]
        scans = task["scans"]

        st.write(f"{name} parameters: valve position:{valve}, spectrum filename: {filename}, scans: {scans}")

        delete = st.button(f"delete {name}")

        if delete:
            delete_task(name)


    for i in range(4):
        st.markdown("")

    st.write("Add new task")





    task_type = st.radio("Select task type",["emergency","scheduled","regular"])

    name = st.text_input("Enter task name")
    valve = st.text_input("Enter valve number")
    filename = st.text_input("Enter filename to record data")
    scans = st.text_input("Enter amount of scans")

    match task_type:
        case "emergency":
            executions = st.text_input("How much executions (either integer or 'inf')")
        case "scheduled":
            freq = st.text_input("Enter frequency")
        case "filename":
            pass


    try:
        assert not(name in name_list)
        valve = int(valve)
        assert (valve >=1 and valve <= 16)
        handle = open(filename,"r")
        for line in handle:
            dictline = json.loads(line)
            if dictline["class"] == "metadata":
                assert dictline["is_a_spectrum"] == "True"
        handle.close()

        scans = int(scans)

        if task_type == "emergency":
            if executions != "inf":
                executions = int(executions)
                assert executions > 0

        if task_type == "scheduled":
            freq = float(freq)



        new_task_data = {"class": "task","name":name, "type": task_type, "valve_position": valve, "filename": filename,
                         "scans": scans}
        if task_type == "emergency":
            new_task_data["how_much_executions"] = executions
        if task_type == "scheduled":
            new_task_data["freq"] = freq
            new_task_data["last_execution"] = 0

        create_task = st.button(f"Create new task")

        if create_task:
            newfile = []

            handle = open("TaskList", "r")
            for line in handle:
                newfile.append(line)
            newfile.append(str(json.dumps(new_task_data)+"\n"))

            handle.close()

            handle = open("TaskList", "w")

            for line in newfile:
                handle.write(line)




    except:
        st.write("Invalid input")
        try:
            handle.close()
        except:
            pass













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

