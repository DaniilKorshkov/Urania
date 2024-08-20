import VSC_comms as vsc
import servo_motor as sm



while True:

    print(f"Type 'data' for full query, type 'pcm' to change PC mode, type 'pcs' to change PC setpoint, type 'mfcm' to change MFC mode, \ntype 'mfcs' to change MFC setpoint, type 'vici' to operate multi inlet valve, type 'quit' to exit")
    print(f"If connection can't be made, try switching /dev/ttyUSB0 to /dev/ttyUSB1 or 2 in config")
    user_command = str(input("Type here: "))

    match user_command.lower():
        case 'data':
            vsc.FullQuery()

        case 'pcm':
            mode = str(input("Enter mode: "))
            match mode.lower():
                case "open":
                    vsc.ChangePCMode("Open")
                case "close":
                    vsc.ChangePCMode("Close")
                case "setpoint":
                    vsc.ChangePCMode("Setpoint")
                case _:
                    print(f"Input not recognized")

        case 'pcs':
            try:
                pressure = float(input("Enter desired pressure: "))
                vsc.ChangePCPressure(pressure)
            except:
                print("Input not recognized")


        case 'mfcm':
            mode = str(input("Enter mode: "))
            match mode.lower():
                case "open":
                    vsc.ChangeMFCMode("Open")
                case "close":
                    vsc.ChangeMFCMode("Close")
                case "setpoint":
                    vsc.ChangeMFCMode("Setpoint")
                case _:
                    print(f"Input not recognized")

        case 'mfcs':
            try:
                pressure = float(input("Enter desired pressure: "))
                vsc.ChangePCPressure(pressure)
            except:
                print("Input not recognized")

        case 'vici':
            try:
                new_position = int(input("Enter new multi inlet valve position:"))
                assert new_position >0 and new_position<17
                sm.switch_valve_position(new_position)
            except:
                print("Invalid input")

        case 'quit':
            break
        case _:
            print(f"Input not recognized")