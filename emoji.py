__module_name__ = "emoji"
__module_version__ = "2.1"
__module_description__ = "Emoji support for HexChat"

import emojis
import hexchat
import re

#############################################
#                                           #
#               Configuration               #
#                                           #
#############################################

# EM command (/em <text>) needs to mimic another command
# It should mimic SAY or ME, other commands may not work
# SAY command: "say"
# ME command:  "me"
COMMAND_EM_SIMULATES = "say"

# Override SAY command to translate the message to emojis if any
# Note: This will trigger when the user hits enter or use /say
# Enabled:  True
# Disabled: False
OVERRIDE_SAY = True

# Override ME command to translate the message to emojis if any
# Enabled:  True
# Disabled: False
OVERRIDE_ME = True

# Convert emoticons into emojis as in Slack
# See table conversion in EMOTICON_TO_EMOJI_ALIASES
# Enabled:  True
# Disabled: False
EMOTICON_TO_EMOJI = True

# Emoticon to Emoji aliases to use if EMOTICON_TO_EMOJI is True
# This is not an extensive list, but includes most popular ones
# Remember to escape backslashs with another backslash: \ --> \\
EMOTICON_TO_EMOJI_ALIASES = {
    "<3": ":heart:",
    "</3": ":broken_heart:",
    "8)": ":sunglasses:",
    "8-)": ":sunglasses:",
    "D:": ":anguished:",
    ":'(": ":cry:",
    ":o)": ":monkey_face:",
    ":*": ":kissing_heart:",
    ":-*": ":kissing_heart:",
    "=)": ":smiley:",
    "=-)": ":smiley:",
    ":D": ":smile:",
    ":-D": ":smile:",
    ";)": ":wink:",
    ";-)": ":wink:",
    ":>": ":laughing:",
    ":->": ":laughing:",
    ":|": ":neutral_face:",
    ":-|": ":neutral_face:",
    ":o": ":open_mouth:",
    ":-o": ":open_mouth:",
    ">:(": ":angry:",
    ">:-(": ":angry:",
    ":)": ":slightly_smiling_face:",
    "(:": ":slightly_smiling_face:",
    ":-)": ":slightly_smiling_face:",
    ":(": ":disappointed:",
    "):": ":disappointed:",
    ":-(": ":disappointed:",
    ":/": ":confused:",
    ":-/": ":confused:",
    ":\\": ":confused:",
    ":-\\": ":confused:",
    ":P": ":stuck_out_tongue:",
    ":p": ":stuck_out_tongue:",
    ":-p": ":stuck_out_tongue:",
    ":b": ":stuck_out_tongue:",
    ":-b": ":stuck_out_tongue:",
    ";P": ":stuck_out_tongue_winking_eye:",
    ";p": ":stuck_out_tongue_winking_eye:",
    ";-p": ":stuck_out_tongue_winking_eye:",
    ";b": ":stuck_out_tongue_winking_eye:",
    ";-b": ":stuck_out_tongue_winking_eye:",
    "}:>": ":smiling_imp:",
}


##################################################################
#                            WARNING!                            #
#                                                                #
# Do not edit below this area unless you know what you are doing #
#                                                                #
#                              See:                              #
#  https://hexchat.readthedocs.io/en/latest/script_python.html   #
##################################################################


def build_re_groups():
    """
        Build a regex string based on the emoticon to emoji aliases
    """
    for alias in EMOTICON_TO_EMOJI_ALIASES:
        yield re.escape(alias)


def get_emoji_alias(match):
    return match.group(1) + EMOTICON_TO_EMOJI_ALIASES[match.group(2)]


RE_GROUPS = "|".join(build_re_groups())
RE_EMOTICON_TO_EMOJI_ALIASES = re.compile("(^|\s)(" + RE_GROUPS + ")(?=\s|$)")


def emojize(msg, emoticon_to_emoji=EMOTICON_TO_EMOJI):
    """ Emojize messages and convert emoticons to emojis if enabled """
    if emoticon_to_emoji:
        msg = RE_EMOTICON_TO_EMOJI_ALIASES.sub(get_emoji_alias, msg)

    return emojis.encode(msg)


def say_cb(words, word_eol, userdata):
    """ Override defaut say command callback to emojize messages """
    if len(word_eol) > 0:
        msg = word_eol[0]
        emojized = emojize(msg)

        if msg != emojized:
            hexchat.command(f"say {emojized}")
            return hexchat.EAT_HEXCHAT

    return hexchat.EAT_NONE


def me_cb(words, word_eol, userdata):
    """ Override defaut me command callback to emojize messages """
    if len(word_eol) > 1:
        msg = word_eol[1]
        emojized = emojize(msg)

        if msg != emojized:
            hexchat.command(f"me {emojized}")
            return hexchat.EAT_HEXCHAT

    return hexchat.EAT_NONE


def em_cb(words, word_eol, userdata):
    """ EM command callback to emojize messages """
    if len(word_eol) > 1:
        msg = word_eol[1]
        emojized = emojize(msg)
        cmd = userdata.get("command", "say")

        hexchat.command(f"{cmd} {emojized}")
    else:
        hexchat.command("help em")

    return hexchat.EAT_ALL


def unload_cb(userdata):
    print(f"{__module_name__} unloaded.")


def load_plugin():
    if OVERRIDE_SAY:
        # override /say command
        hexchat.hook_command("", say_cb)

    if OVERRIDE_ME:
        # override /me command
        hexchat.hook_command("ME", me_cb)

    # register emojify command (/em <text>)
    hexchat.hook_command("EM", em_cb,
        userdata={"command": COMMAND_EM_SIMULATES},
        help="Usage: EM <text>, converts text with emojis aliases into an unicode encoded text")

    hexchat.hook_unload(unload_cb)

    print(f"{__module_name__} version {__module_version__} loaded.")


if __name__ == "__main__":
    load_plugin()
