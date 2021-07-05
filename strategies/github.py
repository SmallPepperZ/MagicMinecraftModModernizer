import requests, wget 
import json
import logging
import os
from utils import configuration as config
from utils import master_logger

auth_header = {'Authorization': f'token {config["github_token"]}'}

github_logger = master_logger.getChild("github")
logger = github_logger.getChild("main")

def get_mod_logger(mod:str) -> logging.Logger:
	return github_logger.getChild(mod)

def print_json(data:"dict|list"):
	logger.info(json.dumps(data,indent=2))

def get_mod_releases(repo:str) -> "list[dict]|None":
	response = requests.get(f"https://api.github.com/repos/{repo}/releases", headers=auth_header).json()

	if not isinstance(response, list):
		logger.error("Not found")
	elif len(response) < 1:
		logger.error("No releases")
	else:
		return response
	
def get_release_jar(release:dict) -> "dict|None":
	assets = requests.get(release["assets_url"]).json()
	jars = [asset for asset in assets if asset["name"].endswith(".jar")]
	if len(jars) == 0:
		logger.error("No jars found")
	elif len(jars) == 1:
		logger.info("jar found")
		return jars[0]
	else:
		final_jars = []
		for jar in jars:
			if not (jar["name"].endswith("dev.jar") or jar["name"].endswith("sources.jar")):
				final_jars.append(jar)
		if len(final_jars) == 1:
			logger.info(f"determined '{final_jars[0]['name']}' to be the correct jar")
			return final_jars[0]
		else:
			logger.error("Cannot determine correct jar")

def download_jar(jar_asset:dict, output_dir:str) -> None:
	url = jar_asset["browser_download_url"]
	output_file = f"{output_dir}/{jar_asset['name']}"
	if not os.path.isfile(output_file):
		logger.info(f"Downloading to '{output_file}'")
		wget.download(url, out=output_file)
		logger.info(f"Downloaded")
	else:
		logger.info(f"File at {output_file} already exists")

def download_optimal_version(mod:str, output_path:str=config["output_path"]):
	global logger
	logger = get_mod_logger(mod)
	pass
print(get_release_jar(get_mod_releases("KaptainWutax/SeedCracker")[0]))