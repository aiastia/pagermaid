# Jarvis

Jarvis is a utility daemon for telegram.

It automates a range of tasks by responding to commands issued to self.

## Get Started

A venv is recommended for this program, python 3.6+ is required too.

Inside the project directory, run:

```bash
/usr/bin/env python3 -m virtualenv venv
```

And then:

```bash
source venv/bin/activate
```

After that, install dependencies:

```bash
pip install -r requirements.txt
```

Generate config files:

```bash
mv config.gen.env config.env
vim config.env
```

Fill in your options, and start the bot.

```bash
python -m jarvis
```

Follow the prompts, after you login, do -help in telegram for the help message.

## Using SystemD

After running the bot first time, you can consider using the systemd unit.

Move the directory to /var/lib:

```bash
sudo mv jarvis /var/lib/jarvis
```

Edit the sample unit file in utils/ to meet your work user and copy it into systemd unit files.

```bash
sudo vim /var/lib/jarvis/utils/jarvis.service
sudo cp /var/lib/jarvis/utils/jarvis.service /usr/lib/systemd/system/jarvis.service
```

Now reload systemd and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now jarvis.service
```