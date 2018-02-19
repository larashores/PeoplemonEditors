from Editor.MoveAnimationEditor.components.animation import Animation

import os
import sys


def main():
    if len(sys.argv) != 2:
        raise ValueError("Invalid Number of arguments")
    path = sys.argv[1]

    for root, dirs, files in os.walk(path):
        for name in files:
            if not name.endswith('.devanim'):
                continue
            print(os.path.join(root, name))
            file = open(os.path.join(root, name), 'rb')
            data = bytearray(file.read())
            file.close()

            anim = Animation.fromByteArray(data)
            export = anim.export()

            file = open(os.path.join(root, os.path.splitext(name)[0] + '.anim'), 'wb')
            file.write(export)
            file.close()

if __name__ == '__main__':
    main()