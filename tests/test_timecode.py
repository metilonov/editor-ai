from editai.utils.timecode import human_duration,srt_time

def test_timecode():
    assert human_duration(65)=="1:05"
    assert srt_time(65.432)=="00:01:05,432"
