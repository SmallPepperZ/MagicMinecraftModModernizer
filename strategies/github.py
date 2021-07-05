import requests
import json
from utils import configuration as config
auth_header = {'Authorization': f'token {config["github_token"]}'}


def print_json(data:"dict|list"):
	print(json.dumps(data,indent=2))

def get_mod_releases(repo:str) -> "list[dict]|None":
	response = requests.get(f"https://api.github.com/repos/{repo}/releases", headers=auth_header).json()

	if not isinstance(response, list):
		print("Not found")
	elif len(response) < 1:
		print("No releases")
	else:
		return response
	
def get_release_jar(release:dict) -> "dict|None":
	assets = requests.get(release["assets_url"]).json()
	jars = [asset for asset in assets if asset["name"].endswith(".jar")]
	if len(jars) == 0:
		print("No jars found")
	elif len(jars) == 1:
		return jars[0]
	else:
		for index, jar in enumerate(jars):
			print(jar["name"])
			print(jar["name"].endswith("dev.jar"))
			print(jar["name"].endswith("sources.jar"))
			if jar["name"].endswith("dev.jar") or jar["name"].endswith("sources.jar"):
				
				jars.pop(index)
		if len(jars) == 1:
			return jars[0]
		else:
			print("Cannot determine correct jar")

def download_jar(jar_asset:dict):
	pass

print(get_release_jar(get_mod_releases("KaptainWutax/SeedCracker")[0]))