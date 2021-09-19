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


class PrepFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.err = Clog.Error()
        self.err.error_setup()

        self.content_string = self.GetContentAsString(self.filepath)
        global content
        content = self.content_string

    def GetContentAsString(self, filepath):
        try:
            with open(filepath) as f:
                content_string = f.read()
                return content_string

        except FileNotFoundError as e:
            self.err.error_handle(e)

        except IOError as e:
            self.err.error_handle(e)


class ChooseCrypt:
    """Prompts user for decryption or encryption of string, using questionary."""

    def __init__(self):
        self.err = Clog.Error()
        self.err.error_setup()

        self.boolFileString = self.AskFileOrString()

        self.AskCryptType()

    def AskFilePath(self):
        try:
            q = questionary.path(message="Please enter the full filepath").ask()
            print(q)
        except questionary.ValidationError as e:
            self.err.error_handle(e)
        except NoConsoleScreenBufferError as e:
            self.err.error_handle(e)

    def AskFileOrString(self):
        try:
            q = questionary.select(message="Is the input type a file or a string?",
                                   choices=["string", "file"]).ask()
        except questionary.ValidationError as e:
            self.err.error_handle(e)
        except NoConsoleScreenBufferError as e:
            self.err.error_handle(e)

        if q == "string":
            return False
        elif q == "file":
            # FIXME: global var content comes back as None
            PrepFile(self.AskFilePath())
            return True

    def AskCryptType(self):
        """Asks user if they want to encrypt or decrypt."""
        try:
            q = questionary.select(message="Would you like to Encrypt, or Decrypt",
                                   choices=["Decrypt", "Encrypt"]).ask()
        except questionary.ValidationError as e:
            self.err.error_handle(e)
        except NoConsoleScreenBufferError as e:
            self.err.error_handle(e)
        try:
            if q == "Decrypt":
                DecryptString(self.boolFileString)
            elif q == "Encrypt":
                EncryptString(self.boolFileString)
        except UnboundLocalError as e:
            self.err.error_handle(e)


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

    def __init__(self, file=False):
        super().__init__()
        self.file = file
        if not self.file:
            self.text_to_crypt = self.GetTextToCrypt("Decrypt")
        else:
            self.text_to_crypt = content

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

    def __init__(self, file=False):
        super().__init__()
        self.file = file
        if not self.file:
            self.text_to_crypt = self.GetTextToCrypt("Encrypt")
        else:
            self.text_to_crypt = content

        self.string_dict_list = self.MakeStringDictList()

        self.transformed_ascii_values = self.TransformString()
        self.convert_to_chr()

    def TransformString(self):
        for x in self.string_dict_list:
            for y in x.keys():
                x[y] = x[y] + y
        return self.string_dict_list
