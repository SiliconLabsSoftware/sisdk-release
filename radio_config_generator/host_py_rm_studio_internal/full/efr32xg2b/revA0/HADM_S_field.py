
# -*- coding: utf-8 -*-

from . static import Base_RM_Field


class RM_Field_HADM_S_IPVERSION_IPVERSION(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IPVERSION_IPVERSION, self).__init__(register,
            'IPVERSION', 'HADM_S.IPVERSION.IPVERSION', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_EN_EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_EN_EN, self).__init__(register,
            'EN', 'HADM_S.EN.EN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_S.IEN.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_S.IEN.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_S.IEN.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_S.IEN.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_S.IEN.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_S.IEN.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_S.IEN.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_S.IEN.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_PBROF, self).__init__(register,
            'PBROF', 'HADM_S.IEN.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_S.IEN.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_S.IEN.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_S.IEN.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_S.IEN.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_S.IEN.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_S.IEN.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_S.IEN.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_S.IEN.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_S.IEN.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_S.IEN.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_S.IEN.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IEN_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IEN_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_S.IEN.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_S.IF.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_S.IF.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_S.IF.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_S.IF.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_S.IF.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_S.IF.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_S.IF.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_S.IF.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_PBROF, self).__init__(register,
            'PBROF', 'HADM_S.IF.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_S.IF.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_S.IF.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_S.IF.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_S.IF.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_S.IF.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_S.IF.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_S.IF.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_S.IF.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_S.IF.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_S.IF.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_S.IF.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_IF_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_IF_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_S.IF.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_S.SEQIEN.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_S.SEQIEN.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_S.SEQIEN.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_S.SEQIEN.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_S.SEQIEN.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_S.SEQIEN.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_S.SEQIEN.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_S.SEQIEN.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_PBROF, self).__init__(register,
            'PBROF', 'HADM_S.SEQIEN.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_S.SEQIEN.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_S.SEQIEN.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_S.SEQIEN.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_S.SEQIEN.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_S.SEQIEN.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_S.SEQIEN.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_S.SEQIEN.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_S.SEQIEN.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_S.SEQIEN.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_S.SEQIEN.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_S.SEQIEN.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIEN_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIEN_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_S.SEQIEN.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_S.SEQIF.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_S.SEQIF.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_S.SEQIF.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_S.SEQIF.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_S.SEQIF.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_S.SEQIF.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_S.SEQIF.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_S.SEQIF.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_PBROF, self).__init__(register,
            'PBROF', 'HADM_S.SEQIF.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_S.SEQIF.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_S.SEQIF.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_S.SEQIF.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_S.SEQIF.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_S.SEQIF.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_S.SEQIF.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_S.SEQIF.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_S.SEQIF.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_S.SEQIF.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_S.SEQIF.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_S.SEQIF.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SEQIF_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SEQIF_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_S.SEQIF.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_S.FSWIEN.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_S.FSWIEN.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_S.FSWIEN.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_S.FSWIEN.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_S.FSWIEN.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_S.FSWIEN.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_S.FSWIEN.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_S.FSWIEN.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_PBROF, self).__init__(register,
            'PBROF', 'HADM_S.FSWIEN.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_S.FSWIEN.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_S.FSWIEN.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_S.FSWIEN.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_S.FSWIEN.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_S.FSWIEN.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_S.FSWIEN.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_S.FSWIEN.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_S.FSWIEN.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_S.FSWIEN.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_S.FSWIEN.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_S.FSWIEN.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIEN_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIEN_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_S.FSWIEN.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_BUFOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_BUFOF, self).__init__(register,
            'BUFOF', 'HADM_S.FSWIF.BUFOF', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_BUFTHR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_BUFTHR, self).__init__(register,
            'BUFTHR', 'HADM_S.FSWIF.BUFTHR', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_BUSERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_BUSERROR, self).__init__(register,
            'BUSERROR', 'HADM_S.FSWIF.BUSERROR', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_FRAMEDET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_FRAMEDET, self).__init__(register,
            'FRAMEDET', 'HADM_S.FSWIF.FRAMEDET', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_PKTINFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_PKTINFOOF, self).__init__(register,
            'PKTINFOOF', 'HADM_S.FSWIF.PKTINFOOF', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_FREQESTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_FREQESTOF, self).__init__(register,
            'FREQESTOF', 'HADM_S.FSWIF.FREQESTOF', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_RTTOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_RTTOF, self).__init__(register,
            'RTTOF', 'HADM_S.FSWIF.RTTOF', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_NADMOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_NADMOF, self).__init__(register,
            'NADMOF', 'HADM_S.FSWIF.NADMOF', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_PBROF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_PBROF, self).__init__(register,
            'PBROF', 'HADM_S.FSWIF.PBROF', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_RESULTSOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_RESULTSOF, self).__init__(register,
            'RESULTSOF', 'HADM_S.FSWIF.RESULTSOF', 'read-write',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_TIMERERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_TIMERERR, self).__init__(register,
            'TIMERERR', 'HADM_S.FSWIF.TIMERERR', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_ANTSWERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_ANTSWERR, self).__init__(register,
            'ANTSWERR', 'HADM_S.FSWIF.ANTSWERR', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_TIMEOUTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_TIMEOUTERR, self).__init__(register,
            'TIMEOUTERR', 'HADM_S.FSWIF.TIMEOUTERR', 'read-write',
            u"",
            12, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_RSLTINSTRERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_RSLTINSTRERR, self).__init__(register,
            'RSLTINSTRERR', 'HADM_S.FSWIF.RSLTINSTRERR', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_TASKSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_TASKSTART, self).__init__(register,
            'TASKSTART', 'HADM_S.FSWIF.TASKSTART', 'read-write',
            u"",
            14, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_TASKDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_TASKDONE, self).__init__(register,
            'TASKDONE', 'HADM_S.FSWIF.TASKDONE', 'read-write',
            u"",
            15, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_TASKSTARTERR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_TASKSTARTERR, self).__init__(register,
            'TASKSTARTERR', 'HADM_S.FSWIF.TASKSTARTERR', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_RESULTSDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_RESULTSDONE, self).__init__(register,
            'RESULTSDONE', 'HADM_S.FSWIF.RESULTSDONE', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_INSTRSTART(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_INSTRSTART, self).__init__(register,
            'INSTRSTART', 'HADM_S.FSWIF.INSTRSTART', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_INSTRDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_INSTRDONE, self).__init__(register,
            'INSTRDONE', 'HADM_S.FSWIF.INSTRDONE', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_FSWIF_RESULTFIFOOF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_FSWIF_RESULTFIFOOF, self).__init__(register,
            'RESULTFIFOOF', 'HADM_S.FSWIF.RESULTFIFOOF', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CMD_START(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CMD_START, self).__init__(register,
            'START', 'HADM_S.CMD.START', 'write-only',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CMD_STOP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CMD_STOP, self).__init__(register,
            'STOP', 'HADM_S.CMD.STOP', 'write-only',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CMD_FORCECTRL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CMD_FORCECTRL, self).__init__(register,
            'FORCECTRL', 'HADM_S.CMD.FORCECTRL', 'write-only',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CMD_RSTANTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CMD_RSTANTSEL, self).__init__(register,
            'RSTANTSEL', 'HADM_S.CMD.RSTANTSEL', 'write-only',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CMD_CLEAR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CMD_CLEAR, self).__init__(register,
            'CLEAR', 'HADM_S.CMD.CLEAR', 'write-only',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CMD_FLUSH(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CMD_FLUSH, self).__init__(register,
            'FLUSH', 'HADM_S.CMD.FLUSH', 'write-only',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_ROLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_ROLE, self).__init__(register,
            'ROLE', 'HADM_S.CTRL0.ROLE', 'read-write',
            u"",
            0, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_PHYSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_PHYSEL, self).__init__(register,
            'PHYSEL', 'HADM_S.CTRL0.PHYSEL', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_SSAFCGEAR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_SSAFCGEAR, self).__init__(register,
            'SSAFCGEAR', 'HADM_S.CTRL0.SSAFCGEAR', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_TXUPSAMPOSR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_TXUPSAMPOSR4, self).__init__(register,
            'TXUPSAMPOSR4', 'HADM_S.CTRL0.TXUPSAMPOSR4', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_TGUARDPERIOD(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_TGUARDPERIOD, self).__init__(register,
            'TGUARDPERIOD', 'HADM_S.CTRL0.TGUARDPERIOD', 'read-write',
            u"",
            6, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_AVGSTARTOFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_AVGSTARTOFF, self).__init__(register,
            'AVGSTARTOFF', 'HADM_S.CTRL0.AVGSTARTOFF', 'read-write',
            u"",
            10, 10)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_OWRRSTDLO(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_OWRRSTDLO, self).__init__(register,
            'OWRRSTDLO', 'HADM_S.CTRL0.OWRRSTDLO', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_GDCOMPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_GDCOMPEN, self).__init__(register,
            'GDCOMPEN', 'HADM_S.CTRL0.GDCOMPEN', 'read-write',
            u"",
            21, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_CTRLMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_CTRLMODE, self).__init__(register,
            'CTRLMODE', 'HADM_S.CTRL0.CTRLMODE', 'read-write',
            u"",
            22, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_WAITONERROR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_WAITONERROR, self).__init__(register,
            'WAITONERROR', 'HADM_S.CTRL0.WAITONERROR', 'read-write',
            u"",
            23, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_CTRL0_TFM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_CTRL0_TFM, self).__init__(register,
            'TFM', 'HADM_S.CTRL0.TFM', 'read-write',
            u"",
            24, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_RTTMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_RTTMODE, self).__init__(register,
            'RTTMODE', 'HADM_S.RTTCTRL0.RTTMODE', 'read-write',
            u"",
            0, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_RTTLEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_RTTLEN, self).__init__(register,
            'RTTLEN', 'HADM_S.RTTCTRL0.RTTLEN', 'read-write',
            u"",
            2, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_PESEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_PESEN, self).__init__(register,
            'PESEN', 'HADM_S.RTTCTRL0.PESEN', 'read-write',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_SNDSEQEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_SNDSEQEN, self).__init__(register,
            'SNDSEQEN', 'HADM_S.RTTCTRL0.SNDSEQEN', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_PKTSENTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_PKTSENTSEL, self).__init__(register,
            'PKTSENTSEL', 'HADM_S.RTTCTRL0.PKTSENTSEL', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_DFTSCALE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_DFTSCALE, self).__init__(register,
            'DFTSCALE', 'HADM_S.RTTCTRL0.DFTSCALE', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_RBSTRACKNUM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_RBSTRACKNUM, self).__init__(register,
            'RBSTRACKNUM', 'HADM_S.RTTCTRL0.RBSTRACKNUM', 'read-write',
            u"",
            11, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_DFTSTARTOFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_DFTSTARTOFF, self).__init__(register,
            'DFTSTARTOFF', 'HADM_S.RTTCTRL0.DFTSTARTOFF', 'read-write',
            u"",
            14, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_RTTTIMEOUT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_RTTTIMEOUT, self).__init__(register,
            'RTTTIMEOUT', 'HADM_S.RTTCTRL0.RTTTIMEOUT', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL0_MAXSCHWIN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL0_MAXSCHWIN, self).__init__(register,
            'MAXSCHWIN', 'HADM_S.RTTCTRL0.MAXSCHWIN', 'read-write',
            u"",
            24, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_TRECSOSR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_TRECSOSR, self).__init__(register,
            'TRECSOSR', 'HADM_S.RTTCTRL1.TRECSOSR', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_RAMRADDRBACK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_RAMRADDRBACK, self).__init__(register,
            'RAMRADDRBACK', 'HADM_S.RTTCTRL1.RAMRADDRBACK', 'read-write',
            u"",
            1, 9)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_FRAMEDETSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_FRAMEDETSEL, self).__init__(register,
            'FRAMEDETSEL', 'HADM_S.RTTCTRL1.FRAMEDETSEL', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_FRAMEDETTIMEOUT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_FRAMEDETTIMEOUT, self).__init__(register,
            'FRAMEDETTIMEOUT', 'HADM_S.RTTCTRL1.FRAMEDETTIMEOUT', 'read-write',
            u"",
            11, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_SBFLIPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_SBFLIPEN, self).__init__(register,
            'SBFLIPEN', 'HADM_S.RTTCTRL1.SBFLIPEN', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_EPLBWREN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_EPLBWREN, self).__init__(register,
            'EPLBWREN', 'HADM_S.RTTCTRL1.EPLBWREN', 'read-write',
            u"",
            20, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_SSPMSWAPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_SSPMSWAPEN, self).__init__(register,
            'SSPMSWAPEN', 'HADM_S.RTTCTRL1.SSPMSWAPEN', 'read-write',
            u"",
            21, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_XOSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_XOSEL, self).__init__(register,
            'XOSEL', 'HADM_S.RTTCTRL1.XOSEL', 'read-write',
            u"",
            22, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_ELSWAPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_ELSWAPEN, self).__init__(register,
            'ELSWAPEN', 'HADM_S.RTTCTRL1.ELSWAPEN', 'read-write',
            u"",
            24, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_CORRACCDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_CORRACCDLY, self).__init__(register,
            'CORRACCDLY', 'HADM_S.RTTCTRL1.CORRACCDLY', 'read-write',
            u"",
            25, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_SSDFTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_SSDFTEN, self).__init__(register,
            'SSDFTEN', 'HADM_S.RTTCTRL1.SSDFTEN', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_TIMEROWEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_TIMEROWEN, self).__init__(register,
            'TIMEROWEN', 'HADM_S.RTTCTRL1.TIMEROWEN', 'read-write',
            u"",
            30, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL1_FBROCEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL1_FBROCEN, self).__init__(register,
            'FBROCEN', 'HADM_S.RTTCTRL1.FBROCEN', 'read-write',
            u"",
            31, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_FBROCMUL2EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_FBROCMUL2EN, self).__init__(register,
            'FBROCMUL2EN', 'HADM_S.RTTCTRL2.FBROCMUL2EN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_TIMERDETSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_TIMERDETSEL, self).__init__(register,
            'TIMERDETSEL', 'HADM_S.RTTCTRL2.TIMERDETSEL', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_FLIPEPL1EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_FLIPEPL1EN, self).__init__(register,
            'FLIPEPL1EN', 'HADM_S.RTTCTRL2.FLIPEPL1EN', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_FLIPEPL2EN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_FLIPEPL2EN, self).__init__(register,
            'FLIPEPL2EN', 'HADM_S.RTTCTRL2.FLIPEPL2EN', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_SINGLEPKTMODEEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_SINGLEPKTMODEEN, self).__init__(register,
            'SINGLEPKTMODEEN', 'HADM_S.RTTCTRL2.SINGLEPKTMODEEN', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_SRCMUREFBACK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_SRCMUREFBACK, self).__init__(register,
            'SRCMUREFBACK', 'HADM_S.RTTCTRL2.SRCMUREFBACK', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_SSFFOLEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_SSFFOLEN, self).__init__(register,
            'SSFFOLEN', 'HADM_S.RTTCTRL2.SSFFOLEN', 'read-write',
            u"",
            8, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTCTRL2_SRCCOMPSAMPSKIPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTCTRL2_SRCCOMPSAMPSKIPEN, self).__init__(register,
            'SRCCOMPSAMPSKIPEN', 'HADM_S.RTTCTRL2.SRCCOMPSAMPSKIPEN', 'read-write',
            u"",
            16, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTTUNE_RTTINITTUNE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTTUNE_RTTINITTUNE, self).__init__(register,
            'RTTINITTUNE', 'HADM_S.RTTTUNE.RTTINITTUNE', 'read-write',
            u"",
            0, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTTUNE_RTTREFLTUNE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTTUNE_RTTREFLTUNE, self).__init__(register,
            'RTTREFLTUNE', 'HADM_S.RTTTUNE.RTTREFLTUNE', 'read-write',
            u"",
            12, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME0_REFBACKSYMB(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME0_REFBACKSYMB, self).__init__(register,
            'REFBACKSYMB', 'HADM_S.RTTRPTTIME0.REFBACKSYMB', 'read-write',
            u"",
            0, 6)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME0_REFBACKCYCLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME0_REFBACKCYCLE, self).__init__(register,
            'REFBACKCYCLE', 'HADM_S.RTTRPTTIME0.REFBACKCYCLE', 'read-write',
            u"",
            6, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME0_GROUPDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME0_GROUPDLY, self).__init__(register,
            'GROUPDLY', 'HADM_S.RTTRPTTIME0.GROUPDLY', 'read-write',
            u"",
            10, 11)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME0_RTTTIP1IDX(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME0_RTTTIP1IDX, self).__init__(register,
            'RTTTIP1IDX', 'HADM_S.RTTRPTTIME0.RTTTIP1IDX', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME0_FLTDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME0_FLTDLY, self).__init__(register,
            'FLTDLY', 'HADM_S.RTTRPTTIME0.FLTDLY', 'read-write',
            u"",
            24, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME1_FFO(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME1_FFO, self).__init__(register,
            'FFO', 'HADM_S.RTTRPTTIME1.FFO', 'read-write',
            u"",
            0, 13)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME1_COARSETIMEOW(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME1_COARSETIMEOW, self).__init__(register,
            'COARSETIMEOW', 'HADM_S.RTTRPTTIME1.COARSETIMEOW', 'read-write',
            u"",
            13, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTRPTTIME1_SSFFONEG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTRPTTIME1_SSFFONEG, self).__init__(register,
            'SSFFONEG', 'HADM_S.RTTRPTTIME1.SSFFONEG', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTPKT0_RTTPAYLOAD0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTPKT0_RTTPAYLOAD0, self).__init__(register,
            'RTTPAYLOAD0', 'HADM_S.RTTPKT0.RTTPAYLOAD0', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTPKT1_RTTPAYLOAD1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTPKT1_RTTPAYLOAD1, self).__init__(register,
            'RTTPAYLOAD1', 'HADM_S.RTTPKT1.RTTPAYLOAD1', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTPKT2_RTTPAYLOAD2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTPKT2_RTTPAYLOAD2, self).__init__(register,
            'RTTPAYLOAD2', 'HADM_S.RTTPKT2.RTTPAYLOAD2', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RTTPKT3_RTTPAYLOAD3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RTTPKT3_RTTPAYLOAD3, self).__init__(register,
            'RTTPAYLOAD3', 'HADM_S.RTTPKT3.RTTPAYLOAD3', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_AVGMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_AVGMODE, self).__init__(register,
            'AVGMODE', 'HADM_S.PBRCTRL0.AVGMODE', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_PM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_PM, self).__init__(register,
            'PM', 'HADM_S.PBRCTRL0.PM', 'read-write',
            u"",
            1, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_TEXCL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_TEXCL, self).__init__(register,
            'TEXCL', 'HADM_S.PBRCTRL0.TEXCL', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_TSWITCH(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_TSWITCH, self).__init__(register,
            'TSWITCH', 'HADM_S.PBRCTRL0.TSWITCH', 'read-write',
            u"",
            6, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_TGRPDLY(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_TGRPDLY, self).__init__(register,
            'TGRPDLY', 'HADM_S.PBRCTRL0.TGRPDLY', 'read-write',
            u"",
            10, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_ACI(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_ACI, self).__init__(register,
            'ACI', 'HADM_S.PBRCTRL0.ACI', 'read-write',
            u"",
            14, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_API(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_API, self).__init__(register,
            'API', 'HADM_S.PBRCTRL0.API', 'read-write',
            u"",
            17, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL0_TONEQUALITYTHRESH(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL0_TONEQUALITYTHRESH, self).__init__(register,
            'TONEQUALITYTHRESH', 'HADM_S.PBRCTRL0.TONEQUALITYTHRESH', 'read-write',
            u"",
            22, 10)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_CHNO(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_CHNO, self).__init__(register,
            'CHNO', 'HADM_S.PBRCTRL1.CHNO', 'read-write',
            u"",
            0, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_DCMEASEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_DCMEASEN, self).__init__(register,
            'DCMEASEN', 'HADM_S.PBRCTRL1.DCMEASEN', 'read-write',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_DCMEASMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_DCMEASMODE, self).__init__(register,
            'DCMEASMODE', 'HADM_S.PBRCTRL1.DCMEASMODE', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_DCMEASWIN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_DCMEASWIN, self).__init__(register,
            'DCMEASWIN', 'HADM_S.PBRCTRL1.DCMEASWIN', 'read-write',
            u"",
            9, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_EMPTYPCTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_EMPTYPCTEN, self).__init__(register,
            'EMPTYPCTEN', 'HADM_S.PBRCTRL1.EMPTYPCTEN', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_TONEQUALITYSCALE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_TONEQUALITYSCALE, self).__init__(register,
            'TONEQUALITYSCALE', 'HADM_S.PBRCTRL1.TONEQUALITYSCALE', 'read-write',
            u"",
            14, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_INLINEPCTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_INLINEPCTEN, self).__init__(register,
            'INLINEPCTEN', 'HADM_S.PBRCTRL1.INLINEPCTEN', 'read-write',
            u"",
            18, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_PBRLIFEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_PBRLIFEN, self).__init__(register,
            'PBRLIFEN', 'HADM_S.PBRCTRL1.PBRLIFEN', 'read-write',
            u"",
            19, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRCTRL1_TPULSE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRCTRL1_TPULSE, self).__init__(register,
            'TPULSE', 'HADM_S.PBRCTRL1.TPULSE', 'read-write',
            u"",
            20, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRDCCOMP_DCCOMPI(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRDCCOMP_DCCOMPI, self).__init__(register,
            'DCCOMPI', 'HADM_S.PBRDCCOMP.DCCOMPI', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRDCCOMP_DCCOMPQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRDCCOMP_DCCOMPQ, self).__init__(register,
            'DCCOMPQ', 'HADM_S.PBRDCCOMP.DCCOMPQ', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRGDCOMP0_PHASEPERCHANNEL0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRGDCOMP0_PHASEPERCHANNEL0, self).__init__(register,
            'PHASEPERCHANNEL0', 'HADM_S.PBRGDCOMP0.PHASEPERCHANNEL0', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRGDCOMP0_PHASEPERCHANNEL1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRGDCOMP0_PHASEPERCHANNEL1, self).__init__(register,
            'PHASEPERCHANNEL1', 'HADM_S.PBRGDCOMP0.PHASEPERCHANNEL1', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRGDCOMP1_PHASEPERCHANNEL2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRGDCOMP1_PHASEPERCHANNEL2, self).__init__(register,
            'PHASEPERCHANNEL2', 'HADM_S.PBRGDCOMP1.PHASEPERCHANNEL2', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRGDCOMP1_PHASEPERCHANNEL3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRGDCOMP1_PHASEPERCHANNEL3, self).__init__(register,
            'PHASEPERCHANNEL3', 'HADM_S.PBRGDCOMP1.PHASEPERCHANNEL3', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRRAMPCTRL_RAMPEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRRAMPCTRL_RAMPEN, self).__init__(register,
            'RAMPEN', 'HADM_S.PBRRAMPCTRL.RAMPEN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRRAMPCTRL_TRAMPPRETRIG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRRAMPCTRL_TRAMPPRETRIG, self).__init__(register,
            'TRAMPPRETRIG', 'HADM_S.PBRRAMPCTRL.TRAMPPRETRIG', 'read-write',
            u"",
            1, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRRAMPCTRL_TRAMPPOSTTRIG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRRAMPCTRL_TRAMPPOSTTRIG, self).__init__(register,
            'TRAMPPOSTTRIG', 'HADM_S.PBRRAMPCTRL.TRAMPPOSTTRIG', 'read-write',
            u"",
            8, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRRAMPCTRL_TRAMP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRRAMPCTRL_TRAMP, self).__init__(register,
            'TRAMP', 'HADM_S.PBRRAMPCTRL.TRAMP', 'read-write',
            u"",
            12, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PBRRAMPCTRL_TRAMPSW(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PBRRAMPCTRL_TRAMPSW, self).__init__(register,
            'TRAMPSW', 'HADM_S.PBRRAMPCTRL.TRAMPSW', 'read-write',
            u"",
            16, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_ANTCTRL_ANTPATTHADM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_ANTCTRL_ANTPATTHADM, self).__init__(register,
            'ANTPATTHADM', 'HADM_S.ANTCTRL.ANTPATTHADM', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_ANTCTRL_CSSYNCNUMANT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_ANTCTRL_CSSYNCNUMANT, self).__init__(register,
            'CSSYNCNUMANT', 'HADM_S.ANTCTRL.CSSYNCNUMANT', 'read-write',
            u"",
            16, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_ANTCTRL_CSSYNCANTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_ANTCTRL_CSSYNCANTSEL, self).__init__(register,
            'CSSYNCANTSEL', 'HADM_S.ANTCTRL.CSSYNCANTSEL', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_ANTCTRL_DCMEASANTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_ANTCTRL_DCMEASANTSEL, self).__init__(register,
            'DCMEASANTSEL', 'HADM_S.ANTCTRL.DCMEASANTSEL', 'read-write',
            u"",
            21, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_ANTCTRL_ANTSWITCHADVANCE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_ANTCTRL_ANTSWITCHADVANCE, self).__init__(register,
            'ANTSWITCHADVANCE', 'HADM_S.ANTCTRL.ANTSWITCHADVANCE', 'read-write',
            u"",
            23, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PRSSEL_DBGSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PRSSEL_DBGSEL, self).__init__(register,
            'DBGSEL', 'HADM_S.PRSSEL.DBGSEL', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PRSSEL_RTTSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PRSSEL_RTTSEL, self).__init__(register,
            'RTTSEL', 'HADM_S.PRSSEL.RTTSEL', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PRSSEL_PBRSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PRSSEL_PBRSEL, self).__init__(register,
            'PBRSEL', 'HADM_S.PRSSEL.PBRSEL', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PRSSEL_RXSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PRSSEL_RXSEL, self).__init__(register,
            'RXSEL', 'HADM_S.PRSSEL.RXSEL', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PRSSEL_TXSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PRSSEL_TXSEL, self).__init__(register,
            'TXSEL', 'HADM_S.PRSSEL.TXSEL', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_PRSSEL_CTRLSEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_PRSSEL_CTRLSEL, self).__init__(register,
            'CTRLSEL', 'HADM_S.PRSSEL.CTRLSEL', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RFECASEL_ECAMODESEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RFECASEL_ECAMODESEL, self).__init__(register,
            'ECAMODESEL', 'HADM_S.RFECASEL.ECAMODESEL', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RFECASEL_RESULTECASEL(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RFECASEL_RESULTECASEL, self).__init__(register,
            'RESULTECASEL', 'HADM_S.RFECASEL.RESULTECASEL', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_NADMDIFFD(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_NADMDIFFD, self).__init__(register,
            'NADMDIFFD', 'HADM_S.NADMCONFIG.NADMDIFFD', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_RECREWINDSAMPLES(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_RECREWINDSAMPLES, self).__init__(register,
            'RECREWINDSAMPLES', 'HADM_S.NADMCONFIG.RECREWINDSAMPLES', 'read-write',
            u"",
            2, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_REFMAPFSK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_REFMAPFSK, self).__init__(register,
            'REFMAPFSK', 'HADM_S.NADMCONFIG.REFMAPFSK', 'read-write',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_FORCEFRAC(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_FORCEFRAC, self).__init__(register,
            'FORCEFRAC', 'HADM_S.NADMCONFIG.FORCEFRAC', 'read-write',
            u"",
            11, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_FORCEDFRAC(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_FORCEDFRAC, self).__init__(register,
            'FORCEDFRAC', 'HADM_S.NADMCONFIG.FORCEDFRAC', 'read-write',
            u"",
            12, 7)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_SNRNUMFASTSAMPLES(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_SNRNUMFASTSAMPLES, self).__init__(register,
            'SNRNUMFASTSAMPLES', 'HADM_S.NADMCONFIG.SNRNUMFASTSAMPLES', 'read-write',
            u"",
            19, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_SNRFASTCOEFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_SNRFASTCOEFF, self).__init__(register,
            'SNRFASTCOEFF', 'HADM_S.NADMCONFIG.SNRFASTCOEFF', 'read-write',
            u"",
            22, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_NADMCONFIG_SNRSLOWCOEFF(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_NADMCONFIG_SNRSLOWCOEFF, self).__init__(register,
            'SNRSLOWCOEFF', 'HADM_S.NADMCONFIG.SNRSLOWCOEFF', 'read-write',
            u"",
            26, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_MSEPEARSONMASK_MSEPEARSONMASK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_MSEPEARSONMASK_MSEPEARSONMASK, self).__init__(register,
            'MSEPEARSONMASK', 'HADM_S.MSEPEARSONMASK.MSEPEARSONMASK', 'read-write',
            u"",
            0, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_DFTAMFREQ_DFTAMFREQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_DFTAMFREQ_DFTAMFREQ, self).__init__(register,
            'DFTAMFREQ', 'HADM_S.DFTAMFREQ.DFTAMFREQ', 'read-write',
            u"",
            0, 20)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_DFTECLDFREQ_DFTECLDFREQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_DFTECLDFREQ_DFTECLDFREQ, self).__init__(register,
            'DFTECLDFREQ', 'HADM_S.DFTECLDFREQ.DFTECLDFREQ', 'read-write',
            u"",
            0, 20)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG0_REFGENCOEFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG0_REFGENCOEFF0, self).__init__(register,
            'REFGENCOEFF0', 'HADM_S.REFGENCOEFFG0.REFGENCOEFF0', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG0_REFGENCOEFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG0_REFGENCOEFF1, self).__init__(register,
            'REFGENCOEFF1', 'HADM_S.REFGENCOEFFG0.REFGENCOEFF1', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG1_REFGENCOEFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG1_REFGENCOEFF2, self).__init__(register,
            'REFGENCOEFF2', 'HADM_S.REFGENCOEFFG1.REFGENCOEFF2', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG1_REFGENCOEFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG1_REFGENCOEFF3, self).__init__(register,
            'REFGENCOEFF3', 'HADM_S.REFGENCOEFFG1.REFGENCOEFF3', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG2_REFGENCOEFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG2_REFGENCOEFF4, self).__init__(register,
            'REFGENCOEFF4', 'HADM_S.REFGENCOEFFG2.REFGENCOEFF4', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG2_REFGENCOEFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG2_REFGENCOEFF5, self).__init__(register,
            'REFGENCOEFF5', 'HADM_S.REFGENCOEFFG2.REFGENCOEFF5', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG3_REFGENCOEFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG3_REFGENCOEFF6, self).__init__(register,
            'REFGENCOEFF6', 'HADM_S.REFGENCOEFFG3.REFGENCOEFF6', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG3_REFGENCOEFF7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG3_REFGENCOEFF7, self).__init__(register,
            'REFGENCOEFF7', 'HADM_S.REFGENCOEFFG3.REFGENCOEFF7', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG4_REFGENCOEFF8(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG4_REFGENCOEFF8, self).__init__(register,
            'REFGENCOEFF8', 'HADM_S.REFGENCOEFFG4.REFGENCOEFF8', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG4_REFGENCOEFF9(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG4_REFGENCOEFF9, self).__init__(register,
            'REFGENCOEFF9', 'HADM_S.REFGENCOEFFG4.REFGENCOEFF9', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG5_REFGENCOEFF10(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG5_REFGENCOEFF10, self).__init__(register,
            'REFGENCOEFF10', 'HADM_S.REFGENCOEFFG5.REFGENCOEFF10', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG5_REFGENCOEFF11(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG5_REFGENCOEFF11, self).__init__(register,
            'REFGENCOEFF11', 'HADM_S.REFGENCOEFFG5.REFGENCOEFF11', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG6_REFGENCOEFF12(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG6_REFGENCOEFF12, self).__init__(register,
            'REFGENCOEFF12', 'HADM_S.REFGENCOEFFG6.REFGENCOEFF12', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG6_REFGENCOEFF13(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG6_REFGENCOEFF13, self).__init__(register,
            'REFGENCOEFF13', 'HADM_S.REFGENCOEFFG6.REFGENCOEFF13', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG7_REFGENCOEFF14(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG7_REFGENCOEFF14, self).__init__(register,
            'REFGENCOEFF14', 'HADM_S.REFGENCOEFFG7.REFGENCOEFF14', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG7_REFGENCOEFF15(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG7_REFGENCOEFF15, self).__init__(register,
            'REFGENCOEFF15', 'HADM_S.REFGENCOEFFG7.REFGENCOEFF15', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG8_REFGENCOEFF16(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG8_REFGENCOEFF16, self).__init__(register,
            'REFGENCOEFF16', 'HADM_S.REFGENCOEFFG8.REFGENCOEFF16', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG8_REFGENCOEFF17(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG8_REFGENCOEFF17, self).__init__(register,
            'REFGENCOEFF17', 'HADM_S.REFGENCOEFFG8.REFGENCOEFF17', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG9_REFGENCOEFF18(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG9_REFGENCOEFF18, self).__init__(register,
            'REFGENCOEFF18', 'HADM_S.REFGENCOEFFG9.REFGENCOEFF18', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG9_REFGENCOEFF19(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG9_REFGENCOEFF19, self).__init__(register,
            'REFGENCOEFF19', 'HADM_S.REFGENCOEFFG9.REFGENCOEFF19', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG10_REFGENCOEFF20(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG10_REFGENCOEFF20, self).__init__(register,
            'REFGENCOEFF20', 'HADM_S.REFGENCOEFFG10.REFGENCOEFF20', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG10_REFGENCOEFF21(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG10_REFGENCOEFF21, self).__init__(register,
            'REFGENCOEFF21', 'HADM_S.REFGENCOEFFG10.REFGENCOEFF21', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG11_REFGENCOEFF22(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG11_REFGENCOEFF22, self).__init__(register,
            'REFGENCOEFF22', 'HADM_S.REFGENCOEFFG11.REFGENCOEFF22', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG11_REFGENCOEFF23(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG11_REFGENCOEFF23, self).__init__(register,
            'REFGENCOEFF23', 'HADM_S.REFGENCOEFFG11.REFGENCOEFF23', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG12_REFGENCOEFF24(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG12_REFGENCOEFF24, self).__init__(register,
            'REFGENCOEFF24', 'HADM_S.REFGENCOEFFG12.REFGENCOEFF24', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG12_REFGENCOEFF25(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG12_REFGENCOEFF25, self).__init__(register,
            'REFGENCOEFF25', 'HADM_S.REFGENCOEFFG12.REFGENCOEFF25', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG13_REFGENCOEFF26(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG13_REFGENCOEFF26, self).__init__(register,
            'REFGENCOEFF26', 'HADM_S.REFGENCOEFFG13.REFGENCOEFF26', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG13_REFGENCOEFF27(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG13_REFGENCOEFF27, self).__init__(register,
            'REFGENCOEFF27', 'HADM_S.REFGENCOEFFG13.REFGENCOEFF27', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG14_REFGENCOEFF28(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG14_REFGENCOEFF28, self).__init__(register,
            'REFGENCOEFF28', 'HADM_S.REFGENCOEFFG14.REFGENCOEFF28', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG14_REFGENCOEFF29(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG14_REFGENCOEFF29, self).__init__(register,
            'REFGENCOEFF29', 'HADM_S.REFGENCOEFFG14.REFGENCOEFF29', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG15_REFGENCOEFF30(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG15_REFGENCOEFF30, self).__init__(register,
            'REFGENCOEFF30', 'HADM_S.REFGENCOEFFG15.REFGENCOEFF30', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_REFGENCOEFFG15_REFGENCOEFF31(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_REFGENCOEFFG15_REFGENCOEFF31, self).__init__(register,
            'REFGENCOEFF31', 'HADM_S.REFGENCOEFFG15.REFGENCOEFF31', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_SPARE_SPARE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_SPARE_SPARE, self).__init__(register,
            'SPARE', 'HADM_S.SPARE.SPARE', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESCTRL_SIZE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESCTRL_SIZE, self).__init__(register,
            'SIZE', 'HADM_S.RESCTRL.SIZE', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESCTRL_BUFMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESCTRL_BUFMODE, self).__init__(register,
            'BUFMODE', 'HADM_S.RESCTRL.BUFMODE', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESCTRL_DEBUGEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESCTRL_DEBUGEN, self).__init__(register,
            'DEBUGEN', 'HADM_S.RESCTRL.DEBUGEN', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESCTRL_NADMEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESCTRL_NADMEN, self).__init__(register,
            'NADMEN', 'HADM_S.RESCTRL.NADMEN', 'read-write',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_ADDR_ADDR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_ADDR_ADDR, self).__init__(register,
            'ADDR', 'HADM_S.ADDR.ADDR', 'read-write',
            u"",
            2, 30)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESSTATUS_BYTES(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESSTATUS_BYTES, self).__init__(register,
            'BYTES', 'HADM_S.RESSTATUS.BYTES', 'read-only',
            u"",
            0, 14)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESSTATUS_STEPS(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESSTATUS_STEPS, self).__init__(register,
            'STEPS', 'HADM_S.RESSTATUS.STEPS', 'read-only',
            u"",
            14, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESSTATUS_THRESHOLDFLAG(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESSTATUS_THRESHOLDFLAG, self).__init__(register,
            'THRESHOLDFLAG', 'HADM_S.RESSTATUS.THRESHOLDFLAG', 'read-only',
            u"",
            22, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_THRESHOLDCTRL_THRESHOLD(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_THRESHOLDCTRL_THRESHOLD, self).__init__(register,
            'THRESHOLD', 'HADM_S.THRESHOLDCTRL.THRESHOLD', 'read-write',
            u"",
            0, 13)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_THRESHOLDCTRL_THRESHOLDMODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_THRESHOLDCTRL_THRESHOLDMODE, self).__init__(register,
            'THRESHOLDMODE', 'HADM_S.THRESHOLDCTRL.THRESHOLDMODE', 'read-write',
            u"",
            13, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_AHBCONFIG_BUFFERABLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_AHBCONFIG_BUFFERABLE, self).__init__(register,
            'BUFFERABLE', 'HADM_S.AHBCONFIG.BUFFERABLE', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_AHBCONFIG_MODIFIABLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_AHBCONFIG_MODIFIABLE, self).__init__(register,
            'MODIFIABLE', 'HADM_S.AHBCONFIG.MODIFIABLE', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_AHBCONFIG_LOOKUP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_AHBCONFIG_LOOKUP, self).__init__(register,
            'LOOKUP', 'HADM_S.AHBCONFIG.LOOKUP', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_AHBCONFIG_ALLOCATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_AHBCONFIG_ALLOCATE, self).__init__(register,
            'ALLOCATE', 'HADM_S.AHBCONFIG.ALLOCATE', 'read-write',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_AHBCONFIG_SHAREABLE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_AHBCONFIG_SHAREABLE, self).__init__(register,
            'SHAREABLE', 'HADM_S.AHBCONFIG.SHAREABLE', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL0_NEXTTASKNUM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL0_NEXTTASKNUM, self).__init__(register,
            'NEXTTASKNUM', 'HADM_S.TASKCTRL0.NEXTTASKNUM', 'read-write',
            u"",
            0, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL0_NEXTPRECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL0_NEXTPRECNT, self).__init__(register,
            'NEXTPRECNT', 'HADM_S.TASKCTRL0.NEXTPRECNT', 'read-write',
            u"",
            2, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL1_NEXTBASECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL1_NEXTBASECNT, self).__init__(register,
            'NEXTBASECNT', 'HADM_S.TASKCTRL1.NEXTBASECNT', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL2_NEXTWRAPCNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL2_NEXTWRAPCNT, self).__init__(register,
            'NEXTWRAPCNT', 'HADM_S.TASKCTRL2.NEXTWRAPCNT', 'read-write',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_PRECNTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_PRECNTEN, self).__init__(register,
            'PRECNTEN', 'HADM_S.TASKCTRL3.PRECNTEN', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_BASECNTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_BASECNTEN, self).__init__(register,
            'BASECNTEN', 'HADM_S.TASKCTRL3.BASECNTEN', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_WRAPCNTEN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_WRAPCNTEN, self).__init__(register,
            'WRAPCNTEN', 'HADM_S.TASKCTRL3.WRAPCNTEN', 'read-write',
            u"",
            2, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_TIMEOUTOFFSET(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_TIMEOUTOFFSET, self).__init__(register,
            'TIMEOUTOFFSET', 'HADM_S.TASKCTRL3.TIMEOUTOFFSET', 'read-write',
            u"",
            3, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_MAXQUEUE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_MAXQUEUE, self).__init__(register,
            'MAXQUEUE', 'HADM_S.TASKCTRL3.MAXQUEUE', 'read-write',
            u"",
            15, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_TIMERERRDIS(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_TIMERERRDIS, self).__init__(register,
            'TIMERERRDIS', 'HADM_S.TASKCTRL3.TIMERERRDIS', 'read-write',
            u"",
            17, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_TASKCTRL3_WRAPCNTWIN(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_TASKCTRL3_WRAPCNTWIN, self).__init__(register,
            'WRAPCNTWIN', 'HADM_S.TASKCTRL3.WRAPCNTWIN', 'read-write',
            u"",
            18, 14)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES0, self).__init__(register,
            'RES0', 'HADM_S.RESULTINSTR0.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES1, self).__init__(register,
            'RES1', 'HADM_S.RESULTINSTR0.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES2, self).__init__(register,
            'RES2', 'HADM_S.RESULTINSTR0.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES3, self).__init__(register,
            'RES3', 'HADM_S.RESULTINSTR0.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES4, self).__init__(register,
            'RES4', 'HADM_S.RESULTINSTR0.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES5, self).__init__(register,
            'RES5', 'HADM_S.RESULTINSTR0.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES6, self).__init__(register,
            'RES6', 'HADM_S.RESULTINSTR0.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR0_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR0_RES7, self).__init__(register,
            'RES7', 'HADM_S.RESULTINSTR0.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_S.INSTR00.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_S.INSTR00.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_S.INSTR00.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_S.INSTR00.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_RTT0, self).__init__(register,
            'RTT0', 'HADM_S.INSTR00.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_NADM0, self).__init__(register,
            'NADM0', 'HADM_S.INSTR00.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_PBR0, self).__init__(register,
            'PBR0', 'HADM_S.INSTR00.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_S.INSTR00.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_S.INSTR00.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_S.INSTR00.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR00_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR00_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_S.INSTR00.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_S.INSTR10.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_S.INSTR10.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_S.INSTR10.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_S.INSTR10.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_RTT1, self).__init__(register,
            'RTT1', 'HADM_S.INSTR10.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_NADM1, self).__init__(register,
            'NADM1', 'HADM_S.INSTR10.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_PBR1, self).__init__(register,
            'PBR1', 'HADM_S.INSTR10.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_S.INSTR10.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_S.INSTR10.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_S.INSTR10.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR10_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR10_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_S.INSTR10.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_S.INSTR20.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_S.INSTR20.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_S.INSTR20.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_S.INSTR20.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_RTT2, self).__init__(register,
            'RTT2', 'HADM_S.INSTR20.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_NADM2, self).__init__(register,
            'NADM2', 'HADM_S.INSTR20.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_PBR2, self).__init__(register,
            'PBR2', 'HADM_S.INSTR20.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_S.INSTR20.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_S.INSTR20.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_S.INSTR20.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR20_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR20_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_S.INSTR20.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_S.INSTR30.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_S.INSTR30.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_S.INSTR30.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_S.INSTR30.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_RTT3, self).__init__(register,
            'RTT3', 'HADM_S.INSTR30.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_NADM3, self).__init__(register,
            'NADM3', 'HADM_S.INSTR30.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_PBR3, self).__init__(register,
            'PBR3', 'HADM_S.INSTR30.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_S.INSTR30.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_S.INSTR30.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_S.INSTR30.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR30_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR30_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_S.INSTR30.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_S.INSTR40.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_S.INSTR40.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_S.INSTR40.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_S.INSTR40.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_RTT4, self).__init__(register,
            'RTT4', 'HADM_S.INSTR40.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_NADM4, self).__init__(register,
            'NADM4', 'HADM_S.INSTR40.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_PBR4, self).__init__(register,
            'PBR4', 'HADM_S.INSTR40.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_S.INSTR40.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_S.INSTR40.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_S.INSTR40.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR40_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR40_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_S.INSTR40.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_S.INSTR50.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_S.INSTR50.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_S.INSTR50.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_S.INSTR50.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_RTT5, self).__init__(register,
            'RTT5', 'HADM_S.INSTR50.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_NADM5, self).__init__(register,
            'NADM5', 'HADM_S.INSTR50.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_PBR5, self).__init__(register,
            'PBR5', 'HADM_S.INSTR50.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_S.INSTR50.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_S.INSTR50.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_S.INSTR50.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR50_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR50_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_S.INSTR50.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_S.INSTR60.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_S.INSTR60.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_S.INSTR60.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_S.INSTR60.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_RTT6, self).__init__(register,
            'RTT6', 'HADM_S.INSTR60.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_NADM6, self).__init__(register,
            'NADM6', 'HADM_S.INSTR60.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_PBR6, self).__init__(register,
            'PBR6', 'HADM_S.INSTR60.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_S.INSTR60.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_S.INSTR60.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_S.INSTR60.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR60_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR60_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_S.INSTR60.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES0, self).__init__(register,
            'RES0', 'HADM_S.RESULTINSTR1.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES1, self).__init__(register,
            'RES1', 'HADM_S.RESULTINSTR1.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES2, self).__init__(register,
            'RES2', 'HADM_S.RESULTINSTR1.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES3, self).__init__(register,
            'RES3', 'HADM_S.RESULTINSTR1.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES4, self).__init__(register,
            'RES4', 'HADM_S.RESULTINSTR1.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES5, self).__init__(register,
            'RES5', 'HADM_S.RESULTINSTR1.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES6, self).__init__(register,
            'RES6', 'HADM_S.RESULTINSTR1.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR1_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR1_RES7, self).__init__(register,
            'RES7', 'HADM_S.RESULTINSTR1.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_S.INSTR01.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_S.INSTR01.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_S.INSTR01.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_S.INSTR01.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_RTT0, self).__init__(register,
            'RTT0', 'HADM_S.INSTR01.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_NADM0, self).__init__(register,
            'NADM0', 'HADM_S.INSTR01.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_PBR0, self).__init__(register,
            'PBR0', 'HADM_S.INSTR01.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_S.INSTR01.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_S.INSTR01.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_S.INSTR01.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR01_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR01_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_S.INSTR01.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_S.INSTR11.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_S.INSTR11.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_S.INSTR11.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_S.INSTR11.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_RTT1, self).__init__(register,
            'RTT1', 'HADM_S.INSTR11.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_NADM1, self).__init__(register,
            'NADM1', 'HADM_S.INSTR11.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_PBR1, self).__init__(register,
            'PBR1', 'HADM_S.INSTR11.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_S.INSTR11.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_S.INSTR11.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_S.INSTR11.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR11_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR11_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_S.INSTR11.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_S.INSTR21.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_S.INSTR21.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_S.INSTR21.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_S.INSTR21.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_RTT2, self).__init__(register,
            'RTT2', 'HADM_S.INSTR21.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_NADM2, self).__init__(register,
            'NADM2', 'HADM_S.INSTR21.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_PBR2, self).__init__(register,
            'PBR2', 'HADM_S.INSTR21.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_S.INSTR21.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_S.INSTR21.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_S.INSTR21.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR21_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR21_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_S.INSTR21.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_S.INSTR31.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_S.INSTR31.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_S.INSTR31.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_S.INSTR31.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_RTT3, self).__init__(register,
            'RTT3', 'HADM_S.INSTR31.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_NADM3, self).__init__(register,
            'NADM3', 'HADM_S.INSTR31.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_PBR3, self).__init__(register,
            'PBR3', 'HADM_S.INSTR31.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_S.INSTR31.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_S.INSTR31.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_S.INSTR31.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR31_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR31_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_S.INSTR31.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_S.INSTR41.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_S.INSTR41.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_S.INSTR41.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_S.INSTR41.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_RTT4, self).__init__(register,
            'RTT4', 'HADM_S.INSTR41.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_NADM4, self).__init__(register,
            'NADM4', 'HADM_S.INSTR41.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_PBR4, self).__init__(register,
            'PBR4', 'HADM_S.INSTR41.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_S.INSTR41.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_S.INSTR41.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_S.INSTR41.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR41_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR41_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_S.INSTR41.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_S.INSTR51.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_S.INSTR51.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_S.INSTR51.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_S.INSTR51.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_RTT5, self).__init__(register,
            'RTT5', 'HADM_S.INSTR51.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_NADM5, self).__init__(register,
            'NADM5', 'HADM_S.INSTR51.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_PBR5, self).__init__(register,
            'PBR5', 'HADM_S.INSTR51.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_S.INSTR51.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_S.INSTR51.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_S.INSTR51.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR51_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR51_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_S.INSTR51.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_S.INSTR61.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_S.INSTR61.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_S.INSTR61.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_S.INSTR61.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_RTT6, self).__init__(register,
            'RTT6', 'HADM_S.INSTR61.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_NADM6, self).__init__(register,
            'NADM6', 'HADM_S.INSTR61.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_PBR6, self).__init__(register,
            'PBR6', 'HADM_S.INSTR61.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_S.INSTR61.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_S.INSTR61.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_S.INSTR61.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR61_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR61_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_S.INSTR61.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES0, self).__init__(register,
            'RES0', 'HADM_S.RESULTINSTR2.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES1, self).__init__(register,
            'RES1', 'HADM_S.RESULTINSTR2.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES2, self).__init__(register,
            'RES2', 'HADM_S.RESULTINSTR2.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES3, self).__init__(register,
            'RES3', 'HADM_S.RESULTINSTR2.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES4, self).__init__(register,
            'RES4', 'HADM_S.RESULTINSTR2.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES5, self).__init__(register,
            'RES5', 'HADM_S.RESULTINSTR2.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES6, self).__init__(register,
            'RES6', 'HADM_S.RESULTINSTR2.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR2_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR2_RES7, self).__init__(register,
            'RES7', 'HADM_S.RESULTINSTR2.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_S.INSTR02.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_S.INSTR02.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_S.INSTR02.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_S.INSTR02.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_RTT0, self).__init__(register,
            'RTT0', 'HADM_S.INSTR02.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_NADM0, self).__init__(register,
            'NADM0', 'HADM_S.INSTR02.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_PBR0, self).__init__(register,
            'PBR0', 'HADM_S.INSTR02.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_S.INSTR02.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_S.INSTR02.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_S.INSTR02.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR02_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR02_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_S.INSTR02.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_S.INSTR12.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_S.INSTR12.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_S.INSTR12.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_S.INSTR12.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_RTT1, self).__init__(register,
            'RTT1', 'HADM_S.INSTR12.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_NADM1, self).__init__(register,
            'NADM1', 'HADM_S.INSTR12.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_PBR1, self).__init__(register,
            'PBR1', 'HADM_S.INSTR12.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_S.INSTR12.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_S.INSTR12.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_S.INSTR12.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR12_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR12_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_S.INSTR12.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_S.INSTR22.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_S.INSTR22.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_S.INSTR22.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_S.INSTR22.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_RTT2, self).__init__(register,
            'RTT2', 'HADM_S.INSTR22.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_NADM2, self).__init__(register,
            'NADM2', 'HADM_S.INSTR22.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_PBR2, self).__init__(register,
            'PBR2', 'HADM_S.INSTR22.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_S.INSTR22.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_S.INSTR22.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_S.INSTR22.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR22_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR22_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_S.INSTR22.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_S.INSTR32.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_S.INSTR32.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_S.INSTR32.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_S.INSTR32.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_RTT3, self).__init__(register,
            'RTT3', 'HADM_S.INSTR32.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_NADM3, self).__init__(register,
            'NADM3', 'HADM_S.INSTR32.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_PBR3, self).__init__(register,
            'PBR3', 'HADM_S.INSTR32.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_S.INSTR32.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_S.INSTR32.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_S.INSTR32.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR32_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR32_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_S.INSTR32.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_S.INSTR42.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_S.INSTR42.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_S.INSTR42.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_S.INSTR42.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_RTT4, self).__init__(register,
            'RTT4', 'HADM_S.INSTR42.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_NADM4, self).__init__(register,
            'NADM4', 'HADM_S.INSTR42.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_PBR4, self).__init__(register,
            'PBR4', 'HADM_S.INSTR42.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_S.INSTR42.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_S.INSTR42.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_S.INSTR42.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR42_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR42_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_S.INSTR42.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_S.INSTR52.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_S.INSTR52.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_S.INSTR52.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_S.INSTR52.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_RTT5, self).__init__(register,
            'RTT5', 'HADM_S.INSTR52.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_NADM5, self).__init__(register,
            'NADM5', 'HADM_S.INSTR52.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_PBR5, self).__init__(register,
            'PBR5', 'HADM_S.INSTR52.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_S.INSTR52.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_S.INSTR52.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_S.INSTR52.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR52_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR52_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_S.INSTR52.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_S.INSTR62.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_S.INSTR62.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_S.INSTR62.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_S.INSTR62.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_RTT6, self).__init__(register,
            'RTT6', 'HADM_S.INSTR62.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_NADM6, self).__init__(register,
            'NADM6', 'HADM_S.INSTR62.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_PBR6, self).__init__(register,
            'PBR6', 'HADM_S.INSTR62.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_S.INSTR62.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_S.INSTR62.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_S.INSTR62.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR62_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR62_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_S.INSTR62.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES0, self).__init__(register,
            'RES0', 'HADM_S.RESULTINSTR3.RES0', 'read-write',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES1, self).__init__(register,
            'RES1', 'HADM_S.RESULTINSTR3.RES1', 'read-write',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES2, self).__init__(register,
            'RES2', 'HADM_S.RESULTINSTR3.RES2', 'read-write',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES3, self).__init__(register,
            'RES3', 'HADM_S.RESULTINSTR3.RES3', 'read-write',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES4, self).__init__(register,
            'RES4', 'HADM_S.RESULTINSTR3.RES4', 'read-write',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES5, self).__init__(register,
            'RES5', 'HADM_S.RESULTINSTR3.RES5', 'read-write',
            u"",
            15, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES6, self).__init__(register,
            'RES6', 'HADM_S.RESULTINSTR3.RES6', 'read-write',
            u"",
            18, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_RESULTINSTR3_RES7(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_RESULTINSTR3_RES7, self).__init__(register,
            'RES7', 'HADM_S.RESULTINSTR3.RES7', 'read-write',
            u"",
            21, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_ACTIVE0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_ACTIVE0, self).__init__(register,
            'ACTIVE0', 'HADM_S.INSTR03.ACTIVE0', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_RESETEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_RESETEN0, self).__init__(register,
            'RESETEN0', 'HADM_S.INSTR03.RESETEN0', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_PKTINFO0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_PKTINFO0, self).__init__(register,
            'PKTINFO0', 'HADM_S.INSTR03.PKTINFO0', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_FREQEST0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_FREQEST0, self).__init__(register,
            'FREQEST0', 'HADM_S.INSTR03.FREQEST0', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_RTT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_RTT0, self).__init__(register,
            'RTT0', 'HADM_S.INSTR03.RTT0', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_NADM0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_NADM0, self).__init__(register,
            'NADM0', 'HADM_S.INSTR03.NADM0', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_PBR0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_PBR0, self).__init__(register,
            'PBR0', 'HADM_S.INSTR03.PBR0', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_PRECNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_PRECNTOFF0, self).__init__(register,
            'PRECNTOFF0', 'HADM_S.INSTR03.PRECNTOFF0', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_BASEWRAPCNTOFF0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_BASEWRAPCNTOFF0, self).__init__(register,
            'BASEWRAPCNTOFF0', 'HADM_S.INSTR03.BASEWRAPCNTOFF0', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_TIMEOUT0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_TIMEOUT0, self).__init__(register,
            'TIMEOUT0', 'HADM_S.INSTR03.TIMEOUT0', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR03_STARTDONEIEN0(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR03_STARTDONEIEN0, self).__init__(register,
            'STARTDONEIEN0', 'HADM_S.INSTR03.STARTDONEIEN0', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_ACTIVE1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_ACTIVE1, self).__init__(register,
            'ACTIVE1', 'HADM_S.INSTR13.ACTIVE1', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_RESETEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_RESETEN1, self).__init__(register,
            'RESETEN1', 'HADM_S.INSTR13.RESETEN1', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_PKTINFO1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_PKTINFO1, self).__init__(register,
            'PKTINFO1', 'HADM_S.INSTR13.PKTINFO1', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_FREQEST1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_FREQEST1, self).__init__(register,
            'FREQEST1', 'HADM_S.INSTR13.FREQEST1', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_RTT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_RTT1, self).__init__(register,
            'RTT1', 'HADM_S.INSTR13.RTT1', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_NADM1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_NADM1, self).__init__(register,
            'NADM1', 'HADM_S.INSTR13.NADM1', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_PBR1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_PBR1, self).__init__(register,
            'PBR1', 'HADM_S.INSTR13.PBR1', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_PRECNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_PRECNTOFF1, self).__init__(register,
            'PRECNTOFF1', 'HADM_S.INSTR13.PRECNTOFF1', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_BASEWRAPCNTOFF1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_BASEWRAPCNTOFF1, self).__init__(register,
            'BASEWRAPCNTOFF1', 'HADM_S.INSTR13.BASEWRAPCNTOFF1', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_TIMEOUT1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_TIMEOUT1, self).__init__(register,
            'TIMEOUT1', 'HADM_S.INSTR13.TIMEOUT1', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR13_STARTDONEIEN1(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR13_STARTDONEIEN1, self).__init__(register,
            'STARTDONEIEN1', 'HADM_S.INSTR13.STARTDONEIEN1', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_ACTIVE2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_ACTIVE2, self).__init__(register,
            'ACTIVE2', 'HADM_S.INSTR23.ACTIVE2', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_RESETEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_RESETEN2, self).__init__(register,
            'RESETEN2', 'HADM_S.INSTR23.RESETEN2', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_PKTINFO2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_PKTINFO2, self).__init__(register,
            'PKTINFO2', 'HADM_S.INSTR23.PKTINFO2', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_FREQEST2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_FREQEST2, self).__init__(register,
            'FREQEST2', 'HADM_S.INSTR23.FREQEST2', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_RTT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_RTT2, self).__init__(register,
            'RTT2', 'HADM_S.INSTR23.RTT2', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_NADM2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_NADM2, self).__init__(register,
            'NADM2', 'HADM_S.INSTR23.NADM2', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_PBR2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_PBR2, self).__init__(register,
            'PBR2', 'HADM_S.INSTR23.PBR2', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_PRECNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_PRECNTOFF2, self).__init__(register,
            'PRECNTOFF2', 'HADM_S.INSTR23.PRECNTOFF2', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_BASEWRAPCNTOFF2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_BASEWRAPCNTOFF2, self).__init__(register,
            'BASEWRAPCNTOFF2', 'HADM_S.INSTR23.BASEWRAPCNTOFF2', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_TIMEOUT2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_TIMEOUT2, self).__init__(register,
            'TIMEOUT2', 'HADM_S.INSTR23.TIMEOUT2', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR23_STARTDONEIEN2(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR23_STARTDONEIEN2, self).__init__(register,
            'STARTDONEIEN2', 'HADM_S.INSTR23.STARTDONEIEN2', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_ACTIVE3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_ACTIVE3, self).__init__(register,
            'ACTIVE3', 'HADM_S.INSTR33.ACTIVE3', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_RESETEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_RESETEN3, self).__init__(register,
            'RESETEN3', 'HADM_S.INSTR33.RESETEN3', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_PKTINFO3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_PKTINFO3, self).__init__(register,
            'PKTINFO3', 'HADM_S.INSTR33.PKTINFO3', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_FREQEST3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_FREQEST3, self).__init__(register,
            'FREQEST3', 'HADM_S.INSTR33.FREQEST3', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_RTT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_RTT3, self).__init__(register,
            'RTT3', 'HADM_S.INSTR33.RTT3', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_NADM3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_NADM3, self).__init__(register,
            'NADM3', 'HADM_S.INSTR33.NADM3', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_PBR3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_PBR3, self).__init__(register,
            'PBR3', 'HADM_S.INSTR33.PBR3', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_PRECNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_PRECNTOFF3, self).__init__(register,
            'PRECNTOFF3', 'HADM_S.INSTR33.PRECNTOFF3', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_BASEWRAPCNTOFF3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_BASEWRAPCNTOFF3, self).__init__(register,
            'BASEWRAPCNTOFF3', 'HADM_S.INSTR33.BASEWRAPCNTOFF3', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_TIMEOUT3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_TIMEOUT3, self).__init__(register,
            'TIMEOUT3', 'HADM_S.INSTR33.TIMEOUT3', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR33_STARTDONEIEN3(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR33_STARTDONEIEN3, self).__init__(register,
            'STARTDONEIEN3', 'HADM_S.INSTR33.STARTDONEIEN3', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_ACTIVE4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_ACTIVE4, self).__init__(register,
            'ACTIVE4', 'HADM_S.INSTR43.ACTIVE4', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_RESETEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_RESETEN4, self).__init__(register,
            'RESETEN4', 'HADM_S.INSTR43.RESETEN4', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_PKTINFO4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_PKTINFO4, self).__init__(register,
            'PKTINFO4', 'HADM_S.INSTR43.PKTINFO4', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_FREQEST4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_FREQEST4, self).__init__(register,
            'FREQEST4', 'HADM_S.INSTR43.FREQEST4', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_RTT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_RTT4, self).__init__(register,
            'RTT4', 'HADM_S.INSTR43.RTT4', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_NADM4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_NADM4, self).__init__(register,
            'NADM4', 'HADM_S.INSTR43.NADM4', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_PBR4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_PBR4, self).__init__(register,
            'PBR4', 'HADM_S.INSTR43.PBR4', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_PRECNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_PRECNTOFF4, self).__init__(register,
            'PRECNTOFF4', 'HADM_S.INSTR43.PRECNTOFF4', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_BASEWRAPCNTOFF4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_BASEWRAPCNTOFF4, self).__init__(register,
            'BASEWRAPCNTOFF4', 'HADM_S.INSTR43.BASEWRAPCNTOFF4', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_TIMEOUT4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_TIMEOUT4, self).__init__(register,
            'TIMEOUT4', 'HADM_S.INSTR43.TIMEOUT4', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR43_STARTDONEIEN4(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR43_STARTDONEIEN4, self).__init__(register,
            'STARTDONEIEN4', 'HADM_S.INSTR43.STARTDONEIEN4', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_ACTIVE5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_ACTIVE5, self).__init__(register,
            'ACTIVE5', 'HADM_S.INSTR53.ACTIVE5', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_RESETEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_RESETEN5, self).__init__(register,
            'RESETEN5', 'HADM_S.INSTR53.RESETEN5', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_PKTINFO5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_PKTINFO5, self).__init__(register,
            'PKTINFO5', 'HADM_S.INSTR53.PKTINFO5', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_FREQEST5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_FREQEST5, self).__init__(register,
            'FREQEST5', 'HADM_S.INSTR53.FREQEST5', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_RTT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_RTT5, self).__init__(register,
            'RTT5', 'HADM_S.INSTR53.RTT5', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_NADM5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_NADM5, self).__init__(register,
            'NADM5', 'HADM_S.INSTR53.NADM5', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_PBR5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_PBR5, self).__init__(register,
            'PBR5', 'HADM_S.INSTR53.PBR5', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_PRECNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_PRECNTOFF5, self).__init__(register,
            'PRECNTOFF5', 'HADM_S.INSTR53.PRECNTOFF5', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_BASEWRAPCNTOFF5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_BASEWRAPCNTOFF5, self).__init__(register,
            'BASEWRAPCNTOFF5', 'HADM_S.INSTR53.BASEWRAPCNTOFF5', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_TIMEOUT5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_TIMEOUT5, self).__init__(register,
            'TIMEOUT5', 'HADM_S.INSTR53.TIMEOUT5', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR53_STARTDONEIEN5(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR53_STARTDONEIEN5, self).__init__(register,
            'STARTDONEIEN5', 'HADM_S.INSTR53.STARTDONEIEN5', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_ACTIVE6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_ACTIVE6, self).__init__(register,
            'ACTIVE6', 'HADM_S.INSTR63.ACTIVE6', 'read-write',
            u"",
            0, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_RESETEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_RESETEN6, self).__init__(register,
            'RESETEN6', 'HADM_S.INSTR63.RESETEN6', 'read-write',
            u"",
            1, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_PKTINFO6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_PKTINFO6, self).__init__(register,
            'PKTINFO6', 'HADM_S.INSTR63.PKTINFO6', 'read-write',
            u"",
            2, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_FREQEST6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_FREQEST6, self).__init__(register,
            'FREQEST6', 'HADM_S.INSTR63.FREQEST6', 'read-write',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_RTT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_RTT6, self).__init__(register,
            'RTT6', 'HADM_S.INSTR63.RTT6', 'read-write',
            u"",
            5, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_NADM6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_NADM6, self).__init__(register,
            'NADM6', 'HADM_S.INSTR63.NADM6', 'read-write',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_PBR6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_PBR6, self).__init__(register,
            'PBR6', 'HADM_S.INSTR63.PBR6', 'read-write',
            u"",
            9, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_PRECNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_PRECNTOFF6, self).__init__(register,
            'PRECNTOFF6', 'HADM_S.INSTR63.PRECNTOFF6', 'read-write',
            u"",
            11, 5)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_BASEWRAPCNTOFF6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_BASEWRAPCNTOFF6, self).__init__(register,
            'BASEWRAPCNTOFF6', 'HADM_S.INSTR63.BASEWRAPCNTOFF6', 'read-write',
            u"",
            16, 12)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_TIMEOUT6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_TIMEOUT6, self).__init__(register,
            'TIMEOUT6', 'HADM_S.INSTR63.TIMEOUT6', 'read-write',
            u"",
            28, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_INSTR63_STARTDONEIEN6(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_INSTR63_STARTDONEIEN6, self).__init__(register,
            'STARTDONEIEN6', 'HADM_S.INSTR63.STARTDONEIEN6', 'read-write',
            u"",
            29, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_CTRLSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_CTRLSTATE, self).__init__(register,
            'CTRLSTATE', 'HADM_S.STATUS0.CTRLSTATE', 'read-only',
            u"",
            0, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_PKTINFOACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_PKTINFOACTIVE, self).__init__(register,
            'PKTINFOACTIVE', 'HADM_S.STATUS0.PKTINFOACTIVE', 'read-only',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_FREQESTACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_FREQESTACTIVE, self).__init__(register,
            'FREQESTACTIVE', 'HADM_S.STATUS0.FREQESTACTIVE', 'read-only',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_RTTACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_RTTACTIVE, self).__init__(register,
            'RTTACTIVE', 'HADM_S.STATUS0.RTTACTIVE', 'read-only',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_NADMACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_NADMACTIVE, self).__init__(register,
            'NADMACTIVE', 'HADM_S.STATUS0.NADMACTIVE', 'read-only',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_PBRACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_PBRACTIVE, self).__init__(register,
            'PBRACTIVE', 'HADM_S.STATUS0.PBRACTIVE', 'read-only',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_RESULTSACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_RESULTSACTIVE, self).__init__(register,
            'RESULTSACTIVE', 'HADM_S.STATUS0.RESULTSACTIVE', 'read-only',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_STARTTASK(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_STARTTASK, self).__init__(register,
            'STARTTASK', 'HADM_S.STATUS0.STARTTASK', 'read-only',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_TASKNUM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_TASKNUM, self).__init__(register,
            'TASKNUM', 'HADM_S.STATUS0.TASKNUM', 'read-only',
            u"",
            11, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_PC(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_PC, self).__init__(register,
            'PC', 'HADM_S.STATUS0.PC', 'read-only',
            u"",
            13, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_ANTSWITCHSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_ANTSWITCHSTATE, self).__init__(register,
            'ANTSWITCHSTATE', 'HADM_S.STATUS0.ANTSWITCHSTATE', 'read-only',
            u"",
            16, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_ANTHADM(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_ANTHADM, self).__init__(register,
            'ANTHADM', 'HADM_S.STATUS0.ANTHADM', 'read-only',
            u"",
            20, 4)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_FREQESTSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_FREQESTSTATE, self).__init__(register,
            'FREQESTSTATE', 'HADM_S.STATUS0.FREQESTSTATE', 'read-only',
            u"",
            24, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_RTTMAINSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_RTTMAINSTATE, self).__init__(register,
            'RTTMAINSTATE', 'HADM_S.STATUS0.RTTMAINSTATE', 'read-only',
            u"",
            26, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS0_RTTRBSSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS0_RTTRBSSTATE, self).__init__(register,
            'RTTRBSSTATE', 'HADM_S.STATUS0.RTTRBSSTATE', 'read-only',
            u"",
            28, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_STARTINSTR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_STARTINSTR, self).__init__(register,
            'STARTINSTR', 'HADM_S.STATUS1.STARTINSTR', 'read-only',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_DONEINSTR(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_DONEINSTR, self).__init__(register,
            'DONEINSTR', 'HADM_S.STATUS1.DONEINSTR', 'read-only',
            u"",
            3, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_PBRCTRLSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_PBRCTRLSTATE, self).__init__(register,
            'PBRCTRLSTATE', 'HADM_S.STATUS1.PBRCTRLSTATE', 'read-only',
            u"",
            6, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_PBRTQSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_PBRTQSTATE, self).__init__(register,
            'PBRTQSTATE', 'HADM_S.STATUS1.PBRTQSTATE', 'read-only',
            u"",
            9, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_PBRGDCOMPSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_PBRGDCOMPSTATE, self).__init__(register,
            'PBRGDCOMPSTATE', 'HADM_S.STATUS1.PBRGDCOMPSTATE', 'read-only',
            u"",
            12, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_PBRRESSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_PBRRESSTATE, self).__init__(register,
            'PBRRESSTATE', 'HADM_S.STATUS1.PBRRESSTATE', 'read-only',
            u"",
            15, 2)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS1_RTTRAMSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS1_RTTRAMSTATE, self).__init__(register,
            'RTTRAMSTATE', 'HADM_S.STATUS1.RTTRAMSTATE', 'read-only',
            u"",
            17, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_CURROPCODE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_CURROPCODE, self).__init__(register,
            'CURROPCODE', 'HADM_S.STATUS2.CURROPCODE', 'read-only',
            u"",
            0, 3)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_RESULTACTIVE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_RESULTACTIVE, self).__init__(register,
            'RESULTACTIVE', 'HADM_S.STATUS2.RESULTACTIVE', 'read-only',
            u"",
            3, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_RESULTDONE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_RESULTDONE, self).__init__(register,
            'RESULTDONE', 'HADM_S.STATUS2.RESULTDONE', 'read-only',
            u"",
            4, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_PKTINFOVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_PKTINFOVALID, self).__init__(register,
            'PKTINFOVALID', 'HADM_S.STATUS2.PKTINFOVALID', 'read-only',
            u"",
            5, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_FREQESTVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_FREQESTVALID, self).__init__(register,
            'FREQESTVALID', 'HADM_S.STATUS2.FREQESTVALID', 'read-only',
            u"",
            6, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_PBRRXVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_PBRRXVALID, self).__init__(register,
            'PBRRXVALID', 'HADM_S.STATUS2.PBRRXVALID', 'read-only',
            u"",
            7, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_RTTVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_RTTVALID, self).__init__(register,
            'RTTVALID', 'HADM_S.STATUS2.RTTVALID', 'read-only',
            u"",
            8, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_NADMVALID(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_NADMVALID, self).__init__(register,
            'NADMVALID', 'HADM_S.STATUS2.NADMVALID', 'read-only',
            u"",
            9, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS2_BUFHANDLERSTATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS2_BUFHANDLERSTATE, self).__init__(register,
            'BUFHANDLERSTATE', 'HADM_S.STATUS2.BUFHANDLERSTATE', 'read-only',
            u"",
            10, 1)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS3_TARGETPRECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS3_TARGETPRECNT, self).__init__(register,
            'TARGETPRECNT', 'HADM_S.STATUS3.TARGETPRECNT', 'read-only',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS4_TARGETBASECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS4_TARGETBASECNT, self).__init__(register,
            'TARGETBASECNT', 'HADM_S.STATUS4.TARGETBASECNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS5_TARGETWRAPCNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS5_TARGETWRAPCNT, self).__init__(register,
            'TARGETWRAPCNT', 'HADM_S.STATUS5.TARGETWRAPCNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS6_ADVTARGETBASECNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS6_ADVTARGETBASECNT, self).__init__(register,
            'ADVTARGETBASECNT', 'HADM_S.STATUS6.ADVTARGETBASECNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


class RM_Field_HADM_S_STATUS7_ADVTARGETWRAPCNT(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_HADM_S_STATUS7_ADVTARGETWRAPCNT, self).__init__(register,
            'ADVTARGETWRAPCNT', 'HADM_S.STATUS7.ADVTARGETWRAPCNT', 'read-only',
            u"",
            0, 32)
        self.__dict__['zz_frozen'] = True


