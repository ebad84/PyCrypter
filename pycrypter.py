import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import re
import time
def crypter_files(file_path):
    import_datas = """
    #begin : base librarys for importing.
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
    #end : base librarys for importing."""

    decrypt_func = """def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding
    """


    def imp_data_finder(t):
        text = t
        imports = []
        print(imports)
        print("==========================================================")
        for i in text.split("\n"):
            for i2 in re.findall(r"^\W{0,}([f-i][r - m].{1,})",i):
                imports.append(i2)
                text = text.replace(i2,"")
        print(imports)
        print("==========================================================")
        return [imports,text]

    def encrypt(key, source, encode=True):
        key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
        IV = Random.new().read(AES.block_size)  # generate IV
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
        source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
        data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
        return base64.b64encode(data).decode("latin-1") if encode else data

    my_password = input("Password: ")
    data = imp_data_finder(open(file_path, 'r').read())

    imports_source, my_data = data[0], encrypt(my_password.encode(),data[1].encode())


    for imp in imports_source:
        import_datas += "\n"+imp



    encrypted_data = '''
#begin : imports. -> librarys for decrypting and imported librarys for program
%s
#end : imports.

#begin : function decrypt for decrypting files.
%s
#end : function decrypt for decrypting files.


exec(decrypt("%s".encode(),"%s").decode())''' % (
        import_datas,
        decrypt_func,
        my_password,
        my_data
    )


    print(encrypted_data)

    open('encrypted_file_%d.py' % int(time.time()), 'w').write(encrypted_data)
crypter_files(input("file: "))
