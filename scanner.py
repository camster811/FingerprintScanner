import board
import adafruit_fingerprint
from digitalio import DigitalInOut, Direction
import time
import serial

CircuitPy = DigitalInOut(board.D13)
CircuitPy.direction = Direction.OUTPUT
serialRate = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
scannerLibrary = adafruit_fingerprint.Adafruit_Fingerprint(serialRate)


def fingerprint_check():
    print("Place your finger on the sensor")
    time.sleep(1)
    while scannerLibrary.get_image() != adafruit_fingerprint.OK:
        pass
    print("Formatting")
    time.sleep(1)
    if scannerLibrary.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching for fingerprint")
    time.sleep(1)
    if scannerLibrary.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


def list_ids():
    print("----------------")
    if scannerLibrary.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to load IDs")
    print("Currently stored IDs:", scannerLibrary.templates)
    print("----------------")


def store_fingerprint(location):
    counter = 1
    while counter < 3:
        if counter == 1:
            print("Place finger precisely on the sensor", end="")
            time.sleep(1)
        else:
            print("Place finger in the same spot again", end="")
            time.sleep(1)

        while True:
            fingerImage = scannerLibrary.get_image()
            if fingerImage == adafruit_fingerprint.OK:
                print("Image taken")
                time.sleep(1)
                break
            if fingerImage == adafruit_fingerprint.NOFINGER:
                print(".", end="")
                time.sleep(0.5)
            else:
                print("Error in scanning finger")
                return False

        print("Templating...", end="")
        time.sleep(1)
        fingerImage = scannerLibrary.image_2_tz(counter)
        if fingerImage == adafruit_fingerprint.OK:
            print("Templated")
            time.sleep(1)
        else:
            print("Error in templating")
            return False

        if counter == 1:
            print("Remove finger")
            time.sleep(1)
            while fingerImage != adafruit_fingerprint.NOFINGER:
                fingerImage = scannerLibrary.get_image()
        counter = counter + 1
    print("Creating model...", end="")
    time.sleep(1)
    fingerImage = scannerLibrary.create_model()
    if fingerImage == adafruit_fingerprint.OK:
        print("Created")
        time.sleep(1)
    else:
        print("Error in matching prints")
        time.sleep(1)
        return False

    print("Storing model #%d..." % location, end="")
    time.sleep(1)
    fingerImage = scannerLibrary.store_model(location)
    if fingerImage == adafruit_fingerprint.OK:
        print("Stored")
        time.sleep(1)
    else:
        print("Error in storing print")
        return False

    return True


def get_storage_ID():
    ID = int(input("Enter ID # from 1-127: "))
    if ID > 127:
        print("Please enter a number less than 128: ", end="")
        ID = int(input())
    elif ID < 1:
        print("Please enter a number greater than 0: ", end="")
        ID = int(input())

    return ID


def delete_print():
    if scannerLibrary.delete_model(get_storage_ID()) == adafruit_fingerprint.OK:
        print("Fingerprint deleted successfully")
        return True
    else:
        print("Error in deleting fingerprint")
    return False
