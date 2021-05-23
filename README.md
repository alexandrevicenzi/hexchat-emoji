# hexchat-emoji

Emoji addon for HexChat

## About

hexchat-emoji allows you to use Slack-like emoji notation in HexChat.

This input:

`This is a message with emojis :smile: :snake:`

Becomes this message:

`This is a message with emojis 😄 🐍`

## Installation

### Python 3 plugin

Ensure you have `Python 3` plugin installed in HexChat, check in `Window > Plugins and Scripts`.

Ubuntu: `apt install hexchat-python3`

Fedora: Present in `hexchat` package, no dependencies needed

openSUSE: `zypper in hexchat-plugins-python3`

> Python 3 plugin name may vary on another distros.

### Emojis library

Ensure you have `emojis` library installed in your system, check with `pip3 freeze | grep emojis`.

`pip3 install -U emojis`

> This command may require `sudo` to install in some distros

### HexChat emoji addon

Copy `emoji.py` to `~/.config/hexchat/addons`.

> HexChat addons path may vary your distro.

Restart HexChat.

## Settings

Emoji addon has a few settings you can change.
They are located and documented in the top of `emoji.py` as constants.

## License

MIT
