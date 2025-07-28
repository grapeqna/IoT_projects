import time

from database import DB
from motion_sensor import MotionSensor
from motion_detection import MotionDetection

MotionSensor(None, "Siemens", "kitchen").create()
MotionSensor(None, "Siemens", "bathroom").create()
MotionSensor(None, "Siemens", "bedroom").create()
MotionSensor(None, "Siemens", "living room").create()

MotionDetection(None, MotionSensor.find_by_room("kitchen").id, None).create()
time.sleep(1)
MotionDetection(None, MotionSensor.find_by_room("kitchen").id, None).create()
time.sleep(1)
MotionDetection(None, MotionSensor.find_by_room("bedroom").id, None).create()
time.sleep(1)
MotionDetection(None, MotionSensor.find_by_room("bathroom").id, None).create()

with DB() as db:
    db.execute('''DELETE FROM motion_sensor WHERE room = "kitchen";''')
