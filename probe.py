# -*- coding: utf-8 -*-
import logging


def probe(entry, file, tooldir=""):
    from subprocess import Popen, STARTUPINFO, STARTF_USESHOWWINDOW, PIPE

    logging.debug("> probe.probe : {} for {}".format(entry, file))
    startupinfo = STARTUPINFO()  # Hide separate window
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
    request = u'{}ffprobe.exe -v error -select_streams v -show_entries {} ' \
              u'-of default=noprint_wrappers=1:nokey=1 "{}"'.format(tooldir, entry, file)
    logging.debug("\tExecuting: {}".format(request))
    result = Popen(request, stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo).stdout.read()\
        .decode('utf-8').strip("\r\n")  # Pyinstaller needs everything piped
    logging.debug("< probe.probe")
    return result


def bit_depth(file, tooldir):
    logging.debug("> probe.bit_depth")
    tooldir="{}\\".format(tooldir)
    result = probe('stream=bits_per_raw_sample', file, tooldir)
    logging.info("Video has {}-bit depth".format(result))
    logging.debug("< probe.bit_depth")
    return result


def frames_total(file):
    logging.debug("> probe.frames_total")
    fps = eval(probe('stream=avg_frame_rate', file))  # Average frames per second
    duration = float(probe('format=duration', file))  # Duration in seconds
    logging.debug("\tTotal frames to decode: {}".format(duration*fps))
    logging.debug("< probe.frames_total")
    return duration*fps