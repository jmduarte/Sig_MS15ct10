import ROOT as rt
import sys

tfile = rt.TFile.Open(sys.argv[1])
hist = {}
#for cat in ['EleMu','EleMuL','TwoMuDY','TwoMuZH']:
for cat in ['TwoMuZH']:
    for bkg in ['light','heavy','other','total']:
        hist[bkg] = tfile.Get('shapes_fit_b/{}/{}'.format(cat,bkg))
        for i in range(1,hist[bkg].GetNbinsX()+1):
            print('{} {} bin {}: {:1.3f} +/- {:1.3f}'.format(cat, bkg, i, hist[bkg].GetBinContent(i), hist[bkg].GetBinError(i)))
