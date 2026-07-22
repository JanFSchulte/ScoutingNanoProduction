import argparse
import glob
import json
import os
import subprocess
from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

MAX_FILES_PER_TASK = 9000
CACHE_DIR = 'filelist_cache'
LUMI_JSON = '2024.json'

data_samples = {
    #'2024B': '/ScoutingPFRun3/Run2024B-v1/HLTSCOUT',
    #'2024C': '/ScoutingPFRun3/Run2024C-v1/HLTSCOUT',
    #'2024D': '/ScoutingPFRun3/Run2024D-v1/HLTSCOUT',
    #'2024E': '/ScoutingPFRun3/Run2024E-v1/HLTSCOUT',
    #'2024F': '/ScoutingPFRun3/Run2024F-v1/HLTSCOUT',
    #'2024G': '/ScoutingPFRun3/Run2024G-v1/HLTSCOUT',
    #'2024H': '/ScoutingPFRun3/Run2024H-v1/HLTSCOUT',
    '2024I': '/ScoutingPFRun3/Run2024I-v1/HLTSCOUT',
}

mc_samples = {

        'WWW': '/WWW-4F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WWZ': '/WWZ-4F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'ZZZ': '/ZZZ-5F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WZZ': '/WZZ-5F_TuneCP5_13p6TeV_amcatnlo-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

        'ZH': '/ZH-Zto2Q-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'GluGluZH': '/GluGluZH-Zto2Q-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

        'WminsH-Wto2Q-Hto2Wto4Q': '/WminusH-Wto2Q-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WplusH-Wto2Q-Hto2Wto4Q': '/WplusH-Wto2Q-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WminusH-Wto2Q-Hto2Wto2L2Nu': '/WminusH-Wto2Q-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WminusH-Wto2Q-Hto2WtoLNu2Q': '/WminusH-Wto2Q-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WminusH-WtoLNu-Hto2Wto2L2Nu': '/WminusH-WtoLNu-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WminusH-WtoLNu-Hto2Wto4Q': '/WminusH-WtoLNu-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WminusH-WtoLNu-Hto2WtoLNu2Q': '/WminusH-WtoLNu-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WplusH-Wto2Q-Hto2WtoLNu2Q': '/WplusH-Wto2Q-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WplusH-Wto2Q-Hto2Wto2L2Nu': '/WplusH_Wto2Q_Hto2Wto2L2Nu_M-125_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WplusH-WtoLNu-Hto2Wto2L2Nu': '/WplusH-WtoLNu-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WplusH-WtoLNu-Hto2Wto4Q': '/WplusH-WtoLNu-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'WplusH-WtoLNu-Hto2WtoLNu2Q': '/WplusH-WtoLNu-Hto2WtoLNu2Q_M-125_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

        'ZH-Zto2L-Hto2Wto2L2Nu': '/ZH-Zto2L-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'ZH-Zto2L-Hto2Wto4Q': '/ZH-Zto2L-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'ZH-Zto2L-Hto2WtoLNu2Q': '/ZH-Zto2L-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'ZH-Zto2Q-Hto2Wto2L2Nu': '/ZH-Zto2Q-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'ZH-Zto2Q-Hto2WtoLNu2Q': '/ZH-Zto2Q-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM', 
        'GluGluZH-Zto2L-Hto2Wto2L2Nu': '/GluGluZH-Zto2L-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'GluGluZH-Zto2L-Hto2Wto4Q': '/GluGluZH-Zto2L-Hto2Wto4Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'GluGluZH-Zto2L-Hto2WtoLNu2Q': '/GluGluZH-Zto2L-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'GluGluZH-Zto2Q-Hto2Wto2L2Nu': '/GluGluZH-Zto2Q-Hto2Wto2L2Nu_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'GluGluZH-Zto2Q-Hto2WtoLNu2Q': '/GluGluZH-Zto2Q-Hto2WtoLNu2Q_Par-M-125_TuneCP5_13p6TeV_powhegMINLO-jhugen-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',


        'QCD_HT-1000to1200': '/QCD-4Jets_Bin-HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-100to200': '/QCD-4Jets_Bin-HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-1200to1500': '/QCD-4Jets_Bin-HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-1500to2000': '/QCD-4Jets_Bin-HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-2000': '/QCD-4Jets_Bin-HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-200to400': '/QCD-4Jets_Bin-HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-400to600': '/QCD-4Jets_Bin-HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-40to70': '/QCD-4Jets_Bin-HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-600to800': '/QCD-4Jets_Bin-HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-70to100': '/QCD-4Jets_Bin-HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'QCD_HT-800to1000': '/QCD-4Jets_Bin-HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

        'TbarWplus' : '/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'TWminus' : '/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'TTTo4Q' : '/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'TTToLNu2Q': '/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
        'TTTo2L2Nu': '/TTto2L2Nu_Par-ERD-On_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

#        'WW' : '/WW_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'WZ' : '/WZ_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#        'ZZ' : '/ZZ_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

        
        
    'Wto2Q_HT-100to400': '/Wto2Q-3Jets_Bin-HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Wto2Q_HT-1500to2500': '/Wto2Q-3Jets_Bin-HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v3/MINIAODSIM',
    'Wto2Q_HT-2500': '/Wto2Q-3Jets_Bin-HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Wto2Q_HT-400to800': '/Wto2Q-3Jets_Bin-HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Wto2Q_HT-800to1500': '/Wto2Q-3Jets_Bin-HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Zto2Q_HT-100to400': '/Zto2Q-4Jets_Bin-HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Zto2Q_HT-1500to2500':'/Zto2Q-4Jets_Bin-HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Zto2Q_HT-2500':'/Zto2Q-4Jets_Bin-HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v3/MINIAODSIM',
    'Zto2Q_HT-400to800':'/Zto2Q-4Jets_Bin-HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
    'Zto2Q_HT-800to1500':'/Zto2Q-4Jets_Bin-HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

#    'WtoLNu-4Jets_Bin-HT-100to400-MLNu-0to120' : '/WtoLNu-4Jets_Bin-HT-100to400-MLNu-0to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-100to400-MLNu-120_' : '/WtoLNu-4Jets_Bin-HT-100to400-MLNu-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-1500to2500-MLNu-0to120' : '/WtoLNu-4Jets_Bin-HT-1500to2500-MLNu-0to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-1500to2500-MLNu-120' : '/WtoLNu-4Jets_Bin-HT-1500to2500-MLNu-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-2500-MLNu-0to120' : '/WtoLNu-4Jets_Bin-HT-2500-MLNu-0to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-2500-MLNu-120' : '/WtoLNu-4Jets_Bin-HT-2500-MLNu-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-400to800' : '/WtoLNu-4Jets_Bin-HT-400to800-MLNu-0to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-400to800-MLNu-120' : '/WtoLNu-4Jets_Bin-HT-400to800-MLNu-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-40to100-MLNu-0to120' : '/WtoLNu-4Jets_Bin-HT-40to100-MLNu-0to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-800to1500-MLNu-0to120' : '/WtoLNu-4Jets_Bin-HT-800to1500-MLNu-0to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WtoLNu-4Jets_Bin-HT-800to1500-MLNu-120' : '/WtoLNu-4Jets_Bin-HT-800to1500-MLNu-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-1500to2500-MLL-120' : '/DYto2L-4Jets_Bin-HT-1500to2500-MLL-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-1500to2500-MLL-4to50' : '/DYto2L-4Jets_Bin-HT-1500to2500-MLL-4to50_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-1500to2500-MLL-50to120' : '/DYto2L-4Jets_Bin-HT-1500to2500-MLL-50to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-2500-MLL-120' : '/DYto2L-4Jets_Bin-HT-2500-MLL-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-2500-MLL-4to50' : '/DYto2L-4Jets_Bin-HT-2500-MLL-4to50_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-2500-MLL-50to120' : '/DYto2L-4Jets_Bin-HT-2500-MLL-50to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-400to800-MLL-120' : '/DYto2L-4Jets_Bin-HT-400to800-MLL-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-800to1500-MLL-120' : '/DYto2L-4Jets_Bin-HT-800to1500-MLL-120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-800to1500-MLL-4to50' : '/DYto2L-4Jets_Bin-HT-800to1500-MLL-4to50_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v4/MINIAODSIM',
#    'DYto2L-4Jets_Bin-HT-800to1500-MLL-50to120' : '/DYto2L-4Jets_Bin-HT-800to1500-MLL-50to120_TuneCP5_13p6TeV_madgraphMLM-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v5/MINIAODSIM',
#    'TWminustoLNu2Q' : '/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'TbarWplustoLNu2Q' : '/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',


#    'ZZto4Q' : '/ZZto4Q-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    '/ZZto4L-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'ZZto2Nu2Q' : '/ZZto2Nu2Q-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'ZZto2L2Q' : '/ZZto2L2Q-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WZto2L2Q' : '/WZto2L2Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'Zto2Nu2Q' : '/WZto2Nu2Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WZto4Q' : '/WZto4Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WZtoLNu2Q' : '/WZtoLNu2Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WWto4Q' : '/WWto4Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',
#    'WWtoLNu2Q' : '/WWtoLNu2Q-1Jets-4FS_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM',

}


parser = argparse.ArgumentParser(description='Submit or resubmit ScoutingNano CRAB tasks')
parser.add_argument('-s', '--submit',   action='store_true', help='Submit new CRAB tasks')
parser.add_argument('-r', '--resubmit', action='store_true', help='Resubmit failed jobs in existing CRAB projects')
parser.add_argument('--report',        action='store_true', help='Report number of events processed (before event filters) for existing MC CRAB tasks')
parser.add_argument('--mc',            action='store_true', help='Run over MC samples instead of data')
args = parser.parse_args()


def das_query(query):
    cmd = ['dasgoclient', '-query', query]
    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    return [line for line in out.splitlines() if line.strip()]


def get_dataset_runs(dataset):
    lines = das_query(f'run dataset={dataset}')
    return set(int(r) for r in lines)


def get_files_for_run(dataset, run):
    return das_query(f'file dataset={dataset} run={run}')


def get_file_lumis(filename, run):
    lines = das_query(f'lumi file={filename} run={run}')
    lumis = set()
    for line in lines:
        try:
            lumis.add(int(line.strip()))
        except ValueError:
            pass
    return lumis


def file_has_golden_lumi(run, file_lumis, lumi_json):
    for ls in file_lumis:
        for start, end in lumi_json.get(str(run), []):
            if start <= ls <= end:
                return True
    return False


def get_cached_files(sample, dataset, lumi_json):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f'{sample}.json')

    if os.path.exists(cache_path):
        print(f'  [{sample}] Loading file list from cache: {cache_path}')
        with open(cache_path) as f:
            return json.load(f)

    json_runs = set(int(r) for r in lumi_json.keys())

    print(f'  [{sample}] Querying runs in dataset...')
    dataset_runs = get_dataset_runs(dataset)
    valid_runs = sorted(dataset_runs & json_runs)
    print(f'  [{sample}] {len(dataset_runs)} runs in dataset, '
          f'{len(valid_runs)} overlap with lumi JSON')

    files = set()
    for i, run in enumerate(valid_runs):
        run_files = get_files_for_run(dataset, run)
        for fname in run_files:
            file_lumis = get_file_lumis(fname, run)
            if file_has_golden_lumi(run, file_lumis, lumi_json):
                files.add(fname)
        if (i + 1) % 10 == 0 or (i + 1) == len(valid_runs):
            print(f'    {i+1}/{len(valid_runs)} runs processed, {len(files)} files so far')

    files = sorted(files)
    with open(cache_path, 'w') as f:
        json.dump(files, f, indent=2)
    print(f'  [{sample}] Cached {len(files)} files to {cache_path}')
    return files


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if not args.mc and not args.resubmit and not args.report:
    with open(LUMI_JSON) as f:
        lumi_json = json.load(f)

if not args.resubmit and not args.report:
  samples = mc_samples if args.mc else data_samples
  mode_label = 'MC' if args.mc else 'Data'

  for sample, dataset in samples.items():
    print(f'\nProcessing {sample}: {dataset}')

    if args.mc:
        task_chunks = [None]  # single task per MC sample; CRAB handles splitting
    else:
        files = get_cached_files(sample, dataset, lumi_json)
        task_chunks = list(chunks(files, MAX_FILES_PER_TASK))
        print(f'  {len(files)} files -> {len(task_chunks)} task(s)')

    for i, file_chunk in enumerate(task_chunks):
        suffix = f'_part{i+1}' if len(task_chunks) > 1 else ''
        task_name = f'scoutingNanoUParT_{sample}{suffix}'
        print(f'  Configuring task: {task_name}')

        cfg = config()
        cfg.General.requestName = task_name
        cfg.General.workArea = 'crab_projects'
        cfg.General.transferLogs = True

        cfg.JobType.pluginName = 'Analysis'
        cfg.JobType.psetName = 'scoutingnano_mc_standalone2.py' if args.mc else 'scoutingnano_data_standalone2.py'
        cfg.JobType.allowUndistributedCMSSW = True
        cfg.JobType.maxMemoryMB = 2500
        cfg.JobType.numCores = 1
        cfg.JobType.maxJobRuntimeMin = 2750

        cfg.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

        cfg.Data.inputDataset = dataset
        cfg.Data.outputDatasetTag = f'ScoutingNano_{mode_label}_{sample}{suffix}_v5_jetMatchFix'
        cfg.Data.outLFNDirBase = '/store/user/jschulte/ScoutingNano/'
        cfg.Data.splitting = 'FileBased'
        cfg.Data.unitsPerJob = 8 if args.mc else  1
        cfg.Data.ignoreLocality = True
        cfg.Data.publication = True

        if not args.mc:
            cfg.Data.userInputFiles = file_chunk

        cfg.Site.storageSite = 'T2_US_Purdue'
        cfg.Site.whitelist = ['T2_*']
        cfg.Site.blacklist = ['T2_BR_UERJ', 'T2_US_Florida', 'T2_US_Wisconsin', 'T2_US_Caltech', 'T2_US_Nebraska']

        if args.submit:
            try:
                crabCommand('submit', config=cfg)
            except:
                print ("can't submit, task with this name is already present")

if args.resubmit:
    project_dirs = sorted(glob.glob(os.path.join('crab_projects', 'crab_scoutingNanoUParT_*')))
    if not project_dirs:
        print('No existing CRAB projects found to resubmit.')
    for d in project_dirs:
        print(f'Resubmitting {d} ...')
        try:
            crabCommand('resubmit', dir=d, siteblacklist='T2_BR_UERJ,T2_US_Florida,T2_US_Wisconsin,T2_US_Caltech,T2_US_Nebraska')
        except:
            print ("failed to resubmit, most likely there are no failed jobs")

if args.report:
    print('\nReporting events processed (before event filters) for MC CRAB tasks:')
    total_events = 0
    for sample in mc_samples:
        task_name = f'scoutingNanoUParT_{sample}'
        d = os.path.join('crab_projects', f'crab_{task_name}')
        if not os.path.isdir(d):
            print(f'  [{sample}] No CRAB project directory found ({d}), skipping.')
            continue
        try:
            res = crabCommand('report', dir=d)
            n = res.get('numEventsRead', 'n/a')
            print(f'  [{sample}] Events read (pre-filter): {n}')
            if isinstance(n, str) and n.isdigit():
                total_events += int(n)
        except Exception as e:
            print(f'  [{sample}] Failed to get report: {e}')
    print(f'\nTotal events read across all MC tasks: {total_events}')

print('\nDone :)')
