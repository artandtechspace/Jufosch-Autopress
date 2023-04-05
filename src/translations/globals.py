from typing import Callable

'''
Yes this file must exists because python cant properly
cross-reference variables inside files when directly importing
a function/variable from a file
'''

# Reference for internationalisation-function
i18n: Callable[[str], str] = None
