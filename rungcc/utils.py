# Copyright (C) 2021  Joakim Skogø Langvand

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    src = src.replace("&", "&amp;")
    src = src.replace("æ", "&aelig;")
    src = src.replace("ø", "&oring;")
    src = src.replace("å", "&aelig")
    src = src.replace("©", "&copy;")
    src = src.replace("<", "&lt;")
    src = src.replace(">", "&gt;")
    return src
