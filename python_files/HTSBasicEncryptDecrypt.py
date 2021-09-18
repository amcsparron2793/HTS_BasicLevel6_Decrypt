"""
HTSBasicEncryptDecrypt.py

Script to encrypt and decrypt a given string based on algorithm used in
https://www.HackThisSite.org/missions/basic/6 challenge.
"""

# imports
from sys import version_info
import dependencies.CustomLog_Classes as Clog
from dependencies.yes_no import yes_no_loop as yn

# ord() changes a character to ASCII, chr() changes from ASCII to character


# noinspection PyAttributeOutsideInit
class EncryptString:
    """ Encrypt a given string based on HTS basic level 6"""
    def __init__(self):
        self.pyver = float(str(version_info.major) + "." + str(version_info.minor))
        self.plain_text = self.GetPlainText()
        self.err = Clog.Error()
        self.err.error_setup()

    def GetPlainText(self):
        while True:
            if self.pyver >= 3:
                plain_text = input("Please enter plain text to be encrypted: ")
            elif self.pyver < 3:
                plain_text = raw_input("Please enter plain text to be encrypted: ")
            else:
                plain_text = input("Please enter plain text to be encrypted: ")

            if plain_text:
                return plain_text
            elif not plain_text:
                if yn("plain text cannot be blank, would you like to try again?"):
                    pass
                else:
                    print("Ok Quitting...")
                    exit()


# noinspection PyAttributeOutsideInit
class DecryptString:
    """ Decrypt a given string based on HTS basic level 6."""
    def __init__(self):
        self.pyver = float(str(version_info.major) + "." + str(version_info.minor))
        self.encrypted_text = self.GetEncryptedText()
        self.err = Clog.Error()
        self.err.error_setup()
        self.string_dict_list = self.MakeStringDictList()
        self.transformed_ascii_values = self.TransformString()
        self.convert_to_chr()

    def GetEncryptedText(self):
        while True:
            if self.pyver >= 3:
                encrypted_text = input("Please enter Encrypted text to be unencrypted: ")
            elif self.pyver < 3:
                encrypted_text = raw_input("Please enter Encrypted text to be unencrypted: ")
            else:
                encrypted_text = input("Please enter Encrypted text to be unencrypted: ")

            if encrypted_text:
                return encrypted_text

            elif not encrypted_text:
                if yn("encrypted text cannot be blank, would you like to try again?"):
                    pass
                else:
                    print("Ok Quitting...")
                    exit()

    def MakeStringDictList(self):
        string_dict_list = []
        for x in range(len(self.encrypted_text)):
            string_dict_list.append({x: ord(self.encrypted_text[x])})
        print(string_dict_list)
        return string_dict_list

    def TransformString(self):
        for x in self.string_dict_list:
            for y in x.keys():
                x[y] = x[y] - y
        return self.string_dict_list

    def convert_to_chr(self):
        chr_list = []
        for x in self.transformed_ascii_values:
            for y in x.keys():
                chr_list.append(chr(x[y]))
        print(''.join(chr_list))


DecryptString()
