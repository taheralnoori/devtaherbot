# fileName : plugins/fileSize.py
# copyright ©️ 2021 nabilanavab

#--------------->
#--------> SIZE FORMATER (TO HUMAN READABLE FORM)
#------------------->
async def get_size_format(
    b, factor=2**10, suffix="B"
):
    for unit in ["", "K", "M", "G", "T"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
"""
مقياس البايت إلى تنسيق البايت المناسب
e.g:
    1253656 => '1.20MB'
    1253656678 => '1.17GB'
"""


#                                                                                  Telegram: @nabilanavab
