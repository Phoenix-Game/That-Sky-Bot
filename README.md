# WonderStormBot
A discord bot for collecting bug reports, and a few other things.

# Server setup

This is a complete-from-the-ground-up setup guide for bot hosting. Skip to the `# TBD SECTION` section for guidance on common bot maintenance tasks.

I being with a base Ubuntu 20.04 install. Note the IP address given for the new system, and use that in place of `000.000.000.000` throughout this guide. If you have the option to register DNS configuration on a domain you own, do that so you don't have to remember that number!

Connect as root
```bash
ssh root@000.000.000.000
```

Once logged in, do some udpates, and accept any prompts:
```bash
apt update
apt upgrade
```

## Install telegraf
```bash
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt-get update && sudo apt-get install telegraf
```

## Install grafana
```bash
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
sudo wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.com/gpg.key
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install grafana
```

## Install other dependencies
```bash
sudo apt install influxdb
sudo apt install mysql-server
sudo apt install python3.9
sudo apt install python3.9-venv
sudo apt install tmux
```

## Configure firewall

The first 2 commands should confirm that openssh firewall rule is available and that ufw is not running.
```bash
ufw app list
ufw status
ufw allow openssh
ufw enable
ufw status
```
The output for `ufw status` should appear as follows:
```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
```

## User setup

Add a user. Some questions will be asked. Answers are optional
```bash
adduser username
```

Add sudo privilege to the new user
```bash
usermod -aG sudo username
```

# Continuing configuration

## SSH key setup

This setup presumes that you have created your own ssh key pair. Leave the root terminal logged in and open a new terminal. In the new terminal, copy your ssh public key into your home directory from your local machine:
```bash
ssh-copy-id username@000.000.000.000
```

Output should be similar to this:
```
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 4 key(s) remain to be installed -- if you are prompted now it is to install the new keys
username@000.000.000.000's password: 

Number of key(s) added:        1

Now try logging into the machine, with:   "ssh 'username@000.000.000.000'"
and check to make sure that only the key(s) you wanted were added.
```

Now attempt to login. If you configured a passphrase for your ssh key, you may be prompted for that. If you are prompted for password by the remote system, then ssh config is not complete and it's time to google for help!
```bash
ssh username@000.000.000.000
```

## Create a tmux configuration file

To use the screen multiplexer tmux and allow persistent terminal sessions across login sessions and from multiple hosts, tmux is strongly recommended. Create a conf file in your home directory:
```bash
vi ~/.tmux.conf
```

The contents of the file can be customized as you like. My default confiuration changes the control key sequence to `Ctrl-o` and sets up 4 panels:
```bash
# remap prefix from 'C-b' to 'C-o'
unbind C-b
set-option -g prefix C-o
bind-key C-o send-prefix

# split panes using | and -
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# reload config file (change file location to your the tmux.conf you want to use)
bind r source-file ~/.tmux.conf

# Enable mouse mode (tmux 2.1 and above)
set -g mouse on
# Set a key bind for toggling mouse mode in case you need mouse off sometimes
bind-key '"' set -g mouse\; display-message "mouse mode is now #{?mouse,on,off}"
unbind -n MouseDrag1Pane
unbind -Tcopy-mode MouseDrag1Pane

# session setup. Session and window names here are arbitrary and
# for ease of use. Replace [hostname] with something meaningful if you like.
# The text here will show in the tmux status line **verbatim**
# so make it whatever you want
new -s "wonderstorm" -n "WONDERSTORM[hostname]" bash

# a window in the bot directory with the python virtual-environment activated
splitw -h -p 50 -t 0 -c /home/username/wonderstormbot
send-keys 'source venv/bin/activate' Enter
# a window in the bot directory without venv
splitw -v -p 50 -t 0 -c /home/username/wonderstormbot
splitw -v -p 50 -t 2
selectp -t 0
```

Attach to a new or existing tmux server with the command
```bash
tmux attach
```

You should see 4 terminals open. Mouse intergration allows you to click each panel to activate it. Explore tmux documentation here:
https://github.com/tmux/tmux/wiki

Now detach from the tmux terminal using the control sequence `Ctrl-o` and then the `d` key. That should close tmux but leave the tmux server running. Then log out with `exit` or `Ctrl-d`.

From here on, any time you access the remote server, you can connect *and* attach to an existing tmux session with one command:
```bash
ssh username@000.000.000.000 -t tmux attach
```

If you want to have ssh key access to github, you can also copy the required keys into git, and copy your private key into your .ssh directory on the server. This guide does not include instructions for that procedure.

# Optional SSH security measures

## Disable password authentication and change SSH port

WARNING: failing to properly set these values may result in losing access to your host. Don't do this without confidence in the steps, or a backup method for accessing your host. For the purpose of this guide, the backup method is the hosting company's VNC access option in the web control panel.

Edit the SSHD config:
```bash
sudo vi /etc/ssh/sshd_config
```

This step must not be followed unless you have successfully configured and tested ssh key-based authentication. Uncomment and change the `PasswordAuthentication` line to disable password-based authentication and prevent brute-force password attacks:
```
PasswordAuthentication no
```

Change the port number to one that you want to use. Choose a number that's in range and unused (33333 is for example only):
```
Port 33333
```

Save your edits and exit vi.

Create a new firewall rule for the new port so lazy h4ck3rZ trolling default ssh port won't bother you:
```bash
sudo ufw allow 33333/tcp
```

Restart the sshd server:
```bash
sudo systemctl restart sshd
```

Cross fingers and hope you got it right! Log out and try logging in again on your newly configured port:
```bash
ssh -p 33333 username@000.000.000.000 -t tmux attach
```

Remove the firewall rule previously set for SSH:
```bash
sudo ufw delete allow ssh
```

# MySQL setup

## Initial configuration of mysql

Mysql defaults to having a root user only with no password-based access. You must log in as root to create new mysql users:
```bash
sudo su -
```

A mysql configuration file is advisable so you can set a pager and do any other desired config when you connect:
```bash
vi ~/.my.cnf
```

The contents of my .my.cnf file:
```ini
[mysql]
pager="less -iMRSX"

[client]
password="whatever your password is"
host=localhost
```

The `[client]` section allows you to connect easily from a terminal, and the `[mysql]` section adds a pager to format output that's streamed into a terminal

```
mysql
```

If you don't create a .my.cnf file, you can set a pager at the mysql prompt so you can read output easily:
```
pager less -S
```

## Create a read-only user with remote access privilege

In order to safely read the production database without fear of accidentally breaking things, it's a very good idea to have a read-only mysql user:
```sql
CREATE USER 'readonly_user'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'enter a strong password here';
GRANT SELECT on *.* TO 'readonly_user'@'localhost';
```
Don't lose the password!

## Create a read-write user with remote access privilege

Use a username that you like instead of "username."
```sql
CREATE USER 'username'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'enter a strong password here';
GRANT ALL PRIVILEGES ON *.* TO 'ahart'@'localhost' WITH GRANT OPTION;
```

Now you can connect to mysql as read-only or read-write, and you can connect using a client that supports ssh tunneling, such as DataGrip.

# Bot Deployment

This section details deployment of the bot to your hosting server.

## Clone the bot

```bash
git clone https://github.com/e-a-h/wonderstormbot.git ~/wonderstormbot
```

## Create a database schema

In a mysql client (command line or remote GUI client, doesn't matter) create a schema for the new bot. The name is not important, but must match in the bot config file. From a mysql command line, the command is:
```sql
create schema wonderstormbot;
```

## Edit configuration files

The bot comes with a config example, but you must create a config file. Values for the config are all sensitive and will not be repeated here. If you are setting up this bot and don't know what the values should be, then you will not be successful. Config can be populated from the example:
```bash
cd ~/wonderstormbot
cp config.example.json config.json
```

## Create a system service for the bot

Make a service file for the bot starting with the example service file:
```bash
mkdir ~/bin
cp ~/wonderstormbot/bot.example.service ~/bin/wonderstormbot.service
vi ~/bin/wonderstormbot.service
```

Edit the WorkingDirectory, ExecStart and User lines to match your environment. Edit other info as necessary when deviating from this guide. Ensure that the Bootloader.sh script is executable and contents are correct for your environment.

Start with the Bootloader.example.sh and edit contents to match your environment:

```bash
cd ~/wonderstormbot
cp Bootloader.example.sh Bootloader.sh
vi Bootloader.sh
```

Enable the service!
```bash
sudo systemctl enable /home/username/bin/wonderstormbot.service --now
```

## Start and stop the bot

Commands to start, stop, restart and check status
```bash
sudo systemctl stop wonderstormbot
sudo systemctl start wonderstormbot
sudo systemctl restart wonderstormbot
sudo systemctl status wonderstormbot
```

## Bot logging

Bot logs are stored in the bot directory in a folder called "logs." Watch the log in realtime like this:

```bash
tail -f ~/wonderstormbot/logs/wonderstormbot.log
```

## Webhook

Grafana can be used to trigger a webhook that restarts the bot in case certain failure conditions are detected. Setting rules for these conditions *is up to you* and should be done with care.

Install webhook
```bash
sudo apt install webhook
```

Create a webhook file
```
something goes here
```

Test it.

## Discord guild steps

This assumes the hosting discord guild uses native member onboarding. Rules verification and phone number requirement are highly recommended.

1. Create channels for:
   * Bug reports per platform and branch, e.g. #bugs-android-beta
   * Bug reporting maintenance channel
1. Create member role and add the id to config.json
1. Channel permissions:
   * Bug report channels should be
     * **@everone:** -read, -add reaction
     * **members:** +read
     * **bot:** +read, +add reaction
1. Config file required. see config.example.json and fill in channel IDs, guild ID, role IDs