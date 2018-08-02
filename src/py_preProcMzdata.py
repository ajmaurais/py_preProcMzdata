
import sys
import os
import argparse
import re

import datProc

MZ_EXT = '.mzdata'

def main(argv):
    parser = argparse.ArgumentParser(prog = 'py_preProcMzdata')

    parser.add_argument('-a', '--align', choices = [0, 1], type = int, default = 1,
                        help = 'Choose whether to run map allignment by pool. Default is 0.')
    parser.add_argument('-e', '--ext', default = MZ_EXT,
                        help = 'Specify extension of mzData files. Default is {}'.format(MZ_EXT))

    parser.add_argument('input_dir', help = 'Directory containing raw .mzdata files.')
    parser.add_argument('output_dir', help = 'Directory to write processed files.')

    args = parser.parse_args()

    #get input files
    inputDir = os.path.realpath(args.input_dir)
    inputFiles = os.listdir(inputDir)
    pattern = '{}$'.format(args.ext)
    inputFiles = ['{}/{}'.format(inputDir, x) for x in inputFiles if re.search(pattern, x)]

    #inputFiles = inputFiles[0:2]
    if args.align:
        sys.stdout.write('\nSplitting polarities and performing alignment by sample pool.\n')
        datProc.processPools(inputFiles, args)
    else:
        sys.stdout.write('\nSplitting polarities without performing alignment.\n')
        datProc.splitAllPolarities(inputFiles, args)


if __name__ == '__main__':
    main(sys.argv)
