if ! [ -f mods.cfg ]
then
	cp mods.cfg.example mods.cfg
fi
if ! [ -f settings.cfg ]
then
	cp settings.cfg.example settings.cfg
fi
cd $(dirname "$0")
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt