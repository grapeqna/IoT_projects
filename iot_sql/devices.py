from database import DB

class Device():
    def __init__(self, id, manufacturer, building):
        self.id = id
        self.manufacturer = manufacturer
        self.building = building

    def create(self):
        with DB() as db:
            row = db.execute('''
                INSERT INTO devices (manufacturer, building) VALUES (?, ?) RETURNING id
            ''', (self.manufacturer, self.building)).fetchone()
            if row:
                (self.id, ) = row

    def update(self):
        if not self.id:
            return
        with DB() as db:
            db.execute('''
                UPDATE devices SET manufacturer = ?, building = ? WHERE id = ?
            ''', (self.manufacturer, self.building, self.id))

    def delete(self):
        if not self.id:
            return
        with DB() as db:
            db.execute('''
                DELETE FROM devices WHERE id = ?
            ''', (self.id, ))

    @staticmethod
    def cnt_by_day(day):
        if day is None:
            return None
        with DB() as db:
            row = db.execute('''
                SELECT COUNT(people.id) FROM people
                WHERE DATE(people.timestamp) = DATE(?)
            ''', (day, )).fetchone()
            if row:
                return "People by day {}: {}".format(day, row[0])

    @staticmethod
    def sort_from_device(device_id):
        if device_id is None:
            return None
        with DB() as db:
            rows = db.execute('''
               SELECT people.name FROM people
                WHERE people.device_id = ?
                ORDER BY people.name ASC
            ''', (device_id, )).fetchall()
        if rows:
            names = ", ".join(row[0] for row in rows)
            return "Device: {}, names: {}".format(device_id, names)

    @staticmethod
    def cnt_by_building(building):
        if building is None:
            return None
        with DB() as db:
            row = db.execute('''
                SELECT COUNT(people.id) FROM people
                LEFT JOIN devices ON people.device_id = devices.id
                WHERE devices.building = ?
            ''', (building, )).fetchone()
            if row:
                return "Building: {}, people: {}".format(building, row[0])

    def __str__(self):
        return "ID: {}, Manufacturer: {}, Building: {}".format(self.id, self.manufacturer, self.building)