import json

import streamlit as st
import JSONoperators as js

def AbnormalitySettings():
    for i in range(15):
        control_spectrum = js.ReadJSONConfig("AbnormalityReaction",f"MIV{i+1}")
        st.write(f"Line {i+1}")

        for key in control_spectrum:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"M/Z = {key}: {(control_spectrum[key])[0]} - {(control_spectrum[key])[1]}")
            with col2:
                new_min_value = st.text_input(f"New minimal PPM threshold for M/Z={key} for line {i+1}: ")
                append_new_min_value = st.button(f"Edit min PPM threshold for M/Z={key} for line {i+1}:")
                if append_new_min_value:

                    try:
                        void = float(new_min_value)
                        assert void <= float((control_spectrum[key])[1])


                        new_line = js.ReadJSONConfig("AbnormalityReaction")

                        (((new_line[f"MIV{i + 1}"])[key])[0]) = float(new_min_value)
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("AbnormalityReaction", str_new_line)

                    except:
                        st.write(f"Provided value is invalid")



            with col3:
                new_max_value = st.text_input(f"New maximal PPM threshold for M/Z={key} for line {i+1}: ")
                append_new_max_value = st.button(f"Edit max PPM threshold for M/Z={key} for line {i + 1}:")
                if append_new_max_value:

                    try:
                        void = float(new_max_value)
                        assert void >= float((control_spectrum[key])[0])

                        new_line = js.ReadJSONConfig("AbnormalityReaction")

                        (((new_line[f"MIV{i+1}"])[key])[1]) = float(new_max_value)
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("AbnormalityReaction",str_new_line)

                    except:
                        st.write(f"Provided value is invalid")

            with col4:

                if (key != "default") and (key != "oxygen"):
                    delete_entry = st.button(f"Delete M/Z = {key} condition for line {i+1}")
                    if delete_entry:
                        try:
                            new_line = js.ReadJSONConfig("AbnormalityReaction")
                            (new_line[f"MIV{i + 1}"]).pop(key)
                            str_new_line = json.dumps(new_line)
                            js.EditJSONConfig("AbnormalityReaction", str_new_line)

                        except:
                            pass








        col1, col2, col3, col4 = st.columns(4)

        with col1:
                new_molar_mass = st.text_input(f"Enter M/Z for new line {i+1} condition")
        with col2:
                new_min_value = st.text_input(f"Enter min PPM threshold for new line {i+1} condition")
        with col3:
                new_max_value = st.text_input(f"Enter max PPM threshold for new line {i+1} condition")
        with col4:
                create_new_entry = st.button(f"Add new condition for line {i+1} scan")

        if create_new_entry:

            try:
                void3 = control_spectrum[new_molar_mass]
                st.write(f"Condition for M/Z = {new_molar_mass} already exist")

            except:
                try:
                    void = int(new_molar_mass)

                    try:
                        void1 = float(new_min_value)
                        void2 = float(new_max_value)
                        assert void2 >= void1

                        new_line = js.ReadJSONConfig("AbnormalityReaction")

                        ((new_line[f"MIV{i + 1}"])[int(new_molar_mass)]) = [float(new_min_value),float(new_max_value)]
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("AbnormalityReaction", str_new_line)




                    except:
                        st.write("Provided min/max values are invalid")


                except:
                    st.write("Provided M/Z is not integer")


        if i == 13:
            for k in range(3):
                st.markdown("")
            st.write(f"Automatically close filling station actuator if abnormal readings on line 14?")

            col1, col2 = st.columns(2)

            with col1:
                auto_close_yes = st.button("Yes")
                if auto_close_yes:
                    new_line = js.ReadJSONConfig("AbnormalityReaction")
                    new_line[f"auto_close"] = "True"
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("AbnormalityReaction", str_new_line)
                    st.write(f"Autoclose turned on")


            with col2:
                auto_close_no = st.button("No")
                if auto_close_no:
                    new_line = js.ReadJSONConfig("AbnormalityReaction")
                    new_line[f"auto_close"] = "False"
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("AbnormalityReaction", str_new_line)
                    st.write(f"Autoclose turned off")











        for j in range(5):
            st.markdown("")

def AbnormalitySettingsForInterpreted():
    for i in range(15):
        control_spectrum = js.ReadJSONConfig("InterpretedAbnormalityReaction",f"MIV{i+1}")
        st.write(f"Line {i+1}")

        for key in control_spectrum:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"{key}: {(control_spectrum[key])[0]} - {(control_spectrum[key])[1]}")
            with col2:
                new_min_value = st.text_input(f"New minimal PPM threshold for {key} for line {i+1}: ")
                append_new_min_value = st.button(f"Edit min PPM threshold for {key} for line {i+1}:")
                if append_new_min_value:

                    try:
                        void = float(new_min_value)
                        assert void <= float((control_spectrum[key])[1])


                        new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                        (((new_line[f"MIV{i + 1}"])[key])[0]) = float(new_min_value)
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)

                    except:
                        st.write(f"Provided value is invalid")



            with col3:
                new_max_value = st.text_input(f"New maximal PPM threshold for {key} for line {i+1}: ")
                append_new_max_value = st.button(f"Edit max PPM threshold for {key} for line {i + 1}:")
                if append_new_max_value:

                    try:
                        void = float(new_max_value)
                        assert void >= float((control_spectrum[key])[0])

                        new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                        (((new_line[f"MIV{i+1}"])[key])[1]) = float(new_max_value)
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("InterpretedAbnormalityReaction",str_new_line)

                    except:
                        st.write(f"Provided value is invalid")

            


        if i == 13:
            for k in range(3):
                st.markdown("")
            st.write(f"Automatically close filling station actuator if abnormal readings on line 14?")

            col1, col2 = st.columns(2)

            with col1:
                auto_close_yes = st.button("Yes")
                if auto_close_yes:
                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")
                    new_line[f"auto_close"] = "True"
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)
                    st.write(f"Autoclose turned on")


            with col2:
                auto_close_no = st.button("No")
                if auto_close_no:
                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")
                    new_line[f"auto_close"] = "False"
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)
                    st.write(f"Autoclose turned off")











        for j in range(5):
            st.markdown("")








AbnormalitySettingsForInterpreted()





def AbnormalitySettingsForGas():
    control_spectrum = js.ReadJSONConfig("InterpretedAbnormalityReaction",f"VSC")
    

    for key in control_spectrum:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"{key}: {(control_spectrum[key])[1]} - {(control_spectrum[key])[2]}")
            st.write(f"{key} critical: {(control_spectrum[key])[0]} - {(control_spectrum[key])[3]}")
        with col2:
            new_min_value = st.text_input(f"New minimal torr or cm3min threshold for {key}: ")
            append_new_min_value = st.button(f"Edit min threshold for {key}:")
            if append_new_min_value:

                try:
                    void = float(new_min_value)
                    assert void <= float((control_spectrum[key])[2])
                    assert void >= float((control_spectrum[key])[0])


                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[1]) = float(new_min_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)

                except:
                    st.write(f"Provided value is invalid")

            
            new_crit_min_value = st.text_input(f"New critical minimal torr or cm3min threshold for {key}: ")
            append_new_crit_min_value = st.button(f"Edit critical min threshold for {key}:")
            if append_new_crit_min_value:

                try:
                    void = float(new_crit_min_value)
                    assert void <= float((control_spectrum[key])[1])


                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[0]) = float(new_crit_min_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)

                except:
                    st.write(f"Provided value is invalid")



        with col3:
            new_max_value = st.text_input(f"New maximal torr or cm3min threshold for {key}: ")
            append_new_max_value = st.button(f"Edit max threshold for {key}:")
            if append_new_max_value:

                try:
                    void = float(new_max_value)
                    assert void >= float((control_spectrum[key])[1])
                    assert void <= float((control_spectrum[key])[3])

                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[2]) = float(new_max_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction",str_new_line)

                except:
                    st.write(f"Provided value is invalid")

            new_crit_max_value = st.text_input(f"New critical maximal torr or cm3min threshold for {key}: ")
            append_new_crit_max_value = st.button(f"Edit critical max threshold for {key}:")
            if append_new_crit_max_value:

                try:
                    void = float(new_crit_max_value)
                    assert void >= float((control_spectrum[key])[2])
                    

                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[3]) = float(new_crit_max_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction",str_new_line)

                except:
                    st.write(f"Provided value is invalid")

        
AbnormalitySettingsForGas()




def AbnormalitySettingsForArduino():
    control_spectrum = js.ReadJSONConfig("InterpretedAbnormalityReaction",f"Arduino")
    

    for key in control_spectrum:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"{key}: {(control_spectrum[key])[1]} - {(control_spectrum[key])[2]}")
            st.write(f"{key} critical: {(control_spectrum[key])[0]} - {(control_spectrum[key])[3]}")
        with col2:
            new_min_value = st.text_input(f"New minimal PSI threshold for {key}: ")
            append_new_min_value = st.button(f"Edit min threshold for {key}:")
            if append_new_min_value:

                try:
                    void = float(new_min_value)
                    assert void <= float((control_spectrum[key])[2])
                    assert void >= float((control_spectrum[key])[0])


                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[1]) = float(new_min_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)

                except:
                    st.write(f"Provided value is invalid")

            
            new_crit_min_value = st.text_input(f"New critical minimal PSI threshold for {key}: ")
            append_new_crit_min_value = st.button(f"Edit critical min threshold for {key}:")
            if append_new_crit_min_value:

                try:
                    void = float(new_crit_min_value)
                    assert void <= float((control_spectrum[key])[1])


                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[0]) = float(new_crit_min_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction", str_new_line)

                except:
                    st.write(f"Provided value is invalid")



        with col3:
            new_max_value = st.text_input(f"New maximal PSI threshold for {key}: ")
            append_new_max_value = st.button(f"Edit max threshold for {key}:")
            if append_new_max_value:

                try:
                    void = float(new_max_value)
                    assert void >= float((control_spectrum[key])[1])
                    assert void <= float((control_spectrum[key])[3])

                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[2]) = float(new_max_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction",str_new_line)

                except:
                    st.write(f"Provided value is invalid")

            new_crit_max_value = st.text_input(f"New critical maximal PSI threshold for {key}: ")
            append_new_crit_max_value = st.button(f"Edit critical max threshold for {key}:")
            if append_new_crit_max_value:

                try:
                    void = float(new_crit_max_value)
                    assert void >= float((control_spectrum[key])[2])
                    

                    new_line = js.ReadJSONConfig("InterpretedAbnormalityReaction")

                    (((new_line[f"VSC"])[key])[3]) = float(new_crit_max_value)
                    str_new_line = json.dumps(new_line)
                    js.EditJSONConfig("InterpretedAbnormalityReaction",str_new_line)

                except:
                    st.write(f"Provided value is invalid")


for i in range(6):
    st.markdown("")

AbnormalitySettingsForArduino()