import oxygen_analyzer as oa
import datetime
import time

def MakeEntry():

    try:
        oxygen_ppm = str(oa.GetOxygenData())
    except:
        oxygen_ppm = "123"
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    handle = open("oxygen_analyzer_csv_data","a")
    handle.write(str(current_time))
    handle.write("\t")
    handle.write(oxygen_ppm)
    handle.write("\n")
    handle.close()

    print(f"{datetime.datetime.now()}: {oxygen_ppm}")

    time.sleep(1)



def main():
    try:
        handle = open("oxygen_analyzer_csv_data","r")
        handle.close()
    except:
        handle = open("oxygen_analyzer_csv_data","w")
        handle.close()
    
    while True:
        MakeEntry()


if __name__ == "__main__":
    main()