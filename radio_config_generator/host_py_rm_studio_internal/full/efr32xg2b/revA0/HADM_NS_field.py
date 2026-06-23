
# -*- coding: utf-8 -*-

from . static import Base_RM_Field


class RM_Field_HADM_NS_IPVERSION_IPVERSION(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IPVERSION_IPVERSION, self).__init__(register,
            'IPVERSION', 'HADM_NS.IPVERSION.IPVERSION', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_EN_EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_EN_EN, self).__init__(register,
            'EN', 'HADM_NS.EN.EN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_NS.IEN.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_NS.IEN.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_NS.IEN.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_NS.IEN.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_NS.IEN.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_NS.IEN.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_NS.IEN.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_NS.IEN.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_PBROF, self).__init__(register,
            'PBROF', 'HADM_NS.IEN.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_NS.IEN.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_NS.IEN.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_NS.IEN.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_NS.IEN.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_NS.IEN.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_NS.IEN.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_NS.IEN.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_NS.IEN.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_NS.IEN.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_NS.IEN.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_NS.IEN.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IEN_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IEN_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_NS.IEN.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_NS.IF.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_NS.IF.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_NS.IF.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_NS.IF.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_NS.IF.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_NS.IF.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_NS.IF.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_NS.IF.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_PBROF, self).__init__(register,
            'PBROF', 'HADM_NS.IF.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_NS.IF.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_NS.IF.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_NS.IF.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_NS.IF.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_NS.IF.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_NS.IF.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_NS.IF.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_NS.IF.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_NS.IF.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_NS.IF.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_NS.IF.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_IF_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_IF_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_NS.IF.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_NS.SEQIEN.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_NS.SEQIEN.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_NS.SEQIEN.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_NS.SEQIEN.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_NS.SEQIEN.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_NS.SEQIEN.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_NS.SEQIEN.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_NS.SEQIEN.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_PBROF, self).__init__(register,
            'PBROF', 'HADM_NS.SEQIEN.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_NS.SEQIEN.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_NS.SEQIEN.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_NS.SEQIEN.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_NS.SEQIEN.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_NS.SEQIEN.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_NS.SEQIEN.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_NS.SEQIEN.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_NS.SEQIEN.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_NS.SEQIEN.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_NS.SEQIEN.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_NS.SEQIEN.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIEN_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIEN_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_NS.SEQIEN.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_NS.SEQIF.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_NS.SEQIF.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_NS.SEQIF.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_NS.SEQIF.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_NS.SEQIF.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_NS.SEQIF.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_NS.SEQIF.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_NS.SEQIF.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_PBROF, self).__init__(register,
            'PBROF', 'HADM_NS.SEQIF.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_NS.SEQIF.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_NS.SEQIF.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_NS.SEQIF.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_NS.SEQIF.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_NS.SEQIF.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_NS.SEQIF.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_NS.SEQIF.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_NS.SEQIF.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_NS.SEQIF.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_NS.SEQIF.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_NS.SEQIF.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SEQIF_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SEQIF_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_NS.SEQIF.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_NS.FSWIEN.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_NS.FSWIEN.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_NS.FSWIEN.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_NS.FSWIEN.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_NS.FSWIEN.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_NS.FSWIEN.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_NS.FSWIEN.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_NS.FSWIEN.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_PBROF, self).__init__(register,
            'PBROF', 'HADM_NS.FSWIEN.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_NS.FSWIEN.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_NS.FSWIEN.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_NS.FSWIEN.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_NS.FSWIEN.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_NS.FSWIEN.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_NS.FSWIEN.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_NS.FSWIEN.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_NS.FSWIEN.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_NS.FSWIEN.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_NS.FSWIEN.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_NS.FSWIEN.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIEN_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIEN_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_NS.FSWIEN.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_NS.FSWIF.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_NS.FSWIF.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_NS.FSWIF.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_NS.FSWIF.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_NS.FSWIF.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_NS.FSWIF.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_NS.FSWIF.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_NS.FSWIF.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_PBROF, self).__init__(register,
            'PBROF', 'HADM_NS.FSWIF.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_NS.FSWIF.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_NS.FSWIF.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_NS.FSWIF.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_NS.FSWIF.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_NS.FSWIF.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_NS.FSWIF.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_NS.FSWIF.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_NS.FSWIF.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_NS.FSWIF.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_NS.FSWIF.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_NS.FSWIF.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_FSWIF_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_FSWIF_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_NS.FSWIF.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CMD_START(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CMD_START, self).__init__(register,
            'START', 'HADM_NS.CMD.START', 'write-only',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CMD_STOP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CMD_STOP, self).__init__(register,
            'STOP', 'HADM_NS.CMD.STOP', 'write-only',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CMD_FORCECTRL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CMD_FORCECTRL, self).__init__(register,
            'FORCECTRL', 'HADM_NS.CMD.FORCECTRL', 'write-only',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CMD_RSTANTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CMD_RSTANTSEL, self).__init__(register,
            'RSTANTSEL', 'HADM_NS.CMD.RSTANTSEL', 'write-only',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CMD_CLEAR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CMD_CLEAR, self).__init__(register,
            'CLEAR', 'HADM_NS.CMD.CLEAR', 'write-only',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CMD_FLUSH(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CMD_FLUSH, self).__init__(register,
            'FLUSH', 'HADM_NS.CMD.FLUSH', 'write-only',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_ROLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_ROLE, self).__init__(register,
            'ROLE', 'HADM_NS.CTRL0.ROLE', 'read-write',
            u"",
            0, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_PHYSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_PHYSEL, self).__init__(register,
            'PHYSEL', 'HADM_NS.CTRL0.PHYSEL', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_SSAFCGEAR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_SSAFCGEAR, self).__init__(register,
            'SSAFCGEAR', 'HADM_NS.CTRL0.SSAFCGEAR', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_TXUPSAMPOSR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_TXUPSAMPOSR4, self).__init__(register,
            'TXUPSAMPOSR4', 'HADM_NS.CTRL0.TXUPSAMPOSR4', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_TGUARDPERIOD(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_TGUARDPERIOD, self).__init__(register,
            'TGUARDPERIOD', 'HADM_NS.CTRL0.TGUARDPERIOD', 'read-write',
            u"",
            6, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_AVGSTARTOFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_AVGSTARTOFF, self).__init__(register,
            'AVGSTARTOFF', 'HADM_NS.CTRL0.AVGSTARTOFF', 'read-write',
            u"",
            10, 10)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_OWRRSTDLO(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_OWRRSTDLO, self).__init__(register,
            'OWRRSTDLO', 'HADM_NS.CTRL0.OWRRSTDLO', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_GDCOMPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_GDCOMPEN, self).__init__(register,
            'GDCOMPEN', 'HADM_NS.CTRL0.GDCOMPEN', 'read-write',
            u"",
            21, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_CTRLMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_CTRLMODE, self).__init__(register,
            'CTRLMODE', 'HADM_NS.CTRL0.CTRLMODE', 'read-write',
            u"",
            22, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_WAITONERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_WAITONERROR, self).__init__(register,
            'WAITONERROR', 'HADM_NS.CTRL0.WAITONERROR', 'read-write',
            u"",
            23, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_CTRL0_TFM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_CTRL0_TFM, self).__init__(register,
            'TFM', 'HADM_NS.CTRL0.TFM', 'read-write',
            u"",
            24, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_RTTMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_RTTMODE, self).__init__(register,
            'RTTMODE', 'HADM_NS.RTTCTRL0.RTTMODE', 'read-write',
            u"",
            0, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_RTTLEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_RTTLEN, self).__init__(register,
            'RTTLEN', 'HADM_NS.RTTCTRL0.RTTLEN', 'read-write',
            u"",
            2, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_PESEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_PESEN, self).__init__(register,
            'PESEN', 'HADM_NS.RTTCTRL0.PESEN', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_SNDSEQEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_SNDSEQEN, self).__init__(register,
            'SNDSEQEN', 'HADM_NS.RTTCTRL0.SNDSEQEN', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_PKTSENTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_PKTSENTSEL, self).__init__(register,
            'PKTSENTSEL', 'HADM_NS.RTTCTRL0.PKTSENTSEL', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_DFTSCALE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_DFTSCALE, self).__init__(register,
            'DFTSCALE', 'HADM_NS.RTTCTRL0.DFTSCALE', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_RBSTRACKNUM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_RBSTRACKNUM, self).__init__(register,
            'RBSTRACKNUM', 'HADM_NS.RTTCTRL0.RBSTRACKNUM', 'read-write',
            u"",
            11, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_DFTSTARTOFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_DFTSTARTOFF, self).__init__(register,
            'DFTSTARTOFF', 'HADM_NS.RTTCTRL0.DFTSTARTOFF', 'read-write',
            u"",
            14, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_RTTTIMEOUT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_RTTTIMEOUT, self).__init__(register,
            'RTTTIMEOUT', 'HADM_NS.RTTCTRL0.RTTTIMEOUT', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL0_MAXSCHWIN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL0_MAXSCHWIN, self).__init__(register,
            'MAXSCHWIN', 'HADM_NS.RTTCTRL0.MAXSCHWIN', 'read-write',
            u"",
            24, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_TRECSOSR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_TRECSOSR, self).__init__(register,
            'TRECSOSR', 'HADM_NS.RTTCTRL1.TRECSOSR', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_RAMRADDRBACK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_RAMRADDRBACK, self).__init__(register,
            'RAMRADDRBACK', 'HADM_NS.RTTCTRL1.RAMRADDRBACK', 'read-write',
            u"",
            1, 9)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_FRAMEDETSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_FRAMEDETSEL, self).__init__(register,
            'FRAMEDETSEL', 'HADM_NS.RTTCTRL1.FRAMEDETSEL', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_FRAMEDETTIMEOUT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_FRAMEDETTIMEOUT, self).__init__(register,
            'FRAMEDETTIMEOUT', 'HADM_NS.RTTCTRL1.FRAMEDETTIMEOUT', 'read-write',
            u"",
            11, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_SBFLIPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_SBFLIPEN, self).__init__(register,
            'SBFLIPEN', 'HADM_NS.RTTCTRL1.SBFLIPEN', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_EPLBWREN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_EPLBWREN, self).__init__(register,
            'EPLBWREN', 'HADM_NS.RTTCTRL1.EPLBWREN', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_SSPMSWAPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_SSPMSWAPEN, self).__init__(register,
            'SSPMSWAPEN', 'HADM_NS.RTTCTRL1.SSPMSWAPEN', 'read-write',
            u"",
            21, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_XOSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_XOSEL, self).__init__(register,
            'XOSEL', 'HADM_NS.RTTCTRL1.XOSEL', 'read-write',
            u"",
            22, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_ELSWAPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_ELSWAPEN, self).__init__(register,
            'ELSWAPEN', 'HADM_NS.RTTCTRL1.ELSWAPEN', 'read-write',
            u"",
            24, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_CORRACCDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_CORRACCDLY, self).__init__(register,
            'CORRACCDLY', 'HADM_NS.RTTCTRL1.CORRACCDLY', 'read-write',
            u"",
            25, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_SSDFTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_SSDFTEN, self).__init__(register,
            'SSDFTEN', 'HADM_NS.RTTCTRL1.SSDFTEN', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_TIMEROWEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_TIMEROWEN, self).__init__(register,
            'TIMEROWEN', 'HADM_NS.RTTCTRL1.TIMEROWEN', 'read-write',
            u"",
            30, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL1_FBROCEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL1_FBROCEN, self).__init__(register,
            'FBROCEN', 'HADM_NS.RTTCTRL1.FBROCEN', 'read-write',
            u"",
            31, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_FBROCMUL2EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_FBROCMUL2EN, self).__init__(register,
            'FBROCMUL2EN', 'HADM_NS.RTTCTRL2.FBROCMUL2EN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_TIMERDETSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_TIMERDETSEL, self).__init__(register,
            'TIMERDETSEL', 'HADM_NS.RTTCTRL2.TIMERDETSEL', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_FLIPEPL1EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_FLIPEPL1EN, self).__init__(register,
            'FLIPEPL1EN', 'HADM_NS.RTTCTRL2.FLIPEPL1EN', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_FLIPEPL2EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_FLIPEPL2EN, self).__init__(register,
            'FLIPEPL2EN', 'HADM_NS.RTTCTRL2.FLIPEPL2EN', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_SINGLEPKTMODEEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_SINGLEPKTMODEEN, self).__init__(register,
            'SINGLEPKTMODEEN', 'HADM_NS.RTTCTRL2.SINGLEPKTMODEEN', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_SRCMUREFBACK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_SRCMUREFBACK, self).__init__(register,
            'SRCMUREFBACK', 'HADM_NS.RTTCTRL2.SRCMUREFBACK', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_SSFFOLEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_SSFFOLEN, self).__init__(register,
            'SSFFOLEN', 'HADM_NS.RTTCTRL2.SSFFOLEN', 'read-write',
            u"",
            8, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTCTRL2_SRCCOMPSAMPSKIPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTCTRL2_SRCCOMPSAMPSKIPEN, self).__init__(register,
            'SRCCOMPSAMPSKIPEN', 'HADM_NS.RTTCTRL2.SRCCOMPSAMPSKIPEN', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTTUNE_RTTINITTUNE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTTUNE_RTTINITTUNE, self).__init__(register,
            'RTTINITTUNE', 'HADM_NS.RTTTUNE.RTTINITTUNE', 'read-write',
            u"",
            0, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTTUNE_RTTREFLTUNE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTTUNE_RTTREFLTUNE, self).__init__(register,
            'RTTREFLTUNE', 'HADM_NS.RTTTUNE.RTTREFLTUNE', 'read-write',
            u"",
            12, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME0_REFBACKSYMB(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME0_REFBACKSYMB, self).__init__(register,
            'REFBACKSYMB', 'HADM_NS.RTTRPTTIME0.REFBACKSYMB', 'read-write',
            u"",
            0, 6)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME0_REFBACKCYCLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME0_REFBACKCYCLE, self).__init__(register,
            'REFBACKCYCLE', 'HADM_NS.RTTRPTTIME0.REFBACKCYCLE', 'read-write',
            u"",
            6, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME0_GROUPDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME0_GROUPDLY, self).__init__(register,
            'GROUPDLY', 'HADM_NS.RTTRPTTIME0.GROUPDLY', 'read-write',
            u"",
            10, 11)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME0_RTTTIP1IDX(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME0_RTTTIP1IDX, self).__init__(register,
            'RTTTIP1IDX', 'HADM_NS.RTTRPTTIME0.RTTTIP1IDX', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME0_FLTDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME0_FLTDLY, self).__init__(register,
            'FLTDLY', 'HADM_NS.RTTRPTTIME0.FLTDLY', 'read-write',
            u"",
            24, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME1_FFO(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME1_FFO, self).__init__(register,
            'FFO', 'HADM_NS.RTTRPTTIME1.FFO', 'read-write',
            u"",
            0, 13)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME1_COARSETIMEOW(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME1_COARSETIMEOW, self).__init__(register,
            'COARSETIMEOW', 'HADM_NS.RTTRPTTIME1.COARSETIMEOW', 'read-write',
            u"",
            13, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTRPTTIME1_SSFFONEG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTRPTTIME1_SSFFONEG, self).__init__(register,
            'SSFFONEG', 'HADM_NS.RTTRPTTIME1.SSFFONEG', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTPKT0_RTTPAYLOAD0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTPKT0_RTTPAYLOAD0, self).__init__(register,
            'RTTPAYLOAD0', 'HADM_NS.RTTPKT0.RTTPAYLOAD0', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTPKT1_RTTPAYLOAD1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTPKT1_RTTPAYLOAD1, self).__init__(register,
            'RTTPAYLOAD1', 'HADM_NS.RTTPKT1.RTTPAYLOAD1', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTPKT2_RTTPAYLOAD2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTPKT2_RTTPAYLOAD2, self).__init__(register,
            'RTTPAYLOAD2', 'HADM_NS.RTTPKT2.RTTPAYLOAD2', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RTTPKT3_RTTPAYLOAD3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RTTPKT3_RTTPAYLOAD3, self).__init__(register,
            'RTTPAYLOAD3', 'HADM_NS.RTTPKT3.RTTPAYLOAD3', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_AVGMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_AVGMODE, self).__init__(register,
            'AVGMODE', 'HADM_NS.PBRCTRL0.AVGMODE', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_PM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_PM, self).__init__(register,
            'PM', 'HADM_NS.PBRCTRL0.PM', 'read-write',
            u"",
            1, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_TEXCL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_TEXCL, self).__init__(register,
            'TEXCL', 'HADM_NS.PBRCTRL0.TEXCL', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_TSWITCH(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_TSWITCH, self).__init__(register,
            'TSWITCH', 'HADM_NS.PBRCTRL0.TSWITCH', 'read-write',
            u"",
            6, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_TGRPDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_TGRPDLY, self).__init__(register,
            'TGRPDLY', 'HADM_NS.PBRCTRL0.TGRPDLY', 'read-write',
            u"",
            10, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_ACI(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_ACI, self).__init__(register,
            'ACI', 'HADM_NS.PBRCTRL0.ACI', 'read-write',
            u"",
            14, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_API(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_API, self).__init__(register,
            'API', 'HADM_NS.PBRCTRL0.API', 'read-write',
            u"",
            17, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL0_TONEQUALITYTHRESH(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL0_TONEQUALITYTHRESH, self).__init__(register,
            'TONEQUALITYTHRESH', 'HADM_NS.PBRCTRL0.TONEQUALITYTHRESH', 'read-write',
            u"",
            22, 10)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_CHNO(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_CHNO, self).__init__(register,
            'CHNO', 'HADM_NS.PBRCTRL1.CHNO', 'read-write',
            u"",
            0, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_DCMEASEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_DCMEASEN, self).__init__(register,
            'DCMEASEN', 'HADM_NS.PBRCTRL1.DCMEASEN', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_DCMEASMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_DCMEASMODE, self).__init__(register,
            'DCMEASMODE', 'HADM_NS.PBRCTRL1.DCMEASMODE', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_DCMEASWIN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_DCMEASWIN, self).__init__(register,
            'DCMEASWIN', 'HADM_NS.PBRCTRL1.DCMEASWIN', 'read-write',
            u"",
            9, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_EMPTYPCTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_EMPTYPCTEN, self).__init__(register,
            'EMPTYPCTEN', 'HADM_NS.PBRCTRL1.EMPTYPCTEN', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_TONEQUALITYSCALE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_TONEQUALITYSCALE, self).__init__(register,
            'TONEQUALITYSCALE', 'HADM_NS.PBRCTRL1.TONEQUALITYSCALE', 'read-write',
            u"",
            14, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_INLINEPCTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_INLINEPCTEN, self).__init__(register,
            'INLINEPCTEN', 'HADM_NS.PBRCTRL1.INLINEPCTEN', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_PBRLIFEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_PBRLIFEN, self).__init__(register,
            'PBRLIFEN', 'HADM_NS.PBRCTRL1.PBRLIFEN', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRCTRL1_TPULSE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRCTRL1_TPULSE, self).__init__(register,
            'TPULSE', 'HADM_NS.PBRCTRL1.TPULSE', 'read-write',
            u"",
            20, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRDCCOMP_DCCOMPI(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRDCCOMP_DCCOMPI, self).__init__(register,
            'DCCOMPI', 'HADM_NS.PBRDCCOMP.DCCOMPI', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRDCCOMP_DCCOMPQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRDCCOMP_DCCOMPQ, self).__init__(register,
            'DCCOMPQ', 'HADM_NS.PBRDCCOMP.DCCOMPQ', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRGDCOMP0_PHASEPERCHANNEL0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRGDCOMP0_PHASEPERCHANNEL0, self).__init__(register,
            'PHASEPERCHANNEL0', 'HADM_NS.PBRGDCOMP0.PHASEPERCHANNEL0', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRGDCOMP0_PHASEPERCHANNEL1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRGDCOMP0_PHASEPERCHANNEL1, self).__init__(register,
            'PHASEPERCHANNEL1', 'HADM_NS.PBRGDCOMP0.PHASEPERCHANNEL1', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRGDCOMP1_PHASEPERCHANNEL2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRGDCOMP1_PHASEPERCHANNEL2, self).__init__(register,
            'PHASEPERCHANNEL2', 'HADM_NS.PBRGDCOMP1.PHASEPERCHANNEL2', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRGDCOMP1_PHASEPERCHANNEL3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRGDCOMP1_PHASEPERCHANNEL3, self).__init__(register,
            'PHASEPERCHANNEL3', 'HADM_NS.PBRGDCOMP1.PHASEPERCHANNEL3', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRRAMPCTRL_RAMPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRRAMPCTRL_RAMPEN, self).__init__(register,
            'RAMPEN', 'HADM_NS.PBRRAMPCTRL.RAMPEN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPPRETRIG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPPRETRIG, self).__init__(register,
            'TRAMPPRETRIG', 'HADM_NS.PBRRAMPCTRL.TRAMPPRETRIG', 'read-write',
            u"",
            1, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPPOSTTRIG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPPOSTTRIG, self).__init__(register,
            'TRAMPPOSTTRIG', 'HADM_NS.PBRRAMPCTRL.TRAMPPOSTTRIG', 'read-write',
            u"",
            8, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRRAMPCTRL_TRAMP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRRAMPCTRL_TRAMP, self).__init__(register,
            'TRAMP', 'HADM_NS.PBRRAMPCTRL.TRAMP', 'read-write',
            u"",
            12, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPSW(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PBRRAMPCTRL_TRAMPSW, self).__init__(register,
            'TRAMPSW', 'HADM_NS.PBRRAMPCTRL.TRAMPSW', 'read-write',
            u"",
            16, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_ANTCTRL_ANTPATTHADM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_ANTCTRL_ANTPATTHADM, self).__init__(register,
            'ANTPATTHADM', 'HADM_NS.ANTCTRL.ANTPATTHADM', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_ANTCTRL_CSSYNCNUMANT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_ANTCTRL_CSSYNCNUMANT, self).__init__(register,
            'CSSYNCNUMANT', 'HADM_NS.ANTCTRL.CSSYNCNUMANT', 'read-write',
            u"",
            16, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_ANTCTRL_CSSYNCANTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_ANTCTRL_CSSYNCANTSEL, self).__init__(register,
            'CSSYNCANTSEL', 'HADM_NS.ANTCTRL.CSSYNCANTSEL', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_ANTCTRL_DCMEASANTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_ANTCTRL_DCMEASANTSEL, self).__init__(register,
            'DCMEASANTSEL', 'HADM_NS.ANTCTRL.DCMEASANTSEL', 'read-write',
            u"",
            21, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_ANTCTRL_ANTSWITCHADVANCE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_ANTCTRL_ANTSWITCHADVANCE, self).__init__(register,
            'ANTSWITCHADVANCE', 'HADM_NS.ANTCTRL.ANTSWITCHADVANCE', 'read-write',
            u"",
            23, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PRSSEL_DBGSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PRSSEL_DBGSEL, self).__init__(register,
            'DBGSEL', 'HADM_NS.PRSSEL.DBGSEL', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PRSSEL_RTTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PRSSEL_RTTSEL, self).__init__(register,
            'RTTSEL', 'HADM_NS.PRSSEL.RTTSEL', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PRSSEL_PBRSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PRSSEL_PBRSEL, self).__init__(register,
            'PBRSEL', 'HADM_NS.PRSSEL.PBRSEL', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PRSSEL_RXSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PRSSEL_RXSEL, self).__init__(register,
            'RXSEL', 'HADM_NS.PRSSEL.RXSEL', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PRSSEL_TXSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PRSSEL_TXSEL, self).__init__(register,
            'TXSEL', 'HADM_NS.PRSSEL.TXSEL', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_PRSSEL_CTRLSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_PRSSEL_CTRLSEL, self).__init__(register,
            'CTRLSEL', 'HADM_NS.PRSSEL.CTRLSEL', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RFECASEL_ECAMODESEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RFECASEL_ECAMODESEL, self).__init__(register,
            'ECAMODESEL', 'HADM_NS.RFECASEL.ECAMODESEL', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RFECASEL_RESULTECASEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RFECASEL_RESULTECASEL, self).__init__(register,
            'RESULTECASEL', 'HADM_NS.RFECASEL.RESULTECASEL', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_NADMDIFFD(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_NADMDIFFD, self).__init__(register,
            'NADMDIFFD', 'HADM_NS.NADMCONFIG.NADMDIFFD', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_RECREWINDSAMPLES(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_RECREWINDSAMPLES, self).__init__(register,
            'RECREWINDSAMPLES', 'HADM_NS.NADMCONFIG.RECREWINDSAMPLES', 'read-write',
            u"",
            2, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_REFMAPFSK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_REFMAPFSK, self).__init__(register,
            'REFMAPFSK', 'HADM_NS.NADMCONFIG.REFMAPFSK', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_FORCEFRAC(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_FORCEFRAC, self).__init__(register,
            'FORCEFRAC', 'HADM_NS.NADMCONFIG.FORCEFRAC', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_FORCEDFRAC(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_FORCEDFRAC, self).__init__(register,
            'FORCEDFRAC', 'HADM_NS.NADMCONFIG.FORCEDFRAC', 'read-write',
            u"",
            12, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_SNRNUMFASTSAMPLES(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_SNRNUMFASTSAMPLES, self).__init__(register,
            'SNRNUMFASTSAMPLES', 'HADM_NS.NADMCONFIG.SNRNUMFASTSAMPLES', 'read-write',
            u"",
            19, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_SNRFASTCOEFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_SNRFASTCOEFF, self).__init__(register,
            'SNRFASTCOEFF', 'HADM_NS.NADMCONFIG.SNRFASTCOEFF', 'read-write',
            u"",
            22, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_NADMCONFIG_SNRSLOWCOEFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_NADMCONFIG_SNRSLOWCOEFF, self).__init__(register,
            'SNRSLOWCOEFF', 'HADM_NS.NADMCONFIG.SNRSLOWCOEFF', 'read-write',
            u"",
            26, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_MSEPEARSONMASK_MSEPEARSONMASK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_MSEPEARSONMASK_MSEPEARSONMASK, self).__init__(register,
            'MSEPEARSONMASK', 'HADM_NS.MSEPEARSONMASK.MSEPEARSONMASK', 'read-write',
            u"",
            0, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_DFTAMFREQ_DFTAMFREQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_DFTAMFREQ_DFTAMFREQ, self).__init__(register,
            'DFTAMFREQ', 'HADM_NS.DFTAMFREQ.DFTAMFREQ', 'read-write',
            u"",
            0, 20)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_DFTECLDFREQ_DFTECLDFREQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_DFTECLDFREQ_DFTECLDFREQ, self).__init__(register,
            'DFTECLDFREQ', 'HADM_NS.DFTECLDFREQ.DFTECLDFREQ', 'read-write',
            u"",
            0, 20)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG0_REFGENCOEFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG0_REFGENCOEFF0, self).__init__(register,
            'REFGENCOEFF0', 'HADM_NS.REFGENCOEFFG0.REFGENCOEFF0', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG0_REFGENCOEFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG0_REFGENCOEFF1, self).__init__(register,
            'REFGENCOEFF1', 'HADM_NS.REFGENCOEFFG0.REFGENCOEFF1', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG1_REFGENCOEFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG1_REFGENCOEFF2, self).__init__(register,
            'REFGENCOEFF2', 'HADM_NS.REFGENCOEFFG1.REFGENCOEFF2', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG1_REFGENCOEFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG1_REFGENCOEFF3, self).__init__(register,
            'REFGENCOEFF3', 'HADM_NS.REFGENCOEFFG1.REFGENCOEFF3', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG2_REFGENCOEFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG2_REFGENCOEFF4, self).__init__(register,
            'REFGENCOEFF4', 'HADM_NS.REFGENCOEFFG2.REFGENCOEFF4', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG2_REFGENCOEFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG2_REFGENCOEFF5, self).__init__(register,
            'REFGENCOEFF5', 'HADM_NS.REFGENCOEFFG2.REFGENCOEFF5', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG3_REFGENCOEFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG3_REFGENCOEFF6, self).__init__(register,
            'REFGENCOEFF6', 'HADM_NS.REFGENCOEFFG3.REFGENCOEFF6', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG3_REFGENCOEFF7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG3_REFGENCOEFF7, self).__init__(register,
            'REFGENCOEFF7', 'HADM_NS.REFGENCOEFFG3.REFGENCOEFF7', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG4_REFGENCOEFF8(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG4_REFGENCOEFF8, self).__init__(register,
            'REFGENCOEFF8', 'HADM_NS.REFGENCOEFFG4.REFGENCOEFF8', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG4_REFGENCOEFF9(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG4_REFGENCOEFF9, self).__init__(register,
            'REFGENCOEFF9', 'HADM_NS.REFGENCOEFFG4.REFGENCOEFF9', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG5_REFGENCOEFF10(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG5_REFGENCOEFF10, self).__init__(register,
            'REFGENCOEFF10', 'HADM_NS.REFGENCOEFFG5.REFGENCOEFF10', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG5_REFGENCOEFF11(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG5_REFGENCOEFF11, self).__init__(register,
            'REFGENCOEFF11', 'HADM_NS.REFGENCOEFFG5.REFGENCOEFF11', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG6_REFGENCOEFF12(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG6_REFGENCOEFF12, self).__init__(register,
            'REFGENCOEFF12', 'HADM_NS.REFGENCOEFFG6.REFGENCOEFF12', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG6_REFGENCOEFF13(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG6_REFGENCOEFF13, self).__init__(register,
            'REFGENCOEFF13', 'HADM_NS.REFGENCOEFFG6.REFGENCOEFF13', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG7_REFGENCOEFF14(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG7_REFGENCOEFF14, self).__init__(register,
            'REFGENCOEFF14', 'HADM_NS.REFGENCOEFFG7.REFGENCOEFF14', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG7_REFGENCOEFF15(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG7_REFGENCOEFF15, self).__init__(register,
            'REFGENCOEFF15', 'HADM_NS.REFGENCOEFFG7.REFGENCOEFF15', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG8_REFGENCOEFF16(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG8_REFGENCOEFF16, self).__init__(register,
            'REFGENCOEFF16', 'HADM_NS.REFGENCOEFFG8.REFGENCOEFF16', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG8_REFGENCOEFF17(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG8_REFGENCOEFF17, self).__init__(register,
            'REFGENCOEFF17', 'HADM_NS.REFGENCOEFFG8.REFGENCOEFF17', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG9_REFGENCOEFF18(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG9_REFGENCOEFF18, self).__init__(register,
            'REFGENCOEFF18', 'HADM_NS.REFGENCOEFFG9.REFGENCOEFF18', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG9_REFGENCOEFF19(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG9_REFGENCOEFF19, self).__init__(register,
            'REFGENCOEFF19', 'HADM_NS.REFGENCOEFFG9.REFGENCOEFF19', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG10_REFGENCOEFF20(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG10_REFGENCOEFF20, self).__init__(register,
            'REFGENCOEFF20', 'HADM_NS.REFGENCOEFFG10.REFGENCOEFF20', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG10_REFGENCOEFF21(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG10_REFGENCOEFF21, self).__init__(register,
            'REFGENCOEFF21', 'HADM_NS.REFGENCOEFFG10.REFGENCOEFF21', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG11_REFGENCOEFF22(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG11_REFGENCOEFF22, self).__init__(register,
            'REFGENCOEFF22', 'HADM_NS.REFGENCOEFFG11.REFGENCOEFF22', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG11_REFGENCOEFF23(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG11_REFGENCOEFF23, self).__init__(register,
            'REFGENCOEFF23', 'HADM_NS.REFGENCOEFFG11.REFGENCOEFF23', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG12_REFGENCOEFF24(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG12_REFGENCOEFF24, self).__init__(register,
            'REFGENCOEFF24', 'HADM_NS.REFGENCOEFFG12.REFGENCOEFF24', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG12_REFGENCOEFF25(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG12_REFGENCOEFF25, self).__init__(register,
            'REFGENCOEFF25', 'HADM_NS.REFGENCOEFFG12.REFGENCOEFF25', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG13_REFGENCOEFF26(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG13_REFGENCOEFF26, self).__init__(register,
            'REFGENCOEFF26', 'HADM_NS.REFGENCOEFFG13.REFGENCOEFF26', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG13_REFGENCOEFF27(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG13_REFGENCOEFF27, self).__init__(register,
            'REFGENCOEFF27', 'HADM_NS.REFGENCOEFFG13.REFGENCOEFF27', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG14_REFGENCOEFF28(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG14_REFGENCOEFF28, self).__init__(register,
            'REFGENCOEFF28', 'HADM_NS.REFGENCOEFFG14.REFGENCOEFF28', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG14_REFGENCOEFF29(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG14_REFGENCOEFF29, self).__init__(register,
            'REFGENCOEFF29', 'HADM_NS.REFGENCOEFFG14.REFGENCOEFF29', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG15_REFGENCOEFF30(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG15_REFGENCOEFF30, self).__init__(register,
            'REFGENCOEFF30', 'HADM_NS.REFGENCOEFFG15.REFGENCOEFF30', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_REFGENCOEFFG15_REFGENCOEFF31(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_REFGENCOEFFG15_REFGENCOEFF31, self).__init__(register,
            'REFGENCOEFF31', 'HADM_NS.REFGENCOEFFG15.REFGENCOEFF31', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_SPARE_SPARE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_SPARE_SPARE, self).__init__(register,
            'SPARE', 'HADM_NS.SPARE.SPARE', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESCTRL_SIZE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESCTRL_SIZE, self).__init__(register,
            'SIZE', 'HADM_NS.RESCTRL.SIZE', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESCTRL_BUFMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESCTRL_BUFMODE, self).__init__(register,
            'BUFMODE', 'HADM_NS.RESCTRL.BUFMODE', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESCTRL_DEBUGEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESCTRL_DEBUGEN, self).__init__(register,
            'DEBUGEN', 'HADM_NS.RESCTRL.DEBUGEN', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESCTRL_NADMEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESCTRL_NADMEN, self).__init__(register,
            'NADMEN', 'HADM_NS.RESCTRL.NADMEN', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_ADDR_ADDR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_ADDR_ADDR, self).__init__(register,
            'ADDR', 'HADM_NS.ADDR.ADDR', 'read-write',
            u"",
            2, 30)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESSTATUS_BYTES(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESSTATUS_BYTES, self).__init__(register,
            'BYTES', 'HADM_NS.RESSTATUS.BYTES', 'read-only',
            u"",
            0, 14)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESSTATUS_STEPS(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESSTATUS_STEPS, self).__init__(register,
            'STEPS', 'HADM_NS.RESSTATUS.STEPS', 'read-only',
            u"",
            14, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESSTATUS_THRESHOLDFLAG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESSTATUS_THRESHOLDFLAG, self).__init__(register,
            'THRESHOLDFLAG', 'HADM_NS.RESSTATUS.THRESHOLDFLAG', 'read-only',
            u"",
            22, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_THRESHOLDCTRL_THRESHOLD(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_THRESHOLDCTRL_THRESHOLD, self).__init__(register,
            'THRESHOLD', 'HADM_NS.THRESHOLDCTRL.THRESHOLD', 'read-write',
            u"",
            0, 13)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_THRESHOLDCTRL_THRESHOLDMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_THRESHOLDCTRL_THRESHOLDMODE, self).__init__(register,
            'THRESHOLDMODE', 'HADM_NS.THRESHOLDCTRL.THRESHOLDMODE', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_AHBCONFIG_BUFFERABLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_AHBCONFIG_BUFFERABLE, self).__init__(register,
            'BUFFERABLE', 'HADM_NS.AHBCONFIG.BUFFERABLE', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_AHBCONFIG_MODIFIABLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_AHBCONFIG_MODIFIABLE, self).__init__(register,
            'MODIFIABLE', 'HADM_NS.AHBCONFIG.MODIFIABLE', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_AHBCONFIG_LOOKUP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_AHBCONFIG_LOOKUP, self).__init__(register,
            'LOOKUP', 'HADM_NS.AHBCONFIG.LOOKUP', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_AHBCONFIG_ALLOCATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_AHBCONFIG_ALLOCATE, self).__init__(register,
            'ALLOCATE', 'HADM_NS.AHBCONFIG.ALLOCATE', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_AHBCONFIG_SHAREABLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_AHBCONFIG_SHAREABLE, self).__init__(register,
            'SHAREABLE', 'HADM_NS.AHBCONFIG.SHAREABLE', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL0_NEXTTASKNUM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL0_NEXTTASKNUM, self).__init__(register,
            'NEXTTASKNUM', 'HADM_NS.TASKCTRL0.NEXTTASKNUM', 'read-write',
            u"",
            0, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL0_NEXTPRECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL0_NEXTPRECNT, self).__init__(register,
            'NEXTPRECNT', 'HADM_NS.TASKCTRL0.NEXTPRECNT', 'read-write',
            u"",
            2, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL1_NEXTBASECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL1_NEXTBASECNT, self).__init__(register,
            'NEXTBASECNT', 'HADM_NS.TASKCTRL1.NEXTBASECNT', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL2_NEXTWRAPCNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL2_NEXTWRAPCNT, self).__init__(register,
            'NEXTWRAPCNT', 'HADM_NS.TASKCTRL2.NEXTWRAPCNT', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_PRECNTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_PRECNTEN, self).__init__(register,
            'PRECNTEN', 'HADM_NS.TASKCTRL3.PRECNTEN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_BASECNTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_BASECNTEN, self).__init__(register,
            'BASECNTEN', 'HADM_NS.TASKCTRL3.BASECNTEN', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_WRAPCNTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_WRAPCNTEN, self).__init__(register,
            'WRAPCNTEN', 'HADM_NS.TASKCTRL3.WRAPCNTEN', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_TIMEOUTOFFSET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_TIMEOUTOFFSET, self).__init__(register,
            'TIMEOUTOFFSET', 'HADM_NS.TASKCTRL3.TIMEOUTOFFSET', 'read-write',
            u"",
            3, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_MAXQUEUE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_MAXQUEUE, self).__init__(register,
            'MAXQUEUE', 'HADM_NS.TASKCTRL3.MAXQUEUE', 'read-write',
            u"",
            15, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_TIMERERRDIS(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_TIMERERRDIS, self).__init__(register,
            'TIMERERRDIS', 'HADM_NS.TASKCTRL3.TIMERERRDIS', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_TASKCTRL3_WRAPCNTWIN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_TASKCTRL3_WRAPCNTWIN, self).__init__(register,
            'WRAPCNTWIN', 'HADM_NS.TASKCTRL3.WRAPCNTWIN', 'read-write',
            u"",
            18, 14)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES0, self).__init__(register,
            'RES0', 'HADM_NS.RESULTINSTR0.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES1, self).__init__(register,
            'RES1', 'HADM_NS.RESULTINSTR0.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES2, self).__init__(register,
            'RES2', 'HADM_NS.RESULTINSTR0.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES3, self).__init__(register,
            'RES3', 'HADM_NS.RESULTINSTR0.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES4, self).__init__(register,
            'RES4', 'HADM_NS.RESULTINSTR0.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES5, self).__init__(register,
            'RES5', 'HADM_NS.RESULTINSTR0.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES6, self).__init__(register,
            'RES6', 'HADM_NS.RESULTINSTR0.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR0_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR0_RES7, self).__init__(register,
            'RES7', 'HADM_NS.RESULTINSTR0.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_NS.INSTR00.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_NS.INSTR00.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_NS.INSTR00.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_NS.INSTR00.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_RTT0, self).__init__(register,
            'RTT0', 'HADM_NS.INSTR00.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_NADM0, self).__init__(register,
            'NADM0', 'HADM_NS.INSTR00.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_PBR0, self).__init__(register,
            'PBR0', 'HADM_NS.INSTR00.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_NS.INSTR00.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_NS.INSTR00.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_NS.INSTR00.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR00_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR00_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_NS.INSTR00.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_NS.INSTR10.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_NS.INSTR10.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_NS.INSTR10.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_NS.INSTR10.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_RTT1, self).__init__(register,
            'RTT1', 'HADM_NS.INSTR10.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_NADM1, self).__init__(register,
            'NADM1', 'HADM_NS.INSTR10.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_PBR1, self).__init__(register,
            'PBR1', 'HADM_NS.INSTR10.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_NS.INSTR10.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_NS.INSTR10.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_NS.INSTR10.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR10_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR10_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_NS.INSTR10.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_NS.INSTR20.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_NS.INSTR20.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_NS.INSTR20.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_NS.INSTR20.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_RTT2, self).__init__(register,
            'RTT2', 'HADM_NS.INSTR20.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_NADM2, self).__init__(register,
            'NADM2', 'HADM_NS.INSTR20.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_PBR2, self).__init__(register,
            'PBR2', 'HADM_NS.INSTR20.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_NS.INSTR20.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_NS.INSTR20.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_NS.INSTR20.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR20_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR20_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_NS.INSTR20.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_NS.INSTR30.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_NS.INSTR30.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_NS.INSTR30.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_NS.INSTR30.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_RTT3, self).__init__(register,
            'RTT3', 'HADM_NS.INSTR30.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_NADM3, self).__init__(register,
            'NADM3', 'HADM_NS.INSTR30.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_PBR3, self).__init__(register,
            'PBR3', 'HADM_NS.INSTR30.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_NS.INSTR30.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_NS.INSTR30.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_NS.INSTR30.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR30_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR30_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_NS.INSTR30.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_NS.INSTR40.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_NS.INSTR40.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_NS.INSTR40.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_NS.INSTR40.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_RTT4, self).__init__(register,
            'RTT4', 'HADM_NS.INSTR40.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_NADM4, self).__init__(register,
            'NADM4', 'HADM_NS.INSTR40.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_PBR4, self).__init__(register,
            'PBR4', 'HADM_NS.INSTR40.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_NS.INSTR40.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_NS.INSTR40.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_NS.INSTR40.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR40_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR40_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_NS.INSTR40.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_NS.INSTR50.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_NS.INSTR50.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_NS.INSTR50.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_NS.INSTR50.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_RTT5, self).__init__(register,
            'RTT5', 'HADM_NS.INSTR50.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_NADM5, self).__init__(register,
            'NADM5', 'HADM_NS.INSTR50.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_PBR5, self).__init__(register,
            'PBR5', 'HADM_NS.INSTR50.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_NS.INSTR50.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_NS.INSTR50.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_NS.INSTR50.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR50_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR50_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_NS.INSTR50.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_NS.INSTR60.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_NS.INSTR60.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_NS.INSTR60.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_NS.INSTR60.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_RTT6, self).__init__(register,
            'RTT6', 'HADM_NS.INSTR60.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_NADM6, self).__init__(register,
            'NADM6', 'HADM_NS.INSTR60.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_PBR6, self).__init__(register,
            'PBR6', 'HADM_NS.INSTR60.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_NS.INSTR60.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_NS.INSTR60.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_NS.INSTR60.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR60_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR60_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_NS.INSTR60.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES0, self).__init__(register,
            'RES0', 'HADM_NS.RESULTINSTR1.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES1, self).__init__(register,
            'RES1', 'HADM_NS.RESULTINSTR1.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES2, self).__init__(register,
            'RES2', 'HADM_NS.RESULTINSTR1.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES3, self).__init__(register,
            'RES3', 'HADM_NS.RESULTINSTR1.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES4, self).__init__(register,
            'RES4', 'HADM_NS.RESULTINSTR1.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES5, self).__init__(register,
            'RES5', 'HADM_NS.RESULTINSTR1.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES6, self).__init__(register,
            'RES6', 'HADM_NS.RESULTINSTR1.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR1_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR1_RES7, self).__init__(register,
            'RES7', 'HADM_NS.RESULTINSTR1.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_NS.INSTR01.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_NS.INSTR01.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_NS.INSTR01.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_NS.INSTR01.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_RTT0, self).__init__(register,
            'RTT0', 'HADM_NS.INSTR01.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_NADM0, self).__init__(register,
            'NADM0', 'HADM_NS.INSTR01.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_PBR0, self).__init__(register,
            'PBR0', 'HADM_NS.INSTR01.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_NS.INSTR01.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_NS.INSTR01.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_NS.INSTR01.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR01_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR01_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_NS.INSTR01.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_NS.INSTR11.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_NS.INSTR11.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_NS.INSTR11.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_NS.INSTR11.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_RTT1, self).__init__(register,
            'RTT1', 'HADM_NS.INSTR11.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_NADM1, self).__init__(register,
            'NADM1', 'HADM_NS.INSTR11.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_PBR1, self).__init__(register,
            'PBR1', 'HADM_NS.INSTR11.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_NS.INSTR11.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_NS.INSTR11.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_NS.INSTR11.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR11_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR11_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_NS.INSTR11.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_NS.INSTR21.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_NS.INSTR21.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_NS.INSTR21.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_NS.INSTR21.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_RTT2, self).__init__(register,
            'RTT2', 'HADM_NS.INSTR21.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_NADM2, self).__init__(register,
            'NADM2', 'HADM_NS.INSTR21.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_PBR2, self).__init__(register,
            'PBR2', 'HADM_NS.INSTR21.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_NS.INSTR21.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_NS.INSTR21.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_NS.INSTR21.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR21_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR21_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_NS.INSTR21.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_NS.INSTR31.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_NS.INSTR31.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_NS.INSTR31.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_NS.INSTR31.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_RTT3, self).__init__(register,
            'RTT3', 'HADM_NS.INSTR31.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_NADM3, self).__init__(register,
            'NADM3', 'HADM_NS.INSTR31.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_PBR3, self).__init__(register,
            'PBR3', 'HADM_NS.INSTR31.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_NS.INSTR31.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_NS.INSTR31.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_NS.INSTR31.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR31_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR31_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_NS.INSTR31.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_NS.INSTR41.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_NS.INSTR41.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_NS.INSTR41.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_NS.INSTR41.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_RTT4, self).__init__(register,
            'RTT4', 'HADM_NS.INSTR41.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_NADM4, self).__init__(register,
            'NADM4', 'HADM_NS.INSTR41.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_PBR4, self).__init__(register,
            'PBR4', 'HADM_NS.INSTR41.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_NS.INSTR41.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_NS.INSTR41.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_NS.INSTR41.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR41_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR41_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_NS.INSTR41.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_NS.INSTR51.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_NS.INSTR51.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_NS.INSTR51.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_NS.INSTR51.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_RTT5, self).__init__(register,
            'RTT5', 'HADM_NS.INSTR51.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_NADM5, self).__init__(register,
            'NADM5', 'HADM_NS.INSTR51.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_PBR5, self).__init__(register,
            'PBR5', 'HADM_NS.INSTR51.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_NS.INSTR51.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_NS.INSTR51.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_NS.INSTR51.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR51_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR51_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_NS.INSTR51.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_NS.INSTR61.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_NS.INSTR61.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_NS.INSTR61.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_NS.INSTR61.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_RTT6, self).__init__(register,
            'RTT6', 'HADM_NS.INSTR61.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_NADM6, self).__init__(register,
            'NADM6', 'HADM_NS.INSTR61.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_PBR6, self).__init__(register,
            'PBR6', 'HADM_NS.INSTR61.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_NS.INSTR61.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_NS.INSTR61.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_NS.INSTR61.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR61_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR61_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_NS.INSTR61.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES0, self).__init__(register,
            'RES0', 'HADM_NS.RESULTINSTR2.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES1, self).__init__(register,
            'RES1', 'HADM_NS.RESULTINSTR2.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES2, self).__init__(register,
            'RES2', 'HADM_NS.RESULTINSTR2.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES3, self).__init__(register,
            'RES3', 'HADM_NS.RESULTINSTR2.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES4, self).__init__(register,
            'RES4', 'HADM_NS.RESULTINSTR2.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES5, self).__init__(register,
            'RES5', 'HADM_NS.RESULTINSTR2.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES6, self).__init__(register,
            'RES6', 'HADM_NS.RESULTINSTR2.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR2_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR2_RES7, self).__init__(register,
            'RES7', 'HADM_NS.RESULTINSTR2.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_NS.INSTR02.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_NS.INSTR02.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_NS.INSTR02.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_NS.INSTR02.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_RTT0, self).__init__(register,
            'RTT0', 'HADM_NS.INSTR02.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_NADM0, self).__init__(register,
            'NADM0', 'HADM_NS.INSTR02.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_PBR0, self).__init__(register,
            'PBR0', 'HADM_NS.INSTR02.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_NS.INSTR02.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_NS.INSTR02.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_NS.INSTR02.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR02_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR02_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_NS.INSTR02.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_NS.INSTR12.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_NS.INSTR12.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_NS.INSTR12.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_NS.INSTR12.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_RTT1, self).__init__(register,
            'RTT1', 'HADM_NS.INSTR12.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_NADM1, self).__init__(register,
            'NADM1', 'HADM_NS.INSTR12.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_PBR1, self).__init__(register,
            'PBR1', 'HADM_NS.INSTR12.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_NS.INSTR12.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_NS.INSTR12.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_NS.INSTR12.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR12_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR12_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_NS.INSTR12.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_NS.INSTR22.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_NS.INSTR22.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_NS.INSTR22.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_NS.INSTR22.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_RTT2, self).__init__(register,
            'RTT2', 'HADM_NS.INSTR22.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_NADM2, self).__init__(register,
            'NADM2', 'HADM_NS.INSTR22.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_PBR2, self).__init__(register,
            'PBR2', 'HADM_NS.INSTR22.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_NS.INSTR22.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_NS.INSTR22.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_NS.INSTR22.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR22_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR22_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_NS.INSTR22.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_NS.INSTR32.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_NS.INSTR32.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_NS.INSTR32.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_NS.INSTR32.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_RTT3, self).__init__(register,
            'RTT3', 'HADM_NS.INSTR32.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_NADM3, self).__init__(register,
            'NADM3', 'HADM_NS.INSTR32.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_PBR3, self).__init__(register,
            'PBR3', 'HADM_NS.INSTR32.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_NS.INSTR32.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_NS.INSTR32.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_NS.INSTR32.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR32_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR32_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_NS.INSTR32.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_NS.INSTR42.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_NS.INSTR42.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_NS.INSTR42.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_NS.INSTR42.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_RTT4, self).__init__(register,
            'RTT4', 'HADM_NS.INSTR42.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_NADM4, self).__init__(register,
            'NADM4', 'HADM_NS.INSTR42.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_PBR4, self).__init__(register,
            'PBR4', 'HADM_NS.INSTR42.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_NS.INSTR42.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_NS.INSTR42.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_NS.INSTR42.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR42_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR42_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_NS.INSTR42.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_NS.INSTR52.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_NS.INSTR52.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_NS.INSTR52.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_NS.INSTR52.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_RTT5, self).__init__(register,
            'RTT5', 'HADM_NS.INSTR52.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_NADM5, self).__init__(register,
            'NADM5', 'HADM_NS.INSTR52.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_PBR5, self).__init__(register,
            'PBR5', 'HADM_NS.INSTR52.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_NS.INSTR52.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_NS.INSTR52.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_NS.INSTR52.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR52_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR52_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_NS.INSTR52.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_NS.INSTR62.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_NS.INSTR62.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_NS.INSTR62.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_NS.INSTR62.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_RTT6, self).__init__(register,
            'RTT6', 'HADM_NS.INSTR62.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_NADM6, self).__init__(register,
            'NADM6', 'HADM_NS.INSTR62.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_PBR6, self).__init__(register,
            'PBR6', 'HADM_NS.INSTR62.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_NS.INSTR62.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_NS.INSTR62.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_NS.INSTR62.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR62_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR62_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_NS.INSTR62.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES0, self).__init__(register,
            'RES0', 'HADM_NS.RESULTINSTR3.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES1, self).__init__(register,
            'RES1', 'HADM_NS.RESULTINSTR3.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES2, self).__init__(register,
            'RES2', 'HADM_NS.RESULTINSTR3.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES3, self).__init__(register,
            'RES3', 'HADM_NS.RESULTINSTR3.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES4, self).__init__(register,
            'RES4', 'HADM_NS.RESULTINSTR3.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES5, self).__init__(register,
            'RES5', 'HADM_NS.RESULTINSTR3.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES6, self).__init__(register,
            'RES6', 'HADM_NS.RESULTINSTR3.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_RESULTINSTR3_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_RESULTINSTR3_RES7, self).__init__(register,
            'RES7', 'HADM_NS.RESULTINSTR3.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_NS.INSTR03.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_NS.INSTR03.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_NS.INSTR03.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_NS.INSTR03.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_RTT0, self).__init__(register,
            'RTT0', 'HADM_NS.INSTR03.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_NADM0, self).__init__(register,
            'NADM0', 'HADM_NS.INSTR03.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_PBR0, self).__init__(register,
            'PBR0', 'HADM_NS.INSTR03.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_NS.INSTR03.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_NS.INSTR03.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_NS.INSTR03.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR03_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR03_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_NS.INSTR03.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_NS.INSTR13.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_NS.INSTR13.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_NS.INSTR13.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_NS.INSTR13.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_RTT1, self).__init__(register,
            'RTT1', 'HADM_NS.INSTR13.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_NADM1, self).__init__(register,
            'NADM1', 'HADM_NS.INSTR13.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_PBR1, self).__init__(register,
            'PBR1', 'HADM_NS.INSTR13.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_NS.INSTR13.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_NS.INSTR13.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_NS.INSTR13.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR13_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR13_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_NS.INSTR13.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_NS.INSTR23.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_NS.INSTR23.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_NS.INSTR23.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_NS.INSTR23.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_RTT2, self).__init__(register,
            'RTT2', 'HADM_NS.INSTR23.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_NADM2, self).__init__(register,
            'NADM2', 'HADM_NS.INSTR23.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_PBR2, self).__init__(register,
            'PBR2', 'HADM_NS.INSTR23.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_NS.INSTR23.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_NS.INSTR23.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_NS.INSTR23.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR23_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR23_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_NS.INSTR23.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_NS.INSTR33.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_NS.INSTR33.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_NS.INSTR33.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_NS.INSTR33.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_RTT3, self).__init__(register,
            'RTT3', 'HADM_NS.INSTR33.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_NADM3, self).__init__(register,
            'NADM3', 'HADM_NS.INSTR33.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_PBR3, self).__init__(register,
            'PBR3', 'HADM_NS.INSTR33.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_NS.INSTR33.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_NS.INSTR33.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_NS.INSTR33.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR33_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR33_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_NS.INSTR33.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_NS.INSTR43.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_NS.INSTR43.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_NS.INSTR43.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_NS.INSTR43.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_RTT4, self).__init__(register,
            'RTT4', 'HADM_NS.INSTR43.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_NADM4, self).__init__(register,
            'NADM4', 'HADM_NS.INSTR43.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_PBR4, self).__init__(register,
            'PBR4', 'HADM_NS.INSTR43.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_NS.INSTR43.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_NS.INSTR43.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_NS.INSTR43.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR43_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR43_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_NS.INSTR43.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_NS.INSTR53.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_NS.INSTR53.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_NS.INSTR53.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_NS.INSTR53.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_RTT5, self).__init__(register,
            'RTT5', 'HADM_NS.INSTR53.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_NADM5, self).__init__(register,
            'NADM5', 'HADM_NS.INSTR53.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_PBR5, self).__init__(register,
            'PBR5', 'HADM_NS.INSTR53.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_NS.INSTR53.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_NS.INSTR53.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_NS.INSTR53.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR53_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR53_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_NS.INSTR53.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_NS.INSTR63.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_NS.INSTR63.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_NS.INSTR63.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_NS.INSTR63.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_RTT6, self).__init__(register,
            'RTT6', 'HADM_NS.INSTR63.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_NADM6, self).__init__(register,
            'NADM6', 'HADM_NS.INSTR63.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_PBR6, self).__init__(register,
            'PBR6', 'HADM_NS.INSTR63.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_NS.INSTR63.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_NS.INSTR63.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_NS.INSTR63.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_INSTR63_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_INSTR63_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_NS.INSTR63.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_CTRLSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_CTRLSTATE, self).__init__(register,
            'CTRLSTATE', 'HADM_NS.STATUS0.CTRLSTATE', 'read-only',
            u"",
            0, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_PKTINFOACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_PKTINFOACTIVE, self).__init__(register,
            'PKTINFOACTIVE', 'HADM_NS.STATUS0.PKTINFOACTIVE', 'read-only',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_FREQESTACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_FREQESTACTIVE, self).__init__(register,
            'FREQESTACTIVE', 'HADM_NS.STATUS0.FREQESTACTIVE', 'read-only',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_RTTACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_RTTACTIVE, self).__init__(register,
            'RTTACTIVE', 'HADM_NS.STATUS0.RTTACTIVE', 'read-only',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_NADMACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_NADMACTIVE, self).__init__(register,
            'NADMACTIVE', 'HADM_NS.STATUS0.NADMACTIVE', 'read-only',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_PBRACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_PBRACTIVE, self).__init__(register,
            'PBRACTIVE', 'HADM_NS.STATUS0.PBRACTIVE', 'read-only',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_RESULTSACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_RESULTSACTIVE, self).__init__(register,
            'RESULTSACTIVE', 'HADM_NS.STATUS0.RESULTSACTIVE', 'read-only',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_STARTTASK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_STARTTASK, self).__init__(register,
            'STARTTASK', 'HADM_NS.STATUS0.STARTTASK', 'read-only',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_TASKNUM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_TASKNUM, self).__init__(register,
            'TASKNUM', 'HADM_NS.STATUS0.TASKNUM', 'read-only',
            u"",
            11, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_PC(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_PC, self).__init__(register,
            'PC', 'HADM_NS.STATUS0.PC', 'read-only',
            u"",
            13, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_ANTSWITCHSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_ANTSWITCHSTATE, self).__init__(register,
            'ANTSWITCHSTATE', 'HADM_NS.STATUS0.ANTSWITCHSTATE', 'read-only',
            u"",
            16, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_ANTHADM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_ANTHADM, self).__init__(register,
            'ANTHADM', 'HADM_NS.STATUS0.ANTHADM', 'read-only',
            u"",
            20, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_FREQESTSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_FREQESTSTATE, self).__init__(register,
            'FREQESTSTATE', 'HADM_NS.STATUS0.FREQESTSTATE', 'read-only',
            u"",
            24, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_RTTMAINSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_RTTMAINSTATE, self).__init__(register,
            'RTTMAINSTATE', 'HADM_NS.STATUS0.RTTMAINSTATE', 'read-only',
            u"",
            26, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS0_RTTRBSSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS0_RTTRBSSTATE, self).__init__(register,
            'RTTRBSSTATE', 'HADM_NS.STATUS0.RTTRBSSTATE', 'read-only',
            u"",
            28, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_STARTINSTR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_STARTINSTR, self).__init__(register,
            'STARTINSTR', 'HADM_NS.STATUS1.STARTINSTR', 'read-only',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_DONEINSTR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_DONEINSTR, self).__init__(register,
            'DONEINSTR', 'HADM_NS.STATUS1.DONEINSTR', 'read-only',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_PBRCTRLSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_PBRCTRLSTATE, self).__init__(register,
            'PBRCTRLSTATE', 'HADM_NS.STATUS1.PBRCTRLSTATE', 'read-only',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_PBRTQSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_PBRTQSTATE, self).__init__(register,
            'PBRTQSTATE', 'HADM_NS.STATUS1.PBRTQSTATE', 'read-only',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_PBRGDCOMPSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_PBRGDCOMPSTATE, self).__init__(register,
            'PBRGDCOMPSTATE', 'HADM_NS.STATUS1.PBRGDCOMPSTATE', 'read-only',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_PBRRESSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_PBRRESSTATE, self).__init__(register,
            'PBRRESSTATE', 'HADM_NS.STATUS1.PBRRESSTATE', 'read-only',
            u"",
            15, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS1_RTTRAMSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS1_RTTRAMSTATE, self).__init__(register,
            'RTTRAMSTATE', 'HADM_NS.STATUS1.RTTRAMSTATE', 'read-only',
            u"",
            17, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_CURROPCODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_CURROPCODE, self).__init__(register,
            'CURROPCODE', 'HADM_NS.STATUS2.CURROPCODE', 'read-only',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_RESULTACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_RESULTACTIVE, self).__init__(register,
            'RESULTACTIVE', 'HADM_NS.STATUS2.RESULTACTIVE', 'read-only',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_RESULTDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_RESULTDONE, self).__init__(register,
            'RESULTDONE', 'HADM_NS.STATUS2.RESULTDONE', 'read-only',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_PKTINFOVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_PKTINFOVALID, self).__init__(register,
            'PKTINFOVALID', 'HADM_NS.STATUS2.PKTINFOVALID', 'read-only',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_FREQESTVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_FREQESTVALID, self).__init__(register,
            'FREQESTVALID', 'HADM_NS.STATUS2.FREQESTVALID', 'read-only',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_PBRRXVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_PBRRXVALID, self).__init__(register,
            'PBRRXVALID', 'HADM_NS.STATUS2.PBRRXVALID', 'read-only',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_RTTVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_RTTVALID, self).__init__(register,
            'RTTVALID', 'HADM_NS.STATUS2.RTTVALID', 'read-only',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_NADMVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_NADMVALID, self).__init__(register,
            'NADMVALID', 'HADM_NS.STATUS2.NADMVALID', 'read-only',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS2_BUFHANDLERSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS2_BUFHANDLERSTATE, self).__init__(register,
            'BUFHANDLERSTATE', 'HADM_NS.STATUS2.BUFHANDLERSTATE', 'read-only',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS3_TARGETPRECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS3_TARGETPRECNT, self).__init__(register,
            'TARGETPRECNT', 'HADM_NS.STATUS3.TARGETPRECNT', 'read-only',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS4_TARGETBASECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS4_TARGETBASECNT, self).__init__(register,
            'TARGETBASECNT', 'HADM_NS.STATUS4.TARGETBASECNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS5_TARGETWRAPCNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS5_TARGETWRAPCNT, self).__init__(register,
            'TARGETWRAPCNT', 'HADM_NS.STATUS5.TARGETWRAPCNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS6_ADVTARGETBASECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS6_ADVTARGETBASECNT, self).__init__(register,
            'ADVTARGETBASECNT', 'HADM_NS.STATUS6.ADVTARGETBASECNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_NS_STATUS7_ADVTARGETWRAPCNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_NS_STATUS7_ADVTARGETWRAPCNT, self).__init__(register,
            'ADVTARGETWRAPCNT', 'HADM_NS.STATUS7.ADVTARGETWRAPCNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


