import ROOT as rt
import math

rt.gSystem.Load('libHiggsAnalysisCombinedLimit')

tfile = rt.TFile.Open('param_ws.root')

w = tfile.Get('wspace')
w.import_ = getattr(w, 'import')
w.Print('v')
w_new = rt.RooWorkspace('wspace_new')
w_new.import_ = getattr(w_new, 'import')

fromcat = {}
fromcat['heavy','twomudy'] = 'elemu'
fromcat['heavy','twomuzh'] = 'elemu'
fromcat['light','twomuzh'] = 'twomudy'

hist = rt.TH1D('hist','hist',3,-0.5,2.5)
for bkg, cat in fromcat.keys():
    for i in range(1,4):
        val = w.var('{bkg}_{fromcat}_bin{i}'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i)).getVal()
        err = 1.+1./math.sqrt(val)
        w_new.import_(w.function('{bkg}_{cat}_bin{i}'.format(bkg=bkg,cat=cat,i=i)),rt.RooFit.RecycleConflictNodes())
        if not w_new.var('{bkg}_{fromcat}_bin{i}_x'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i)):
            print("VAR {bkg}_{fromcat}_bin{i}_x DOESN'T EXIST".format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i))
            w_new.factory('{bkg}_{fromcat}_bin{i}_In[{val}]'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i,val=val))
            w_new.factory('{bkg}_{fromcat}_bin{i}_Err[{err}]'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i,err=err))
            w_new.factory('{bkg}_{fromcat}_bin{i}_x[0]'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i))
            w_new.var('{bkg}_{fromcat}_bin{i}_x'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i)).setConstant(False)
            w_new.factory('expr::{bkg}_{fromcat}_bin{i}_new("@0*TMath::Power(@1,@2)",{bkg}_{fromcat}_bin{i}_In,{bkg}_{fromcat}_bin{i}_Err,{bkg}_{fromcat}_bin{i}_x)'.format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i))
        else:
            print("VAR {bkg}_{fromcat}_bin{i}_x EXISTS".format(bkg=bkg,fromcat=fromcat[bkg,cat],i=i))
        w_new.factory('expr::{bkg}_{cat}_bin{i}_new("@0*@1",tf_{bkg}_{fromcat}_to_{cat}_bin{i},{bkg}_{fromcat}_bin{i}_new)'.format(bkg=bkg,cat=cat,i=i,fromcat=fromcat[bkg,cat]))

bin_list = []
arg_list = []
pdf_list = []
for bkg, cat in [('heavy', 'elemu'), ('heavy','twomudy'), ('heavy','twomuzh'), ('light','twomudy'), ('light','twomuzh')]:
    w_new.import_(w.pdf('{bkg}_{cat}'.format(bkg=bkg,cat=cat)),rt.RooFit.RecycleConflictNodes())
    w_new.factory('sum::{bkg}_{cat}_new_norm({bkg}_{cat}_bin1_new,{bkg}_{cat}_bin2_new,{bkg}_{cat}_bin3_new)'.format(bkg=bkg,cat=cat))
    bins = rt.RooArgList()
    for i in range(1,4):
        bini = w_new.function('{bkg}_{cat}_bin{i}_new'.format(bkg=bkg,cat=cat,i=i))
        bins.add(bini)
        bin_list.append(bini)
    arg_list.append(bins)

    pdf = rt.RooParametricHist('{bkg}_{cat}_new'.format(bkg=bkg,cat=cat),
                               '{bkg}_{cat}_new'.format(bkg=bkg,cat=cat), 
                               w_new.var('ntags'), 
                               bins, 
                               hist)
    pdf_list.append(pdf)
    w_new.import_(pdf,rt.RooFit.RecycleConflictNodes())

w_new.import_(w.data('data_obs_elemu'))
w_new.import_(w.data('light_elemu'))
w_new.import_(w.data('other_elemu'))
w_new.import_(w.data('data_obs_twomudy'))
w_new.import_(w.data('other_twomudy'))
w_new.import_(w.data('signal_twomudy'))
w_new.import_(w.data('data_obs_twomuzh'))
w_new.import_(w.data('other_twomuzh'))
w_new.import_(w.pdf('signal_twomuzh'))


w_new.Print('v')
w_new.writeToFile('param_ws_new.root')
