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
                new_min_value = st.text_input(f"New minimal value for M/Z={key} for line {i+1}: ")
                append_new_min_value = st.button(f"Edit min value for M/Z={key} for line {i+1}:")
                if append_new_min_value:

                    try:
                        void = float(new_min_value)
                        assert void <= float((control_spectrum[key])[1])


                        new_line = js.ReadJSONConfig("AbnormalityReaction")

                        (((new_line[f"MIV{i + 1}"])[key])[0]) = new_min_value
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("AbnormalityReaction", str_new_line)

                    except:
                        st.write(f"Provided value is invalid")



            with col3:
                new_max_value = st.text_input(f"New maximal value for M/Z={key} for line {i+1}: ")
                append_new_max_value = st.button(f"Edit max value for M/Z={key} for line {i + 1}:")
                if append_new_max_value:

                    try:
                        void = float(new_max_value)
                        assert void >= float((control_spectrum[key])[0])

                        new_line = js.ReadJSONConfig("AbnormalityReaction")

                        (((new_line[f"MIV{i+1}"])[key])[1]) = new_max_value
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
                new_min_value = st.text_input(f"Enter min value for new line {i+1} condition")
        with col3:
                new_max_value = st.text_input(f"Enter max value for new line {i+1} condition")
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

                        ((new_line[f"MIV{i + 1}"])[new_molar_mass]) = [new_min_value,new_max_value]
                        str_new_line = json.dumps(new_line)
                        js.EditJSONConfig("AbnormalityReaction", str_new_line)




                    except:
                        st.write("Provided min/max values are invalid")


                except:
                    st.write("Provided M/Z is not integer")






        for j in range(5):
            st.markdown("")




AbnormalitySettings()