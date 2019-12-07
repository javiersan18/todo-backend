from passlib.context import CryptContext

# The password context to be used to hash and verify user passwords.
# pwd_context.hash('somepass')
# pwd_context.verify('somepass', hash)
# For more information, see https://passlib.readthedocs.io/en/stable/narr/quickstart.html
pwd_context = CryptContext(
    schemes=['argon2'],
)