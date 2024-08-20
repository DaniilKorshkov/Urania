from TaskManagement import DoTask

while True:
    try:
        DoTask()
    except:
        print(f"Error encountered during task execution")