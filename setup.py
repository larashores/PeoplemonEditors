__author__ = 'Vincent'

from distutils.core import setup
import py2exe

CONVERSATION_EDITOR = {'dest_base': 'Conversation Editor',
                       'script': r'Editor\ConversationEditor\main.py'}
CREDITS_EDITOR = {'dest_base': 'Credits Editor',
                  'script': r'Editor\CreditsEditor\main.py'}
ANIMATION_EDITOR = {'dest_base': 'Animation Editor',
                    'script': r'Editor\AnimationEditor\main.py'}
TRAINER_EDITOR = {'dest_base': 'Trainer Editor',
                  'script': r'Editor\TrainerEditor\main.py'}
TRAINER_PEOPLEMON_EDITOR = {'dest_base': 'Trainer Peoplemon Editor',
                            'script': r'Editor\TrainerPeoplemonEditor\main.py'}
MOVE_ANIMATION_EDITOR = {'dest_base': 'Move Animation Editor',
                         'script': r'Editor\MoveAnimationEditor\main.py',
                         'data_files': ('resources', r'Editor\\MoveAnimationEditor\\resources\\layour.png')}
NPC_EDITOR = {'dest_base': 'NPC Editor',
              'script': r'Editor\NPCEditor\main.py'}
WILD_PEOPLEMON_EDITOR = {'dest_base': 'Wild Peoplemon Editor',
                         'script': r'Editor\WildPeoplemonEditor\wildeditor.py'}
TRAVEL_MAP_EDITOR = {'dest_base': 'Travel Map Editor',
                         'script': r'Editor\TravelMapEditor\main.py'}

DEV_ANIM_TO_ANIM_SCRIPT = {'dest_base': 'devanim_to_anim',
                           'script': r'Editor\scripts\devanim_to_anim.py'}

possible_exludes = ['doctest', 'pdb', 'unittest', 'difflib', 'argparse', 'subproccess'
                                     'locale']

data_files = [('icons', [r'Editor\icons\editor.ico'])]
icon_resources = [(1, r'Editor\icons\editor.ico')]
builds = [ANIMATION_EDITOR]
for build in builds:
    if 'data_files' in build:
        data_files.extend(build['data_files'])
    build['icon_resources'] = icon_resources

setup(
    windows=builds,
    data_files=data_files,
    options={"py2exe": {'bundle_files': 2,
                        "excludes": ['doctest', 'pdb', 'unittest', 'difflib', 'argparse',
                                     'locale'],
                        "includes": []
                       }
            },
    zipfile=None
)

