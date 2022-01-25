import wmi
def GetGPUs():
    GPU_1 = wmi.WMI().Win32_VideoController()[0].Name
    try:
        GPU_2 = wmi.WMI().Win32_VideoController()[1].Name
    except:
        GPU_2 = None
    GPU_List=(GPU_1,GPU_2)
    return GPU_List

def Settings():
    List=GetGPUs()
    if List[1] is not None:
        print("\nSelect a GPU to encode with:")
        print("0:", List[0]+"\n"+"1:", List[1])
        while True:
            try:
                Index=int(input("\nSelect GPU by ID: "))
                if Index not in [0,1] or type(Index) is not int:
                    continue
                else:
                    print("\nSelected:",List[Index]+"\n")
                    break
                
            except:
                continue
    else:
        Index=0                  

    if "nvidia" in List[Index].lower():
        Arguments = "-c:v hevc_nvenc -rc constqp -preset p7 -qp 18"

    elif "amd" in List[Index].lower() or "vega" in List[Index].lower() or "radeon" in List[Index].lower():
        Arguments = "-c:v hevc_amf -qp_i 16 -qp_p 16 -qp_b 16 -quality quality"

    elif "intel" in List[Index].lower():
        Arguments = "-c:v hevc_qsv -preset veryslow -global_quality:v 18"
    else:
        Arguments = "-c:v libx265 -preset medium -crf 18"

    return (Arguments)







