from xhalpy import *

import logging, os

gMAX_RETRIES = 5
gRetries = 5

#from gempython.utils.wrappers import envCheck
#envCheck("GEM_ADDRESS_TABLE_PATH")

# Set TTC Generator Params
ttcGenParams = ParamTtcGen()
ttcGenParams.enable = True
ttcGenParams.L1Ainterval = 250
ttcGenParams.mode = 0
ttcGenParams.nPulses = 0
ttcGenParams.pulseDelay = 40
ttcGenParams.pulseRate = ttcGenParams.calcRate()
ttcGenParams.type = 0

def getCalObject(cardName,debug=False):
    calibrator = CalRoutines(cardName)

    return calibrator

def configureTTCGenerator(calibrator, ohN, params=ttcGenParams):
    """
    Configures the TTC Generator (T1 Controller) on v3 (2b) electronics

    calibrator - instance of xhalpy.CalRoutines
    ohN - optohybrid number
    params - instance of xhalpy.ParamTtcGen

    Default values reflects v3 electronics behavior

    =======v3 electronics Behavior=======
         params.pulseDelay (only for enable = true), delay between CalPulse and L1A
         params.L1Ainterval (only for enable = true), how often to repeat signals
         params.enable = true (false) ignore (take) ttc commands from backplane for this AMC (affects all links)
    =======v2b electronics behavior=======
         Configure the T1 controller
         params.mode: 0 (Single T1 signal),
                      1 (CalPulse followed by L1A),
                      2 (pattern)
         params.type (only for mode 0, type of T1 signal to send):
               0 L1A
               1 CalPulse
               2 Resync
               3 BC0
         params.pulseDelay (only for mode 1), delay between CalPulse and L1A
         params.L1Ainterval (only for mode 0,1), how often to repeat signals
         params.nPulses how many signals to send (0 is continuous)
         params.enable = true (false) start (stop) the T1Controller for link ohN
    """

    calibrator.ttcGenConf(ohN,ttcGenParams)
    return

def toggleTTCGen(calibrator, ohN, enable=True):
    """
    v3  electronics: enable = true (false) ignore (take) ttc commands from backplane for this AMC
    v2b electronics: enable = true (false) start (stop) the T1Controller for link ohN
    """

    calibrator.ttcGenToggle(ohN, enable)
    return
