# Sig_MS15ct10

Set up combine
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone -b v8.1.0 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit 
scramv1 b clean
scramv1 b -j 8
```
Reparametrize
```
python rewriteWorkspace.py
text2workspace.py card_systematics_new.txt --channel-masks
text2workspace.py card_systematics.txt --channel-masks
```

Run masked fit before and after reparametrization
```
combine -M FitDiagnostics card_systematics.root --saveNormalizations --plot --saveShapes --saveWithUncertainties --saveWorkspace --setParameters mask_TwoMuZH=1 -n MaskedData --robustHesse 1
combine -M FitDiagnostics card_systematics_new.root --saveNormalizations --plot --saveShapes --saveWithUncertainties --saveWorkspace --setParameters mask_TwoMuZH=1 -n MaskedData_new
```

Check yields
```
python printYields.py fitDiagnosticsMaskedData.root 
python printYields.py fitDiagnosticsMaskedData_new.root 
```

