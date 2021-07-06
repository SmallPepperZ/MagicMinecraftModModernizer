import requests, wget 
import json
import logging
import os
import jproperties
from utils import configuration as config
from utils import master_logger

auth_header = {'Authorization': f'token {config["github_token"]}'}

github_logger = master_logger.getChild("github")
logger = github_logger.getChild("main")

def get_mod_logger(mod:str) -> logging.Logger:
	return github_logger.getChild(mod)

def print_json(data:"dict|list"):
	print(json.dumps(data,indent=2))

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
			if not (jar["name"].endswith("dev.jar") or jar["name"].endswith("sources.jar") or jar["name"].endswith("-api.jar")):
				final_jars.append(jar)
		if len(final_jars) == 1:
			logger.info(f"determined '{final_jars[0]['name']}' to be the correct jar")
			return final_jars[0]
		else:
			logger.error("Cannot determine correct jar")

def get_compatible_release(mod:str, version:str, automatic:bool=False) -> "dict|None":
	releases = get_mod_releases(mod)
	if releases is None:
		logger.error("Repository has no releases")
		return
	sorted_versions = {
		"micro":[], # Match exact version, eg. 1.17.1-pre1
		"minor":[], # Match minor version, eg. 1.17.1
		"major":[]  # Match major version, eg. 1.17
	}
	version_separated = version.split(".")[:-1] + version.split(".")[-1].split("-", 1)
	for index, release in enumerate(releases.copy()):
		# try:
			mod_properties = requests.get(f"https://raw.githubusercontent.com/{mod}/{release['tag_name']}/gradle.properties").text
			properties = jproperties.Properties()
			properties.load(mod_properties)
			mc_version = properties.get("minecraft_version").data
			mc_version_separated = mc_version.split(".")[:-1] + mc_version.split(".")[-1].split("-", 1)
			release["mc_version"] = mc_version
			releases[index]["mc_version"] = mc_version
			if mc_version == version:
				logger.info(f'Micro       | {mc_version:8} | {release["name"]}')
				sorted_versions["micro"].append(release)
			elif mc_version_separated[:3] == version_separated[:3]:
				logger.debug(f'Minor       | {mc_version:8} | {release["name"]}')
				sorted_versions["minor"].append(release)
			elif mc_version_separated[:2] == version_separated[:2]:
				logger.debug(f'Major       | {mc_version:8} | {release["name"]}')
				sorted_versions["major"].append(release)
			else:
				logger.debug(f'Extra-Major | {mc_version:8} | {release["name"]}')
		# except:
		# 	logger.error("Cannot find version info")
		# 	return
	for key in ("micro", "minor", "major"):
		sorted_versions[key].sort(key=lambda x: x["published_at"], reverse=True)
	if len(sorted_versions["micro"]) >= 1:
		logger.info("Perfect release match found")
		return sorted_versions["micro"][0]
	elif len(sorted_versions["minor"]) >= 1:
		logger.info("Release version match found")
		return sorted_versions["minor"][0]
	elif len(sorted_versions["major"]) >= 1:
		for release in sorted_versions["major"]:
			if f'{".".join(version_separated[:2])}.x' in release["name"]:
				logger.info(f'Wildcard release version match found ({release["name"]}).')
				return release
	else:
		logger.warning("No detected version matches")
		return 

def download_jar(jar_asset:dict, output_dir:str) -> None:
	url = jar_asset["browser_download_url"]
	output_file = f"{output_dir}/{jar_asset['name']}"
	if not os.path.isfile(output_file):
		logger.info(f"Downloading to '{output_file}'")
		wget.download(url, out=output_file)
		logger.info(f"Downloaded")
	else:
		logger.info(f"File at {output_file} already exists")

def download_optimal_version(mod:str, version:str, output_path:str=config["output_path"] ):
	global logger
	logger = get_mod_logger(mod)
	compatible_release = get_compatible_release(mod, version)
	if compatible_release is not None:
		logger.info("Compatable release found")
		release_jar = get_release_jar(compatible_release)
	else:
		return	
	if release_jar is not None:
		logger.info("Compatable Jar found")
		download_jar(release_jar, output_path)
	else:
		logger.error("No releases found")

