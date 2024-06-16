#!/usr/bin/env python3
import argparse
import keyboard
import time
import struct
import base64
import random
import json
import ctypes


# Define necessary constants and structures
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Define SendInput function
SendInput = ctypes.windll.user32.SendInput

def press_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Virtual-Key code for the Enter key
VK_RETURN = 0x0D


def coords_to_id(x: float, y: float, z: float) -> str:
    # Pack the coords into bytes
    packed = struct.pack('fff', x, y, z)
    # Encode bytes into a Base64 string
    encoded = base64.urlsafe_b64encode(packed).rstrip(b'=').decode('ascii')
    return encoded


def id_to_coords(id_str: str) -> (float, float, float):
    # Decode Base64 string into bytes
    padded = id_str + '=' * (-len(id_str) % 4)
    decoded = base64.urlsafe_b64decode(padded)
    # Unpack bytes back into floats
    unpacked = struct.unpack('fff', decoded)
    return unpacked


def random_city(args):
    with open(args.file, 'r', encoding='utf8') as file:
        data = json.load(file)
        cities = data['citiesList']

        idx = random.randint(0, len(cities))
        city = cities[idx]

        print(city['realName'])

        x = float(city['x'])
        y = float(city['y'])
        z = float(city['z'])

        print(x, y, z)

        id_str = coords_to_id(x, y, z)

        print(f'Your ID string is: {id_str}')


def random_position(args):
    # Choose random coords
    x = -85_000 + random.random() + (85_000 + 70_000)
    y = 150.0
    z = random.random()
    # Generate ID string
    id_str = coords_to_id(x, y, z)
    # Print to user
    print(f'Your ID string is: {id_str}')


def write_command(args):
    print(f'Waiting for {args.delay} seconds before writing command')
    time.sleep(args.delay)

    x, y, z = id_to_coords(args.id)

    print('Writing command')
    # Open console
    keyboard.press_and_release(args.console)
    time.sleep(0.1)
    # Write command
    keyboard.write(f'goto {x};{y};{z}')
    time.sleep(1)
    keyboard.press_and_release('enter') # Or maybe return?
    time.sleep(0.1)
    # Close console
    # keyboard.press_and_release(args.console)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Generate a ID and auto write command to teleport to a
            random position in ETS2'''
    )

    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )

    parser_random_city = subparsers.add_parser(
        'generate-city',
        help='Generate ID for a randon city'
    )
    parser_random_city.set_defaults(func=random_city)
    parser_random_city.add_argument(
        "--file",
        default=('cities.json'),
        help="Json file of cities to use"
    )

    parser_random_position = subparsers.add_parser(
        'generate-position',
        help='Generate ID for a random position'
    )
    parser_random_position.set_defaults(func=random_position)

    parser_write_command = subparsers.add_parser(
        'write-command',
        help='Automatically write the command after delay'
    )
    parser_write_command.set_defaults(func=write_command)
    parser_write_command.add_argument(
        "id",
        type=str,
        help='The ID string to use'
    )
    parser_write_command.add_argument(
        "--delay",
        type=int,
        default=10,
        help='The amount of seconds to sleep before writing command'
    )
    parser_write_command.add_argument(
        "--console",
        type=str,
        default='f10',
        help='The key to open the console'
    )

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()
