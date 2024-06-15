#!/usr/bin/env python3
import argparse
import pyautogui
import time
import struct
import base64
import random


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
    print('Generate random city')


def random_position(args):
    # Choose random coords
    x = random.random()
    y = random.random()
    z = 100.0
    # Generate ID string
    id_str = coords_to_id(x, y, z)
    # Print to user
    print(f'Your ID string is: {id_str}')


def write_command(args):
    print(f'Waiting for {args.delay} seconds before writing command')
    time.sleep(args.delay)

    print('Writing command')
    #pyautogui.write('~´')


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
    parser.add_argument(
        "id",
        type=str,
        help='The ID string to use'
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=10,
        help='The amount of seconds to sleep before writing command'
    )

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()
