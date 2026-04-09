import os
from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

samples = {
        'WWW': '/WWW-4F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'WWZ': '/WWZ-4F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'ZZZ': '/ZZZ-5F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'WZZ': '/WZZ-5F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

#        'WminsH': '/WminusH-WtoLNu-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'WplusH': '/WplusH-WtoLNu-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'ZH': '/ZH-Zto2Q-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'GluGluZH': '/GluGluZH-Zto2Q-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

#        'QCD_HT-1000to1200': '/QCD-4Jets_Bin-HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-100to200': '/QCD-4Jets_Bin-HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-1200to1500': '/QCD-4Jets_Bin-HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-1500to2000': '/QCD-4Jets_Bin-HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-1500to2000': '/QCD-4Jets_Bin-HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-NoPU_150X_mcRun3_2024_realistic_v2_ext1-v2/MINIAODSIM',
#        'QCD_HT-2000': '/QCD-4Jets_Bin-HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-2000': '/QCD-4Jets_Bin-HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-NoPU_150X_mcRun3_2024_realistic_v2_ext1-v2/MINIAODSIM',
#        'QCD_HT-200to400': '/QCD-4Jets_Bin-HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-400to600': '/QCD-4Jets_Bin-HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-40to70': '/QCD-4Jets_Bin-HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-600to800': '/QCD-4Jets_Bin-HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-70to100': '/QCD-4Jets_Bin-HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'QCD_HT-800to1000': '/QCD-4Jets_Bin-HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

#        'TbarWplus' : '/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'TWminus' : '/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'TTTo4Q' : '/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'TTToLNu2Q': '/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

#        'WW' : '/WW_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'WZ' : '/WZ_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'ZZ' : '/ZZ_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

        }


for sample in samples:


    config_tmp = config()

    config_tmp.General.requestName = 'scoutingNanoUParT_%s'%sample
    config_tmp.General.workArea = 'crab_projects'
    config_tmp.General.transferLogs = True

    config_tmp.JobType.pluginName = 'Analysis'
    config_tmp.JobType.psetName = 'scoutingnano_mc_standalone2.py'
    config_tmp.JobType.allowUndistributedCMSSW = True
    config_tmp.JobType.maxMemoryMB = 2500
    config_tmp.JobType.numCores    = 1

    config_tmp.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

    config_tmp.Data.inputDataset = samples[sample]
    config_tmp.Data.outLFNDirBase = "/store/user/jschulte/ScoutingNano/"
    config_tmp.Data.outputDatasetTag = "ScoutingNanoUPart_v3"
    config_tmp.Data.inputDBS = "global"
    config_tmp.Data.publishDBS = "phys03"
    config_tmp.Data.splitting = "FileBased"
    config_tmp.Data.ignoreLocality = False
    config_tmp.Data.unitsPerJob = 10
    config_tmp.Data.publication = True
    config_tmp.JobType.maxJobRuntimeMin = 2750

    config_tmp.Site.storageSite = "T2_US_Purdue"
    config_tmp.Site.whitelist = ["T2_*","T3_*"]
    config_tmp.Site.blacklist = ["T2_BR_UERJ", "T2_US_Florida", "T2_US_Wisconsin"]


    crabCommand('submit', config = config_tmp)

print("Done :)")
