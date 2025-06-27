import streamlit as st
from VSC_Gui_Operation import ArduinoGUI



def filling_station_gui():
    try:
        handle = open(".VSCINUSE","r")
        handle.close()
        st.write("VSC currently in use")

        try:

            turn_on_act_one = st.button("Force open actuator 1")
            turn_off_act_one = st.button("Force close actuator 1")

            if turn_on_act_one:
                ArduinoComms.TurnActuatorOneOn()
                st.write(f"Actuator 1 opened!")
            if turn_off_act_one:
                ArduinoComms.TurnActuatorOneOff()
                st.write(f"Actuator 1 closed!")
        except:
            pass



    except:
        ArduinoGUI()




filling_station_gui()