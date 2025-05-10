import re
import requests


class JavaCodeCleaner:

    CLEANER_API_ADDRESS = "http://localhost:7001"

    @staticmethod
    def clean_by_cleaner_api(originalCode: str):
        # print(originalCode)
        # originalCode = re.sub(r'//.*', '', originalCode)
        try:
            data = requests.post(
                f"{JavaCodeCleaner.CLEANER_API_ADDRESS}/api/v1/clean-code",
                json={
                    "originalCode": originalCode
                },
                headers={
                    'Content-Type': 'application/json',
                }
            )

            # print(data.status_code)
            if data.status_code == 200:
                return data.json()["cleanCode"]
            else:
                originalCode = "class C{" + originalCode + "}"
                data = requests.post(
                    f"{JavaCodeCleaner.CLEANER_API_ADDRESS}/api/v1/clean-code",
                    json={
                        "originalCode": originalCode
                    },
                    headers={
                        'Content-Type': 'application/json',
                    }
                )
                # print(data.status_code)
                if data.status_code == 200:
                    return data.json()["cleanCode"][8: -1]
        except:
            print("ERROR")
        return ""

    @staticmethod
    def clean(code):
        # SINGLE-LINE COMMENTS //
        code = re.sub(r'//.*/n', '', code)

        # JAVADoc AND MULTI-LINE COMMENTS /** */ AND /* */
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        # EXTRA SPACE TO ONE SPACE
        code = re.sub(r'\s+', ' ', code).strip()

        # IMPORT STATEMENT
        code = re.sub(
            r'\s*import\s+(static\s+)?[^\s;]+(\.[^\s;]+)*;\s*', '', code, flags=re.MULTILINE)

        code = re.sub(
            r'\s*package\s+[^\s;]+;\s*', '', code, flags=re.MULTILINE)

        return code

    @staticmethod
    def clean_extra_space(code):
        return re.sub(r'\s+', ' ', code).strip()

    @staticmethod
    def clean_single_line_comments(code):
        return re.sub(r'//.*', '', code)
