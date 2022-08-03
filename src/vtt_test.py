import vtt
import time

course = vtt.get_crn('2022', vtt.Semester.FALL, '83201')

while True:
    print(course.has_open_spots())
    time.sleep(1)