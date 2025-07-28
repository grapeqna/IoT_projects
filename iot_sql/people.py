from database import DB

class People:
    def __init__(self, id, device_id, timestamp, name):
        self.id = id
        self.device_id = device_id
        self.timestamp = timestamp
        self.name = name

    def create(self):
        with DB() as db:
            row = db.execute('''
                INSERT INTO people (device_id, name) VALUES (?, ?) RETURNING id, timestamp, name
            ''', (self.device_id, self.name, )).fetchone()
            if row:
                self.id, self.timestamp, self.name = row

    def delete(self):
        if not self.id:
            return
        with DB() as db:
            db.execute('''
                DELETE FROM people WHERE id = ?
            ''', (self.id, ))

    def __str__(self):
        return "ID: {}, Device ID: {}, Timestamp: {}, Name: {}".format(self.id, self.device_id, self.timestamp, self.name)