''' SpellChecker Module '''
import xlsxwriter
from . spellchecker import SpellChecker, WordFrequency
from . info import (__author__, __maintainer__, __email__, __license__,
                    __version__, __credits__, __url__, __bugtrack_url__)

from . parseDict import parseTextFile
__all__ = ['SpellChecker', 'WordFrequency']
