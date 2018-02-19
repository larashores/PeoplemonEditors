import shelve
from Editor import constants

import os
import traceback
import dbm.dumb


def get_path():
    app_data = os.getenv('APPDATA')
    if app_data != '':
        root = os.path.join(app_data, 'Peoplemon', 'PeoplemonEditors')
        if not os.path.exists(root):
            os.makedirs(root)
    else:
        root = os.getcwd()
    return os.path.join(root, constants.PATH_FILE)


def save_location(locations):
    """
    Saves all path locations in a shelf. Locations are given in a simple dictionary that maps a description of the path
    to the path.

    :param locations: Dictionary of description[path]
    :return: None
    """
    try:
        shelf = shelve.open(get_path())
        for location in locations:
            shelf[location] = locations[location]
        shelf.close()
    except Exception as e:
        traceback.print_exc()


def load_location(location):
    return load_locations([location])[0]


def load_locations(locations):
    try:
        shelf = shelve.open(get_path())
        loc_list = []
        for location in locations:
            if location in shelf:
                loc_list.append(shelf[location])
            else:
                loc_list.append(None)
        shelf.close()
        return loc_list
    except:
        return [None for location in locations]


def load_location_dict(locations):
    try:
        shelf = shelve.open(get_path())
        loc_dict = {}
        for location in locations:
            if location in shelf:
                loc_dict[location] = shelf[location]
            else:
                loc_dict[location] = None

        shelf.close()
        return loc_dict
    except:
        return dict([(location, None) for location in locations])

