import subprocess

def GetPowerStatus():
    power_sources = str((subprocess.run(["upower", "-e"], capture_output=True)).stdout)
    power_sources = power_sources[2:(len(power_sources)-1)]
    print(power_sources)
    power_sources_list = power_sources.split("\\n")
    for element in power_sources_list:
        if "battery" in element:
            source_status = str((subprocess.run(["upower", "-i", element], capture_output=True)).stdout)

            source_status_split = source_status.split("\\n")

            for subelement in source_status_split:
                subelement_split = subelement.split()
                if "state:" in subelement_split:  # 'discharging','charging'
                    if subelement_split[1] == "charging" or subelement_split[1] == "fully-charged":
                        return True
                    else:
                        return False





print(GetPowerStatus())