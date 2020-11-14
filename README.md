# Sig_MS15ct10

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

