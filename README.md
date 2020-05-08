# Pretty-history

History. But pretty!

## Setup:

1. `git clone https://github.com/slin63/rich-history`
1. `pip3 install -r requirements.txt`
2. Update and copy the contents below into your `.zshrc` or `.bashrc` or whatever runcom file you use.
```bash
# Rich & interactive command history
ph() {
    # Path to your Python3.7 executable
    PYTHONPATH="/usr/local/bin/python3.7"

    # Path to where you cloned this script
    SCRIPTPATH="/Users/seanlin/projects/sh/visual-history"

    # Magic
    HISTFILE=$HISTFILE $PYTHONPATH $SCRIPTPATH/history.py $(tput lines) && \
        print -z $(cat $SCRIPTPATH/prettyhistory)
}

# Rich & interactive cd -- history
# TODO
```
3. Source your `.rc` file.
4. Use `ph` anywhere.
