#!/usr/bin/env python3
import atheris
import sys
import io

from minidump.exceptions import *

with atheris.instrument_imports():
    import minidump
    from minidump.minidumpfile import MinidumpFile


@atheris.instrument_func
def TestOneInput(data):

    fdp = atheris.FuzzedDataProvider(data)
    clean_data = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes()).encode('utf-8', 'ignore')

    try:
        with io.BytesIO(clean_data) as f_handle:
            mini_file = MinidumpFile()
            mini_file.filename = 'fuzz.fake'
            mini_file.file_handle = f_handle
            mini_file._parse()
    except (MinidumpException, MinidumpHeaderSignatureMismatchException):
        pass
    except UnicodeDecodeError:
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()


