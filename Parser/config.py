import json

fp = open("./ipdc9090.bin","rb")
file = fp.readlines()
sourcesCFG = int(file[9].decode().split(" ")[1])
# print("CFG: ",sourcesCFG) 
config_lineno = 9

PMUs_config = []

for j in range(sourcesCFG):
    maindictionary = {}
    # print("CFG: ",j+1)
    config = file[config_lineno+2]
    # print("config size: ",len(config))
    index = 0
    config_lineno+=2
    sync = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    # print(sync)
    maindictionary["sync"] = sync
    framesize = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    # print(framesize)
    maindictionary["framesize"] = framesize
    idcode = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    # print(idcode)
    maindictionary["idcode"] = idcode
    soc = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
    index+=4
    # print(soc)
    maindictionary["soc"] = soc
    fracsec = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
    index+=4
    # print(fracsec)
    maindictionary["fracsec"] = fracsec
    time_base = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
    index+=4
    # print(time_base)
    maindictionary["time_base"] = time_base
    num_pmu = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    maindictionary["num_pmu"] = num_pmu
    # print("num_pmu: ",num_pmu)
    for k in range(num_pmu):
        key = "pmu"+str(k+1)
        maindictionary[key] = {}
        station = config[index:index+16].decode().strip()
        index+=16
        # print(station)
        maindictionary[key]["station"] = station
        idcodepmu = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(idcodepmu)
        maindictionary[key]["idcode"] = idcodepmu
        Format = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(Format)
        maindictionary[key]["Format"] = Format
        phnmr = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(phnmr)
        maindictionary[key]["phnmr"] = phnmr
        anmr = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(anmr)
        maindictionary[key]["anmr"] = anmr
        dgnmr = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(dgnmr)
        maindictionary[key]["dgnmr"] = dgnmr
        for i in range(phnmr):
            channelkey = "phasor channel"+str(i+1)
            channel = config[index:(index+16)].decode().strip()
            index += 16
            # print("channel: ",channel)
            maindictionary[key][channelkey] = channel
        for i in range(anmr):
            channelkey = "analog channel"+str(i+1)
            channel = config[index:(index+16)].decode().strip()
            index += 16
            # print("channel: ",channel)
            maindictionary[key][channelkey] = channel
        for i in range(dgnmr):
            for h in range(16):
                channelkey = "Digital channel"+str((i*16)+1)
                channel = config[index:(index+16)].decode().strip()
                index += 16
                # print("channel: ",channel)
                maindictionary[key][channelkey] = channel
        
        for i in range(phnmr):
            factorkey = "phasor factor"+str(i+1)
            factor = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
            index += 4
            # print(factor)
            maindictionary[key][factorkey] = factor

        for i in range(anmr):
            factorkey = "analog factor"+str(i+1)
            factor = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
            index += 4
            # print(factor)
            maindictionary[key][factorkey] = factor

        for i in range(dgnmr):
            factorkey = "analog factor"+str(i+1)
            factor = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
            index += 4
            # print(factor)
            maindictionary[key][factorkey] = factor

        fnom = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(fnom)
        maindictionary[key]["fnom"] = fnom
        cfg_cnt = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        # print(cfg_cnt)
        maindictionary[key]["cfg_cnt"] = cfg_cnt
    data_rate = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    # print("Data_rate: ",data_rate)
    maindictionary["data_rate"] = data_rate
    chk = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    # print(chk)
    maindictionary["chk"] = chk
    PMUs_config.append(maindictionary)

for i in PMUs_config:
    print(json.dumps(i, indent = 4))