from subprocess import run, DEVNULL, STDOUT

NVENC=('-hwaccel cuda -threads 8',
'-c:v hevc_nvenc -rc constqp -preset p7 -qp 18', 
'-c:v h264_nvenc -rc constqp -preset p7 -qp 15')

AMF=('-hwaccel d3d11va',
'-c:v hevc_amf -quality quality -qp_i 16 -qp_p 18 -qp_b 20',
'-c:v h264_amf -quality quality -qp_i 12 -qp_p 12 -qp_b 12')

QSV=('-hwaccel d3d11va',
'-c:v hevc_qsv -preset veryslow -global_quality:v 18',
'-c:v h264_qsv -preset veryslow -global_quality:v 15')

CPU=("-c:v libx265 -preset medium -crf 18",
"-c:v libx264 -preset slow -crf 15")


def GetEncoder():
    Encoders=(
    'hevc_nvenc', 
    'h264_nvenc', 
    'hevc_amf', 
    'h264_amf',
    'hevc_qsv', 
    'h264_qsv',
    'libx265', 
    'libx264')

    Command="ffmpeg.exe -loglevel warning -f lavfi -i nullsrc=3840x2160 -t 0 -c:v {Encoder} -f null NUL"
    for Encoder in Encoders:
        ExitCode=run(Command.format(Encoder=Encoder),stdout=DEVNULL, stderr=STDOUT).returncode

        if ExitCode == 0:
            # NVIDIA
            if Encoder == 'hevc_nvenc':
                HWAccelArgs=NVENC[0]
                Arguments=NVENC[1]

            elif Encoder == 'h264_nvenc':
                HWAccelArgs=NVENC[0]
                Arguments=NVENC[2]


            # AMD
            elif Encoder == 'hevc_amf':
                HWAccelArgs=AMF[0]
                Arguments=AMF[1]

            elif Encoder == 'h264_amf':
                HWAccelArgs=AMF[0]
                Arguments=AMF[2]

            # INTEL
            elif Encoder == 'hevc_qsv':
                HWAccelArgs=QSV[0]
                Arguments=QSV[1]

            elif Encoder == 'h264_qsv':
                HWAccelArgs=QSV[0]
                Arguments=QSV[2]

            # CPU
            elif Encoder == 'libx265':
                HWAccelArgs=""
                Arguments=CPU[0]
            
            elif Encoder == 'libx264':
                HWAccelArgs=""
                Arguments=CPU[1]

            break    

    return (HWAccelArgs, Arguments)

# Legacy Method

"""
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
"""   







