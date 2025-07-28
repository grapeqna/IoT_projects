from database import DB


class MotionSensor:
    # initialise
    def __init__(self, motion_sensor_id, manufacturer, room):
        self.id = motion_sensor_id
        self.manufacturer = manufacturer
        self.room = room

    # add to database
    def create(self):
        with DB() as db:
            values = (self.manufacturer, self.room)
            db.execute('''
                INSERT INTO motion_sensor (manufacturer, room) VALUES (?, ?)
            ''', values)

    # find motion sensor by room
    @staticmethod
    def find_by_room(room):
        if not room:
            return None
        with DB() as db:
            row = db.execute('''
                SELECT * FROM motion_sensor WHERE room = ?
            ''', (room,)).fetchone()
            if row:
                return MotionSensor(*row)
