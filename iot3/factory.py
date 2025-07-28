import time
import random
import threading
from queue import Queue
from colorama import Fore, Style

from freezer import Freezer

FREEZERS = 5
TECHNICIANS = 3

def freezer_functioning(freezer):
    while 1:
        desired_temperature = freezer.features["temperatureControl"]["desiredProperties"]["temperature"]
        current_humidity = freezer.features["temperatureControl"]["properties"]["humidity"]

        if random.randint(0, 100) < 40:
            freezer.break_freezer()
            manager_queue.put(freezer)
            manager_event.set()
            manager_event.clear()
            freezer.event.wait()
        else:
            temperature = random.randint(desired_temperature - 3, desired_temperature + 3)
            humidity = random.randint(current_humidity - 5 if current_humidity - 5 > 0 else 0, current_humidity + 5 if current_humidity + 5 < 100 else 100)
            freezer.update_temperature_control(temperature, humidity)

        time.sleep(random.randint(3, 5))

def technician_fix_freezer(technician_id, freezer):
    freezer.fix_freezer(technician_id)
    freezer.event.set()
    freezer.event.clear()
    available_technicians.put(technician_id)


def manager():
    while True:
        manager_event.wait()
        while not manager_queue.empty():
            if not available_technicians.empty():
                threading.Thread(target=technician_fix_freezer, args=(available_technicians.get(), manager_queue.get(),), daemon=True).start()

def print_dashboard(freezers):
    #izpolzvam bibliotecata colorama, za da dobavq cvetove pri printeneto za po-golqma `etlivost i krasota`
    while True:
        for freezer in freezers:
            status = Fore.GREEN if freezer.features['state']['properties']['working'] else Fore.RED

            print(f" {Style.BRIGHT}{Fore.MAGENTA}{freezer.thing_id}{Style.RESET_ALL}: ", end="")
            print(f"{status}{'On' if freezer.features['state']['properties']['working'] else 'Off'}{Style.RESET_ALL} | ", end="")
            print(f" {Style.BRIGHT}{Fore.MAGENTA}{freezer.features['temperatureControl']['properties']['temperature']}°C{Style.RESET_ALL} | ", end="")
            print(f" {Style.BRIGHT}{Fore.MAGENTA}{freezer.features['temperatureControl']['properties']['humidity']}%{Style.RESET_ALL} | ")

        time.sleep(1)

if __name__ == "__main__":
    # Generate technicians
    available_technicians = Queue()
    for i in range(TECHNICIANS):
        available_technicians.put(i + 1)

    # Generate freezer numbers
    freezer_numbers = [i + 1 for i in range(FREEZERS)]
    # Generate freezer thing IDs
    freezer_thing_ids = ["freezer-" + str(num) for num in freezer_numbers]
    # Generate freezers
    freezers = [Freezer(freezer_thing_ids[i], freezer_numbers[i]) for i in range(FREEZERS)]

    dashboard_thread = threading.Thread(target=print_dashboard, args=(freezers,), daemon=True)
    dashboard_thread.start()

    # Generate manager
    manager_thread = threading.Thread(target=manager, daemon=True)
    manager_queue = Queue()
    manager_event = threading.Event()

    # Start manager thread
    manager_thread.start()

    # Generate freezer threads
    freezer_threads = []
    for freezer in freezers:
        ft = threading.Thread(target=freezer_functioning, args=(freezer,), daemon=True)
        freezer_threads.append(ft)

    # Start freezer threads
    for ft in freezer_threads:
        ft.start()
        time.sleep(0.5)

    for ft in freezer_threads:
        ft.join()

    dashboard_thread.join()
    manager_thread.join()
