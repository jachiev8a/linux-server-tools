# linux-server-tools

specific tools and utils for linux servers

# Setup
- Create user

    ```
    adduser servertools
    ```
- Create directory in which the tool will be executed. and CD into it.

    ```
    mkdir /var/lib/server-tools/

    cd /var/lib/server-tools/
    ```
- clone the git project (let it create the directory):

    ```
    git clone git@git-test-oc.osramcontinental.net:eex/linux-server-tools.git
    ```
- Setup crontab line:

    ```
    # linux-server-tools (os-monitor) - contact: javier.ochoa
    0 23 * * * /data/git/linux-server-tools/os-monitor.sh
    ```

## Common Crontab
---
```
# linux-server-tools (os-monitor) - contact: javier.ochoa
0 23 * * * /var/lib/server-tools/linux-server-tools/os-monitor.sh
```
