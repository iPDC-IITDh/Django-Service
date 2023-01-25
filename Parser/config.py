import json
from bitstring import BitArray

IDCODE = 3467

def bytes_to_float(bytes_array):
    bytes_array = int.from_bytes(bytes_array, byteorder='big', signed=False)
    bytes_array = BitArray(uint=bytes_array, length=32)
    bytes_array = bytes_array.bin
    bytes_array = int(bytes_array, 2)
    sign = 1 - 2 * (bytes_array >> 31)
    exp = (bytes_array >> 23) & 0xff
    mantissa = bytes_array & 0x7fffff
    if exp == 0:
        return sign * (2 ** (-126)) * (mantissa / (2 ** 23))
    elif exp == 255:
        if mantissa == 0:
            return sign * float('inf')
        else:
            return float('nan')
    else:
        return sign * (2 ** (exp - 127)) * (1 + mantissa / (2 ** 23))

def config_file_parser(file_path):
    fp = open(file_path,"rb")
    file = fp.readlines()
    sourcesCFG = int(file[8].decode().split(" ")[1])
    # print("CFG: ",sourcesCFG) 
    config_lineno = 8

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
            format = int.from_bytes(config[index:index+2],byteorder='big',signed=False)
            Format_bits = bin(format)[2:].zfill(16)
            index+=2
            # print(Format)
            maindictionary[key]["Format"] = Format_bits
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
                    channelkey = "digital channel"+str((i*16)+h+1)
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
                factorkey = "digital factor"+str(i+1)
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
    
    return PMUs_config

configs = config_file_parser("/home/academia/iPDC/iPDC/ipdc"+str(IDCODE)+".bin")


def combine_configs():
    global configs
    total_pmus = 0
    ret = {}
    for i in configs:
        total_pmus += i["num_pmu"]
        for j in range(i["num_pmu"]):
            key = "pmu"+str(j+1)
            ret[i[key]["idcode"]] = i[key]
    retu = {}
    retu["total_pmus"] = total_pmus
    retu[IDCODE] = ret
    return retu

print(combine_configs())
all_configs = combine_configs()


def data_frame_parser(string_buffer):
    df = {}
    index = 0
    sync = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=False)
    index+=2
    print(sync)
    df["sync"] = sync
    framesize = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=False)
    index+=2
    print(framesize)
    df["framesize"] = framesize

    idcode = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=False)
    index+=2
    print(idcode)
    df["idcode"] = idcode

    soc = int.from_bytes(string_buffer[index:index+4],byteorder='big',signed=False)
    index+=4
    print(soc)
    df["soc"] = soc

    fracsec = int.from_bytes(string_buffer[index:index+4],byteorder='big',signed=False)
    index+=4
    print(fracsec)
    df["fracsec"] = fracsec

    print(idcode)
    df["pmus_data"] = {}
    config = all_configs[IDCODE]
    for key,value in config.items():
        idcode = key
        pmu_config = value

        stat = int.from_bytes(string_buffer[index:index+4],byteorder='big',signed=True)
        index+=4
        stat_bits = bin(stat)[2:].zfill(32)
        print(stat_bits)

        df["pmus_data"][idcode] = {}
        df["pmus_data"][idcode]["stat"] = stat_bits

        phnmr = pmu_config["phnmr"]
        anmr = pmu_config["anmr"]
        dgnmr = pmu_config["dgnmr"]
        df["pmus_data"][idcode]["phasors"] = []
        for i in range(phnmr):
            phasor = {}
            real = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=True)
            index+=2
            imag = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=True)
            index+=2
            phasor["real"] = real
            phasor["imag"] = imag
            df["pmus_data"][idcode]["phasors"].append(phasor)

        if(config[idcode]['Format'][-4] == '0'):
            df["pmus_data"][idcode]["freq"] = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=False)
            index+=2
            df["pmus_data"][idcode]["dfreq"] = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=False)
            index+=2
        else:
            bytes_array = string_buffer[index:index+4]
            df["pmus_data"][idcode]["freq"] = bytes_to_float(bytes_array)
            index+=4
            bytes_array = string_buffer[index:index+4]
            df["pmus_data"][idcode]["dfreq"] = bytes_to_float(bytes_array)
            index+=4
        df["pmus_data"][idcode]["analog"] = []
        for i in range(anmr):
            analog = {}
            analog["value"] = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=True)
            index+=2
            df["pmus_data"][idcode]["analog"].append(analog)
        df["pmus_data"][idcode]["digital"] = []
        for i in range(dgnmr):
            digital = {}
            digital["value"] = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=True)
            index+=2
            df["pmus_data"][idcode]["digital"].append(digital)
    chk = int.from_bytes(string_buffer[index:index+2],byteorder='big',signed=False)
    df["chk"] = chk
    index+=2

    print(json.dumps(df, indent = 4))
    print("index last: ",index)
    return df
        


# string_buffer = b"\xaa\x01\x00,#\x82c\xc4;7\x00\x1e\xb8R\x00\x00\x00\x0f\x00\x00\xff\xad\x00@\xff\xcb\x00Y\xff\x9f\x009\x01,\x00\x00\x00d\x03\xe8\x00\x00'\x92"
string_buffer = b'\xaa\x01\x00$\r\x8bc\xc6\xcf\x05\x00\x99\x99\x9a\x00\x00\x00\x00\xff\xc2\x00TC\x96\x00\x00\x00\x00\x00\x00\x00d\x00\x00\xeb\x8d'
# string_buffer = b"\xaa\x01\x00*'\x0fc\xc7\x99\xee\x00\x8f\\)\x00\x00\x00\x00\xff\xc2\x00Y\xff\xd1\x00]\xff\xa6\x00B\x01\x90\x00\x00\x00d\x03\xe8\x00\x00\xdaH"
data_frame_parser(string_buffer)
print("df length: ",len(string_buffer))