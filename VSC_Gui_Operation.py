import ArduinoComms
import JSONoperators
import StreamlitGUI as sg
import streamlit as st
import VSC_comms as vscc
from JSONoperators import ReadJSONConfig
import asyncio
import servo_motor as sm
import json

def pressure_meter_gui(MainConfig="MainConfig"):
    try:
        pressure = vscc.ReadPressureGauge(MainConfig)
        st.write(f"Pressure Transducer pressure: {pressure} torr")
    except:
        pg_port = ReadJSONConfig("vsc", "pressure_gauge_port")
        st.write(f"Failed to connect to pressure meter. Make sure it is connected to port {pg_port}")


def pressure_controller_gui(MainConfig="MainConfig"):
    try:
        pressure = vscc.ReadPCPressure(MainConfig)
        mode = vscc.ReadPCMode(MainConfig)
        current_sp = vscc.ReadPCSetpoint(MainConfig)

        st.write(f"Pressure Controller pressure: {pressure} torr")
        st.write(f"Pressure Controller mode: {mode}")
        st.write(f"Pressure Controller setpoint: {current_sp}")

        col1,col2,col3 = st.columns(3)
        with col1:
            openpc = st.button("Open Pressure Controller")
            if openpc:
                vscc.ChangePCMode("Open",MainConfig)

        with col2:
            closepc = st.button("Close Pressure Controller")
            if closepc:
                vscc.ChangePCMode("Close", MainConfig)

        with col3:
            setpointpc = st.button("Setpoint Mode")
            if setpointpc:
                vscc.ChangePCMode("Setpoint", MainConfig)


        new_setpoint = st.text_input(label="Enter new PC setpoint")
        change_sp = st.button("Apply PC setpoint")
        if change_sp:
            try:
                new_setpoint = float(new_setpoint)
                if new_setpoint >= 20 and new_setpoint <= 1000:
                    st.write(f"Trying to apply PC setpoint: {new_setpoint}")
                    vscc.ChangePCPressure(new_setpoint,MainConfig)

            except:
                pass

    except:
        pc_port = ReadJSONConfig("vsc", "pressure_controller_port")
        st.write(f"Failed to connect to pressure controller. Make sure it is connected to port {pc_port}")





def mfm_gui(MainConfig="MainConfig"):
    try:
        flow = vscc.ReadMFMFlowRate(MainConfig)
        st.write(f"MFM flow rate: {flow} cm3 / min")
    except:
        mfm_port = ReadJSONConfig("vsc", "mfm_port")
        st.write(f"Failed to connect to MFM. Make sure it is connected to port {mfm_port}")


def filling_mfm_gui(MainConfig="MainConfig"):
    try:
        filling_flow = vscc.ReadFillingMFMFlowRate(MainConfig)
        st.write(f"Filling flow rate: {filling_flow} cm3 / min")
    except:
        filling_mfm_port = ReadJSONConfig("vsc", "filling_mfm_port")
        st.write(f"Failed to connect to filling MFM. Make sure it is connected to port {filling_mfm_port}")






def mfc_gui(MainConfig="MainConfig"):
    try:
        flow = vscc.ReadMFCFlowRate(MainConfig)
        mode = vscc.ReadMFCMode(MainConfig)
        current_sp = vscc.ReadMFCSetpoint(MainConfig)

        st.write(f"MFC flow rate: {flow} cm3 / min")
        st.write(f"MFC mode: {mode}")
        st.write(f"MFC setpoint: {current_sp}")

        col1,col2,col3 = st.columns(3)
        with col1:
            openpc = st.button("Open MFC")
            if openpc:
                vscc.ChangeMFCMode("Open",MainConfig)

        with col2:
            closepc = st.button("Close MFC")
            if closepc:
                vscc.ChangeMFCMode("Close", MainConfig)

        with col3:
            setpointpc = st.button("Setpoint Mode MFC")
            if setpointpc:
                vscc.ChangeMFCMode("Setpoint", MainConfig)


        new_setpoint = st.text_input(label="Enter new MFC setpoint")
        change_sp = st.button("Apply MFC setpoint")
        if change_sp:
            try:
                new_setpoint = float(new_setpoint)
                if new_setpoint >= 20 and new_setpoint <= 1000:

                    st.write(f"Trying to apply MFC setpoint: {new_setpoint}")
                    vscc.ChangeMFCFlowRate(new_setpoint,MainConfig)

            except:
                pass

    except:
        mfc_port = ReadJSONConfig("vsc", "mfc_port")
        st.write(f"Failed to connect to MFC. Make sure it is connected to port {mfc_port}")


def vicivalve_gui(MainConfig="MainConfig"):
    new_valve_position = st.text_input(label="Enter new multi inlet valve position")
    apply_new_position = st.button("Apply new valve position")
    if apply_new_position:
        try:
            new_valve_position = int(new_valve_position)
            if new_valve_position >= 1 and new_valve_position <= 16:
                sm.switch_valve_position(new_valve_position)
            else:
                st.write("Bad input")
        except:
            st.write("Bad input")




def VSC_Gui(MainConfig="MainConfig"):

    try:
        handle = open(".VSCINUSE","r")
        handle.close()
        st.write("VSC currently in use")

        


    except:

        vicivalve_gui(MainConfig)
        for i in range(6):
            st.markdown("")
        pressure_controller_gui(MainConfig)
        for i in range(6):
            st.markdown("")
        mfc_gui(MainConfig)
        for i in range(6):
            st.markdown("")
        mfm_gui(MainConfig)
        for i in range(6):
            st.markdown("")
        filling_mfm_gui(MainConfig)
        for i in range(6):
            st.markdown("")
        pressure_meter_gui(MainConfig)
        




def ArduinoGUI():

    


    try:




        show_pressure = st.button("Display pressure on filling station")

        if show_pressure:

            ret = ArduinoComms.GetReadingsData()


            st.write(f"PT-01 pressure: {ret[0]} psi")
            st.write(f"PT-02 pressure: {ret[1]} psi")
            st.write(f"PT-03 pressure: {ret[2]} psi")
            st.write(f"PT-04 pressure: {ret[3]} psi")
            st.write(f"PT-05 pressure: {ret[4]} psi")
            st.write(f"PT-06 pressure: {ret[5]} psi")


            for i in range(6):
                st.markdown("")


            col1, col2 = st.columns(2)



            with col1:

                if (ret[6] == "1") or (ret[6] == 1):
                    st.write(f"FS actuator is open")
                else:
                    st.write(f"FS actuator is closed")

                for i in range(2):
                    st.markdown("")

            


            with col2:



                if (ret[7] == "1") or (ret[7] == 1):
                    st.write(f"SS actuator is open")
                else:
                    st.write(f"SS actuator is closed")

                for i in range(2):
                    st.markdown("")





        col3, col4 = st.columns(2)

        with col3:
            turn_on_act_one = st.button("Open FS actuator")
            turn_off_act_one = st.button("Close FS actuator")

            if turn_on_act_one:
                ArduinoComms.FillingActOpen()
                st.write(f"FS actuator opened!")
            if turn_off_act_one:
                ArduinoComms.FillingActClose()
                st.write(f"FS actuator closed!")
        
        with col4:
            turn_on_act_two = st.button("Open SS actuator")
            turn_off_act_two = st.button("Close SS actuator")

            if turn_on_act_two:
                ArduinoComms.SamplingActOpen()
                st.write(f"SS actuator opened!")
            if turn_off_act_two:
                ArduinoComms.SamplingActClose()
                st.write(f"SS actuator closed!")



                
        

    except:
        st.write(f"Failed to read data from filling station. Try reloading the page")