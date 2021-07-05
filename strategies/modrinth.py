from typing import Callable, Union
import os, sys
import requests
from datetime import datetime
import wget
import logging

from utils import configuration as config
from utils import master_logger
modrinth_logger = master_logger.getChild("modrinth")

def get_mod_logger(mod:str) -> logging.Logger:
	return modrinth_logger.getChild(mod)
	
if "debug" in [arg.lower() for arg in sys.argv]:
	master_logger.setLevel(logging.DEBUG)
else:
	master_logger.setLevel(logging.INFO)

#mod = "sodium"
def hash_file(filename:str) -> str:
	filehash = os.popen(f' shasum -a 1 {filename}').read().split()[0]
	logger.debug("hash retrieved")
	return filehash

def get_mod_versions(slug:str) -> "list[dict]":
	mod = requests.get(f'https://api.modrinth.com/api/v1/mod/{slug.lower()}')
	if not mod.ok:
		logger.error("Mod not found, check your slug and strategy")
		raise ValueError("Invalid slug")
	else:
		logger.debug("mod found")
		mod_data = mod.json()
		versions = requests.get(f'''https://api.modrinth.com/api/v1/versions?ids={str(mod_data["versions"]).replace("'", '"')}''').json()
		logger.debug("versions retrieved")
		return versions

def get_compatable_versions(mod_versions:list, version:str=config["minecraft_version"]) -> "list[dict]":
	compatible_versions = []
	for mod_version in mod_versions:
		game_versions = mod_version["game_versions"]
		if version in game_versions:
			compatible_versions.append(mod_version)
	return compatible_versions

def get_newest_version(mod_versions:list=None) -> dict:
	for version in mod_versions:
		update_time = version["date_published"]
		update_time = int(datetime.strptime(update_time[:update_time.find(".")], "%Y-%m-%dT%H:%M:%S").timestamp())
		version["update_time"] = update_time

	for version in mod_versions:
		if version["update_time"] == max([v["update_time"] for v in mod_versions]):
			return version

def get_newest_compatable_version(mod) -> "dict|None":
	try:
		mod_versions = get_mod_versions(mod)
	except:
		return
	return get_newest_version(get_compatable_versions(mod_versions))

def download_version(mod_version:dict, output:str=".") -> None:
	if mod_version is None:
		logger.warning("No compatable version found")
		return
	url = mod_version['files'][0]['url']
	filename = f"{output}/{mod_version['files'][0]['filename']}"
	sha1 = mod_version['files'][0]['hashes']['sha1']
	if not os.path.isfile(filename):
		wget.download(url, filename, None)
		logger.info("File downloaded")
		if hash_file(filename) != sha1:
			logger.error("Downloaded file does not match hash")
			os.remove(filename)

	elif os.path.isfile(filename) and hash_file(filename) != sha1:
		logger.warning(f'Invalid version of {filename} exists')
		os.remove(filename)
		wget.download(url, filename, None)
		logger.debug("File replaced with accurate file")
		if hash_file(filename) != sha1:
			logger.warn("Downloaded file does not match expected file")
			os.remove(filename)
	else:
		logger.info(f"{filename} already exists")
	
def download_optimal_version(mod:str, output_path:str) -> None:
	global logger
	logger = get_mod_logger(mod)
	logger.info("starting search")
	mod_version = get_newest_compatable_version(mod)
	if mod_version is not None:
		download_version(mod_version, output_path)
	else:
		logger.warning("No compatable version found")