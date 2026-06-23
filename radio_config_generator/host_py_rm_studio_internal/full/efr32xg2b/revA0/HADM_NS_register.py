
# -*- coding: utf-8 -*-

from . static import Base_RM_Register
from . HADM_NS_field import *


class RM_Register_HADM_NS_IPVERSION(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_IPVERSION, self).__init__(rmio, label,
            0xb8034000, 0x000,
            'IPVERSION', 'HADM_NS.IPVERSION', 'read-only',
            u"",
            0x00000001, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.IPVERSION = RM_Field_HADM_NS_IPVERSION_IPVERSION(self)
        self.zz_fdict['IPVERSION'] = self.IPVERSION
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_EN(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_EN, self).__init__(rmio, label,
            0xb8034000, 0x004,
            'EN', 'HADM_NS.EN', 'read-write',
            u"",
            0x00000000, 0x00000001,
            0x00001000, 0x00002000,
            0x00003000)

        self.EN = RM_Field_HADM_NS_EN_EN(self)
        self.zz_fdict['EN'] = self.EN
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_IEN(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_IEN, self).__init__(rmio, label,
            0xb8034000, 0x020,
            'IEN', 'HADM_NS.IEN', 'read-write',
            u"",
            0x00000000, 0x001FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFOF = RM_Field_HADM_NS_IEN_BUFOF(self)
        self.zz_fdict['BUFOF'] = self.BUFOF
        self.BUFTHR = RM_Field_HADM_NS_IEN_BUFTHR(self)
        self.zz_fdict['BUFTHR'] = self.BUFTHR
        self.BUSERROR = RM_Field_HADM_NS_IEN_BUSERROR(self)
        self.zz_fdict['BUSERROR'] = self.BUSERROR
        self.FRAMEDET = RM_Field_HADM_NS_IEN_FRAMEDET(self)
        self.zz_fdict['FRAMEDET'] = self.FRAMEDET
        self.PKTINFOOF = RM_Field_HADM_NS_IEN_PKTINFOOF(self)
        self.zz_fdict['PKTINFOOF'] = self.PKTINFOOF
        self.FREQESTOF = RM_Field_HADM_NS_IEN_FREQESTOF(self)
        self.zz_fdict['FREQESTOF'] = self.FREQESTOF
        self.RTTOF = RM_Field_HADM_NS_IEN_RTTOF(self)
        self.zz_fdict['RTTOF'] = self.RTTOF
        self.NADMOF = RM_Field_HADM_NS_IEN_NADMOF(self)
        self.zz_fdict['NADMOF'] = self.NADMOF
        self.PBROF = RM_Field_HADM_NS_IEN_PBROF(self)
        self.zz_fdict['PBROF'] = self.PBROF
        self.RESULTSOF = RM_Field_HADM_NS_IEN_RESULTSOF(self)
        self.zz_fdict['RESULTSOF'] = self.RESULTSOF
        self.TIMERERR = RM_Field_HADM_NS_IEN_TIMERERR(self)
        self.zz_fdict['TIMERERR'] = self.TIMERERR
        self.ANTSWERR = RM_Field_HADM_NS_IEN_ANTSWERR(self)
        self.zz_fdict['ANTSWERR'] = self.ANTSWERR
        self.TIMEOUTERR = RM_Field_HADM_NS_IEN_TIMEOUTERR(self)
        self.zz_fdict['TIMEOUTERR'] = self.TIMEOUTERR
        self.RSLTINSTRERR = RM_Field_HADM_NS_IEN_RSLTINSTRERR(self)
        self.zz_fdict['RSLTINSTRERR'] = self.RSLTINSTRERR
        self.TASKSTART = RM_Field_HADM_NS_IEN_TASKSTART(self)
        self.zz_fdict['TASKSTART'] = self.TASKSTART
        self.TASKDONE = RM_Field_HADM_NS_IEN_TASKDONE(self)
        self.zz_fdict['TASKDONE'] = self.TASKDONE
        self.TASKSTARTERR = RM_Field_HADM_NS_IEN_TASKSTARTERR(self)
        self.zz_fdict['TASKSTARTERR'] = self.TASKSTARTERR
        self.RESULTSDONE = RM_Field_HADM_NS_IEN_RESULTSDONE(self)
        self.zz_fdict['RESULTSDONE'] = self.RESULTSDONE
        self.INSTRSTART = RM_Field_HADM_NS_IEN_INSTRSTART(self)
        self.zz_fdict['INSTRSTART'] = self.INSTRSTART
        self.INSTRDONE = RM_Field_HADM_NS_IEN_INSTRDONE(self)
        self.zz_fdict['INSTRDONE'] = self.INSTRDONE
        self.RESULTFIFOOF = RM_Field_HADM_NS_IEN_RESULTFIFOOF(self)
        self.zz_fdict['RESULTFIFOOF'] = self.RESULTFIFOOF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_IF(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_IF, self).__init__(rmio, label,
            0xb8034000, 0x024,
            'IF', 'HADM_NS.IF', 'read-write',
            u"",
            0x00000000, 0x001FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFOF = RM_Field_HADM_NS_IF_BUFOF(self)
        self.zz_fdict['BUFOF'] = self.BUFOF
        self.BUFTHR = RM_Field_HADM_NS_IF_BUFTHR(self)
        self.zz_fdict['BUFTHR'] = self.BUFTHR
        self.BUSERROR = RM_Field_HADM_NS_IF_BUSERROR(self)
        self.zz_fdict['BUSERROR'] = self.BUSERROR
        self.FRAMEDET = RM_Field_HADM_NS_IF_FRAMEDET(self)
        self.zz_fdict['FRAMEDET'] = self.FRAMEDET
        self.PKTINFOOF = RM_Field_HADM_NS_IF_PKTINFOOF(self)
        self.zz_fdict['PKTINFOOF'] = self.PKTINFOOF
        self.FREQESTOF = RM_Field_HADM_NS_IF_FREQESTOF(self)
        self.zz_fdict['FREQESTOF'] = self.FREQESTOF
        self.RTTOF = RM_Field_HADM_NS_IF_RTTOF(self)
        self.zz_fdict['RTTOF'] = self.RTTOF
        self.NADMOF = RM_Field_HADM_NS_IF_NADMOF(self)
        self.zz_fdict['NADMOF'] = self.NADMOF
        self.PBROF = RM_Field_HADM_NS_IF_PBROF(self)
        self.zz_fdict['PBROF'] = self.PBROF
        self.RESULTSOF = RM_Field_HADM_NS_IF_RESULTSOF(self)
        self.zz_fdict['RESULTSOF'] = self.RESULTSOF
        self.TIMERERR = RM_Field_HADM_NS_IF_TIMERERR(self)
        self.zz_fdict['TIMERERR'] = self.TIMERERR
        self.ANTSWERR = RM_Field_HADM_NS_IF_ANTSWERR(self)
        self.zz_fdict['ANTSWERR'] = self.ANTSWERR
        self.TIMEOUTERR = RM_Field_HADM_NS_IF_TIMEOUTERR(self)
        self.zz_fdict['TIMEOUTERR'] = self.TIMEOUTERR
        self.RSLTINSTRERR = RM_Field_HADM_NS_IF_RSLTINSTRERR(self)
        self.zz_fdict['RSLTINSTRERR'] = self.RSLTINSTRERR
        self.TASKSTART = RM_Field_HADM_NS_IF_TASKSTART(self)
        self.zz_fdict['TASKSTART'] = self.TASKSTART
        self.TASKDONE = RM_Field_HADM_NS_IF_TASKDONE(self)
        self.zz_fdict['TASKDONE'] = self.TASKDONE
        self.TASKSTARTERR = RM_Field_HADM_NS_IF_TASKSTARTERR(self)
        self.zz_fdict['TASKSTARTERR'] = self.TASKSTARTERR
        self.RESULTSDONE = RM_Field_HADM_NS_IF_RESULTSDONE(self)
        self.zz_fdict['RESULTSDONE'] = self.RESULTSDONE
        self.INSTRSTART = RM_Field_HADM_NS_IF_INSTRSTART(self)
        self.zz_fdict['INSTRSTART'] = self.INSTRSTART
        self.INSTRDONE = RM_Field_HADM_NS_IF_INSTRDONE(self)
        self.zz_fdict['INSTRDONE'] = self.INSTRDONE
        self.RESULTFIFOOF = RM_Field_HADM_NS_IF_RESULTFIFOOF(self)
        self.zz_fdict['RESULTFIFOOF'] = self.RESULTFIFOOF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_SEQIEN(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_SEQIEN, self).__init__(rmio, label,
            0xb8034000, 0x028,
            'SEQIEN', 'HADM_NS.SEQIEN', 'read-write',
            u"",
            0x00000000, 0x001FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFOF = RM_Field_HADM_NS_SEQIEN_BUFOF(self)
        self.zz_fdict['BUFOF'] = self.BUFOF
        self.BUFTHR = RM_Field_HADM_NS_SEQIEN_BUFTHR(self)
        self.zz_fdict['BUFTHR'] = self.BUFTHR
        self.BUSERROR = RM_Field_HADM_NS_SEQIEN_BUSERROR(self)
        self.zz_fdict['BUSERROR'] = self.BUSERROR
        self.FRAMEDET = RM_Field_HADM_NS_SEQIEN_FRAMEDET(self)
        self.zz_fdict['FRAMEDET'] = self.FRAMEDET
        self.PKTINFOOF = RM_Field_HADM_NS_SEQIEN_PKTINFOOF(self)
        self.zz_fdict['PKTINFOOF'] = self.PKTINFOOF
        self.FREQESTOF = RM_Field_HADM_NS_SEQIEN_FREQESTOF(self)
        self.zz_fdict['FREQESTOF'] = self.FREQESTOF
        self.RTTOF = RM_Field_HADM_NS_SEQIEN_RTTOF(self)
        self.zz_fdict['RTTOF'] = self.RTTOF
        self.NADMOF = RM_Field_HADM_NS_SEQIEN_NADMOF(self)
        self.zz_fdict['NADMOF'] = self.NADMOF
        self.PBROF = RM_Field_HADM_NS_SEQIEN_PBROF(self)
        self.zz_fdict['PBROF'] = self.PBROF
        self.RESULTSOF = RM_Field_HADM_NS_SEQIEN_RESULTSOF(self)
        self.zz_fdict['RESULTSOF'] = self.RESULTSOF
        self.TIMERERR = RM_Field_HADM_NS_SEQIEN_TIMERERR(self)
        self.zz_fdict['TIMERERR'] = self.TIMERERR
        self.ANTSWERR = RM_Field_HADM_NS_SEQIEN_ANTSWERR(self)
        self.zz_fdict['ANTSWERR'] = self.ANTSWERR
        self.TIMEOUTERR = RM_Field_HADM_NS_SEQIEN_TIMEOUTERR(self)
        self.zz_fdict['TIMEOUTERR'] = self.TIMEOUTERR
        self.RSLTINSTRERR = RM_Field_HADM_NS_SEQIEN_RSLTINSTRERR(self)
        self.zz_fdict['RSLTINSTRERR'] = self.RSLTINSTRERR
        self.TASKSTART = RM_Field_HADM_NS_SEQIEN_TASKSTART(self)
        self.zz_fdict['TASKSTART'] = self.TASKSTART
        self.TASKDONE = RM_Field_HADM_NS_SEQIEN_TASKDONE(self)
        self.zz_fdict['TASKDONE'] = self.TASKDONE
        self.TASKSTARTERR = RM_Field_HADM_NS_SEQIEN_TASKSTARTERR(self)
        self.zz_fdict['TASKSTARTERR'] = self.TASKSTARTERR
        self.RESULTSDONE = RM_Field_HADM_NS_SEQIEN_RESULTSDONE(self)
        self.zz_fdict['RESULTSDONE'] = self.RESULTSDONE
        self.INSTRSTART = RM_Field_HADM_NS_SEQIEN_INSTRSTART(self)
        self.zz_fdict['INSTRSTART'] = self.INSTRSTART
        self.INSTRDONE = RM_Field_HADM_NS_SEQIEN_INSTRDONE(self)
        self.zz_fdict['INSTRDONE'] = self.INSTRDONE
        self.RESULTFIFOOF = RM_Field_HADM_NS_SEQIEN_RESULTFIFOOF(self)
        self.zz_fdict['RESULTFIFOOF'] = self.RESULTFIFOOF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_SEQIF(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_SEQIF, self).__init__(rmio, label,
            0xb8034000, 0x02C,
            'SEQIF', 'HADM_NS.SEQIF', 'read-write',
            u"",
            0x00000000, 0x001FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFOF = RM_Field_HADM_NS_SEQIF_BUFOF(self)
        self.zz_fdict['BUFOF'] = self.BUFOF
        self.BUFTHR = RM_Field_HADM_NS_SEQIF_BUFTHR(self)
        self.zz_fdict['BUFTHR'] = self.BUFTHR
        self.BUSERROR = RM_Field_HADM_NS_SEQIF_BUSERROR(self)
        self.zz_fdict['BUSERROR'] = self.BUSERROR
        self.FRAMEDET = RM_Field_HADM_NS_SEQIF_FRAMEDET(self)
        self.zz_fdict['FRAMEDET'] = self.FRAMEDET
        self.PKTINFOOF = RM_Field_HADM_NS_SEQIF_PKTINFOOF(self)
        self.zz_fdict['PKTINFOOF'] = self.PKTINFOOF
        self.FREQESTOF = RM_Field_HADM_NS_SEQIF_FREQESTOF(self)
        self.zz_fdict['FREQESTOF'] = self.FREQESTOF
        self.RTTOF = RM_Field_HADM_NS_SEQIF_RTTOF(self)
        self.zz_fdict['RTTOF'] = self.RTTOF
        self.NADMOF = RM_Field_HADM_NS_SEQIF_NADMOF(self)
        self.zz_fdict['NADMOF'] = self.NADMOF
        self.PBROF = RM_Field_HADM_NS_SEQIF_PBROF(self)
        self.zz_fdict['PBROF'] = self.PBROF
        self.RESULTSOF = RM_Field_HADM_NS_SEQIF_RESULTSOF(self)
        self.zz_fdict['RESULTSOF'] = self.RESULTSOF
        self.TIMERERR = RM_Field_HADM_NS_SEQIF_TIMERERR(self)
        self.zz_fdict['TIMERERR'] = self.TIMERERR
        self.ANTSWERR = RM_Field_HADM_NS_SEQIF_ANTSWERR(self)
        self.zz_fdict['ANTSWERR'] = self.ANTSWERR
        self.TIMEOUTERR = RM_Field_HADM_NS_SEQIF_TIMEOUTERR(self)
        self.zz_fdict['TIMEOUTERR'] = self.TIMEOUTERR
        self.RSLTINSTRERR = RM_Field_HADM_NS_SEQIF_RSLTINSTRERR(self)
        self.zz_fdict['RSLTINSTRERR'] = self.RSLTINSTRERR
        self.TASKSTART = RM_Field_HADM_NS_SEQIF_TASKSTART(self)
        self.zz_fdict['TASKSTART'] = self.TASKSTART
        self.TASKDONE = RM_Field_HADM_NS_SEQIF_TASKDONE(self)
        self.zz_fdict['TASKDONE'] = self.TASKDONE
        self.TASKSTARTERR = RM_Field_HADM_NS_SEQIF_TASKSTARTERR(self)
        self.zz_fdict['TASKSTARTERR'] = self.TASKSTARTERR
        self.RESULTSDONE = RM_Field_HADM_NS_SEQIF_RESULTSDONE(self)
        self.zz_fdict['RESULTSDONE'] = self.RESULTSDONE
        self.INSTRSTART = RM_Field_HADM_NS_SEQIF_INSTRSTART(self)
        self.zz_fdict['INSTRSTART'] = self.INSTRSTART
        self.INSTRDONE = RM_Field_HADM_NS_SEQIF_INSTRDONE(self)
        self.zz_fdict['INSTRDONE'] = self.INSTRDONE
        self.RESULTFIFOOF = RM_Field_HADM_NS_SEQIF_RESULTFIFOOF(self)
        self.zz_fdict['RESULTFIFOOF'] = self.RESULTFIFOOF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_FSWIEN(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_FSWIEN, self).__init__(rmio, label,
            0xb8034000, 0x030,
            'FSWIEN', 'HADM_NS.FSWIEN', 'read-write',
            u"",
            0x00000000, 0x001FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFOF = RM_Field_HADM_NS_FSWIEN_BUFOF(self)
        self.zz_fdict['BUFOF'] = self.BUFOF
        self.BUFTHR = RM_Field_HADM_NS_FSWIEN_BUFTHR(self)
        self.zz_fdict['BUFTHR'] = self.BUFTHR
        self.BUSERROR = RM_Field_HADM_NS_FSWIEN_BUSERROR(self)
        self.zz_fdict['BUSERROR'] = self.BUSERROR
        self.FRAMEDET = RM_Field_HADM_NS_FSWIEN_FRAMEDET(self)
        self.zz_fdict['FRAMEDET'] = self.FRAMEDET
        self.PKTINFOOF = RM_Field_HADM_NS_FSWIEN_PKTINFOOF(self)
        self.zz_fdict['PKTINFOOF'] = self.PKTINFOOF
        self.FREQESTOF = RM_Field_HADM_NS_FSWIEN_FREQESTOF(self)
        self.zz_fdict['FREQESTOF'] = self.FREQESTOF
        self.RTTOF = RM_Field_HADM_NS_FSWIEN_RTTOF(self)
        self.zz_fdict['RTTOF'] = self.RTTOF
        self.NADMOF = RM_Field_HADM_NS_FSWIEN_NADMOF(self)
        self.zz_fdict['NADMOF'] = self.NADMOF
        self.PBROF = RM_Field_HADM_NS_FSWIEN_PBROF(self)
        self.zz_fdict['PBROF'] = self.PBROF
        self.RESULTSOF = RM_Field_HADM_NS_FSWIEN_RESULTSOF(self)
        self.zz_fdict['RESULTSOF'] = self.RESULTSOF
        self.TIMERERR = RM_Field_HADM_NS_FSWIEN_TIMERERR(self)
        self.zz_fdict['TIMERERR'] = self.TIMERERR
        self.ANTSWERR = RM_Field_HADM_NS_FSWIEN_ANTSWERR(self)
        self.zz_fdict['ANTSWERR'] = self.ANTSWERR
        self.TIMEOUTERR = RM_Field_HADM_NS_FSWIEN_TIMEOUTERR(self)
        self.zz_fdict['TIMEOUTERR'] = self.TIMEOUTERR
        self.RSLTINSTRERR = RM_Field_HADM_NS_FSWIEN_RSLTINSTRERR(self)
        self.zz_fdict['RSLTINSTRERR'] = self.RSLTINSTRERR
        self.TASKSTART = RM_Field_HADM_NS_FSWIEN_TASKSTART(self)
        self.zz_fdict['TASKSTART'] = self.TASKSTART
        self.TASKDONE = RM_Field_HADM_NS_FSWIEN_TASKDONE(self)
        self.zz_fdict['TASKDONE'] = self.TASKDONE
        self.TASKSTARTERR = RM_Field_HADM_NS_FSWIEN_TASKSTARTERR(self)
        self.zz_fdict['TASKSTARTERR'] = self.TASKSTARTERR
        self.RESULTSDONE = RM_Field_HADM_NS_FSWIEN_RESULTSDONE(self)
        self.zz_fdict['RESULTSDONE'] = self.RESULTSDONE
        self.INSTRSTART = RM_Field_HADM_NS_FSWIEN_INSTRSTART(self)
        self.zz_fdict['INSTRSTART'] = self.INSTRSTART
        self.INSTRDONE = RM_Field_HADM_NS_FSWIEN_INSTRDONE(self)
        self.zz_fdict['INSTRDONE'] = self.INSTRDONE
        self.RESULTFIFOOF = RM_Field_HADM_NS_FSWIEN_RESULTFIFOOF(self)
        self.zz_fdict['RESULTFIFOOF'] = self.RESULTFIFOOF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_FSWIF(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_FSWIF, self).__init__(rmio, label,
            0xb8034000, 0x034,
            'FSWIF', 'HADM_NS.FSWIF', 'read-write',
            u"",
            0x00000000, 0x001FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFOF = RM_Field_HADM_NS_FSWIF_BUFOF(self)
        self.zz_fdict['BUFOF'] = self.BUFOF
        self.BUFTHR = RM_Field_HADM_NS_FSWIF_BUFTHR(self)
        self.zz_fdict['BUFTHR'] = self.BUFTHR
        self.BUSERROR = RM_Field_HADM_NS_FSWIF_BUSERROR(self)
        self.zz_fdict['BUSERROR'] = self.BUSERROR
        self.FRAMEDET = RM_Field_HADM_NS_FSWIF_FRAMEDET(self)
        self.zz_fdict['FRAMEDET'] = self.FRAMEDET
        self.PKTINFOOF = RM_Field_HADM_NS_FSWIF_PKTINFOOF(self)
        self.zz_fdict['PKTINFOOF'] = self.PKTINFOOF
        self.FREQESTOF = RM_Field_HADM_NS_FSWIF_FREQESTOF(self)
        self.zz_fdict['FREQESTOF'] = self.FREQESTOF
        self.RTTOF = RM_Field_HADM_NS_FSWIF_RTTOF(self)
        self.zz_fdict['RTTOF'] = self.RTTOF
        self.NADMOF = RM_Field_HADM_NS_FSWIF_NADMOF(self)
        self.zz_fdict['NADMOF'] = self.NADMOF
        self.PBROF = RM_Field_HADM_NS_FSWIF_PBROF(self)
        self.zz_fdict['PBROF'] = self.PBROF
        self.RESULTSOF = RM_Field_HADM_NS_FSWIF_RESULTSOF(self)
        self.zz_fdict['RESULTSOF'] = self.RESULTSOF
        self.TIMERERR = RM_Field_HADM_NS_FSWIF_TIMERERR(self)
        self.zz_fdict['TIMERERR'] = self.TIMERERR
        self.ANTSWERR = RM_Field_HADM_NS_FSWIF_ANTSWERR(self)
        self.zz_fdict['ANTSWERR'] = self.ANTSWERR
        self.TIMEOUTERR = RM_Field_HADM_NS_FSWIF_TIMEOUTERR(self)
        self.zz_fdict['TIMEOUTERR'] = self.TIMEOUTERR
        self.RSLTINSTRERR = RM_Field_HADM_NS_FSWIF_RSLTINSTRERR(self)
        self.zz_fdict['RSLTINSTRERR'] = self.RSLTINSTRERR
        self.TASKSTART = RM_Field_HADM_NS_FSWIF_TASKSTART(self)
        self.zz_fdict['TASKSTART'] = self.TASKSTART
        self.TASKDONE = RM_Field_HADM_NS_FSWIF_TASKDONE(self)
        self.zz_fdict['TASKDONE'] = self.TASKDONE
        self.TASKSTARTERR = RM_Field_HADM_NS_FSWIF_TASKSTARTERR(self)
        self.zz_fdict['TASKSTARTERR'] = self.TASKSTARTERR
        self.RESULTSDONE = RM_Field_HADM_NS_FSWIF_RESULTSDONE(self)
        self.zz_fdict['RESULTSDONE'] = self.RESULTSDONE
        self.INSTRSTART = RM_Field_HADM_NS_FSWIF_INSTRSTART(self)
        self.zz_fdict['INSTRSTART'] = self.INSTRSTART
        self.INSTRDONE = RM_Field_HADM_NS_FSWIF_INSTRDONE(self)
        self.zz_fdict['INSTRDONE'] = self.INSTRDONE
        self.RESULTFIFOOF = RM_Field_HADM_NS_FSWIF_RESULTFIFOOF(self)
        self.zz_fdict['RESULTFIFOOF'] = self.RESULTFIFOOF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_CMD(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_CMD, self).__init__(rmio, label,
            0xb8034000, 0x038,
            'CMD', 'HADM_NS.CMD', 'write-only',
            u"",
            0x00000000, 0x0000003F,
            0x00001000, 0x00002000,
            0x00003000)

        self.START = RM_Field_HADM_NS_CMD_START(self)
        self.zz_fdict['START'] = self.START
        self.STOP = RM_Field_HADM_NS_CMD_STOP(self)
        self.zz_fdict['STOP'] = self.STOP
        self.FORCECTRL = RM_Field_HADM_NS_CMD_FORCECTRL(self)
        self.zz_fdict['FORCECTRL'] = self.FORCECTRL
        self.RSTANTSEL = RM_Field_HADM_NS_CMD_RSTANTSEL(self)
        self.zz_fdict['RSTANTSEL'] = self.RSTANTSEL
        self.CLEAR = RM_Field_HADM_NS_CMD_CLEAR(self)
        self.zz_fdict['CLEAR'] = self.CLEAR
        self.FLUSH = RM_Field_HADM_NS_CMD_FLUSH(self)
        self.zz_fdict['FLUSH'] = self.FLUSH
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_CTRL0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_CTRL0, self).__init__(rmio, label,
            0xb8034000, 0x03C,
            'CTRL0', 'HADM_NS.CTRL0', 'read-write',
            u"",
            0x00800000, 0x07FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ROLE = RM_Field_HADM_NS_CTRL0_ROLE(self)
        self.zz_fdict['ROLE'] = self.ROLE
        self.PHYSEL = RM_Field_HADM_NS_CTRL0_PHYSEL(self)
        self.zz_fdict['PHYSEL'] = self.PHYSEL
        self.SSAFCGEAR = RM_Field_HADM_NS_CTRL0_SSAFCGEAR(self)
        self.zz_fdict['SSAFCGEAR'] = self.SSAFCGEAR
        self.TXUPSAMPOSR4 = RM_Field_HADM_NS_CTRL0_TXUPSAMPOSR4(self)
        self.zz_fdict['TXUPSAMPOSR4'] = self.TXUPSAMPOSR4
        self.TGUARDPERIOD = RM_Field_HADM_NS_CTRL0_TGUARDPERIOD(self)
        self.zz_fdict['TGUARDPERIOD'] = self.TGUARDPERIOD
        self.AVGSTARTOFF = RM_Field_HADM_NS_CTRL0_AVGSTARTOFF(self)
        self.zz_fdict['AVGSTARTOFF'] = self.AVGSTARTOFF
        self.OWRRSTDLO = RM_Field_HADM_NS_CTRL0_OWRRSTDLO(self)
        self.zz_fdict['OWRRSTDLO'] = self.OWRRSTDLO
        self.GDCOMPEN = RM_Field_HADM_NS_CTRL0_GDCOMPEN(self)
        self.zz_fdict['GDCOMPEN'] = self.GDCOMPEN
        self.CTRLMODE = RM_Field_HADM_NS_CTRL0_CTRLMODE(self)
        self.zz_fdict['CTRLMODE'] = self.CTRLMODE
        self.WAITONERROR = RM_Field_HADM_NS_CTRL0_WAITONERROR(self)
        self.zz_fdict['WAITONERROR'] = self.WAITONERROR
        self.TFM = RM_Field_HADM_NS_CTRL0_TFM(self)
        self.zz_fdict['TFM'] = self.TFM
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTCTRL0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTCTRL0, self).__init__(rmio, label,
            0xb8034000, 0x040,
            'RTTCTRL0', 'HADM_NS.RTTCTRL0', 'read-write',
            u"",
            0x08000000, 0x0FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RTTMODE = RM_Field_HADM_NS_RTTCTRL0_RTTMODE(self)
        self.zz_fdict['RTTMODE'] = self.RTTMODE
        self.RTTLEN = RM_Field_HADM_NS_RTTCTRL0_RTTLEN(self)
        self.zz_fdict['RTTLEN'] = self.RTTLEN
        self.PESEN = RM_Field_HADM_NS_RTTCTRL0_PESEN(self)
        self.zz_fdict['PESEN'] = self.PESEN
        self.SNDSEQEN = RM_Field_HADM_NS_RTTCTRL0_SNDSEQEN(self)
        self.zz_fdict['SNDSEQEN'] = self.SNDSEQEN
        self.PKTSENTSEL = RM_Field_HADM_NS_RTTCTRL0_PKTSENTSEL(self)
        self.zz_fdict['PKTSENTSEL'] = self.PKTSENTSEL
        self.DFTSCALE = RM_Field_HADM_NS_RTTCTRL0_DFTSCALE(self)
        self.zz_fdict['DFTSCALE'] = self.DFTSCALE
        self.RBSTRACKNUM = RM_Field_HADM_NS_RTTCTRL0_RBSTRACKNUM(self)
        self.zz_fdict['RBSTRACKNUM'] = self.RBSTRACKNUM
        self.DFTSTARTOFF = RM_Field_HADM_NS_RTTCTRL0_DFTSTARTOFF(self)
        self.zz_fdict['DFTSTARTOFF'] = self.DFTSTARTOFF
        self.RTTTIMEOUT = RM_Field_HADM_NS_RTTCTRL0_RTTTIMEOUT(self)
        self.zz_fdict['RTTTIMEOUT'] = self.RTTTIMEOUT
        self.MAXSCHWIN = RM_Field_HADM_NS_RTTCTRL0_MAXSCHWIN(self)
        self.zz_fdict['MAXSCHWIN'] = self.MAXSCHWIN
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTCTRL1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTCTRL1, self).__init__(rmio, label,
            0xb8034000, 0x044,
            'RTTCTRL1', 'HADM_NS.RTTCTRL1', 'read-write',
            u"",
            0x03000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.TRECSOSR = RM_Field_HADM_NS_RTTCTRL1_TRECSOSR(self)
        self.zz_fdict['TRECSOSR'] = self.TRECSOSR
        self.RAMRADDRBACK = RM_Field_HADM_NS_RTTCTRL1_RAMRADDRBACK(self)
        self.zz_fdict['RAMRADDRBACK'] = self.RAMRADDRBACK
        self.FRAMEDETSEL = RM_Field_HADM_NS_RTTCTRL1_FRAMEDETSEL(self)
        self.zz_fdict['FRAMEDETSEL'] = self.FRAMEDETSEL
        self.FRAMEDETTIMEOUT = RM_Field_HADM_NS_RTTCTRL1_FRAMEDETTIMEOUT(self)
        self.zz_fdict['FRAMEDETTIMEOUT'] = self.FRAMEDETTIMEOUT
        self.SBFLIPEN = RM_Field_HADM_NS_RTTCTRL1_SBFLIPEN(self)
        self.zz_fdict['SBFLIPEN'] = self.SBFLIPEN
        self.EPLBWREN = RM_Field_HADM_NS_RTTCTRL1_EPLBWREN(self)
        self.zz_fdict['EPLBWREN'] = self.EPLBWREN
        self.SSPMSWAPEN = RM_Field_HADM_NS_RTTCTRL1_SSPMSWAPEN(self)
        self.zz_fdict['SSPMSWAPEN'] = self.SSPMSWAPEN
        self.XOSEL = RM_Field_HADM_NS_RTTCTRL1_XOSEL(self)
        self.zz_fdict['XOSEL'] = self.XOSEL
        self.ELSWAPEN = RM_Field_HADM_NS_RTTCTRL1_ELSWAPEN(self)
        self.zz_fdict['ELSWAPEN'] = self.ELSWAPEN
        self.CORRACCDLY = RM_Field_HADM_NS_RTTCTRL1_CORRACCDLY(self)
        self.zz_fdict['CORRACCDLY'] = self.CORRACCDLY
        self.SSDFTEN = RM_Field_HADM_NS_RTTCTRL1_SSDFTEN(self)
        self.zz_fdict['SSDFTEN'] = self.SSDFTEN
        self.TIMEROWEN = RM_Field_HADM_NS_RTTCTRL1_TIMEROWEN(self)
        self.zz_fdict['TIMEROWEN'] = self.TIMEROWEN
        self.FBROCEN = RM_Field_HADM_NS_RTTCTRL1_FBROCEN(self)
        self.zz_fdict['FBROCEN'] = self.FBROCEN
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTCTRL2(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTCTRL2, self).__init__(rmio, label,
            0xb8034000, 0x048,
            'RTTCTRL2', 'HADM_NS.RTTCTRL2', 'read-write',
            u"",
            0x000000A0, 0x0001FFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.FBROCMUL2EN = RM_Field_HADM_NS_RTTCTRL2_FBROCMUL2EN(self)
        self.zz_fdict['FBROCMUL2EN'] = self.FBROCMUL2EN
        self.TIMERDETSEL = RM_Field_HADM_NS_RTTCTRL2_TIMERDETSEL(self)
        self.zz_fdict['TIMERDETSEL'] = self.TIMERDETSEL
        self.FLIPEPL1EN = RM_Field_HADM_NS_RTTCTRL2_FLIPEPL1EN(self)
        self.zz_fdict['FLIPEPL1EN'] = self.FLIPEPL1EN
        self.FLIPEPL2EN = RM_Field_HADM_NS_RTTCTRL2_FLIPEPL2EN(self)
        self.zz_fdict['FLIPEPL2EN'] = self.FLIPEPL2EN
        self.SINGLEPKTMODEEN = RM_Field_HADM_NS_RTTCTRL2_SINGLEPKTMODEEN(self)
        self.zz_fdict['SINGLEPKTMODEEN'] = self.SINGLEPKTMODEEN
        self.SRCMUREFBACK = RM_Field_HADM_NS_RTTCTRL2_SRCMUREFBACK(self)
        self.zz_fdict['SRCMUREFBACK'] = self.SRCMUREFBACK
        self.SSFFOLEN = RM_Field_HADM_NS_RTTCTRL2_SSFFOLEN(self)
        self.zz_fdict['SSFFOLEN'] = self.SSFFOLEN
        self.SRCCOMPSAMPSKIPEN = RM_Field_HADM_NS_RTTCTRL2_SRCCOMPSAMPSKIPEN(self)
        self.zz_fdict['SRCCOMPSAMPSKIPEN'] = self.SRCCOMPSAMPSKIPEN
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTTUNE(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTTUNE, self).__init__(rmio, label,
            0xb8034000, 0x04C,
            'RTTTUNE', 'HADM_NS.RTTTUNE', 'read-write',
            u"",
            0x00000000, 0x00FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RTTINITTUNE = RM_Field_HADM_NS_RTTTUNE_RTTINITTUNE(self)
        self.zz_fdict['RTTINITTUNE'] = self.RTTINITTUNE
        self.RTTREFLTUNE = RM_Field_HADM_NS_RTTTUNE_RTTREFLTUNE(self)
        self.zz_fdict['RTTREFLTUNE'] = self.RTTREFLTUNE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTRPTTIME0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTRPTTIME0, self).__init__(rmio, label,
            0xb8034000, 0x050,
            'RTTRPTTIME0', 'HADM_NS.RTTRPTTIME0', 'read-write',
            u"",
            0x00000000, 0x7FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFBACKSYMB = RM_Field_HADM_NS_RTTRPTTIME0_REFBACKSYMB(self)
        self.zz_fdict['REFBACKSYMB'] = self.REFBACKSYMB
        self.REFBACKCYCLE = RM_Field_HADM_NS_RTTRPTTIME0_REFBACKCYCLE(self)
        self.zz_fdict['REFBACKCYCLE'] = self.REFBACKCYCLE
        self.GROUPDLY = RM_Field_HADM_NS_RTTRPTTIME0_GROUPDLY(self)
        self.zz_fdict['GROUPDLY'] = self.GROUPDLY
        self.RTTTIP1IDX = RM_Field_HADM_NS_RTTRPTTIME0_RTTTIP1IDX(self)
        self.zz_fdict['RTTTIP1IDX'] = self.RTTTIP1IDX
        self.FLTDLY = RM_Field_HADM_NS_RTTRPTTIME0_FLTDLY(self)
        self.zz_fdict['FLTDLY'] = self.FLTDLY
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTRPTTIME1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTRPTTIME1, self).__init__(rmio, label,
            0xb8034000, 0x054,
            'RTTRPTTIME1', 'HADM_NS.RTTRPTTIME1', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.FFO = RM_Field_HADM_NS_RTTRPTTIME1_FFO(self)
        self.zz_fdict['FFO'] = self.FFO
        self.COARSETIMEOW = RM_Field_HADM_NS_RTTRPTTIME1_COARSETIMEOW(self)
        self.zz_fdict['COARSETIMEOW'] = self.COARSETIMEOW
        self.SSFFONEG = RM_Field_HADM_NS_RTTRPTTIME1_SSFFONEG(self)
        self.zz_fdict['SSFFONEG'] = self.SSFFONEG
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTPKT0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTPKT0, self).__init__(rmio, label,
            0xb8034000, 0x058,
            'RTTPKT0', 'HADM_NS.RTTPKT0', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RTTPAYLOAD0 = RM_Field_HADM_NS_RTTPKT0_RTTPAYLOAD0(self)
        self.zz_fdict['RTTPAYLOAD0'] = self.RTTPAYLOAD0
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTPKT1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTPKT1, self).__init__(rmio, label,
            0xb8034000, 0x05C,
            'RTTPKT1', 'HADM_NS.RTTPKT1', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RTTPAYLOAD1 = RM_Field_HADM_NS_RTTPKT1_RTTPAYLOAD1(self)
        self.zz_fdict['RTTPAYLOAD1'] = self.RTTPAYLOAD1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTPKT2(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTPKT2, self).__init__(rmio, label,
            0xb8034000, 0x060,
            'RTTPKT2', 'HADM_NS.RTTPKT2', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RTTPAYLOAD2 = RM_Field_HADM_NS_RTTPKT2_RTTPAYLOAD2(self)
        self.zz_fdict['RTTPAYLOAD2'] = self.RTTPAYLOAD2
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RTTPKT3(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RTTPKT3, self).__init__(rmio, label,
            0xb8034000, 0x064,
            'RTTPKT3', 'HADM_NS.RTTPKT3', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RTTPAYLOAD3 = RM_Field_HADM_NS_RTTPKT3_RTTPAYLOAD3(self)
        self.zz_fdict['RTTPAYLOAD3'] = self.RTTPAYLOAD3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PBRCTRL0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PBRCTRL0, self).__init__(rmio, label,
            0xb8034000, 0x068,
            'PBRCTRL0', 'HADM_NS.PBRCTRL0', 'read-write',
            u"",
            0x00002000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.AVGMODE = RM_Field_HADM_NS_PBRCTRL0_AVGMODE(self)
        self.zz_fdict['AVGMODE'] = self.AVGMODE
        self.PM = RM_Field_HADM_NS_PBRCTRL0_PM(self)
        self.zz_fdict['PM'] = self.PM
        self.TEXCL = RM_Field_HADM_NS_PBRCTRL0_TEXCL(self)
        self.zz_fdict['TEXCL'] = self.TEXCL
        self.TSWITCH = RM_Field_HADM_NS_PBRCTRL0_TSWITCH(self)
        self.zz_fdict['TSWITCH'] = self.TSWITCH
        self.TGRPDLY = RM_Field_HADM_NS_PBRCTRL0_TGRPDLY(self)
        self.zz_fdict['TGRPDLY'] = self.TGRPDLY
        self.ACI = RM_Field_HADM_NS_PBRCTRL0_ACI(self)
        self.zz_fdict['ACI'] = self.ACI
        self.API = RM_Field_HADM_NS_PBRCTRL0_API(self)
        self.zz_fdict['API'] = self.API
        self.TONEQUALITYTHRESH = RM_Field_HADM_NS_PBRCTRL0_TONEQUALITYTHRESH(self)
        self.zz_fdict['TONEQUALITYTHRESH'] = self.TONEQUALITYTHRESH
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PBRCTRL1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PBRCTRL1, self).__init__(rmio, label,
            0xb8034000, 0x06C,
            'PBRCTRL1', 'HADM_NS.PBRCTRL1', 'read-write',
            u"",
            0x00028000, 0x01FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.CHNO = RM_Field_HADM_NS_PBRCTRL1_CHNO(self)
        self.zz_fdict['CHNO'] = self.CHNO
        self.DCMEASEN = RM_Field_HADM_NS_PBRCTRL1_DCMEASEN(self)
        self.zz_fdict['DCMEASEN'] = self.DCMEASEN
        self.DCMEASMODE = RM_Field_HADM_NS_PBRCTRL1_DCMEASMODE(self)
        self.zz_fdict['DCMEASMODE'] = self.DCMEASMODE
        self.DCMEASWIN = RM_Field_HADM_NS_PBRCTRL1_DCMEASWIN(self)
        self.zz_fdict['DCMEASWIN'] = self.DCMEASWIN
        self.EMPTYPCTEN = RM_Field_HADM_NS_PBRCTRL1_EMPTYPCTEN(self)
        self.zz_fdict['EMPTYPCTEN'] = self.EMPTYPCTEN
        self.TONEQUALITYSCALE = RM_Field_HADM_NS_PBRCTRL1_TONEQUALITYSCALE(self)
        self.zz_fdict['TONEQUALITYSCALE'] = self.TONEQUALITYSCALE
        self.INLINEPCTEN = RM_Field_HADM_NS_PBRCTRL1_INLINEPCTEN(self)
        self.zz_fdict['INLINEPCTEN'] = self.INLINEPCTEN
        self.PBRLIFEN = RM_Field_HADM_NS_PBRCTRL1_PBRLIFEN(self)
        self.zz_fdict['PBRLIFEN'] = self.PBRLIFEN
        self.TPULSE = RM_Field_HADM_NS_PBRCTRL1_TPULSE(self)
        self.zz_fdict['TPULSE'] = self.TPULSE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PBRDCCOMP(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PBRDCCOMP, self).__init__(rmio, label,
            0xb8034000, 0x070,
            'PBRDCCOMP', 'HADM_NS.PBRDCCOMP', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.DCCOMPI = RM_Field_HADM_NS_PBRDCCOMP_DCCOMPI(self)
        self.zz_fdict['DCCOMPI'] = self.DCCOMPI
        self.DCCOMPQ = RM_Field_HADM_NS_PBRDCCOMP_DCCOMPQ(self)
        self.zz_fdict['DCCOMPQ'] = self.DCCOMPQ
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PBRGDCOMP0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PBRGDCOMP0, self).__init__(rmio, label,
            0xb8034000, 0x074,
            'PBRGDCOMP0', 'HADM_NS.PBRGDCOMP0', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.PHASEPERCHANNEL0 = RM_Field_HADM_NS_PBRGDCOMP0_PHASEPERCHANNEL0(self)
        self.zz_fdict['PHASEPERCHANNEL0'] = self.PHASEPERCHANNEL0
        self.PHASEPERCHANNEL1 = RM_Field_HADM_NS_PBRGDCOMP0_PHASEPERCHANNEL1(self)
        self.zz_fdict['PHASEPERCHANNEL1'] = self.PHASEPERCHANNEL1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PBRGDCOMP1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PBRGDCOMP1, self).__init__(rmio, label,
            0xb8034000, 0x078,
            'PBRGDCOMP1', 'HADM_NS.PBRGDCOMP1', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.PHASEPERCHANNEL2 = RM_Field_HADM_NS_PBRGDCOMP1_PHASEPERCHANNEL2(self)
        self.zz_fdict['PHASEPERCHANNEL2'] = self.PHASEPERCHANNEL2
        self.PHASEPERCHANNEL3 = RM_Field_HADM_NS_PBRGDCOMP1_PHASEPERCHANNEL3(self)
        self.zz_fdict['PHASEPERCHANNEL3'] = self.PHASEPERCHANNEL3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PBRRAMPCTRL(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PBRRAMPCTRL, self).__init__(rmio, label,
            0xb8034000, 0x07C,
            'PBRRAMPCTRL', 'HADM_NS.PBRRAMPCTRL', 'read-write',
            u"",
            0x00000000, 0x000FFF1F,
            0x00001000, 0x00002000,
            0x00003000)

        self.RAMPEN = RM_Field_HADM_NS_PBRRAMPCTRL_RAMPEN(self)
        self.zz_fdict['RAMPEN'] = self.RAMPEN
        self.TRAMPPRETRIG = RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPPRETRIG(self)
        self.zz_fdict['TRAMPPRETRIG'] = self.TRAMPPRETRIG
        self.TRAMPPOSTTRIG = RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPPOSTTRIG(self)
        self.zz_fdict['TRAMPPOSTTRIG'] = self.TRAMPPOSTTRIG
        self.TRAMP = RM_Field_HADM_NS_PBRRAMPCTRL_TRAMP(self)
        self.zz_fdict['TRAMP'] = self.TRAMP
        self.TRAMPSW = RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPSW(self)
        self.zz_fdict['TRAMPSW'] = self.TRAMPSW
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_ANTCTRL(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_ANTCTRL, self).__init__(rmio, label,
            0xb8034000, 0x080,
            'ANTCTRL', 'HADM_NS.ANTCTRL', 'read-write',
            u"",
            0x00000000, 0x7FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ANTPATTHADM = RM_Field_HADM_NS_ANTCTRL_ANTPATTHADM(self)
        self.zz_fdict['ANTPATTHADM'] = self.ANTPATTHADM
        self.CSSYNCNUMANT = RM_Field_HADM_NS_ANTCTRL_CSSYNCNUMANT(self)
        self.zz_fdict['CSSYNCNUMANT'] = self.CSSYNCNUMANT
        self.CSSYNCANTSEL = RM_Field_HADM_NS_ANTCTRL_CSSYNCANTSEL(self)
        self.zz_fdict['CSSYNCANTSEL'] = self.CSSYNCANTSEL
        self.DCMEASANTSEL = RM_Field_HADM_NS_ANTCTRL_DCMEASANTSEL(self)
        self.zz_fdict['DCMEASANTSEL'] = self.DCMEASANTSEL
        self.ANTSWITCHADVANCE = RM_Field_HADM_NS_ANTCTRL_ANTSWITCHADVANCE(self)
        self.zz_fdict['ANTSWITCHADVANCE'] = self.ANTSWITCHADVANCE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_PRSSEL(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_PRSSEL, self).__init__(rmio, label,
            0xb8034000, 0x084,
            'PRSSEL', 'HADM_NS.PRSSEL', 'read-write',
            u"",
            0x00000000, 0x0003FFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.DBGSEL = RM_Field_HADM_NS_PRSSEL_DBGSEL(self)
        self.zz_fdict['DBGSEL'] = self.DBGSEL
        self.RTTSEL = RM_Field_HADM_NS_PRSSEL_RTTSEL(self)
        self.zz_fdict['RTTSEL'] = self.RTTSEL
        self.PBRSEL = RM_Field_HADM_NS_PRSSEL_PBRSEL(self)
        self.zz_fdict['PBRSEL'] = self.PBRSEL
        self.RXSEL = RM_Field_HADM_NS_PRSSEL_RXSEL(self)
        self.zz_fdict['RXSEL'] = self.RXSEL
        self.TXSEL = RM_Field_HADM_NS_PRSSEL_TXSEL(self)
        self.zz_fdict['TXSEL'] = self.TXSEL
        self.CTRLSEL = RM_Field_HADM_NS_PRSSEL_CTRLSEL(self)
        self.zz_fdict['CTRLSEL'] = self.CTRLSEL
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RFECASEL(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RFECASEL, self).__init__(rmio, label,
            0xb8034000, 0x088,
            'RFECASEL', 'HADM_NS.RFECASEL', 'read-write',
            u"",
            0x00000000, 0x0000000F,
            0x00001000, 0x00002000,
            0x00003000)

        self.ECAMODESEL = RM_Field_HADM_NS_RFECASEL_ECAMODESEL(self)
        self.zz_fdict['ECAMODESEL'] = self.ECAMODESEL
        self.RESULTECASEL = RM_Field_HADM_NS_RFECASEL_RESULTECASEL(self)
        self.zz_fdict['RESULTECASEL'] = self.RESULTECASEL
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_NADMCONFIG(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_NADMCONFIG, self).__init__(rmio, label,
            0xb8034000, 0x0A4,
            'NADMCONFIG', 'HADM_NS.NADMCONFIG', 'read-write',
            u"",
            0x19180001, 0x3FFFFFFD,
            0x00001000, 0x00002000,
            0x00003000)

        self.NADMDIFFD = RM_Field_HADM_NS_NADMCONFIG_NADMDIFFD(self)
        self.zz_fdict['NADMDIFFD'] = self.NADMDIFFD
        self.RECREWINDSAMPLES = RM_Field_HADM_NS_NADMCONFIG_RECREWINDSAMPLES(self)
        self.zz_fdict['RECREWINDSAMPLES'] = self.RECREWINDSAMPLES
        self.REFMAPFSK = RM_Field_HADM_NS_NADMCONFIG_REFMAPFSK(self)
        self.zz_fdict['REFMAPFSK'] = self.REFMAPFSK
        self.FORCEFRAC = RM_Field_HADM_NS_NADMCONFIG_FORCEFRAC(self)
        self.zz_fdict['FORCEFRAC'] = self.FORCEFRAC
        self.FORCEDFRAC = RM_Field_HADM_NS_NADMCONFIG_FORCEDFRAC(self)
        self.zz_fdict['FORCEDFRAC'] = self.FORCEDFRAC
        self.SNRNUMFASTSAMPLES = RM_Field_HADM_NS_NADMCONFIG_SNRNUMFASTSAMPLES(self)
        self.zz_fdict['SNRNUMFASTSAMPLES'] = self.SNRNUMFASTSAMPLES
        self.SNRFASTCOEFF = RM_Field_HADM_NS_NADMCONFIG_SNRFASTCOEFF(self)
        self.zz_fdict['SNRFASTCOEFF'] = self.SNRFASTCOEFF
        self.SNRSLOWCOEFF = RM_Field_HADM_NS_NADMCONFIG_SNRSLOWCOEFF(self)
        self.zz_fdict['SNRSLOWCOEFF'] = self.SNRSLOWCOEFF
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_MSEPEARSONMASK(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_MSEPEARSONMASK, self).__init__(rmio, label,
            0xb8034000, 0x0A8,
            'MSEPEARSONMASK', 'HADM_NS.MSEPEARSONMASK', 'read-write',
            u"",
            0x0000000F, 0x0000000F,
            0x00001000, 0x00002000,
            0x00003000)

        self.MSEPEARSONMASK = RM_Field_HADM_NS_MSEPEARSONMASK_MSEPEARSONMASK(self)
        self.zz_fdict['MSEPEARSONMASK'] = self.MSEPEARSONMASK
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_DFTAMFREQ(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_DFTAMFREQ, self).__init__(rmio, label,
            0xb8034000, 0x0AC,
            'DFTAMFREQ', 'HADM_NS.DFTAMFREQ', 'read-write',
            u"",
            0x00000000, 0x000FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.DFTAMFREQ = RM_Field_HADM_NS_DFTAMFREQ_DFTAMFREQ(self)
        self.zz_fdict['DFTAMFREQ'] = self.DFTAMFREQ
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_DFTECLDFREQ(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_DFTECLDFREQ, self).__init__(rmio, label,
            0xb8034000, 0x0B0,
            'DFTECLDFREQ', 'HADM_NS.DFTECLDFREQ', 'read-write',
            u"",
            0x00000000, 0x000FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.DFTECLDFREQ = RM_Field_HADM_NS_DFTECLDFREQ_DFTECLDFREQ(self)
        self.zz_fdict['DFTECLDFREQ'] = self.DFTECLDFREQ
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG0, self).__init__(rmio, label,
            0xb8034000, 0x0B4,
            'REFGENCOEFFG0', 'HADM_NS.REFGENCOEFFG0', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF0 = RM_Field_HADM_NS_REFGENCOEFFG0_REFGENCOEFF0(self)
        self.zz_fdict['REFGENCOEFF0'] = self.REFGENCOEFF0
        self.REFGENCOEFF1 = RM_Field_HADM_NS_REFGENCOEFFG0_REFGENCOEFF1(self)
        self.zz_fdict['REFGENCOEFF1'] = self.REFGENCOEFF1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG1, self).__init__(rmio, label,
            0xb8034000, 0x0B8,
            'REFGENCOEFFG1', 'HADM_NS.REFGENCOEFFG1', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF2 = RM_Field_HADM_NS_REFGENCOEFFG1_REFGENCOEFF2(self)
        self.zz_fdict['REFGENCOEFF2'] = self.REFGENCOEFF2
        self.REFGENCOEFF3 = RM_Field_HADM_NS_REFGENCOEFFG1_REFGENCOEFF3(self)
        self.zz_fdict['REFGENCOEFF3'] = self.REFGENCOEFF3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG2(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG2, self).__init__(rmio, label,
            0xb8034000, 0x0BC,
            'REFGENCOEFFG2', 'HADM_NS.REFGENCOEFFG2', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF4 = RM_Field_HADM_NS_REFGENCOEFFG2_REFGENCOEFF4(self)
        self.zz_fdict['REFGENCOEFF4'] = self.REFGENCOEFF4
        self.REFGENCOEFF5 = RM_Field_HADM_NS_REFGENCOEFFG2_REFGENCOEFF5(self)
        self.zz_fdict['REFGENCOEFF5'] = self.REFGENCOEFF5
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG3(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG3, self).__init__(rmio, label,
            0xb8034000, 0x0C0,
            'REFGENCOEFFG3', 'HADM_NS.REFGENCOEFFG3', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF6 = RM_Field_HADM_NS_REFGENCOEFFG3_REFGENCOEFF6(self)
        self.zz_fdict['REFGENCOEFF6'] = self.REFGENCOEFF6
        self.REFGENCOEFF7 = RM_Field_HADM_NS_REFGENCOEFFG3_REFGENCOEFF7(self)
        self.zz_fdict['REFGENCOEFF7'] = self.REFGENCOEFF7
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG4(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG4, self).__init__(rmio, label,
            0xb8034000, 0x0C4,
            'REFGENCOEFFG4', 'HADM_NS.REFGENCOEFFG4', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF8 = RM_Field_HADM_NS_REFGENCOEFFG4_REFGENCOEFF8(self)
        self.zz_fdict['REFGENCOEFF8'] = self.REFGENCOEFF8
        self.REFGENCOEFF9 = RM_Field_HADM_NS_REFGENCOEFFG4_REFGENCOEFF9(self)
        self.zz_fdict['REFGENCOEFF9'] = self.REFGENCOEFF9
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG5(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG5, self).__init__(rmio, label,
            0xb8034000, 0x0C8,
            'REFGENCOEFFG5', 'HADM_NS.REFGENCOEFFG5', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF10 = RM_Field_HADM_NS_REFGENCOEFFG5_REFGENCOEFF10(self)
        self.zz_fdict['REFGENCOEFF10'] = self.REFGENCOEFF10
        self.REFGENCOEFF11 = RM_Field_HADM_NS_REFGENCOEFFG5_REFGENCOEFF11(self)
        self.zz_fdict['REFGENCOEFF11'] = self.REFGENCOEFF11
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG6(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG6, self).__init__(rmio, label,
            0xb8034000, 0x0CC,
            'REFGENCOEFFG6', 'HADM_NS.REFGENCOEFFG6', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF12 = RM_Field_HADM_NS_REFGENCOEFFG6_REFGENCOEFF12(self)
        self.zz_fdict['REFGENCOEFF12'] = self.REFGENCOEFF12
        self.REFGENCOEFF13 = RM_Field_HADM_NS_REFGENCOEFFG6_REFGENCOEFF13(self)
        self.zz_fdict['REFGENCOEFF13'] = self.REFGENCOEFF13
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG7(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG7, self).__init__(rmio, label,
            0xb8034000, 0x0D0,
            'REFGENCOEFFG7', 'HADM_NS.REFGENCOEFFG7', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF14 = RM_Field_HADM_NS_REFGENCOEFFG7_REFGENCOEFF14(self)
        self.zz_fdict['REFGENCOEFF14'] = self.REFGENCOEFF14
        self.REFGENCOEFF15 = RM_Field_HADM_NS_REFGENCOEFFG7_REFGENCOEFF15(self)
        self.zz_fdict['REFGENCOEFF15'] = self.REFGENCOEFF15
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG8(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG8, self).__init__(rmio, label,
            0xb8034000, 0x0D4,
            'REFGENCOEFFG8', 'HADM_NS.REFGENCOEFFG8', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF16 = RM_Field_HADM_NS_REFGENCOEFFG8_REFGENCOEFF16(self)
        self.zz_fdict['REFGENCOEFF16'] = self.REFGENCOEFF16
        self.REFGENCOEFF17 = RM_Field_HADM_NS_REFGENCOEFFG8_REFGENCOEFF17(self)
        self.zz_fdict['REFGENCOEFF17'] = self.REFGENCOEFF17
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG9(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG9, self).__init__(rmio, label,
            0xb8034000, 0x0D8,
            'REFGENCOEFFG9', 'HADM_NS.REFGENCOEFFG9', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF18 = RM_Field_HADM_NS_REFGENCOEFFG9_REFGENCOEFF18(self)
        self.zz_fdict['REFGENCOEFF18'] = self.REFGENCOEFF18
        self.REFGENCOEFF19 = RM_Field_HADM_NS_REFGENCOEFFG9_REFGENCOEFF19(self)
        self.zz_fdict['REFGENCOEFF19'] = self.REFGENCOEFF19
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG10(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG10, self).__init__(rmio, label,
            0xb8034000, 0x0DC,
            'REFGENCOEFFG10', 'HADM_NS.REFGENCOEFFG10', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF20 = RM_Field_HADM_NS_REFGENCOEFFG10_REFGENCOEFF20(self)
        self.zz_fdict['REFGENCOEFF20'] = self.REFGENCOEFF20
        self.REFGENCOEFF21 = RM_Field_HADM_NS_REFGENCOEFFG10_REFGENCOEFF21(self)
        self.zz_fdict['REFGENCOEFF21'] = self.REFGENCOEFF21
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG11(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG11, self).__init__(rmio, label,
            0xb8034000, 0x0E0,
            'REFGENCOEFFG11', 'HADM_NS.REFGENCOEFFG11', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF22 = RM_Field_HADM_NS_REFGENCOEFFG11_REFGENCOEFF22(self)
        self.zz_fdict['REFGENCOEFF22'] = self.REFGENCOEFF22
        self.REFGENCOEFF23 = RM_Field_HADM_NS_REFGENCOEFFG11_REFGENCOEFF23(self)
        self.zz_fdict['REFGENCOEFF23'] = self.REFGENCOEFF23
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG12(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG12, self).__init__(rmio, label,
            0xb8034000, 0x0E4,
            'REFGENCOEFFG12', 'HADM_NS.REFGENCOEFFG12', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF24 = RM_Field_HADM_NS_REFGENCOEFFG12_REFGENCOEFF24(self)
        self.zz_fdict['REFGENCOEFF24'] = self.REFGENCOEFF24
        self.REFGENCOEFF25 = RM_Field_HADM_NS_REFGENCOEFFG12_REFGENCOEFF25(self)
        self.zz_fdict['REFGENCOEFF25'] = self.REFGENCOEFF25
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG13(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG13, self).__init__(rmio, label,
            0xb8034000, 0x0E8,
            'REFGENCOEFFG13', 'HADM_NS.REFGENCOEFFG13', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF26 = RM_Field_HADM_NS_REFGENCOEFFG13_REFGENCOEFF26(self)
        self.zz_fdict['REFGENCOEFF26'] = self.REFGENCOEFF26
        self.REFGENCOEFF27 = RM_Field_HADM_NS_REFGENCOEFFG13_REFGENCOEFF27(self)
        self.zz_fdict['REFGENCOEFF27'] = self.REFGENCOEFF27
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG14(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG14, self).__init__(rmio, label,
            0xb8034000, 0x0EC,
            'REFGENCOEFFG14', 'HADM_NS.REFGENCOEFFG14', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF28 = RM_Field_HADM_NS_REFGENCOEFFG14_REFGENCOEFF28(self)
        self.zz_fdict['REFGENCOEFF28'] = self.REFGENCOEFF28
        self.REFGENCOEFF29 = RM_Field_HADM_NS_REFGENCOEFFG14_REFGENCOEFF29(self)
        self.zz_fdict['REFGENCOEFF29'] = self.REFGENCOEFF29
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_REFGENCOEFFG15(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_REFGENCOEFFG15, self).__init__(rmio, label,
            0xb8034000, 0x0F0,
            'REFGENCOEFFG15', 'HADM_NS.REFGENCOEFFG15', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.REFGENCOEFF30 = RM_Field_HADM_NS_REFGENCOEFFG15_REFGENCOEFF30(self)
        self.zz_fdict['REFGENCOEFF30'] = self.REFGENCOEFF30
        self.REFGENCOEFF31 = RM_Field_HADM_NS_REFGENCOEFFG15_REFGENCOEFF31(self)
        self.zz_fdict['REFGENCOEFF31'] = self.REFGENCOEFF31
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_SPARE(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_SPARE, self).__init__(rmio, label,
            0xb8034000, 0x0F4,
            'SPARE', 'HADM_NS.SPARE', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.SPARE = RM_Field_HADM_NS_SPARE_SPARE(self)
        self.zz_fdict['SPARE'] = self.SPARE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RESCTRL(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RESCTRL, self).__init__(rmio, label,
            0xb8034000, 0x0F8,
            'RESCTRL', 'HADM_NS.RESCTRL', 'read-write',
            u"",
            0x00000000, 0x0000003F,
            0x00001000, 0x00002000,
            0x00003000)

        self.SIZE = RM_Field_HADM_NS_RESCTRL_SIZE(self)
        self.zz_fdict['SIZE'] = self.SIZE
        self.BUFMODE = RM_Field_HADM_NS_RESCTRL_BUFMODE(self)
        self.zz_fdict['BUFMODE'] = self.BUFMODE
        self.DEBUGEN = RM_Field_HADM_NS_RESCTRL_DEBUGEN(self)
        self.zz_fdict['DEBUGEN'] = self.DEBUGEN
        self.NADMEN = RM_Field_HADM_NS_RESCTRL_NADMEN(self)
        self.zz_fdict['NADMEN'] = self.NADMEN
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_ADDR(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_ADDR, self).__init__(rmio, label,
            0xb8034000, 0x0FC,
            'ADDR', 'HADM_NS.ADDR', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFC,
            0x00001000, 0x00002000,
            0x00003000)

        self.ADDR = RM_Field_HADM_NS_ADDR_ADDR(self)
        self.zz_fdict['ADDR'] = self.ADDR
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RESSTATUS(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RESSTATUS, self).__init__(rmio, label,
            0xb8034000, 0x100,
            'RESSTATUS', 'HADM_NS.RESSTATUS', 'read-only',
            u"",
            0x00000000, 0x007FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.BYTES = RM_Field_HADM_NS_RESSTATUS_BYTES(self)
        self.zz_fdict['BYTES'] = self.BYTES
        self.STEPS = RM_Field_HADM_NS_RESSTATUS_STEPS(self)
        self.zz_fdict['STEPS'] = self.STEPS
        self.THRESHOLDFLAG = RM_Field_HADM_NS_RESSTATUS_THRESHOLDFLAG(self)
        self.zz_fdict['THRESHOLDFLAG'] = self.THRESHOLDFLAG
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_THRESHOLDCTRL(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_THRESHOLDCTRL, self).__init__(rmio, label,
            0xb8034000, 0x104,
            'THRESHOLDCTRL', 'HADM_NS.THRESHOLDCTRL', 'read-write',
            u"",
            0x00000000, 0x00003FFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.THRESHOLD = RM_Field_HADM_NS_THRESHOLDCTRL_THRESHOLD(self)
        self.zz_fdict['THRESHOLD'] = self.THRESHOLD
        self.THRESHOLDMODE = RM_Field_HADM_NS_THRESHOLDCTRL_THRESHOLDMODE(self)
        self.zz_fdict['THRESHOLDMODE'] = self.THRESHOLDMODE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_AHBCONFIG(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_AHBCONFIG, self).__init__(rmio, label,
            0xb8034000, 0x108,
            'AHBCONFIG', 'HADM_NS.AHBCONFIG', 'read-write',
            u"",
            0x00000000, 0x0000001F,
            0x00001000, 0x00002000,
            0x00003000)

        self.BUFFERABLE = RM_Field_HADM_NS_AHBCONFIG_BUFFERABLE(self)
        self.zz_fdict['BUFFERABLE'] = self.BUFFERABLE
        self.MODIFIABLE = RM_Field_HADM_NS_AHBCONFIG_MODIFIABLE(self)
        self.zz_fdict['MODIFIABLE'] = self.MODIFIABLE
        self.LOOKUP = RM_Field_HADM_NS_AHBCONFIG_LOOKUP(self)
        self.zz_fdict['LOOKUP'] = self.LOOKUP
        self.ALLOCATE = RM_Field_HADM_NS_AHBCONFIG_ALLOCATE(self)
        self.zz_fdict['ALLOCATE'] = self.ALLOCATE
        self.SHAREABLE = RM_Field_HADM_NS_AHBCONFIG_SHAREABLE(self)
        self.zz_fdict['SHAREABLE'] = self.SHAREABLE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_TASKCTRL0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_TASKCTRL0, self).__init__(rmio, label,
            0xb8034000, 0x10C,
            'TASKCTRL0', 'HADM_NS.TASKCTRL0', 'read-write',
            u"",
            0x00000000, 0x0003FFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.NEXTTASKNUM = RM_Field_HADM_NS_TASKCTRL0_NEXTTASKNUM(self)
        self.zz_fdict['NEXTTASKNUM'] = self.NEXTTASKNUM
        self.NEXTPRECNT = RM_Field_HADM_NS_TASKCTRL0_NEXTPRECNT(self)
        self.zz_fdict['NEXTPRECNT'] = self.NEXTPRECNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_TASKCTRL1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_TASKCTRL1, self).__init__(rmio, label,
            0xb8034000, 0x110,
            'TASKCTRL1', 'HADM_NS.TASKCTRL1', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.NEXTBASECNT = RM_Field_HADM_NS_TASKCTRL1_NEXTBASECNT(self)
        self.zz_fdict['NEXTBASECNT'] = self.NEXTBASECNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_TASKCTRL2(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_TASKCTRL2, self).__init__(rmio, label,
            0xb8034000, 0x114,
            'TASKCTRL2', 'HADM_NS.TASKCTRL2', 'read-write',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.NEXTWRAPCNT = RM_Field_HADM_NS_TASKCTRL2_NEXTWRAPCNT(self)
        self.zz_fdict['NEXTWRAPCNT'] = self.NEXTWRAPCNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_TASKCTRL3(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_TASKCTRL3, self).__init__(rmio, label,
            0xb8034000, 0x118,
            'TASKCTRL3', 'HADM_NS.TASKCTRL3', 'read-write',
            u"",
            0x80008000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.PRECNTEN = RM_Field_HADM_NS_TASKCTRL3_PRECNTEN(self)
        self.zz_fdict['PRECNTEN'] = self.PRECNTEN
        self.BASECNTEN = RM_Field_HADM_NS_TASKCTRL3_BASECNTEN(self)
        self.zz_fdict['BASECNTEN'] = self.BASECNTEN
        self.WRAPCNTEN = RM_Field_HADM_NS_TASKCTRL3_WRAPCNTEN(self)
        self.zz_fdict['WRAPCNTEN'] = self.WRAPCNTEN
        self.TIMEOUTOFFSET = RM_Field_HADM_NS_TASKCTRL3_TIMEOUTOFFSET(self)
        self.zz_fdict['TIMEOUTOFFSET'] = self.TIMEOUTOFFSET
        self.MAXQUEUE = RM_Field_HADM_NS_TASKCTRL3_MAXQUEUE(self)
        self.zz_fdict['MAXQUEUE'] = self.MAXQUEUE
        self.TIMERERRDIS = RM_Field_HADM_NS_TASKCTRL3_TIMERERRDIS(self)
        self.zz_fdict['TIMERERRDIS'] = self.TIMERERRDIS
        self.WRAPCNTWIN = RM_Field_HADM_NS_TASKCTRL3_WRAPCNTWIN(self)
        self.zz_fdict['WRAPCNTWIN'] = self.WRAPCNTWIN
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RESULTINSTR0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RESULTINSTR0, self).__init__(rmio, label,
            0xb8034000, 0x11C,
            'RESULTINSTR0', 'HADM_NS.RESULTINSTR0', 'read-write',
            u"",
            0x00000000, 0x00FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RES0 = RM_Field_HADM_NS_RESULTINSTR0_RES0(self)
        self.zz_fdict['RES0'] = self.RES0
        self.RES1 = RM_Field_HADM_NS_RESULTINSTR0_RES1(self)
        self.zz_fdict['RES1'] = self.RES1
        self.RES2 = RM_Field_HADM_NS_RESULTINSTR0_RES2(self)
        self.zz_fdict['RES2'] = self.RES2
        self.RES3 = RM_Field_HADM_NS_RESULTINSTR0_RES3(self)
        self.zz_fdict['RES3'] = self.RES3
        self.RES4 = RM_Field_HADM_NS_RESULTINSTR0_RES4(self)
        self.zz_fdict['RES4'] = self.RES4
        self.RES5 = RM_Field_HADM_NS_RESULTINSTR0_RES5(self)
        self.zz_fdict['RES5'] = self.RES5
        self.RES6 = RM_Field_HADM_NS_RESULTINSTR0_RES6(self)
        self.zz_fdict['RES6'] = self.RES6
        self.RES7 = RM_Field_HADM_NS_RESULTINSTR0_RES7(self)
        self.zz_fdict['RES7'] = self.RES7
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR00(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR00, self).__init__(rmio, label,
            0xb8034000, 0x120,
            'INSTR00', 'HADM_NS.INSTR00', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE0 = RM_Field_HADM_NS_INSTR00_ACTIVE0(self)
        self.zz_fdict['ACTIVE0'] = self.ACTIVE0
        self.RESETEN0 = RM_Field_HADM_NS_INSTR00_RESETEN0(self)
        self.zz_fdict['RESETEN0'] = self.RESETEN0
        self.PKTINFO0 = RM_Field_HADM_NS_INSTR00_PKTINFO0(self)
        self.zz_fdict['PKTINFO0'] = self.PKTINFO0
        self.FREQEST0 = RM_Field_HADM_NS_INSTR00_FREQEST0(self)
        self.zz_fdict['FREQEST0'] = self.FREQEST0
        self.RTT0 = RM_Field_HADM_NS_INSTR00_RTT0(self)
        self.zz_fdict['RTT0'] = self.RTT0
        self.NADM0 = RM_Field_HADM_NS_INSTR00_NADM0(self)
        self.zz_fdict['NADM0'] = self.NADM0
        self.PBR0 = RM_Field_HADM_NS_INSTR00_PBR0(self)
        self.zz_fdict['PBR0'] = self.PBR0
        self.PRECNTOFF0 = RM_Field_HADM_NS_INSTR00_PRECNTOFF0(self)
        self.zz_fdict['PRECNTOFF0'] = self.PRECNTOFF0
        self.BASEWRAPCNTOFF0 = RM_Field_HADM_NS_INSTR00_BASEWRAPCNTOFF0(self)
        self.zz_fdict['BASEWRAPCNTOFF0'] = self.BASEWRAPCNTOFF0
        self.TIMEOUT0 = RM_Field_HADM_NS_INSTR00_TIMEOUT0(self)
        self.zz_fdict['TIMEOUT0'] = self.TIMEOUT0
        self.STARTDONEIEN0 = RM_Field_HADM_NS_INSTR00_STARTDONEIEN0(self)
        self.zz_fdict['STARTDONEIEN0'] = self.STARTDONEIEN0
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR10(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR10, self).__init__(rmio, label,
            0xb8034000, 0x124,
            'INSTR10', 'HADM_NS.INSTR10', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE1 = RM_Field_HADM_NS_INSTR10_ACTIVE1(self)
        self.zz_fdict['ACTIVE1'] = self.ACTIVE1
        self.RESETEN1 = RM_Field_HADM_NS_INSTR10_RESETEN1(self)
        self.zz_fdict['RESETEN1'] = self.RESETEN1
        self.PKTINFO1 = RM_Field_HADM_NS_INSTR10_PKTINFO1(self)
        self.zz_fdict['PKTINFO1'] = self.PKTINFO1
        self.FREQEST1 = RM_Field_HADM_NS_INSTR10_FREQEST1(self)
        self.zz_fdict['FREQEST1'] = self.FREQEST1
        self.RTT1 = RM_Field_HADM_NS_INSTR10_RTT1(self)
        self.zz_fdict['RTT1'] = self.RTT1
        self.NADM1 = RM_Field_HADM_NS_INSTR10_NADM1(self)
        self.zz_fdict['NADM1'] = self.NADM1
        self.PBR1 = RM_Field_HADM_NS_INSTR10_PBR1(self)
        self.zz_fdict['PBR1'] = self.PBR1
        self.PRECNTOFF1 = RM_Field_HADM_NS_INSTR10_PRECNTOFF1(self)
        self.zz_fdict['PRECNTOFF1'] = self.PRECNTOFF1
        self.BASEWRAPCNTOFF1 = RM_Field_HADM_NS_INSTR10_BASEWRAPCNTOFF1(self)
        self.zz_fdict['BASEWRAPCNTOFF1'] = self.BASEWRAPCNTOFF1
        self.TIMEOUT1 = RM_Field_HADM_NS_INSTR10_TIMEOUT1(self)
        self.zz_fdict['TIMEOUT1'] = self.TIMEOUT1
        self.STARTDONEIEN1 = RM_Field_HADM_NS_INSTR10_STARTDONEIEN1(self)
        self.zz_fdict['STARTDONEIEN1'] = self.STARTDONEIEN1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR20(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR20, self).__init__(rmio, label,
            0xb8034000, 0x128,
            'INSTR20', 'HADM_NS.INSTR20', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE2 = RM_Field_HADM_NS_INSTR20_ACTIVE2(self)
        self.zz_fdict['ACTIVE2'] = self.ACTIVE2
        self.RESETEN2 = RM_Field_HADM_NS_INSTR20_RESETEN2(self)
        self.zz_fdict['RESETEN2'] = self.RESETEN2
        self.PKTINFO2 = RM_Field_HADM_NS_INSTR20_PKTINFO2(self)
        self.zz_fdict['PKTINFO2'] = self.PKTINFO2
        self.FREQEST2 = RM_Field_HADM_NS_INSTR20_FREQEST2(self)
        self.zz_fdict['FREQEST2'] = self.FREQEST2
        self.RTT2 = RM_Field_HADM_NS_INSTR20_RTT2(self)
        self.zz_fdict['RTT2'] = self.RTT2
        self.NADM2 = RM_Field_HADM_NS_INSTR20_NADM2(self)
        self.zz_fdict['NADM2'] = self.NADM2
        self.PBR2 = RM_Field_HADM_NS_INSTR20_PBR2(self)
        self.zz_fdict['PBR2'] = self.PBR2
        self.PRECNTOFF2 = RM_Field_HADM_NS_INSTR20_PRECNTOFF2(self)
        self.zz_fdict['PRECNTOFF2'] = self.PRECNTOFF2
        self.BASEWRAPCNTOFF2 = RM_Field_HADM_NS_INSTR20_BASEWRAPCNTOFF2(self)
        self.zz_fdict['BASEWRAPCNTOFF2'] = self.BASEWRAPCNTOFF2
        self.TIMEOUT2 = RM_Field_HADM_NS_INSTR20_TIMEOUT2(self)
        self.zz_fdict['TIMEOUT2'] = self.TIMEOUT2
        self.STARTDONEIEN2 = RM_Field_HADM_NS_INSTR20_STARTDONEIEN2(self)
        self.zz_fdict['STARTDONEIEN2'] = self.STARTDONEIEN2
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR30(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR30, self).__init__(rmio, label,
            0xb8034000, 0x12C,
            'INSTR30', 'HADM_NS.INSTR30', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE3 = RM_Field_HADM_NS_INSTR30_ACTIVE3(self)
        self.zz_fdict['ACTIVE3'] = self.ACTIVE3
        self.RESETEN3 = RM_Field_HADM_NS_INSTR30_RESETEN3(self)
        self.zz_fdict['RESETEN3'] = self.RESETEN3
        self.PKTINFO3 = RM_Field_HADM_NS_INSTR30_PKTINFO3(self)
        self.zz_fdict['PKTINFO3'] = self.PKTINFO3
        self.FREQEST3 = RM_Field_HADM_NS_INSTR30_FREQEST3(self)
        self.zz_fdict['FREQEST3'] = self.FREQEST3
        self.RTT3 = RM_Field_HADM_NS_INSTR30_RTT3(self)
        self.zz_fdict['RTT3'] = self.RTT3
        self.NADM3 = RM_Field_HADM_NS_INSTR30_NADM3(self)
        self.zz_fdict['NADM3'] = self.NADM3
        self.PBR3 = RM_Field_HADM_NS_INSTR30_PBR3(self)
        self.zz_fdict['PBR3'] = self.PBR3
        self.PRECNTOFF3 = RM_Field_HADM_NS_INSTR30_PRECNTOFF3(self)
        self.zz_fdict['PRECNTOFF3'] = self.PRECNTOFF3
        self.BASEWRAPCNTOFF3 = RM_Field_HADM_NS_INSTR30_BASEWRAPCNTOFF3(self)
        self.zz_fdict['BASEWRAPCNTOFF3'] = self.BASEWRAPCNTOFF3
        self.TIMEOUT3 = RM_Field_HADM_NS_INSTR30_TIMEOUT3(self)
        self.zz_fdict['TIMEOUT3'] = self.TIMEOUT3
        self.STARTDONEIEN3 = RM_Field_HADM_NS_INSTR30_STARTDONEIEN3(self)
        self.zz_fdict['STARTDONEIEN3'] = self.STARTDONEIEN3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR40(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR40, self).__init__(rmio, label,
            0xb8034000, 0x130,
            'INSTR40', 'HADM_NS.INSTR40', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE4 = RM_Field_HADM_NS_INSTR40_ACTIVE4(self)
        self.zz_fdict['ACTIVE4'] = self.ACTIVE4
        self.RESETEN4 = RM_Field_HADM_NS_INSTR40_RESETEN4(self)
        self.zz_fdict['RESETEN4'] = self.RESETEN4
        self.PKTINFO4 = RM_Field_HADM_NS_INSTR40_PKTINFO4(self)
        self.zz_fdict['PKTINFO4'] = self.PKTINFO4
        self.FREQEST4 = RM_Field_HADM_NS_INSTR40_FREQEST4(self)
        self.zz_fdict['FREQEST4'] = self.FREQEST4
        self.RTT4 = RM_Field_HADM_NS_INSTR40_RTT4(self)
        self.zz_fdict['RTT4'] = self.RTT4
        self.NADM4 = RM_Field_HADM_NS_INSTR40_NADM4(self)
        self.zz_fdict['NADM4'] = self.NADM4
        self.PBR4 = RM_Field_HADM_NS_INSTR40_PBR4(self)
        self.zz_fdict['PBR4'] = self.PBR4
        self.PRECNTOFF4 = RM_Field_HADM_NS_INSTR40_PRECNTOFF4(self)
        self.zz_fdict['PRECNTOFF4'] = self.PRECNTOFF4
        self.BASEWRAPCNTOFF4 = RM_Field_HADM_NS_INSTR40_BASEWRAPCNTOFF4(self)
        self.zz_fdict['BASEWRAPCNTOFF4'] = self.BASEWRAPCNTOFF4
        self.TIMEOUT4 = RM_Field_HADM_NS_INSTR40_TIMEOUT4(self)
        self.zz_fdict['TIMEOUT4'] = self.TIMEOUT4
        self.STARTDONEIEN4 = RM_Field_HADM_NS_INSTR40_STARTDONEIEN4(self)
        self.zz_fdict['STARTDONEIEN4'] = self.STARTDONEIEN4
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR50(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR50, self).__init__(rmio, label,
            0xb8034000, 0x134,
            'INSTR50', 'HADM_NS.INSTR50', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE5 = RM_Field_HADM_NS_INSTR50_ACTIVE5(self)
        self.zz_fdict['ACTIVE5'] = self.ACTIVE5
        self.RESETEN5 = RM_Field_HADM_NS_INSTR50_RESETEN5(self)
        self.zz_fdict['RESETEN5'] = self.RESETEN5
        self.PKTINFO5 = RM_Field_HADM_NS_INSTR50_PKTINFO5(self)
        self.zz_fdict['PKTINFO5'] = self.PKTINFO5
        self.FREQEST5 = RM_Field_HADM_NS_INSTR50_FREQEST5(self)
        self.zz_fdict['FREQEST5'] = self.FREQEST5
        self.RTT5 = RM_Field_HADM_NS_INSTR50_RTT5(self)
        self.zz_fdict['RTT5'] = self.RTT5
        self.NADM5 = RM_Field_HADM_NS_INSTR50_NADM5(self)
        self.zz_fdict['NADM5'] = self.NADM5
        self.PBR5 = RM_Field_HADM_NS_INSTR50_PBR5(self)
        self.zz_fdict['PBR5'] = self.PBR5
        self.PRECNTOFF5 = RM_Field_HADM_NS_INSTR50_PRECNTOFF5(self)
        self.zz_fdict['PRECNTOFF5'] = self.PRECNTOFF5
        self.BASEWRAPCNTOFF5 = RM_Field_HADM_NS_INSTR50_BASEWRAPCNTOFF5(self)
        self.zz_fdict['BASEWRAPCNTOFF5'] = self.BASEWRAPCNTOFF5
        self.TIMEOUT5 = RM_Field_HADM_NS_INSTR50_TIMEOUT5(self)
        self.zz_fdict['TIMEOUT5'] = self.TIMEOUT5
        self.STARTDONEIEN5 = RM_Field_HADM_NS_INSTR50_STARTDONEIEN5(self)
        self.zz_fdict['STARTDONEIEN5'] = self.STARTDONEIEN5
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR60(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR60, self).__init__(rmio, label,
            0xb8034000, 0x138,
            'INSTR60', 'HADM_NS.INSTR60', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE6 = RM_Field_HADM_NS_INSTR60_ACTIVE6(self)
        self.zz_fdict['ACTIVE6'] = self.ACTIVE6
        self.RESETEN6 = RM_Field_HADM_NS_INSTR60_RESETEN6(self)
        self.zz_fdict['RESETEN6'] = self.RESETEN6
        self.PKTINFO6 = RM_Field_HADM_NS_INSTR60_PKTINFO6(self)
        self.zz_fdict['PKTINFO6'] = self.PKTINFO6
        self.FREQEST6 = RM_Field_HADM_NS_INSTR60_FREQEST6(self)
        self.zz_fdict['FREQEST6'] = self.FREQEST6
        self.RTT6 = RM_Field_HADM_NS_INSTR60_RTT6(self)
        self.zz_fdict['RTT6'] = self.RTT6
        self.NADM6 = RM_Field_HADM_NS_INSTR60_NADM6(self)
        self.zz_fdict['NADM6'] = self.NADM6
        self.PBR6 = RM_Field_HADM_NS_INSTR60_PBR6(self)
        self.zz_fdict['PBR6'] = self.PBR6
        self.PRECNTOFF6 = RM_Field_HADM_NS_INSTR60_PRECNTOFF6(self)
        self.zz_fdict['PRECNTOFF6'] = self.PRECNTOFF6
        self.BASEWRAPCNTOFF6 = RM_Field_HADM_NS_INSTR60_BASEWRAPCNTOFF6(self)
        self.zz_fdict['BASEWRAPCNTOFF6'] = self.BASEWRAPCNTOFF6
        self.TIMEOUT6 = RM_Field_HADM_NS_INSTR60_TIMEOUT6(self)
        self.zz_fdict['TIMEOUT6'] = self.TIMEOUT6
        self.STARTDONEIEN6 = RM_Field_HADM_NS_INSTR60_STARTDONEIEN6(self)
        self.zz_fdict['STARTDONEIEN6'] = self.STARTDONEIEN6
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RESULTINSTR1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RESULTINSTR1, self).__init__(rmio, label,
            0xb8034000, 0x13C,
            'RESULTINSTR1', 'HADM_NS.RESULTINSTR1', 'read-write',
            u"",
            0x00000000, 0x00FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RES0 = RM_Field_HADM_NS_RESULTINSTR1_RES0(self)
        self.zz_fdict['RES0'] = self.RES0
        self.RES1 = RM_Field_HADM_NS_RESULTINSTR1_RES1(self)
        self.zz_fdict['RES1'] = self.RES1
        self.RES2 = RM_Field_HADM_NS_RESULTINSTR1_RES2(self)
        self.zz_fdict['RES2'] = self.RES2
        self.RES3 = RM_Field_HADM_NS_RESULTINSTR1_RES3(self)
        self.zz_fdict['RES3'] = self.RES3
        self.RES4 = RM_Field_HADM_NS_RESULTINSTR1_RES4(self)
        self.zz_fdict['RES4'] = self.RES4
        self.RES5 = RM_Field_HADM_NS_RESULTINSTR1_RES5(self)
        self.zz_fdict['RES5'] = self.RES5
        self.RES6 = RM_Field_HADM_NS_RESULTINSTR1_RES6(self)
        self.zz_fdict['RES6'] = self.RES6
        self.RES7 = RM_Field_HADM_NS_RESULTINSTR1_RES7(self)
        self.zz_fdict['RES7'] = self.RES7
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR01(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR01, self).__init__(rmio, label,
            0xb8034000, 0x140,
            'INSTR01', 'HADM_NS.INSTR01', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE0 = RM_Field_HADM_NS_INSTR01_ACTIVE0(self)
        self.zz_fdict['ACTIVE0'] = self.ACTIVE0
        self.RESETEN0 = RM_Field_HADM_NS_INSTR01_RESETEN0(self)
        self.zz_fdict['RESETEN0'] = self.RESETEN0
        self.PKTINFO0 = RM_Field_HADM_NS_INSTR01_PKTINFO0(self)
        self.zz_fdict['PKTINFO0'] = self.PKTINFO0
        self.FREQEST0 = RM_Field_HADM_NS_INSTR01_FREQEST0(self)
        self.zz_fdict['FREQEST0'] = self.FREQEST0
        self.RTT0 = RM_Field_HADM_NS_INSTR01_RTT0(self)
        self.zz_fdict['RTT0'] = self.RTT0
        self.NADM0 = RM_Field_HADM_NS_INSTR01_NADM0(self)
        self.zz_fdict['NADM0'] = self.NADM0
        self.PBR0 = RM_Field_HADM_NS_INSTR01_PBR0(self)
        self.zz_fdict['PBR0'] = self.PBR0
        self.PRECNTOFF0 = RM_Field_HADM_NS_INSTR01_PRECNTOFF0(self)
        self.zz_fdict['PRECNTOFF0'] = self.PRECNTOFF0
        self.BASEWRAPCNTOFF0 = RM_Field_HADM_NS_INSTR01_BASEWRAPCNTOFF0(self)
        self.zz_fdict['BASEWRAPCNTOFF0'] = self.BASEWRAPCNTOFF0
        self.TIMEOUT0 = RM_Field_HADM_NS_INSTR01_TIMEOUT0(self)
        self.zz_fdict['TIMEOUT0'] = self.TIMEOUT0
        self.STARTDONEIEN0 = RM_Field_HADM_NS_INSTR01_STARTDONEIEN0(self)
        self.zz_fdict['STARTDONEIEN0'] = self.STARTDONEIEN0
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR11(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR11, self).__init__(rmio, label,
            0xb8034000, 0x144,
            'INSTR11', 'HADM_NS.INSTR11', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE1 = RM_Field_HADM_NS_INSTR11_ACTIVE1(self)
        self.zz_fdict['ACTIVE1'] = self.ACTIVE1
        self.RESETEN1 = RM_Field_HADM_NS_INSTR11_RESETEN1(self)
        self.zz_fdict['RESETEN1'] = self.RESETEN1
        self.PKTINFO1 = RM_Field_HADM_NS_INSTR11_PKTINFO1(self)
        self.zz_fdict['PKTINFO1'] = self.PKTINFO1
        self.FREQEST1 = RM_Field_HADM_NS_INSTR11_FREQEST1(self)
        self.zz_fdict['FREQEST1'] = self.FREQEST1
        self.RTT1 = RM_Field_HADM_NS_INSTR11_RTT1(self)
        self.zz_fdict['RTT1'] = self.RTT1
        self.NADM1 = RM_Field_HADM_NS_INSTR11_NADM1(self)
        self.zz_fdict['NADM1'] = self.NADM1
        self.PBR1 = RM_Field_HADM_NS_INSTR11_PBR1(self)
        self.zz_fdict['PBR1'] = self.PBR1
        self.PRECNTOFF1 = RM_Field_HADM_NS_INSTR11_PRECNTOFF1(self)
        self.zz_fdict['PRECNTOFF1'] = self.PRECNTOFF1
        self.BASEWRAPCNTOFF1 = RM_Field_HADM_NS_INSTR11_BASEWRAPCNTOFF1(self)
        self.zz_fdict['BASEWRAPCNTOFF1'] = self.BASEWRAPCNTOFF1
        self.TIMEOUT1 = RM_Field_HADM_NS_INSTR11_TIMEOUT1(self)
        self.zz_fdict['TIMEOUT1'] = self.TIMEOUT1
        self.STARTDONEIEN1 = RM_Field_HADM_NS_INSTR11_STARTDONEIEN1(self)
        self.zz_fdict['STARTDONEIEN1'] = self.STARTDONEIEN1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR21(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR21, self).__init__(rmio, label,
            0xb8034000, 0x148,
            'INSTR21', 'HADM_NS.INSTR21', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE2 = RM_Field_HADM_NS_INSTR21_ACTIVE2(self)
        self.zz_fdict['ACTIVE2'] = self.ACTIVE2
        self.RESETEN2 = RM_Field_HADM_NS_INSTR21_RESETEN2(self)
        self.zz_fdict['RESETEN2'] = self.RESETEN2
        self.PKTINFO2 = RM_Field_HADM_NS_INSTR21_PKTINFO2(self)
        self.zz_fdict['PKTINFO2'] = self.PKTINFO2
        self.FREQEST2 = RM_Field_HADM_NS_INSTR21_FREQEST2(self)
        self.zz_fdict['FREQEST2'] = self.FREQEST2
        self.RTT2 = RM_Field_HADM_NS_INSTR21_RTT2(self)
        self.zz_fdict['RTT2'] = self.RTT2
        self.NADM2 = RM_Field_HADM_NS_INSTR21_NADM2(self)
        self.zz_fdict['NADM2'] = self.NADM2
        self.PBR2 = RM_Field_HADM_NS_INSTR21_PBR2(self)
        self.zz_fdict['PBR2'] = self.PBR2
        self.PRECNTOFF2 = RM_Field_HADM_NS_INSTR21_PRECNTOFF2(self)
        self.zz_fdict['PRECNTOFF2'] = self.PRECNTOFF2
        self.BASEWRAPCNTOFF2 = RM_Field_HADM_NS_INSTR21_BASEWRAPCNTOFF2(self)
        self.zz_fdict['BASEWRAPCNTOFF2'] = self.BASEWRAPCNTOFF2
        self.TIMEOUT2 = RM_Field_HADM_NS_INSTR21_TIMEOUT2(self)
        self.zz_fdict['TIMEOUT2'] = self.TIMEOUT2
        self.STARTDONEIEN2 = RM_Field_HADM_NS_INSTR21_STARTDONEIEN2(self)
        self.zz_fdict['STARTDONEIEN2'] = self.STARTDONEIEN2
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR31(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR31, self).__init__(rmio, label,
            0xb8034000, 0x14C,
            'INSTR31', 'HADM_NS.INSTR31', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE3 = RM_Field_HADM_NS_INSTR31_ACTIVE3(self)
        self.zz_fdict['ACTIVE3'] = self.ACTIVE3
        self.RESETEN3 = RM_Field_HADM_NS_INSTR31_RESETEN3(self)
        self.zz_fdict['RESETEN3'] = self.RESETEN3
        self.PKTINFO3 = RM_Field_HADM_NS_INSTR31_PKTINFO3(self)
        self.zz_fdict['PKTINFO3'] = self.PKTINFO3
        self.FREQEST3 = RM_Field_HADM_NS_INSTR31_FREQEST3(self)
        self.zz_fdict['FREQEST3'] = self.FREQEST3
        self.RTT3 = RM_Field_HADM_NS_INSTR31_RTT3(self)
        self.zz_fdict['RTT3'] = self.RTT3
        self.NADM3 = RM_Field_HADM_NS_INSTR31_NADM3(self)
        self.zz_fdict['NADM3'] = self.NADM3
        self.PBR3 = RM_Field_HADM_NS_INSTR31_PBR3(self)
        self.zz_fdict['PBR3'] = self.PBR3
        self.PRECNTOFF3 = RM_Field_HADM_NS_INSTR31_PRECNTOFF3(self)
        self.zz_fdict['PRECNTOFF3'] = self.PRECNTOFF3
        self.BASEWRAPCNTOFF3 = RM_Field_HADM_NS_INSTR31_BASEWRAPCNTOFF3(self)
        self.zz_fdict['BASEWRAPCNTOFF3'] = self.BASEWRAPCNTOFF3
        self.TIMEOUT3 = RM_Field_HADM_NS_INSTR31_TIMEOUT3(self)
        self.zz_fdict['TIMEOUT3'] = self.TIMEOUT3
        self.STARTDONEIEN3 = RM_Field_HADM_NS_INSTR31_STARTDONEIEN3(self)
        self.zz_fdict['STARTDONEIEN3'] = self.STARTDONEIEN3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR41(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR41, self).__init__(rmio, label,
            0xb8034000, 0x150,
            'INSTR41', 'HADM_NS.INSTR41', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE4 = RM_Field_HADM_NS_INSTR41_ACTIVE4(self)
        self.zz_fdict['ACTIVE4'] = self.ACTIVE4
        self.RESETEN4 = RM_Field_HADM_NS_INSTR41_RESETEN4(self)
        self.zz_fdict['RESETEN4'] = self.RESETEN4
        self.PKTINFO4 = RM_Field_HADM_NS_INSTR41_PKTINFO4(self)
        self.zz_fdict['PKTINFO4'] = self.PKTINFO4
        self.FREQEST4 = RM_Field_HADM_NS_INSTR41_FREQEST4(self)
        self.zz_fdict['FREQEST4'] = self.FREQEST4
        self.RTT4 = RM_Field_HADM_NS_INSTR41_RTT4(self)
        self.zz_fdict['RTT4'] = self.RTT4
        self.NADM4 = RM_Field_HADM_NS_INSTR41_NADM4(self)
        self.zz_fdict['NADM4'] = self.NADM4
        self.PBR4 = RM_Field_HADM_NS_INSTR41_PBR4(self)
        self.zz_fdict['PBR4'] = self.PBR4
        self.PRECNTOFF4 = RM_Field_HADM_NS_INSTR41_PRECNTOFF4(self)
        self.zz_fdict['PRECNTOFF4'] = self.PRECNTOFF4
        self.BASEWRAPCNTOFF4 = RM_Field_HADM_NS_INSTR41_BASEWRAPCNTOFF4(self)
        self.zz_fdict['BASEWRAPCNTOFF4'] = self.BASEWRAPCNTOFF4
        self.TIMEOUT4 = RM_Field_HADM_NS_INSTR41_TIMEOUT4(self)
        self.zz_fdict['TIMEOUT4'] = self.TIMEOUT4
        self.STARTDONEIEN4 = RM_Field_HADM_NS_INSTR41_STARTDONEIEN4(self)
        self.zz_fdict['STARTDONEIEN4'] = self.STARTDONEIEN4
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR51(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR51, self).__init__(rmio, label,
            0xb8034000, 0x154,
            'INSTR51', 'HADM_NS.INSTR51', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE5 = RM_Field_HADM_NS_INSTR51_ACTIVE5(self)
        self.zz_fdict['ACTIVE5'] = self.ACTIVE5
        self.RESETEN5 = RM_Field_HADM_NS_INSTR51_RESETEN5(self)
        self.zz_fdict['RESETEN5'] = self.RESETEN5
        self.PKTINFO5 = RM_Field_HADM_NS_INSTR51_PKTINFO5(self)
        self.zz_fdict['PKTINFO5'] = self.PKTINFO5
        self.FREQEST5 = RM_Field_HADM_NS_INSTR51_FREQEST5(self)
        self.zz_fdict['FREQEST5'] = self.FREQEST5
        self.RTT5 = RM_Field_HADM_NS_INSTR51_RTT5(self)
        self.zz_fdict['RTT5'] = self.RTT5
        self.NADM5 = RM_Field_HADM_NS_INSTR51_NADM5(self)
        self.zz_fdict['NADM5'] = self.NADM5
        self.PBR5 = RM_Field_HADM_NS_INSTR51_PBR5(self)
        self.zz_fdict['PBR5'] = self.PBR5
        self.PRECNTOFF5 = RM_Field_HADM_NS_INSTR51_PRECNTOFF5(self)
        self.zz_fdict['PRECNTOFF5'] = self.PRECNTOFF5
        self.BASEWRAPCNTOFF5 = RM_Field_HADM_NS_INSTR51_BASEWRAPCNTOFF5(self)
        self.zz_fdict['BASEWRAPCNTOFF5'] = self.BASEWRAPCNTOFF5
        self.TIMEOUT5 = RM_Field_HADM_NS_INSTR51_TIMEOUT5(self)
        self.zz_fdict['TIMEOUT5'] = self.TIMEOUT5
        self.STARTDONEIEN5 = RM_Field_HADM_NS_INSTR51_STARTDONEIEN5(self)
        self.zz_fdict['STARTDONEIEN5'] = self.STARTDONEIEN5
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR61(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR61, self).__init__(rmio, label,
            0xb8034000, 0x158,
            'INSTR61', 'HADM_NS.INSTR61', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE6 = RM_Field_HADM_NS_INSTR61_ACTIVE6(self)
        self.zz_fdict['ACTIVE6'] = self.ACTIVE6
        self.RESETEN6 = RM_Field_HADM_NS_INSTR61_RESETEN6(self)
        self.zz_fdict['RESETEN6'] = self.RESETEN6
        self.PKTINFO6 = RM_Field_HADM_NS_INSTR61_PKTINFO6(self)
        self.zz_fdict['PKTINFO6'] = self.PKTINFO6
        self.FREQEST6 = RM_Field_HADM_NS_INSTR61_FREQEST6(self)
        self.zz_fdict['FREQEST6'] = self.FREQEST6
        self.RTT6 = RM_Field_HADM_NS_INSTR61_RTT6(self)
        self.zz_fdict['RTT6'] = self.RTT6
        self.NADM6 = RM_Field_HADM_NS_INSTR61_NADM6(self)
        self.zz_fdict['NADM6'] = self.NADM6
        self.PBR6 = RM_Field_HADM_NS_INSTR61_PBR6(self)
        self.zz_fdict['PBR6'] = self.PBR6
        self.PRECNTOFF6 = RM_Field_HADM_NS_INSTR61_PRECNTOFF6(self)
        self.zz_fdict['PRECNTOFF6'] = self.PRECNTOFF6
        self.BASEWRAPCNTOFF6 = RM_Field_HADM_NS_INSTR61_BASEWRAPCNTOFF6(self)
        self.zz_fdict['BASEWRAPCNTOFF6'] = self.BASEWRAPCNTOFF6
        self.TIMEOUT6 = RM_Field_HADM_NS_INSTR61_TIMEOUT6(self)
        self.zz_fdict['TIMEOUT6'] = self.TIMEOUT6
        self.STARTDONEIEN6 = RM_Field_HADM_NS_INSTR61_STARTDONEIEN6(self)
        self.zz_fdict['STARTDONEIEN6'] = self.STARTDONEIEN6
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RESULTINSTR2(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RESULTINSTR2, self).__init__(rmio, label,
            0xb8034000, 0x15C,
            'RESULTINSTR2', 'HADM_NS.RESULTINSTR2', 'read-write',
            u"",
            0x00000000, 0x00FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RES0 = RM_Field_HADM_NS_RESULTINSTR2_RES0(self)
        self.zz_fdict['RES0'] = self.RES0
        self.RES1 = RM_Field_HADM_NS_RESULTINSTR2_RES1(self)
        self.zz_fdict['RES1'] = self.RES1
        self.RES2 = RM_Field_HADM_NS_RESULTINSTR2_RES2(self)
        self.zz_fdict['RES2'] = self.RES2
        self.RES3 = RM_Field_HADM_NS_RESULTINSTR2_RES3(self)
        self.zz_fdict['RES3'] = self.RES3
        self.RES4 = RM_Field_HADM_NS_RESULTINSTR2_RES4(self)
        self.zz_fdict['RES4'] = self.RES4
        self.RES5 = RM_Field_HADM_NS_RESULTINSTR2_RES5(self)
        self.zz_fdict['RES5'] = self.RES5
        self.RES6 = RM_Field_HADM_NS_RESULTINSTR2_RES6(self)
        self.zz_fdict['RES6'] = self.RES6
        self.RES7 = RM_Field_HADM_NS_RESULTINSTR2_RES7(self)
        self.zz_fdict['RES7'] = self.RES7
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR02(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR02, self).__init__(rmio, label,
            0xb8034000, 0x160,
            'INSTR02', 'HADM_NS.INSTR02', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE0 = RM_Field_HADM_NS_INSTR02_ACTIVE0(self)
        self.zz_fdict['ACTIVE0'] = self.ACTIVE0
        self.RESETEN0 = RM_Field_HADM_NS_INSTR02_RESETEN0(self)
        self.zz_fdict['RESETEN0'] = self.RESETEN0
        self.PKTINFO0 = RM_Field_HADM_NS_INSTR02_PKTINFO0(self)
        self.zz_fdict['PKTINFO0'] = self.PKTINFO0
        self.FREQEST0 = RM_Field_HADM_NS_INSTR02_FREQEST0(self)
        self.zz_fdict['FREQEST0'] = self.FREQEST0
        self.RTT0 = RM_Field_HADM_NS_INSTR02_RTT0(self)
        self.zz_fdict['RTT0'] = self.RTT0
        self.NADM0 = RM_Field_HADM_NS_INSTR02_NADM0(self)
        self.zz_fdict['NADM0'] = self.NADM0
        self.PBR0 = RM_Field_HADM_NS_INSTR02_PBR0(self)
        self.zz_fdict['PBR0'] = self.PBR0
        self.PRECNTOFF0 = RM_Field_HADM_NS_INSTR02_PRECNTOFF0(self)
        self.zz_fdict['PRECNTOFF0'] = self.PRECNTOFF0
        self.BASEWRAPCNTOFF0 = RM_Field_HADM_NS_INSTR02_BASEWRAPCNTOFF0(self)
        self.zz_fdict['BASEWRAPCNTOFF0'] = self.BASEWRAPCNTOFF0
        self.TIMEOUT0 = RM_Field_HADM_NS_INSTR02_TIMEOUT0(self)
        self.zz_fdict['TIMEOUT0'] = self.TIMEOUT0
        self.STARTDONEIEN0 = RM_Field_HADM_NS_INSTR02_STARTDONEIEN0(self)
        self.zz_fdict['STARTDONEIEN0'] = self.STARTDONEIEN0
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR12(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR12, self).__init__(rmio, label,
            0xb8034000, 0x164,
            'INSTR12', 'HADM_NS.INSTR12', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE1 = RM_Field_HADM_NS_INSTR12_ACTIVE1(self)
        self.zz_fdict['ACTIVE1'] = self.ACTIVE1
        self.RESETEN1 = RM_Field_HADM_NS_INSTR12_RESETEN1(self)
        self.zz_fdict['RESETEN1'] = self.RESETEN1
        self.PKTINFO1 = RM_Field_HADM_NS_INSTR12_PKTINFO1(self)
        self.zz_fdict['PKTINFO1'] = self.PKTINFO1
        self.FREQEST1 = RM_Field_HADM_NS_INSTR12_FREQEST1(self)
        self.zz_fdict['FREQEST1'] = self.FREQEST1
        self.RTT1 = RM_Field_HADM_NS_INSTR12_RTT1(self)
        self.zz_fdict['RTT1'] = self.RTT1
        self.NADM1 = RM_Field_HADM_NS_INSTR12_NADM1(self)
        self.zz_fdict['NADM1'] = self.NADM1
        self.PBR1 = RM_Field_HADM_NS_INSTR12_PBR1(self)
        self.zz_fdict['PBR1'] = self.PBR1
        self.PRECNTOFF1 = RM_Field_HADM_NS_INSTR12_PRECNTOFF1(self)
        self.zz_fdict['PRECNTOFF1'] = self.PRECNTOFF1
        self.BASEWRAPCNTOFF1 = RM_Field_HADM_NS_INSTR12_BASEWRAPCNTOFF1(self)
        self.zz_fdict['BASEWRAPCNTOFF1'] = self.BASEWRAPCNTOFF1
        self.TIMEOUT1 = RM_Field_HADM_NS_INSTR12_TIMEOUT1(self)
        self.zz_fdict['TIMEOUT1'] = self.TIMEOUT1
        self.STARTDONEIEN1 = RM_Field_HADM_NS_INSTR12_STARTDONEIEN1(self)
        self.zz_fdict['STARTDONEIEN1'] = self.STARTDONEIEN1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR22(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR22, self).__init__(rmio, label,
            0xb8034000, 0x168,
            'INSTR22', 'HADM_NS.INSTR22', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE2 = RM_Field_HADM_NS_INSTR22_ACTIVE2(self)
        self.zz_fdict['ACTIVE2'] = self.ACTIVE2
        self.RESETEN2 = RM_Field_HADM_NS_INSTR22_RESETEN2(self)
        self.zz_fdict['RESETEN2'] = self.RESETEN2
        self.PKTINFO2 = RM_Field_HADM_NS_INSTR22_PKTINFO2(self)
        self.zz_fdict['PKTINFO2'] = self.PKTINFO2
        self.FREQEST2 = RM_Field_HADM_NS_INSTR22_FREQEST2(self)
        self.zz_fdict['FREQEST2'] = self.FREQEST2
        self.RTT2 = RM_Field_HADM_NS_INSTR22_RTT2(self)
        self.zz_fdict['RTT2'] = self.RTT2
        self.NADM2 = RM_Field_HADM_NS_INSTR22_NADM2(self)
        self.zz_fdict['NADM2'] = self.NADM2
        self.PBR2 = RM_Field_HADM_NS_INSTR22_PBR2(self)
        self.zz_fdict['PBR2'] = self.PBR2
        self.PRECNTOFF2 = RM_Field_HADM_NS_INSTR22_PRECNTOFF2(self)
        self.zz_fdict['PRECNTOFF2'] = self.PRECNTOFF2
        self.BASEWRAPCNTOFF2 = RM_Field_HADM_NS_INSTR22_BASEWRAPCNTOFF2(self)
        self.zz_fdict['BASEWRAPCNTOFF2'] = self.BASEWRAPCNTOFF2
        self.TIMEOUT2 = RM_Field_HADM_NS_INSTR22_TIMEOUT2(self)
        self.zz_fdict['TIMEOUT2'] = self.TIMEOUT2
        self.STARTDONEIEN2 = RM_Field_HADM_NS_INSTR22_STARTDONEIEN2(self)
        self.zz_fdict['STARTDONEIEN2'] = self.STARTDONEIEN2
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR32(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR32, self).__init__(rmio, label,
            0xb8034000, 0x16C,
            'INSTR32', 'HADM_NS.INSTR32', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE3 = RM_Field_HADM_NS_INSTR32_ACTIVE3(self)
        self.zz_fdict['ACTIVE3'] = self.ACTIVE3
        self.RESETEN3 = RM_Field_HADM_NS_INSTR32_RESETEN3(self)
        self.zz_fdict['RESETEN3'] = self.RESETEN3
        self.PKTINFO3 = RM_Field_HADM_NS_INSTR32_PKTINFO3(self)
        self.zz_fdict['PKTINFO3'] = self.PKTINFO3
        self.FREQEST3 = RM_Field_HADM_NS_INSTR32_FREQEST3(self)
        self.zz_fdict['FREQEST3'] = self.FREQEST3
        self.RTT3 = RM_Field_HADM_NS_INSTR32_RTT3(self)
        self.zz_fdict['RTT3'] = self.RTT3
        self.NADM3 = RM_Field_HADM_NS_INSTR32_NADM3(self)
        self.zz_fdict['NADM3'] = self.NADM3
        self.PBR3 = RM_Field_HADM_NS_INSTR32_PBR3(self)
        self.zz_fdict['PBR3'] = self.PBR3
        self.PRECNTOFF3 = RM_Field_HADM_NS_INSTR32_PRECNTOFF3(self)
        self.zz_fdict['PRECNTOFF3'] = self.PRECNTOFF3
        self.BASEWRAPCNTOFF3 = RM_Field_HADM_NS_INSTR32_BASEWRAPCNTOFF3(self)
        self.zz_fdict['BASEWRAPCNTOFF3'] = self.BASEWRAPCNTOFF3
        self.TIMEOUT3 = RM_Field_HADM_NS_INSTR32_TIMEOUT3(self)
        self.zz_fdict['TIMEOUT3'] = self.TIMEOUT3
        self.STARTDONEIEN3 = RM_Field_HADM_NS_INSTR32_STARTDONEIEN3(self)
        self.zz_fdict['STARTDONEIEN3'] = self.STARTDONEIEN3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR42(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR42, self).__init__(rmio, label,
            0xb8034000, 0x170,
            'INSTR42', 'HADM_NS.INSTR42', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE4 = RM_Field_HADM_NS_INSTR42_ACTIVE4(self)
        self.zz_fdict['ACTIVE4'] = self.ACTIVE4
        self.RESETEN4 = RM_Field_HADM_NS_INSTR42_RESETEN4(self)
        self.zz_fdict['RESETEN4'] = self.RESETEN4
        self.PKTINFO4 = RM_Field_HADM_NS_INSTR42_PKTINFO4(self)
        self.zz_fdict['PKTINFO4'] = self.PKTINFO4
        self.FREQEST4 = RM_Field_HADM_NS_INSTR42_FREQEST4(self)
        self.zz_fdict['FREQEST4'] = self.FREQEST4
        self.RTT4 = RM_Field_HADM_NS_INSTR42_RTT4(self)
        self.zz_fdict['RTT4'] = self.RTT4
        self.NADM4 = RM_Field_HADM_NS_INSTR42_NADM4(self)
        self.zz_fdict['NADM4'] = self.NADM4
        self.PBR4 = RM_Field_HADM_NS_INSTR42_PBR4(self)
        self.zz_fdict['PBR4'] = self.PBR4
        self.PRECNTOFF4 = RM_Field_HADM_NS_INSTR42_PRECNTOFF4(self)
        self.zz_fdict['PRECNTOFF4'] = self.PRECNTOFF4
        self.BASEWRAPCNTOFF4 = RM_Field_HADM_NS_INSTR42_BASEWRAPCNTOFF4(self)
        self.zz_fdict['BASEWRAPCNTOFF4'] = self.BASEWRAPCNTOFF4
        self.TIMEOUT4 = RM_Field_HADM_NS_INSTR42_TIMEOUT4(self)
        self.zz_fdict['TIMEOUT4'] = self.TIMEOUT4
        self.STARTDONEIEN4 = RM_Field_HADM_NS_INSTR42_STARTDONEIEN4(self)
        self.zz_fdict['STARTDONEIEN4'] = self.STARTDONEIEN4
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR52(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR52, self).__init__(rmio, label,
            0xb8034000, 0x174,
            'INSTR52', 'HADM_NS.INSTR52', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE5 = RM_Field_HADM_NS_INSTR52_ACTIVE5(self)
        self.zz_fdict['ACTIVE5'] = self.ACTIVE5
        self.RESETEN5 = RM_Field_HADM_NS_INSTR52_RESETEN5(self)
        self.zz_fdict['RESETEN5'] = self.RESETEN5
        self.PKTINFO5 = RM_Field_HADM_NS_INSTR52_PKTINFO5(self)
        self.zz_fdict['PKTINFO5'] = self.PKTINFO5
        self.FREQEST5 = RM_Field_HADM_NS_INSTR52_FREQEST5(self)
        self.zz_fdict['FREQEST5'] = self.FREQEST5
        self.RTT5 = RM_Field_HADM_NS_INSTR52_RTT5(self)
        self.zz_fdict['RTT5'] = self.RTT5
        self.NADM5 = RM_Field_HADM_NS_INSTR52_NADM5(self)
        self.zz_fdict['NADM5'] = self.NADM5
        self.PBR5 = RM_Field_HADM_NS_INSTR52_PBR5(self)
        self.zz_fdict['PBR5'] = self.PBR5
        self.PRECNTOFF5 = RM_Field_HADM_NS_INSTR52_PRECNTOFF5(self)
        self.zz_fdict['PRECNTOFF5'] = self.PRECNTOFF5
        self.BASEWRAPCNTOFF5 = RM_Field_HADM_NS_INSTR52_BASEWRAPCNTOFF5(self)
        self.zz_fdict['BASEWRAPCNTOFF5'] = self.BASEWRAPCNTOFF5
        self.TIMEOUT5 = RM_Field_HADM_NS_INSTR52_TIMEOUT5(self)
        self.zz_fdict['TIMEOUT5'] = self.TIMEOUT5
        self.STARTDONEIEN5 = RM_Field_HADM_NS_INSTR52_STARTDONEIEN5(self)
        self.zz_fdict['STARTDONEIEN5'] = self.STARTDONEIEN5
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR62(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR62, self).__init__(rmio, label,
            0xb8034000, 0x178,
            'INSTR62', 'HADM_NS.INSTR62', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE6 = RM_Field_HADM_NS_INSTR62_ACTIVE6(self)
        self.zz_fdict['ACTIVE6'] = self.ACTIVE6
        self.RESETEN6 = RM_Field_HADM_NS_INSTR62_RESETEN6(self)
        self.zz_fdict['RESETEN6'] = self.RESETEN6
        self.PKTINFO6 = RM_Field_HADM_NS_INSTR62_PKTINFO6(self)
        self.zz_fdict['PKTINFO6'] = self.PKTINFO6
        self.FREQEST6 = RM_Field_HADM_NS_INSTR62_FREQEST6(self)
        self.zz_fdict['FREQEST6'] = self.FREQEST6
        self.RTT6 = RM_Field_HADM_NS_INSTR62_RTT6(self)
        self.zz_fdict['RTT6'] = self.RTT6
        self.NADM6 = RM_Field_HADM_NS_INSTR62_NADM6(self)
        self.zz_fdict['NADM6'] = self.NADM6
        self.PBR6 = RM_Field_HADM_NS_INSTR62_PBR6(self)
        self.zz_fdict['PBR6'] = self.PBR6
        self.PRECNTOFF6 = RM_Field_HADM_NS_INSTR62_PRECNTOFF6(self)
        self.zz_fdict['PRECNTOFF6'] = self.PRECNTOFF6
        self.BASEWRAPCNTOFF6 = RM_Field_HADM_NS_INSTR62_BASEWRAPCNTOFF6(self)
        self.zz_fdict['BASEWRAPCNTOFF6'] = self.BASEWRAPCNTOFF6
        self.TIMEOUT6 = RM_Field_HADM_NS_INSTR62_TIMEOUT6(self)
        self.zz_fdict['TIMEOUT6'] = self.TIMEOUT6
        self.STARTDONEIEN6 = RM_Field_HADM_NS_INSTR62_STARTDONEIEN6(self)
        self.zz_fdict['STARTDONEIEN6'] = self.STARTDONEIEN6
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_RESULTINSTR3(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_RESULTINSTR3, self).__init__(rmio, label,
            0xb8034000, 0x17C,
            'RESULTINSTR3', 'HADM_NS.RESULTINSTR3', 'read-write',
            u"",
            0x00000000, 0x00FFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.RES0 = RM_Field_HADM_NS_RESULTINSTR3_RES0(self)
        self.zz_fdict['RES0'] = self.RES0
        self.RES1 = RM_Field_HADM_NS_RESULTINSTR3_RES1(self)
        self.zz_fdict['RES1'] = self.RES1
        self.RES2 = RM_Field_HADM_NS_RESULTINSTR3_RES2(self)
        self.zz_fdict['RES2'] = self.RES2
        self.RES3 = RM_Field_HADM_NS_RESULTINSTR3_RES3(self)
        self.zz_fdict['RES3'] = self.RES3
        self.RES4 = RM_Field_HADM_NS_RESULTINSTR3_RES4(self)
        self.zz_fdict['RES4'] = self.RES4
        self.RES5 = RM_Field_HADM_NS_RESULTINSTR3_RES5(self)
        self.zz_fdict['RES5'] = self.RES5
        self.RES6 = RM_Field_HADM_NS_RESULTINSTR3_RES6(self)
        self.zz_fdict['RES6'] = self.RES6
        self.RES7 = RM_Field_HADM_NS_RESULTINSTR3_RES7(self)
        self.zz_fdict['RES7'] = self.RES7
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR03(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR03, self).__init__(rmio, label,
            0xb8034000, 0x180,
            'INSTR03', 'HADM_NS.INSTR03', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE0 = RM_Field_HADM_NS_INSTR03_ACTIVE0(self)
        self.zz_fdict['ACTIVE0'] = self.ACTIVE0
        self.RESETEN0 = RM_Field_HADM_NS_INSTR03_RESETEN0(self)
        self.zz_fdict['RESETEN0'] = self.RESETEN0
        self.PKTINFO0 = RM_Field_HADM_NS_INSTR03_PKTINFO0(self)
        self.zz_fdict['PKTINFO0'] = self.PKTINFO0
        self.FREQEST0 = RM_Field_HADM_NS_INSTR03_FREQEST0(self)
        self.zz_fdict['FREQEST0'] = self.FREQEST0
        self.RTT0 = RM_Field_HADM_NS_INSTR03_RTT0(self)
        self.zz_fdict['RTT0'] = self.RTT0
        self.NADM0 = RM_Field_HADM_NS_INSTR03_NADM0(self)
        self.zz_fdict['NADM0'] = self.NADM0
        self.PBR0 = RM_Field_HADM_NS_INSTR03_PBR0(self)
        self.zz_fdict['PBR0'] = self.PBR0
        self.PRECNTOFF0 = RM_Field_HADM_NS_INSTR03_PRECNTOFF0(self)
        self.zz_fdict['PRECNTOFF0'] = self.PRECNTOFF0
        self.BASEWRAPCNTOFF0 = RM_Field_HADM_NS_INSTR03_BASEWRAPCNTOFF0(self)
        self.zz_fdict['BASEWRAPCNTOFF0'] = self.BASEWRAPCNTOFF0
        self.TIMEOUT0 = RM_Field_HADM_NS_INSTR03_TIMEOUT0(self)
        self.zz_fdict['TIMEOUT0'] = self.TIMEOUT0
        self.STARTDONEIEN0 = RM_Field_HADM_NS_INSTR03_STARTDONEIEN0(self)
        self.zz_fdict['STARTDONEIEN0'] = self.STARTDONEIEN0
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR13(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR13, self).__init__(rmio, label,
            0xb8034000, 0x184,
            'INSTR13', 'HADM_NS.INSTR13', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE1 = RM_Field_HADM_NS_INSTR13_ACTIVE1(self)
        self.zz_fdict['ACTIVE1'] = self.ACTIVE1
        self.RESETEN1 = RM_Field_HADM_NS_INSTR13_RESETEN1(self)
        self.zz_fdict['RESETEN1'] = self.RESETEN1
        self.PKTINFO1 = RM_Field_HADM_NS_INSTR13_PKTINFO1(self)
        self.zz_fdict['PKTINFO1'] = self.PKTINFO1
        self.FREQEST1 = RM_Field_HADM_NS_INSTR13_FREQEST1(self)
        self.zz_fdict['FREQEST1'] = self.FREQEST1
        self.RTT1 = RM_Field_HADM_NS_INSTR13_RTT1(self)
        self.zz_fdict['RTT1'] = self.RTT1
        self.NADM1 = RM_Field_HADM_NS_INSTR13_NADM1(self)
        self.zz_fdict['NADM1'] = self.NADM1
        self.PBR1 = RM_Field_HADM_NS_INSTR13_PBR1(self)
        self.zz_fdict['PBR1'] = self.PBR1
        self.PRECNTOFF1 = RM_Field_HADM_NS_INSTR13_PRECNTOFF1(self)
        self.zz_fdict['PRECNTOFF1'] = self.PRECNTOFF1
        self.BASEWRAPCNTOFF1 = RM_Field_HADM_NS_INSTR13_BASEWRAPCNTOFF1(self)
        self.zz_fdict['BASEWRAPCNTOFF1'] = self.BASEWRAPCNTOFF1
        self.TIMEOUT1 = RM_Field_HADM_NS_INSTR13_TIMEOUT1(self)
        self.zz_fdict['TIMEOUT1'] = self.TIMEOUT1
        self.STARTDONEIEN1 = RM_Field_HADM_NS_INSTR13_STARTDONEIEN1(self)
        self.zz_fdict['STARTDONEIEN1'] = self.STARTDONEIEN1
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR23(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR23, self).__init__(rmio, label,
            0xb8034000, 0x188,
            'INSTR23', 'HADM_NS.INSTR23', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE2 = RM_Field_HADM_NS_INSTR23_ACTIVE2(self)
        self.zz_fdict['ACTIVE2'] = self.ACTIVE2
        self.RESETEN2 = RM_Field_HADM_NS_INSTR23_RESETEN2(self)
        self.zz_fdict['RESETEN2'] = self.RESETEN2
        self.PKTINFO2 = RM_Field_HADM_NS_INSTR23_PKTINFO2(self)
        self.zz_fdict['PKTINFO2'] = self.PKTINFO2
        self.FREQEST2 = RM_Field_HADM_NS_INSTR23_FREQEST2(self)
        self.zz_fdict['FREQEST2'] = self.FREQEST2
        self.RTT2 = RM_Field_HADM_NS_INSTR23_RTT2(self)
        self.zz_fdict['RTT2'] = self.RTT2
        self.NADM2 = RM_Field_HADM_NS_INSTR23_NADM2(self)
        self.zz_fdict['NADM2'] = self.NADM2
        self.PBR2 = RM_Field_HADM_NS_INSTR23_PBR2(self)
        self.zz_fdict['PBR2'] = self.PBR2
        self.PRECNTOFF2 = RM_Field_HADM_NS_INSTR23_PRECNTOFF2(self)
        self.zz_fdict['PRECNTOFF2'] = self.PRECNTOFF2
        self.BASEWRAPCNTOFF2 = RM_Field_HADM_NS_INSTR23_BASEWRAPCNTOFF2(self)
        self.zz_fdict['BASEWRAPCNTOFF2'] = self.BASEWRAPCNTOFF2
        self.TIMEOUT2 = RM_Field_HADM_NS_INSTR23_TIMEOUT2(self)
        self.zz_fdict['TIMEOUT2'] = self.TIMEOUT2
        self.STARTDONEIEN2 = RM_Field_HADM_NS_INSTR23_STARTDONEIEN2(self)
        self.zz_fdict['STARTDONEIEN2'] = self.STARTDONEIEN2
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR33(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR33, self).__init__(rmio, label,
            0xb8034000, 0x18C,
            'INSTR33', 'HADM_NS.INSTR33', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE3 = RM_Field_HADM_NS_INSTR33_ACTIVE3(self)
        self.zz_fdict['ACTIVE3'] = self.ACTIVE3
        self.RESETEN3 = RM_Field_HADM_NS_INSTR33_RESETEN3(self)
        self.zz_fdict['RESETEN3'] = self.RESETEN3
        self.PKTINFO3 = RM_Field_HADM_NS_INSTR33_PKTINFO3(self)
        self.zz_fdict['PKTINFO3'] = self.PKTINFO3
        self.FREQEST3 = RM_Field_HADM_NS_INSTR33_FREQEST3(self)
        self.zz_fdict['FREQEST3'] = self.FREQEST3
        self.RTT3 = RM_Field_HADM_NS_INSTR33_RTT3(self)
        self.zz_fdict['RTT3'] = self.RTT3
        self.NADM3 = RM_Field_HADM_NS_INSTR33_NADM3(self)
        self.zz_fdict['NADM3'] = self.NADM3
        self.PBR3 = RM_Field_HADM_NS_INSTR33_PBR3(self)
        self.zz_fdict['PBR3'] = self.PBR3
        self.PRECNTOFF3 = RM_Field_HADM_NS_INSTR33_PRECNTOFF3(self)
        self.zz_fdict['PRECNTOFF3'] = self.PRECNTOFF3
        self.BASEWRAPCNTOFF3 = RM_Field_HADM_NS_INSTR33_BASEWRAPCNTOFF3(self)
        self.zz_fdict['BASEWRAPCNTOFF3'] = self.BASEWRAPCNTOFF3
        self.TIMEOUT3 = RM_Field_HADM_NS_INSTR33_TIMEOUT3(self)
        self.zz_fdict['TIMEOUT3'] = self.TIMEOUT3
        self.STARTDONEIEN3 = RM_Field_HADM_NS_INSTR33_STARTDONEIEN3(self)
        self.zz_fdict['STARTDONEIEN3'] = self.STARTDONEIEN3
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR43(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR43, self).__init__(rmio, label,
            0xb8034000, 0x190,
            'INSTR43', 'HADM_NS.INSTR43', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE4 = RM_Field_HADM_NS_INSTR43_ACTIVE4(self)
        self.zz_fdict['ACTIVE4'] = self.ACTIVE4
        self.RESETEN4 = RM_Field_HADM_NS_INSTR43_RESETEN4(self)
        self.zz_fdict['RESETEN4'] = self.RESETEN4
        self.PKTINFO4 = RM_Field_HADM_NS_INSTR43_PKTINFO4(self)
        self.zz_fdict['PKTINFO4'] = self.PKTINFO4
        self.FREQEST4 = RM_Field_HADM_NS_INSTR43_FREQEST4(self)
        self.zz_fdict['FREQEST4'] = self.FREQEST4
        self.RTT4 = RM_Field_HADM_NS_INSTR43_RTT4(self)
        self.zz_fdict['RTT4'] = self.RTT4
        self.NADM4 = RM_Field_HADM_NS_INSTR43_NADM4(self)
        self.zz_fdict['NADM4'] = self.NADM4
        self.PBR4 = RM_Field_HADM_NS_INSTR43_PBR4(self)
        self.zz_fdict['PBR4'] = self.PBR4
        self.PRECNTOFF4 = RM_Field_HADM_NS_INSTR43_PRECNTOFF4(self)
        self.zz_fdict['PRECNTOFF4'] = self.PRECNTOFF4
        self.BASEWRAPCNTOFF4 = RM_Field_HADM_NS_INSTR43_BASEWRAPCNTOFF4(self)
        self.zz_fdict['BASEWRAPCNTOFF4'] = self.BASEWRAPCNTOFF4
        self.TIMEOUT4 = RM_Field_HADM_NS_INSTR43_TIMEOUT4(self)
        self.zz_fdict['TIMEOUT4'] = self.TIMEOUT4
        self.STARTDONEIEN4 = RM_Field_HADM_NS_INSTR43_STARTDONEIEN4(self)
        self.zz_fdict['STARTDONEIEN4'] = self.STARTDONEIEN4
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR53(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR53, self).__init__(rmio, label,
            0xb8034000, 0x194,
            'INSTR53', 'HADM_NS.INSTR53', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE5 = RM_Field_HADM_NS_INSTR53_ACTIVE5(self)
        self.zz_fdict['ACTIVE5'] = self.ACTIVE5
        self.RESETEN5 = RM_Field_HADM_NS_INSTR53_RESETEN5(self)
        self.zz_fdict['RESETEN5'] = self.RESETEN5
        self.PKTINFO5 = RM_Field_HADM_NS_INSTR53_PKTINFO5(self)
        self.zz_fdict['PKTINFO5'] = self.PKTINFO5
        self.FREQEST5 = RM_Field_HADM_NS_INSTR53_FREQEST5(self)
        self.zz_fdict['FREQEST5'] = self.FREQEST5
        self.RTT5 = RM_Field_HADM_NS_INSTR53_RTT5(self)
        self.zz_fdict['RTT5'] = self.RTT5
        self.NADM5 = RM_Field_HADM_NS_INSTR53_NADM5(self)
        self.zz_fdict['NADM5'] = self.NADM5
        self.PBR5 = RM_Field_HADM_NS_INSTR53_PBR5(self)
        self.zz_fdict['PBR5'] = self.PBR5
        self.PRECNTOFF5 = RM_Field_HADM_NS_INSTR53_PRECNTOFF5(self)
        self.zz_fdict['PRECNTOFF5'] = self.PRECNTOFF5
        self.BASEWRAPCNTOFF5 = RM_Field_HADM_NS_INSTR53_BASEWRAPCNTOFF5(self)
        self.zz_fdict['BASEWRAPCNTOFF5'] = self.BASEWRAPCNTOFF5
        self.TIMEOUT5 = RM_Field_HADM_NS_INSTR53_TIMEOUT5(self)
        self.zz_fdict['TIMEOUT5'] = self.TIMEOUT5
        self.STARTDONEIEN5 = RM_Field_HADM_NS_INSTR53_STARTDONEIEN5(self)
        self.zz_fdict['STARTDONEIEN5'] = self.STARTDONEIEN5
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_INSTR63(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_INSTR63, self).__init__(rmio, label,
            0xb8034000, 0x198,
            'INSTR63', 'HADM_NS.INSTR63', 'read-write',
            u"",
            0x00000000, 0x3FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ACTIVE6 = RM_Field_HADM_NS_INSTR63_ACTIVE6(self)
        self.zz_fdict['ACTIVE6'] = self.ACTIVE6
        self.RESETEN6 = RM_Field_HADM_NS_INSTR63_RESETEN6(self)
        self.zz_fdict['RESETEN6'] = self.RESETEN6
        self.PKTINFO6 = RM_Field_HADM_NS_INSTR63_PKTINFO6(self)
        self.zz_fdict['PKTINFO6'] = self.PKTINFO6
        self.FREQEST6 = RM_Field_HADM_NS_INSTR63_FREQEST6(self)
        self.zz_fdict['FREQEST6'] = self.FREQEST6
        self.RTT6 = RM_Field_HADM_NS_INSTR63_RTT6(self)
        self.zz_fdict['RTT6'] = self.RTT6
        self.NADM6 = RM_Field_HADM_NS_INSTR63_NADM6(self)
        self.zz_fdict['NADM6'] = self.NADM6
        self.PBR6 = RM_Field_HADM_NS_INSTR63_PBR6(self)
        self.zz_fdict['PBR6'] = self.PBR6
        self.PRECNTOFF6 = RM_Field_HADM_NS_INSTR63_PRECNTOFF6(self)
        self.zz_fdict['PRECNTOFF6'] = self.PRECNTOFF6
        self.BASEWRAPCNTOFF6 = RM_Field_HADM_NS_INSTR63_BASEWRAPCNTOFF6(self)
        self.zz_fdict['BASEWRAPCNTOFF6'] = self.BASEWRAPCNTOFF6
        self.TIMEOUT6 = RM_Field_HADM_NS_INSTR63_TIMEOUT6(self)
        self.zz_fdict['TIMEOUT6'] = self.TIMEOUT6
        self.STARTDONEIEN6 = RM_Field_HADM_NS_INSTR63_STARTDONEIEN6(self)
        self.zz_fdict['STARTDONEIEN6'] = self.STARTDONEIEN6
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS0(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS0, self).__init__(rmio, label,
            0xb8034000, 0x19C,
            'STATUS0', 'HADM_NS.STATUS0', 'read-only',
            u"",
            0x00000000, 0x7FFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.CTRLSTATE = RM_Field_HADM_NS_STATUS0_CTRLSTATE(self)
        self.zz_fdict['CTRLSTATE'] = self.CTRLSTATE
        self.PKTINFOACTIVE = RM_Field_HADM_NS_STATUS0_PKTINFOACTIVE(self)
        self.zz_fdict['PKTINFOACTIVE'] = self.PKTINFOACTIVE
        self.FREQESTACTIVE = RM_Field_HADM_NS_STATUS0_FREQESTACTIVE(self)
        self.zz_fdict['FREQESTACTIVE'] = self.FREQESTACTIVE
        self.RTTACTIVE = RM_Field_HADM_NS_STATUS0_RTTACTIVE(self)
        self.zz_fdict['RTTACTIVE'] = self.RTTACTIVE
        self.NADMACTIVE = RM_Field_HADM_NS_STATUS0_NADMACTIVE(self)
        self.zz_fdict['NADMACTIVE'] = self.NADMACTIVE
        self.PBRACTIVE = RM_Field_HADM_NS_STATUS0_PBRACTIVE(self)
        self.zz_fdict['PBRACTIVE'] = self.PBRACTIVE
        self.RESULTSACTIVE = RM_Field_HADM_NS_STATUS0_RESULTSACTIVE(self)
        self.zz_fdict['RESULTSACTIVE'] = self.RESULTSACTIVE
        self.STARTTASK = RM_Field_HADM_NS_STATUS0_STARTTASK(self)
        self.zz_fdict['STARTTASK'] = self.STARTTASK
        self.TASKNUM = RM_Field_HADM_NS_STATUS0_TASKNUM(self)
        self.zz_fdict['TASKNUM'] = self.TASKNUM
        self.PC = RM_Field_HADM_NS_STATUS0_PC(self)
        self.zz_fdict['PC'] = self.PC
        self.ANTSWITCHSTATE = RM_Field_HADM_NS_STATUS0_ANTSWITCHSTATE(self)
        self.zz_fdict['ANTSWITCHSTATE'] = self.ANTSWITCHSTATE
        self.ANTHADM = RM_Field_HADM_NS_STATUS0_ANTHADM(self)
        self.zz_fdict['ANTHADM'] = self.ANTHADM
        self.FREQESTSTATE = RM_Field_HADM_NS_STATUS0_FREQESTSTATE(self)
        self.zz_fdict['FREQESTSTATE'] = self.FREQESTSTATE
        self.RTTMAINSTATE = RM_Field_HADM_NS_STATUS0_RTTMAINSTATE(self)
        self.zz_fdict['RTTMAINSTATE'] = self.RTTMAINSTATE
        self.RTTRBSSTATE = RM_Field_HADM_NS_STATUS0_RTTRBSSTATE(self)
        self.zz_fdict['RTTRBSSTATE'] = self.RTTRBSSTATE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS1(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS1, self).__init__(rmio, label,
            0xb8034000, 0x1A0,
            'STATUS1', 'HADM_NS.STATUS1', 'read-only',
            u"",
            0x00000000, 0x000FFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.STARTINSTR = RM_Field_HADM_NS_STATUS1_STARTINSTR(self)
        self.zz_fdict['STARTINSTR'] = self.STARTINSTR
        self.DONEINSTR = RM_Field_HADM_NS_STATUS1_DONEINSTR(self)
        self.zz_fdict['DONEINSTR'] = self.DONEINSTR
        self.PBRCTRLSTATE = RM_Field_HADM_NS_STATUS1_PBRCTRLSTATE(self)
        self.zz_fdict['PBRCTRLSTATE'] = self.PBRCTRLSTATE
        self.PBRTQSTATE = RM_Field_HADM_NS_STATUS1_PBRTQSTATE(self)
        self.zz_fdict['PBRTQSTATE'] = self.PBRTQSTATE
        self.PBRGDCOMPSTATE = RM_Field_HADM_NS_STATUS1_PBRGDCOMPSTATE(self)
        self.zz_fdict['PBRGDCOMPSTATE'] = self.PBRGDCOMPSTATE
        self.PBRRESSTATE = RM_Field_HADM_NS_STATUS1_PBRRESSTATE(self)
        self.zz_fdict['PBRRESSTATE'] = self.PBRRESSTATE
        self.RTTRAMSTATE = RM_Field_HADM_NS_STATUS1_RTTRAMSTATE(self)
        self.zz_fdict['RTTRAMSTATE'] = self.RTTRAMSTATE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS2(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS2, self).__init__(rmio, label,
            0xb8034000, 0x1A4,
            'STATUS2', 'HADM_NS.STATUS2', 'read-only',
            u"",
            0x00000000, 0x000007FF,
            0x00001000, 0x00002000,
            0x00003000)

        self.CURROPCODE = RM_Field_HADM_NS_STATUS2_CURROPCODE(self)
        self.zz_fdict['CURROPCODE'] = self.CURROPCODE
        self.RESULTACTIVE = RM_Field_HADM_NS_STATUS2_RESULTACTIVE(self)
        self.zz_fdict['RESULTACTIVE'] = self.RESULTACTIVE
        self.RESULTDONE = RM_Field_HADM_NS_STATUS2_RESULTDONE(self)
        self.zz_fdict['RESULTDONE'] = self.RESULTDONE
        self.PKTINFOVALID = RM_Field_HADM_NS_STATUS2_PKTINFOVALID(self)
        self.zz_fdict['PKTINFOVALID'] = self.PKTINFOVALID
        self.FREQESTVALID = RM_Field_HADM_NS_STATUS2_FREQESTVALID(self)
        self.zz_fdict['FREQESTVALID'] = self.FREQESTVALID
        self.PBRRXVALID = RM_Field_HADM_NS_STATUS2_PBRRXVALID(self)
        self.zz_fdict['PBRRXVALID'] = self.PBRRXVALID
        self.RTTVALID = RM_Field_HADM_NS_STATUS2_RTTVALID(self)
        self.zz_fdict['RTTVALID'] = self.RTTVALID
        self.NADMVALID = RM_Field_HADM_NS_STATUS2_NADMVALID(self)
        self.zz_fdict['NADMVALID'] = self.NADMVALID
        self.BUFHANDLERSTATE = RM_Field_HADM_NS_STATUS2_BUFHANDLERSTATE(self)
        self.zz_fdict['BUFHANDLERSTATE'] = self.BUFHANDLERSTATE
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS3(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS3, self).__init__(rmio, label,
            0xb8034000, 0x1A8,
            'STATUS3', 'HADM_NS.STATUS3', 'read-only',
            u"",
            0x00000000, 0x0000FFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.TARGETPRECNT = RM_Field_HADM_NS_STATUS3_TARGETPRECNT(self)
        self.zz_fdict['TARGETPRECNT'] = self.TARGETPRECNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS4(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS4, self).__init__(rmio, label,
            0xb8034000, 0x1AC,
            'STATUS4', 'HADM_NS.STATUS4', 'read-only',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.TARGETBASECNT = RM_Field_HADM_NS_STATUS4_TARGETBASECNT(self)
        self.zz_fdict['TARGETBASECNT'] = self.TARGETBASECNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS5(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS5, self).__init__(rmio, label,
            0xb8034000, 0x1B0,
            'STATUS5', 'HADM_NS.STATUS5', 'read-only',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.TARGETWRAPCNT = RM_Field_HADM_NS_STATUS5_TARGETWRAPCNT(self)
        self.zz_fdict['TARGETWRAPCNT'] = self.TARGETWRAPCNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS6(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS6, self).__init__(rmio, label,
            0xb8034000, 0x1B4,
            'STATUS6', 'HADM_NS.STATUS6', 'read-only',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ADVTARGETBASECNT = RM_Field_HADM_NS_STATUS6_ADVTARGETBASECNT(self)
        self.zz_fdict['ADVTARGETBASECNT'] = self.ADVTARGETBASECNT
        self.__dict__['zz_frozen'] = True


class RM_Register_HADM_NS_STATUS7(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_HADM_NS_STATUS7, self).__init__(rmio, label,
            0xb8034000, 0x1B8,
            'STATUS7', 'HADM_NS.STATUS7', 'read-only',
            u"",
            0x00000000, 0xFFFFFFFF,
            0x00001000, 0x00002000,
            0x00003000)

        self.ADVTARGETWRAPCNT = RM_Field_HADM_NS_STATUS7_ADVTARGETWRAPCNT(self)
        self.zz_fdict['ADVTARGETWRAPCNT'] = self.ADVTARGETWRAPCNT
        self.__dict__['zz_frozen'] = True


