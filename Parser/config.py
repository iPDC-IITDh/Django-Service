fp = open("./ipdc9090.bin","rb")
file = fp.readlines()
# for i in file:
#     # print(i)

config = file[-1]
sourcesCFG = int(file[9].decode().split(" ")[1])
print("CFG: ",sourcesCFG) 
config_lineno = 9

PMUs_config = []

for j in range(sourcesCFG):
    dictionary = {}
    print("CFG: ",j+1)
    config = file[config_lineno+2]
    print("config size: ",len(config))
    index = 0
    config_lineno+=2
    sync = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    print(sync)
    dictionary["sync"] = sync
    framesize = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    print(framesize)
    idcode = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    print(idcode)
    soc = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
    index+=4
    print(soc)
    fracsec = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
    index+=4
    print(fracsec)
    time_base = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
    index+=4
    print(time_base)
    num_pmu = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    print("num_pmu: ",num_pmu)
    num_pmu = 1
    for k in range(num_pmu):
        station = config[index:index+16].decode()
        index+=16
        print(station)
        idcodepmu = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(idcodepmu)
        Format = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(Format)
        phnmr = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(phnmr)
        anmr = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(anmr)
        dgnmr = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(dgnmr)
        for i in range(phnmr):
            channel = config[index:(index+16)].decode()
            index += 16
            print("channel: ",channel)
        for i in range(anmr):
            channel = config[index:(index+16)].decode()
            index += 16
            print("channel: ",channel)
        for i in range(dgnmr):
            for h in range(16):
                channel = config[index:(index+16)].decode()
                index += 16
                print("channel: ",channel)
        
        for i in range(phnmr):
                factor = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
                index += 4
                print(factor)
        for i in range(anmr):
                factor = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
                index += 4
                print(factor)
        for i in range(dgnmr):
            factor = int.from_bytes(config[index:index+4],byteorder='big',signed=False)
            index += 4
            print(factor)
        fnom = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(fnom)
        cfg_cnt = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
        index+=2
        print(cfg_cnt)
    data_rate = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    print("Data_rate: ",data_rate)
    chk = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
    index+=2
    print(chk)
    # print("last index: ",index)
    # print("DATA_RATE", int.from_bytes(config[framesize-4:framesize-2],byteorder='big',signed=False))
    # print("FNOM", int.from_bytes(config[framesize-8:framesize-6],byteorder='big',signed=False))
    # # print("somelast bytes: ",config[index:].decode())