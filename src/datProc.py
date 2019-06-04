
import pyopenms
import sys
import os
import re

def splitPolarity(raw):
    pos = pyopenms.PeakMap()
    neg = pyopenms.PeakMap()

    for scan in raw.getSpectra():
        if scan.getInstrumentSettings().getPolarity() == pyopenms.IonSource.Polarity.POSITIVE:
            pos.addSpectrum(scan)
        elif scan.getInstrumentSettings().getPolarity() == pyopenms.IonSource.Polarity.NEGATIVE:
            neg.addSpectrum(scan)
        elif scan.getInstrumentSettings().getPolarity() == pyopenms.IonSource.Polarity.POLNULL:
            sys.stderr('POLNULL polarity found! Skipping...')

    pos.sortSpectra(True)
    pos.updateRanges()
    neg.sortSpectra(True)
    neg.updateRanges()

    return pos, neg

def groupSamplePools(files):
    ret = dict()
    for file in files:
        match = re.search('^(Pool_[0-9]+|DMSO_[A-Z]?)', os.path.basename(file))
        curGroup = match.group(0)
        if curGroup in ret.keys():
            ret[curGroup].append(file)
        else:
            sys.stdout.write('Found {}\n'.format(curGroup))
            ret[curGroup] = [file]

    return ret

def processPools(fileList, args):
    groups = groupSamplePools(fileList)

    # read raw input files and process
    for key, value in groups.items():
        sys.stdout.write('Working on {}\n'.format(key))

        # load files and split polarity
        posRuns = list()
        negRuns = list()
        raw = pyopenms.MSExperiment()
        for file in value:
            pyopenms.MzDataFile().load(file, raw)
            pos, neg = splitPolarity(raw)
            posRuns.append(pos)
            negRuns.append(neg)

        # run alignment
        alg = pyopenms.MapAlignmentAlgorithmIdentification()
        posTrans = list()
        posTrans = [pyopenms.TransformationDescription() for x in range(1)]
        #negTrans = [pyopenms.TransformationDescription() for x in range(len(negRuns))]

        alg.align(posRuns, posTrans)


def splitAllPolarities(fileList, args):
    for file in fileList:
        sys.stdout.write('Working on {}\n'.format(os.path.basename(file)))
        #read raw file and split polarity
        raw = pyopenms.MSExperiment()
        pyopenms.MzDataFile().load(file, raw)
        pos, neg = splitPolarity(raw)

        #get output file names
        baseName = os.path.basename(os.path.splitext(file)[0])
        posOfname = '{}/{}_pos_processed{}'.format(args.output_dir, baseName, args.ext)
        negOfname = '{}/{}_neg_processed{}'.format(args.output_dir, baseName, args.ext)

        #write files
        pyopenms.MzDataFile().store(posOfname, pos)
        pyopenms.MzDataFile().store(negOfname, neg)

