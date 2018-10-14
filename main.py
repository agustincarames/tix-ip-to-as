import concat
import download_files
import conf

import os
import urllib

try:
        conf.make_dirs()

        download_files.download_asn()
        download_files.download_rv()

        concat.build_files()
finally:
        #conf.rm_temp_dirs()
        pass

