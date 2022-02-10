import base64

from cryptography.fernet import Fernet

from shared_directory.state_manager.constant import APP_STATUS

__m_fernet = Fernet(base64.urlsafe_b64encode(str.encode(APP_STATUS.S_FERNET_KEY)))
ss = __m_fernet.encrypt("hello how are you".encode())
print(__m_fernet.decrypt(ss))
#if __m_fernet.decrypt(ss).startswith(APP_STATUS.S_APP_BLOCK_KEY) is False:
#    print("false")
#print("true")
