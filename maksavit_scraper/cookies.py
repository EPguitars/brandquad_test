""" 
Class Cooker is responsible for grabbing cookies from the browser and converting them to a dictionary.
"""
cookie_string = "_ssruuid=a37fd1fb-e5b4-4e92-9eec-00a17988e7a7; _gid=GA1.2.958621806.1711361926; rrpvid=75439826432672; _userGUID=0:lu6spe0t:oArpeIAXcObNguU5nJFtTyvvAavSNzOV; digi_uc=W10=; tmr_lvid=874acf9659eb792cfc1653ecba41dfd2; tmr_lvidTS=1711361927357; _ym_uid=1711361927219000719; _ym_d=1711361927; rcuid=66014f87a120b324a346567e; supportOnlineTalkID=XAhzZQgOGVsmy6K4vafBb447MOaXnfxX; _ct=2200000000195482347; _ct_client_global_id=d2ca5ebd-b7ee-5766-9c41-0486f8dd7a2b; stDeIdU=102aa403-ea4e-4ff7-b945-a6111806f76e; analytic_id=1711361945018802; location_selected=Y; location_code=0000949228; _ym_isad=2; qrator_jsr=1711577757.970.yrA9rejN57sb9tYQ-i7q43j2u9hchetvm9qolia6dp7ga9mij-00; qrator_jsid=1711577757.970.yrA9rejN57sb9tYQ-hd99thqg2cc2djk0vp54gv2n12rnirsu; dSesn=a6290c75-d656-2a9a-7a9e-0ad705781e5a; _dvs=0:luad7iqe:tC5jcZy6YacqVZADu_DWXvCe_26_bu6N; _ym_visorc=b; cted=modId%3Dzsrw7tvm%3Bclient_id%3D1965996350.1711361925%3Bya_client_id%3D1711361927219000719; _ct_ids=zsrw7tvm%3A53436%3A304587574; _ct_session_id=304587574; _ct_site_id=53436; rrwpswu=true; PHPSESSID=jqevi55s9nrk4lu9kuaae5cppj; mainBannerIndex=0; _ga=GA1.2.1965996350.1711361925; _ga_NT5WFXGWZY=GS1.1.1711576435.16.1.1711577905.0.0.0; call_s=%3C!%3E%7B%22zsrw7tvm%22%3A%5B1711579706%2C304587574%2C%7B%22265058%22%3A%22794826%22%7D%5D%2C%22d%22%3A2%7D%3C!%3E; tmr_detect=0%7C1711577907169"

class Cooker:
    """
    Этот класс нужен для подготовки куки для использования со Scrapy
    Его нужно дополнить функционалом для автоматической генерации куки
    Пока он работает только с заранее заготовленной строкой с куки
    """
    def __init__(self, cookies_string: str):
        self.cookie_string = cookies_string
        self.cookie_dict = self.__to_dict(self.cookie_string)

    
    def __to_dict(self, cookie_string: str):
        cookie_dict = {}
        parts = cookie_string.split('; ')
        
        for part in parts:
            key_value = part.split('=', 1)
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else None
            cookie_dict[key] = value
        
        return cookie_dict
    
