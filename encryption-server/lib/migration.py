import re
import pathlib
from .crypto import encrypt_string_aes_256, decrypt_aes_256_cbc 
import base64

pattern = r'<span class="inline-protected">((?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)</span>'

class Migration:
    def __init__(self, directory, last_password, new_password) -> None:
        self.directory = directory
        self.last_password = last_password
        self.new_password = new_password


    def find_files_recursive(self, directory):
        path = pathlib.Path(directory)
        files = path.glob('**/*.md')
        return [str(file) for file in files if file.is_file()]

    def update_token(self, encrypted_string):
        encrypted_string = base64.b64decode(encrypted_string)
        raw_string = decrypt_aes_256_cbc(encrypted_string, self.last_password)
        new_encrypted_string = encrypt_string_aes_256(raw_string, self.new_password)
        new_encrypted_string = base64.b64encode(new_encrypted_string).decode()

        return new_encrypted_string

    def replace_string_in_file(self, file_path, mocked=False):
        with open(file_path, 'r') as file:
            content = file.read()

        if mocked:
            for token in re.findall(pattern, content):
                print(f"Find token {token} file: ", file_path)
        else:
            tokens = re.findall(pattern, content)
            new_tokens = [self.update_token(token) for token in tokens]

            for token,new_token in zip(tokens, new_tokens):
                content = content.replace(token, new_token)

            with open(file_path, 'w') as file:
                file.write(content)

    def migrate(self):
        for file in self.find_files_recursive(self.directory):
            self.replace_string_in_file(file)
        print("End migration")

    def search(self):
        for file in self.find_files_recursive(self.directory):
            self.replace_string_in_file(file, mocked=True)

        print("End search")