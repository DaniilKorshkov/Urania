import streamlit as st

def ShowAbnormalityLog():
    try:
        LogCopy = []
        handle = open("AbnormalityLog","r")
        for line in handle:
            LogCopy.append(line)
        handle.close()

        for line in LogCopy:
            st.write(line)


    except:
        st.write("No entries in AbnormalityLog yet")



ShowAbnormalityLog()