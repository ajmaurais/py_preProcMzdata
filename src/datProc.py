
import pyopenms
import sys
import os

def splitPolarity(raw):

    pos = pyopenms.MSExperiment()
    neg = pyopenms.MSExperiment()

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

def processPools(fileList, args):
    print('hello')

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



