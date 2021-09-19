"""
HTSBasicEncryptDecrypt.py

Script to encrypt and decrypt a given string based on algorithm used in
https://www.HackThisSite.org/missions/basic/6 challenge.

# ord() changes a character to ASCII, chr() changes from ASCII to character
"""

# imports
from sys import version_info

import dependencies.CustomLog_Classes as Clog
from dependencies.yes_no import yes_no_loop as yn

import questionary
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError


class ChooseCrypt:
    def __init__(self):
        self.err = Clog.Error()
        self.err.error_setup()

        self.AskType()

    def AskType(self):
        try:
            q = questionary.select(message="Would you like to Encrypt, or Decrypt",
                                   choices=["Decrypt", "Encrypt"]).ask()
        except questionary.ValidationError as e:
            self.err.error_handle(e)
        except NoConsoleScreenBufferError as e:
            self.err.error_handle(e)

        if q == "Decrypt":
            DecryptString()
        elif q == "Encrypt":
            EncryptString()


class _CryptParent:
    """ All of these methods are common to both encryption and decryption."""

    def __init__(self):
        self.transformed_ascii_values = None
        self.text_to_crypt = None
        self.pyver = float(str(version_info.major) + "." + str(version_info.minor))

        self.err = Clog.Error()
        self.err.error_setup()

    # noinspection PyUnboundLocalVariable
    def GetTextToCrypt(self, crypt_type):
        if crypt_type.lower() == "encrypt":
            t1 = "plain"
            t2 = "encrypted"
        elif crypt_type.lower() == "decrypt":
            t1 = "encrypted"
            t2 = "decrypted"
        else:
            try:
                raise AttributeError("crypt_type can only be \'encrypt\' or \'decrypt\'")
            except AttributeError as e:
                self.err.error_handle(e)

        while True:
            if self.pyver >= 3:
                input_text = input("Please enter {} text to be {}: ".format(t1, t2))
            elif self.pyver < 3:
                input_text = raw_input("Please enter {} text to be {}: ".format(t1, t2))
            else:
                input_text = input("Please enter {} text to be {}: ".format(t1, t2))

            if input_text:
                return input_text

            elif not input_text:
                if yn("input text cannot be blank, would you like to try again?"):
                    pass
                else:
                    print("Ok Quitting...")
                    exit()

    def MakeStringDictList(self):
        string_dict_list = []
        for x in range(len(self.text_to_crypt)):
            string_dict_list.append({x: ord(self.text_to_crypt[x])})
        # print(string_dict_list)
        return string_dict_list

    def convert_to_chr(self):
        chr_list = []
        for x in self.transformed_ascii_values:
            for y in x.keys():
                chr_list.append(chr(x[y]))
        print(''.join(chr_list))


# noinspection PyAttributeOutsideInit
class DecryptString(_CryptParent):
    """ Decrypt a given string based on HTS basic level 6."""

    def __init__(self):
        super().__init__()
        self.text_to_crypt = self.GetTextToCrypt("Decrypt")

        self.string_dict_list = self.MakeStringDictList()

        self.transformed_ascii_values = self.TransformString()
        self.convert_to_chr()

    def TransformString(self):
        for x in self.string_dict_list:
            for y in x.keys():
                x[y] = x[y] - y
        return self.string_dict_list


# noinspection PyAttributeOutsideInit
class EncryptString(_CryptParent):
    """ Encrypt a given string based on HTS basic level 6"""

    def __init__(self):
        super().__init__()
        self.text_to_crypt = self.GetTextToCrypt("Encrypt")

        self.string_dict_list = self.MakeStringDictList()

        self.transformed_ascii_values = self.TransformString()
        self.convert_to_chr()

    def TransformString(self):
        for x in self.string_dict_list:
            for y in x.keys():
                x[y] = x[y] + y
        return self.string_dict_list
