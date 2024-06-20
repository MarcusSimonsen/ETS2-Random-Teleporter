import keyboard


def print_pressed(event):
    print(f"Key: {event.name}, event: {event}")


if __name__ == "__main__":
    keyboard.hook(print_pressed)
    keyboard.wait()
