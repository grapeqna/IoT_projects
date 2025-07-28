from database import DB


class MotionDetection:
	# initialise
	def __init__(self, motion_detection_id, motion_sensor_id, timestamp):
		self.id = motion_detection_id
		self.motion_sensor_id = motion_sensor_id
		self.timestamp = timestamp

	# add to database
	def create(self):
		with DB() as db:
			values = (self.motion_sensor_id, )
			db.execute('''
				INSERT INTO motion_detection (motion_sensor_id) VALUES (?)
			''', values)
