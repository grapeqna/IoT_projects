from devices import Device
from people import People

# Create
device1 = Device(None, "NFC World", "Warehouse")
device1.create()
print(device1)

device2 = Device(None, "CoreRFID", "Office")
device2.create()
print(device2)

person1 = People(None, device1.id, None, "Ivan Ivanov")
person1.create()
print(person1)

person2 = People(None, device2.id, None, "Martin Martinov")
person2.create()
print(person2)

person3 = People(None, device1.id, None, "Yana")
person3.create()
print(person3)

person4 = People(None, device1.id, None, "Militsa")
person4.create()
print(person4)


# Select invalid
cnt_by_day = Device.cnt_by_day("2024-05-17")
print(cnt_by_day)

# Update
device1.manufacturer = "CoreRFID"
device1.update()
print(device1)

# Test
cnt_by_day = Device.cnt_by_day("2024-04-17")
print(cnt_by_day)

sort_from_device = Device.sort_from_device(device1.id)
print(sort_from_device)

cnt_by_building = Device.cnt_by_building("Warehouse")
print(cnt_by_building)

other_cnt = Device.cnt_by_building("Office")
print(other_cnt)

device1.delete()
device2.delete()
person1.delete()
person2.delete()
person3.delete()
person4.delete()