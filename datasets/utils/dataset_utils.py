import hashlib


class DatasetUtils:

    @staticmethod
    def get_file_hash(file_path, hash_algorithm='sha256'):
        hash_func = hashlib.new(hash_algorithm)

        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)

        return hash_func.hexdigest()

    @staticmethod
    def verify_file_hash(file, original_hash):
        return original_hash == DatasetUtils.get_file_hash(file)


class JsonDatasetUtils:

    @staticmethod
    def create_item(code_smells, source_code):
        return {
            "code_smells": code_smells,
            "source_code": source_code
        }
