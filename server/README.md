
## Overview

* Server - A simple server that encrypts and decrypts text using a key provided as a docker secret.
TODO maybe use a vault instead of this server.
* An Obsidian plugin (*obsidian-encrypted-refs*) that handles the encryption and decryption of the text.

To migrate the vault from $key1$ to $key2$
1. Backup
2. in ```obsidian_note```: ```python3.10 shared/scripts/main.py migrate .```


# Old README 
pour tester  http POST http://localhost:8000/encrypt to_decrypt="bE0maisgTUmMijz+k0WoPWbxPUVVy8H39FUmVRPFHuC7WLM2pfDdn8NUVJRPqafH"


npm run dev
