import VSC_comms as vsc



while True:

    print(f"Type 'data' for full query, type 'pcm' to change PC mode, type 'pcs' to change PC setpoint, type 'mfcm' to change MFC mode, type 'mfcs' to change MFC setpoint, type 'quit' to exit")
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

        case 'quit':
            break
        case _:
            print(f"Input not recognized")