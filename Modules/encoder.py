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
            match(Encoder):
                case('hevc_nvenc'):
                    HWAccelArgs=NVENC[0]
                    Arguments=NVENC[1]
                case('h264_nvenc'):
                        HWAccelArgs=NVENC[0]
                        Arguments=NVENC[2]
                # AMD
                case('hevc_amf'):
                        HWAccelArgs=AMF[0]
                        Arguments=AMF[1]
                case('h264_amf'):
                        HWAccelArgs=AMF[0]
                        Arguments=AMF[2]
                # INTEL
                case('hevc_qsv'):
                        HWAccelArgs=QSV[0]
                        Arguments=QSV[1]
                case('h264_qsv'):
                        HWAccelArgs=QSV[0]
                        Arguments=QSV[2]
                # CPU
                case('libx265'):
                        HWAccelArgs=""
                        Arguments=CPU[0]
                case('libx264'):
                        HWAccelArgs=""
                        Arguments=CPU[1]
            break    
    return (HWAccelArgs, Arguments)






