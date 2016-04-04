def probe(entry, file):
    from subprocess import Popen, STARTUPINFO, STARTF_USESHOWWINDOW, PIPE
    startupinfo = STARTUPINFO()  # Hide separate window
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
    return Popen('ffprobe.exe -v error -select_streams v -show_entries {} '
                 '-of default=noprint_wrappers=1:nokey=1 "{}"'.format(entry, file), stdout=PIPE, stderr=PIPE,
                 startupinfo=startupinfo).stdout.read().decode('utf-8').strip("\r\n")

def bit_depth(file):
    return probe('stream=bits_per_raw_sample', file)

def frames_total(file):
    fps = eval(probe('stream=avg_frame_rate', file))  # Average frames per second
    duration = float(probe('format=duration', file))  # Duration in seconds
    return duration*fps