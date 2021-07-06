import re

from strategies import modrinth, github
from utils import configuration as config

def check_strategy(line:str, index:int) -> "str|None":
	if re.fullmatch("\[\S+\]", line): #Check if it is a strategy header
		strategy_headers[index] = line
		print(line)
		return
	else:
		headers = [header for header in strategy_headers.keys() if index > header]
		headers.sort()
		return strategy_headers[headers[-1]]

def run_strategy(mod:str, strategy:str) -> None:
	strategies = {
		"[MODRINTH]": lambda: modrinth.download_optimal_version(mod),
		"[GITHUB]": lambda: modrinth.download_optimal_version(mod, config["minecraft_version"]),
		"[CURSEFORGE]": lambda: print(mod)
	}
	strategies[strategy]()

with open("mods.cfg", "r") as file:
	mod_list = []
	for line in file.readlines():
		commentless = line.split("#",1)[0].strip()
		if len(commentless) > 0:
			mod_list.append(commentless)

strategy_headers={}


for index, line in enumerate(mod_list):
	strategy = check_strategy(line, index)
	if strategy is not None:
		run_strategy(line, strategy)
