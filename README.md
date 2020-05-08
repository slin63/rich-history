# pretty-history

History. But pretty!

## Setup:

1. `git clone me`
2. Update and copy the contents below into your `.zshrc` or `.bashrc` or whatever runcom file you use.
```bash
ph(
    # Path to your Python3.7 executable
    PYTHONPATH="/usr/local/bin/python3.7"

    # Path to where you cloned this script
    SCRIPTPATH="/Users/seanlin/projects/sh/visual-history"

    # Magic
    HISTFILE=$HISTFILE $PYTHONPATH $SCRIPTPATH/history.py $(tput lines) && \
        print -z $(cat $SCRIPTPATH/prettyhistory)
)
```
3. Source your `.rc` file.
4. `ph` anywhere.
