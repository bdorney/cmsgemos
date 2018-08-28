#from gempython.utils.gemlogger import colors

#from reg_utils.reg_interface.common.reg_base_ops import rpc_connect, rReg, writeReg
#from reg_utils.reg_interface.common.reg_xml_parser import getNode, parseInt, parseXML

#from xhal.reg_interface_gem.core.reg_extra_ops import rBlock
from xhalpy import *

import logging, os

gMAX_RETRIES = 5
gRetries = 5

from gempython.utils.wrappers import envCheck
envCheck("GEM_ADDRESS_TABLE_PATH")

def getAMCObject(cardName,addrTable=None,debug=False):
    if addrTable is None:
        addrTable = "{0}/amc_address_table_top.xml".format(os.getenv("GEM_ADDRESS_TABLE_PATH"))

    amcboard = AMC(cardName,addrTable)

    if debug:
        print("FW release major = {0}".format(amcboard.readReg("GEM_AMC.GEM_SYSTEM.RELEASE.MAJOR"))

    return amcboard

def acquireSBits(amcboard, ohN, outFilePath, acquireTime=300):
    """
    Acquires SBITs from optohybrid ohN on AMC amcboard for acquireTime seconds.

    amcboard - instance of xhalpy.AMC
    ohN - optohybrid number of amcboard
    outFilePath - filepath where data should be written too
    acquireTime - time in seconds to acquire data for
    """
    amcboard.sbitReadOut(ohN, acquireTime, outFilePath)
    return

def blockL1A(amcboard):
    """
    blocks L1A's to AMC amcboard
    """
    amcboard.writeReg("GEM_AMC.TTC.CTRL.L1A_ENABLE", 0x0)
    return

def enableL1A(amcboard):
    """
    enables L1A's from backplane for this AMC
    """

    amcboard.writeReg("GEM_AMC.TTC.CTRL.L1A_ENABLE", 0x1)
    return

def getLinkVFATMask(amcBoard,ohN):
    """
    V3 electronics only

    Returns a 24 bit number that can be used as the VFAT Mask
    for the Optohybrid ohN

    amcBoard - instance of xhalpy.AMC
    ohN - optohybrid on amcBoard
    """

    mask = amcBoard.getOHVFATMask(ohN)
    if mask == 0xffffffff:
        raise Exception("RPC response was overflow, failed to determine VFAT mask for OH{0}".format(ohN))
    else:
        return mask

def getMultiLinkVFATMask(amcboard,ohMask=0xfff):
    """
    v3 electronics only

    Returns a list of uint32 of size 12.  Each element of the
    list is the vfat mask for the ohN defined by the index

    ohMask - Mask which defines which OH's to query; 12 bit number where
             having a 1 in the N^th bit means to query the N^th optohybrid
    """

    return amcboard.getOHVFATMaskMultiLink(ohMask)

def getL1ACount(amcboard):
    return amcboard.readReg("GEM_AMC.TTC.CMD_COUNTERS.L1A")

    #class HwAMC(object):
#    def __init__(self, cardName, debug=False):
#        """
#        Initialize the HW board an open an RPC connection
#        """
#        
#        # Debug flag
#        self.debug = debug
#        
#        # Logger
#        self.amclogger = logging.getLogger(__name__)
#
#        # Store HW info
#        self.name = cardName
#        #self.nOHs = 12
#        self.nOHs = 4
#
#        # Open the foreign function library
#        self.lib = CDLL("librpcman.so")
#       
#        # Define VFAT3 DAC Monitoring
#        self.confDacMonitorMulti = self.lib.configureVFAT3DacMonitorMultiLink
#        self.confDacMonitorMulti.argTypes = [ c_uint, POINTER(c_uint32), c_uint ]
#        self.confDacMonitorMulti.restype = c_uint
#
#        self.readADCsMulti = self.lib.readVFAT3ADCMultiLink
#        self.readADCsMulti.argTypes = [ c_uint, POINTER(c_uint32), c_uint, c_uint ]
#        self.readADCsMulti.restype = c_uint
#
#        # Define Get OH Mask functionality
#        self.self.lib.getOHVFATMask = self.lib.getOHVFATMask
#        self.self.lib.getOHVFATMask.argTypes = [ c_uint ]
#        self.self.lib.getOHVFATMask.restype = c_uint
#
#        self.getOHVFATMaskMultiLink = self.lib.getOHVFATMaskMultiLink
#        self.getOHVFATMaskMultiLink.argTypes = [ c_uint, POINTER(c_uint32) ]
#        self.getOHVFATMaskMultiLink.restype = c_uint
#
#        # Define TTC Functions
#        self.ttcGenConf = self.lib.ttcGenConf
#        self.ttcGenConf.restype = c_uint
#        self.ttcGenConf.argtypes = [c_uint, c_uint, c_uint, c_uint, c_uint, c_uint, c_bool]
#
#        self.ttcGenToggle = self.lib.ttcGenToggle
#        self.ttcGenToggle.restype = c_uint
#        self.ttcGenToggle.argtypes = [c_uint, c_bool]
#
#        # Define SBIT Local Readout
#        self.readSBits = self.lib.sbitReadOut
#        self.readSBits.restype = c_uint
#        self.readSBits.argtypes = [c_uint, c_uint, c_char_p]
#
#        # Parse XML
#        parseXML()
#
#        # Open RPC Connection
#        print "Initializing AMC", self.name
#        rpc_connect(self.name)
#        self.fwVersion = self.readRegister("GEM_AMC.GEM_SYSTEM.RELEASE.MAJOR")
#        print "My FW release major = ", self.fwVersion
#
#        return
#
#
#
#
#
#
#    def getTTCStatus(self, ohN, display=False):
#        running = 0xdeaddead
#        if self.fwVersion < 3:
#            contBase = "GEM_AMC.OH.OH%i.T1Controller"%(ohN)
#            running = self.readRegister("%s.MONITOR"%(contBase))
#            if display:
#                print("Info for %s"%(contBase))
#                print("\tDELAY:\t\t%i"%(self.readRegister("%s.DELAY"%(contBase))))
#                print("\tINTERVAL:\t%i"%(self.readRegister("%s.INTERVAL"%(contBase))))
#                print("\tMODE:\t\t%i"%(self.readRegister("%s.MODE"%(contBase))))
#                print("\tMONITOR:\t%i"%(running))
#                print("\tNUMBER:\t\t%i"%(self.readRegister("%s.NUMBER"%(contBase))))
#                print("\tTYPE:\t\t%i"%(self.readRegister("%s.TYPE"%(contBase))))
#        else:
#            contBase = "GEM_AMC.TTC.GENERATOR"
#            running = self.readRegister("%s.ENABLE"%(contBase))
#            if display:
#                print("Info for %s"%(contBase))
#                print("\tCYCLIC_L1A_GAP: \t\t%i"%(self.readRegister("%s.CYCLIC_L1A_GAP"%(contBase))))
#                print("\tCYCLIC_CALPULSE_TO_L1A_GAP: \t%i"%(self.readRegister("%s.CYCLIC_CALPULSE_TO_L1A_GAP"%(contBase))))
#                print("\tENABLE: \t\t\t%i"%(running))
#        return running
#
#    def readAllADCsMulti(self, adcDataAll, useExtRefADC=False, ohMask=0xFFF):
#        """
#        Reads the ADC value from all unmasked VFATs
#
#        adcDataAll - Array of type c_uint32 of size 24*12=288
#        useExtRefADC - True (False) use the externally (internally) referenced ADC
#        ohMask - Mask which defines which OH's to query; 12 bit number where
#                 having a 1 in the N^th bit means to query the N^th optohybrid
#        """
#
#        ohVFATMaskArray = self.getMultiLinkVFATMask(ohMask)
#        return self.readADCsMulti(ohMask,ohVFATMaskArray, adcDataAll, useExtRefADC)
#
#    def readBlock(register, nwords, debug=False):
#        """
#        read block 'register'
#        returns 'nwords' values in the register
#        """
#        global gRetries
#        nRetries = 0
#        m_node = getNode(register)
#        if m_node is None:
#            print colors.MAGENTA,"NODE %s NOT FOUND" %(register),colors.ENDC
#            return 0x0
#     
#        p = (c_uint32*nwords)()
#        words = []
#        if (debug):
#            print "reading %d words from register %s"%(nwords,register)
#        res = rBlock(m_node.real_address,p,len(p))
#        if (res == 0):
#            words = list(p)
#            if (debug):
#                print "ReadBlock result:\n"
#                print words
#            return words
#        else:
#            print colors.RED, "error encountered, retried read operation (%d)"%(nRetries),colors.ENDC
#            nRetries += 1
#        return words
#
#    def readRegister(self, register, debug=False):
#        """
#        read register 'register' using remote procedure call
#        returns value of the register
#        """
#        global gRetries
#        nRetries = 0
#        m_node = getNode(register)
#        if m_node is None:
#            print colors.MAGENTA,"NODE %s NOT FOUND" %(register),colors.ENDC
#            return 0x0
#        elif 'r' not in m_node.permission:
#            print colors.MAGENTA,"No read permission for register %s" %(register),colors.ENDC
#            return 0x0
#        if debug:
#            print "Trying to read\n"
#            print m_node.output()
#        while (nRetries<gRetries):
#            res = rReg(parseInt(m_node.real_address))
#            if res == 0xdeaddead:
#                print colors.MAGENTA,"Bus error encountered while reading (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
#                continue
#            else:
#                if m_node.mask is not None:
#                    shift_amount=0
#                    for bit in reversed('{0:b}'.format(m_node.mask)):
#                        if bit=='0': shift_amount+=1
#                        else: break
#                    fin_res = (res&m_node.mask)>>shift_amount
#                else:
#                    fin_res = res
#                if debug: print "Read register result: %s" %(fin_res)
#                return fin_res
#        return 0xdeaddead
#
#    def writeRegister(self, register, value, debug=False):
#        """
#        write value 'value' into register 'register' using remote procedure call
#        """
#        global gRetries
#        nRetries = 0
#        #m_node = self.getNode(register)
#        m_node = getNode(register)
#        if m_node is None:
#            print colors.MAGENTA,"NODE %s NOT FOUND"%(register),colors.ENDC
#            return 0x0
#    
#        if debug:
#            print "Trying to write\n"
#            print m_node.output()
#     
#        while (nRetries < gMAX_RETRIES):
#            rsp = writeReg(m_node, value)
#            if "permission" in rsp:
#                print colors.MAGENTA,"NO WRITE PERMISSION",colors.ENDC
#                return
#            elif "Error" in rsp:
#                print colors.MAGENTA,"write error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
#                return
#            elif "0xdeaddead" in rsp:
#                print colors.MAGENTA,"0xdeaddead found (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),colors.ENDC
#                return
#            else:
#                return
#
#    def writeRegisterList(self, regs_with_vals, debug=False):
#        """
#        write value 'value' into register 'register' using remote procedure call
#        from an input dict
#        """
#        global gRetries
#        nRetries = 0
#        while (nRetries < gMAX_RETRIES):
#            for reg in regs_with_vals.keys():
#                self.writeRegister(reg,regs_with_vals[reg],debug)
#            return

