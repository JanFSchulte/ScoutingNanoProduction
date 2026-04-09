# ScoutingNanoProduction

Installation recipe:

```
cmsrel CMSSW_16_1_0_pre4
cd CMSSW_16_1_0_pre4/src
cmsenv
git cms-checkout-topic JanFSchulte:derivedScouting -u 
scram b -j 8

git clone https://github.com/JanFSchulte/ScoutingNanoProduction.git
mkdir -p RecoBTag/CombinedScouting/data/model
cp ScoutingNanoProduction/model_v2.onnx RecoBTag/CombinedScouting/data/
```

In ScoutingNanoProduction, use `submit_scoutingNano.py` to configure which samples to process and details of the processing and publishing of the ScoutingNano. 
