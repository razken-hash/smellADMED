import requests
import re


class GithubUtils:

    @staticmethod
    def generate_raw_url(owner=None, repository=None, owner_and_repository=None, branch=None, commit_hash=None, path=None):
        raw_url_base = "https://raw.githubusercontent.com"
        if not owner_and_repository:
            if not commit_hash:
                return f"{raw_url_base}/{owner}/{repository}/{branch}/{path}"
            return f"{raw_url_base}/{owner}/{repository}/{commit_hash}/{path}"
        if not commit_hash:
            return f"{raw_url_base}/{owner_and_repository}/{branch}/{path}"
        return f"{raw_url_base}/{owner_and_repository}/{commit_hash}/{path}"

    @staticmethod
    def generate_blob_url(owner=None, repository=None, owner_and_repository=None, branch=None, commit_hash=None, path=None):
        raw_url_base = "https://github.com"
        if not owner_and_repository:
            if not commit_hash:
                return f"{raw_url_base}/{owner}/{repository}/blob/{branch}/{path}"
            return f"{raw_url_base}/{owner}/{repository}/blob/{commit_hash}/{path}"
        if not commit_hash:
            return f"{raw_url_base}/{owner_and_repository}/blob/{branch}/{path}"
        return f"{raw_url_base}/{owner_and_repository}/blob/{commit_hash}/{path}"

    @staticmethod
    def convert_blob_to_raw_url(blob_url: str):
        # if "#" in blob_url:
        #     blob_url = blob_url[0:blob_url.rfind("/")]
        return blob_url.replace(
            "github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    @staticmethod
    def convert_raw_to_blob_url(raw_url: str):
        if "#" in raw_url:
            raw_url = raw_url[0:raw_url.rfind("/")]

        slash_count = 0
        blob_position = 0
        for index, char in enumerate(raw_url):
            if char == '/':
                slash_count += 1
                if slash_count == 5:
                    blob_position = index
                    break

        blob_url = raw_url[:blob_position + 1] + \
            "blob/" + raw_url[blob_position + 1:]
        return blob_url.replace(
            "raw.githubusercontent.com", "github.com")

    @staticmethod
    def clone_code(raw_url=""):
        try:
            response = requests.get(raw_url[:raw_url.index("#") - 1])
            if response.status_code == 200:
                if "#" in raw_url:
                    match = re.search(r'#L(\d+)-L(\d+)', raw_url)
                    if not match:
                        raise ValueError("Line range not found in the URL")
                    start_line, end_line = map(int, match.groups())
                    lines = response.text.splitlines()
                    selected_lines = lines[start_line - 1:end_line]
                    # ! COMMENTS MAY CAUSE PROBLEM
                    return "\n".join(selected_lines) + "   \n"
                return response.text + "   \n"
            else:
                print(f"{response.status_code}: FAILED Code Clone")
        except:
            print("EXCEPTION: FAILED Code Clone")
        return ""

    @staticmethod
    def generate_github_api_url_to_locate_file_by_commit_hash_and_file_name(owner=None, repository=None, owner_and_repository=None, branch=None, commit_hash=None):
        github_api_url_base = "https://api.github.com/repos"
        if not owner_and_repository:
            if not commit_hash:
                return f"{github_api_url_base}/{owner}/{repository}/git/trees/{branch}?recursive=1"
            return f"{github_api_url_base}/{owner}/{repository}/git/trees/{commit_hash}?recursive=1"
        if not commit_hash:  # ! Not yet sure
            return f"{github_api_url_base}/{owner_and_repository}/git/trees/{branch}?recursive=1"
        return f"{github_api_url_base}/{owner_and_repository}/git/trees/{commit_hash}?recursive=1"

    @staticmethod
    def locate_file_by_commit_hash_and_file_name(owner=None, repository=None, owner_and_repository=None, branch=None, commit_hash=None, file_name=""):
        github_api_url = GithubUtils.generate_github_api_url_to_locate_file_by_commit_hash_and_file_name(
            owner=owner, repository=repository, owner_and_repository=owner_and_repository, branch=branch, commit_hash=commit_hash)
        print(github_api_url)
        response = requests.get(github_api_url)
        if response.status_code == 200:
            tree_data = response.json().get("tree", [])

            matching_files = [
                GithubUtils.generate_blob_url(owner=owner, repository=repository, owner_and_repository=owner_and_repository,
                                              branch=branch, commit_hash=commit_hash, path=file["path"])
                for file in tree_data if file["path"].endswith(file_name)
            ]

            if matching_files:
                print("Possible GitHub URLs:")
                for url in matching_files:
                    print(url)
                return matching_files[0]
            else:
                print("No File Exist")
        else:
            print("EXCEPTION", response.status_code)

        return ""
