import base64

from cryptography.fernet import Fernet

from shared_directory.state_manager.constant import APP_STATUS

# gAAAAABiBO-DDvFZzBRGjSWY_1aA8P_4w4rsI0SDKyKkSHdXtPrBYZB_NbO0UTz4ir57lNynuo-_6IrN4uySzAAluciYiPBDeXCh3TSRP0rQIwy1oCWgxJixeiYGCAajlZf3wZw1eq0Q

__m_fernet = Fernet(base64.urlsafe_b64encode(str.encode(APP_STATUS.S_FERNET_KEY)))
ss = __m_fernet.encrypt("D~S=05y68#M25oj]vprm}9HE))Tr'VX?[p|m-Wg`mrg^----1644498774".encode())

print(ss.decode("utf-8"))

#if __m_fernet.decrypt(ss).startswith(APP_STATUS.S_APP_BLOCK_KEY) is False:
#    print("false")
#print("true")




#gAAAAABiBO-DDvFZzBRGjSWY_1aA8P_4w4rsI0SDKyKkSHdXtPrBYZB_NbO0UTz4ir57lNynuo-_6IrN4uySzAAluciYiPBDeXCh3TSRP0rQIwy1oCWgxJixeiYGCAajlZf3wZw1eq0Q
#gAAAAABiBPAORMZvGrsYGdETBLW15twPOGC36Srr2Bgvw2-uA_iEpB9HvmHj_AznhSuQ6XPGduiTac18qiEGVTjQLPO1P505emhibN2-inq8YADaPQBet1XeyISbcDNubjOYtZRmI57G



#D~S=05y68#M25oj]vprm}9HE))Tr'VX?[p|m-Wg`mrg^