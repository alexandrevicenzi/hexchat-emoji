__module_name__ = "emoji"
__module_version__ = "1.0"
__module_description__ = "Emoji support for HexChat"

import re

import emojis
import hexchat


# you can use /em :emoji:
# /em can simulate say or me
COMMAND_EM_SIMULATE = 'say'

# Auto translate /say message to emojis if any
OVERRIDE_SAY = True

# Auto translate /me message to emojis if any
OVERRIDE_ME = True

# Convert emoticons into emojis as in Slack
EMOTICON_TO_EMOJI = True


EMOTICON_TO_EMOJI_ALIASES = {
    '<3': ':heart:',
    '</3': ':broken_heart:',
    '8)': ':sunglasses:',
    '8-)': ':sunglasses:',
    'D:': ':anguished:',
    ':\'(': ':cry:',
    ':o)': ':monkey_face:',
    ':*': ':kissing_heart:',
    ':-*': ':kissing_heart:',
    '=)': ':smiley:',
    '=-)': ':smiley:',
    ':D': ':smile:',
    ':-D': ':smile:',
    ';)': ':wink:',
    ';-)': ':wink:',
    ':>': ':laughing:',
    ':->': ':laughing:',
    ':|': ':neutral_face:',
    ':-|': ':neutral_face:',
    ':o': ':open_mouth:',
    ':-o': ':open_mouth:',
    '>:(': ':angry:',
    '>:-(': ':angry:',
    ':)': ':slightly_smiling_face:',
    '(:': ':slightly_smiling_face:',
    ':-)': ':slightly_smiling_face:',
    ':(': ':disappointed:',
    '):': ':disappointed:',
    ':-(': ':disappointed:',
    ':-/': ':confused:',
    ':\\': ':confused:',
    ':-\\': ':confused:',
    ':P': ':stuck_out_tongue:',
    ':p': ':stuck_out_tongue:',
    ':-p': ':stuck_out_tongue:',
    ':b': ':stuck_out_tongue:',
    ':-b': ':stuck_out_tongue:',
    ';P': ':stuck_out_tongue_winking_eye:',
    ';p': ':stuck_out_tongue_winking_eye:',
    ';-p': ':stuck_out_tongue_winking_eye:',
    ';b': ':stuck_out_tongue_winking_eye:',
    ';-b': ':stuck_out_tongue_winking_eye:',
}


RE_GROUPS = '|'.join(['({0})'.format(re.escape(x)) for x in EMOTICON_TO_EMOJI_ALIASES])
RE_EMOTICON_TO_EMOJI_ALIASES = re.compile(RE_GROUPS)


def emojize(msg):
    if EMOTICON_TO_EMOJI:
        msg = RE_EMOTICON_TO_EMOJI_ALIASES.sub(lambda match: EMOTICON_TO_EMOJI_ALIASES[match.group(0)], msg)

    return emojis.encode(msg)


def msg_cb(words, word_eol, userdata):
    msg = word_eol[0]
    emojized = emojize(msg)

    if msg != emojized:
        hexchat.command('say {0}'.format(emojized))
        return hexchat.EAT_HEXCHAT

    return hexchat.EAT_NONE


def say_cb(words, word_eol, userdata):
    if len(word_eol) > 1:
        msg = word_eol[1]
        emojized = emojize(msg)

        if msg != emojized:
            hexchat.command('say {0}'.format(emojized))
            return hexchat.EAT_HEXCHAT

        return hexchat.EAT_NONE

    hexchat.command('help em')
    return hexchat.EAT_ALL


def me_cb(words, word_eol, userdata):
    if len(word_eol) > 1:
        msg = word_eol[1]
        emojized = emojize(msg)

        if msg != emojized:
            hexchat.command('me {0}'.format(emojized))
            return hexchat.EAT_HEXCHAT

        return hexchat.EAT_NONE

    hexchat.command('help em')
    return hexchat.EAT_ALL


def em_cb(words, word_eol, userdata):
    if len(word_eol) > 1:
        msg = word_eol[1]
        emojized = emojize(msg)

        if COMMAND_EM_SIMULATE in ['say', 'em']:
            cmd = COMMAND_EM_SIMULATE
        else:
            cmd = 'say'

        hexchat.command('{0} {1}'.format(cmd, emojized))
        return hexchat.EAT_HEXCHAT

    hexchat.command('help em')
    return hexchat.EAT_ALL


def unload_cb(userdata):
    print('{0} unloaded.'.format(__module_name__))


if OVERRIDE_SAY:
    # override input enter
    hexchat.hook_command('', msg_cb)
    # override SAY command
    hexchat.hook_command('SAY', say_cb)

if OVERRIDE_ME:
    # override ME command
    hexchat.hook_command('ME', me_cb)

# EM emojify command
hexchat.hook_command('EM', em_cb, help='Usage: EM <text>, converts emoji alias into unicode encoded text')

hexchat.hook_unload(unload_cb)

print('{0} version {1} loaded.'.format(__module_name__, __module_version__))
