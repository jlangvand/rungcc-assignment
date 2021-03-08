def bytes_to_str(bytes_in):
    str_out = ""
    for b in bytes_in:
        str_out += hex(b) + " "
    return str_out


def replace_special_chars(src: str) -> str:
    src = src.replace("%3C", "<")
    src = src.replace("%3D", "=")
    src = src.replace("%3E", ">")
    src = src.replace("%21", "!")
    src = src.replace("%22", "\"")
    src = src.replace("%23", "#")
    src = src.replace("%25", "%")
    src = src.replace("%26", "&")
    src = src.replace("%28", "(")
    src = src.replace("%29", ")")
    src = src.replace("%2C", ",")
    src = src.replace("%3A", ":")
    src = src.replace("%3B", ";")
    src = src.replace("%3F", "?")
    src = src.replace("%5C", "\\")
    src = src.replace("%7B", "{")
    src = src.replace("%7D", "}")
    src = src.replace("%7E", "~")
    src = src.replace("+", " ")
    src = src.replace("%0D%0A", "\n")
    return src


def html_safe(src: str) -> str:
    src = src.replace("æ", "&aelig;")
    src = src.replace("ø", "&oring;")
    src = src.replace("å", "&aelig")
    src = src.replace("©", "&copy;")
    return src
