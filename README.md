# 🌈 Pretty && Rich History

Colorful and interactive directory and command history for `zshell`. Made rich with [github.com/willmcgugan/rich](https://github.com/willmcgugan/rich).

![BEHOLD!](./demo.gif)


## Setup:

1. `git clone https://github.com/slin63/rich-history`
1. `pip3 install -r requirements.txt`
2. Update and copy the contents below into your `.zshrc`.
```bash
# Rich & interactive command history
ph() {
    # Path to your Python3.7 executable
    PYTHONPATH="/usr/local/bin/python3.7"

    # Path to where you cloned this script
    SCRIPTPATH="/Users/seanlin/projects/sh/visual-history"

    # Call Python script
    HISTFILE=$HISTFILE $PYTHONPATH $SCRIPTPATH/commandhistory.py $(tput lines) && \
        print -z $(cat $SCRIPTPATH/prettycommandhistory)
}

# Rich & interactive cd history
setopt AUTO_PUSHD # automatically do a pushd of each directory you change to.
dh() {
    # Path to your Python3.7 executable
    PYTHONPATH="/usr/local/bin/python3.7"

    # Path to where you cloned this script
    SCRIPTPATH="/Users/seanlin/projects/sh/visual-history"

    # Call Python script
    $PYTHONPATH $SCRIPTPATH/cdhistory.py $(tput lines) $(dirs -v) && \
        print -z $(cat $SCRIPTPATH/prettycdhistory)

    # Uncomment below and comment above if you want to just immediately change directories
    # $PYTHONPATH $SCRIPTPATH/cdhistory.py $(tput lines) $(dirs -v) && \
    #     . $SCRIPTPATH/prettycdhistory
}
```
3. Source your `.zshrc` file.
4. Use `ph` or `dh` anywhere.
