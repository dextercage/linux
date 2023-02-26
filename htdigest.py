import hashlib

password = "Skills53"
realm = "myrealm"
with open("passwords", "w") as file:
    for i in range(1, 51):
        username = f"user{i}"
        hash_obj = hashlib.new("md5")
        hash_obj.update(f"{username}:{realm}:{password}".encode("utf-8"))
        password_digest = hash_obj.hexdigest()
        file.write(f"{username}:{realm}:{password_digest}\n")
        