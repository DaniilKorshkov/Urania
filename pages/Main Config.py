import streamlit as st


def DisplayMainConfig():
    try:
        handle = open("MainConfig","r")
        for line in handle:
            st.write(line)
        handle.close()
    except:
        pass



if __name__ == "__main__":
    DisplayMainConfig()