import streamlit as st


def ShowMainLog():
    try:
        LogCopy = []
        handle = open("MainLog", "r")
        for line in handle:
            LogCopy.append(line)
        handle.close()

        for line in LogCopy:
            st.write(line)


    except:
        st.write("No entries in MainLog yet")


ShowMainLog()