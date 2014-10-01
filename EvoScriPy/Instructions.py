__author__ = 'qPCR4vir'

from Instruction_Base import *
import Robot
#todo organize the arg in each instruction according to the more common use
#todo implement all the instruction, from all the devices, and from script only (not documented-inverse engineering) !!

class aspirate(Pipetting):
    """ A.15.4.1 Aspirate command (Worklist: Aspirate)  A - 125
    """
    def __init__(self,  tipMask     = curTipMask,
                        liquidClass = def_liquidClass,
                        volume      = def_vol,
                        labware     = def_LabW,
                        spacing     = 1,
                        wellSelection= None,       # TODO implement
                        LoopOptions = def_LoopOp,
                        RackName    = None,        # TODO implement
                        Well        = None,        # TODO implement
                        arm         = Pipette.LiHa1):
        Pipetting.__init__(self, 'Aspirate',
                            tipMask,
                            liquidClass,
                            volume,
                            labware,
                            spacing,
                            wellSelection,
                            LoopOptions,
                            RackName,
                            Well,
                            arm )

    def action(self):
        return Robot.Robot.Arm.Aspire


class dispense(Pipetting):
    """ A.15.4.2 Dispense (Worklist: Dispense)
    """
    def __init__(self,  tipMask     = curTipMask,
                        liquidClass = def_liquidClass,
                        volume      = def_vol,
                        labware     = def_LabW,
                        spacing     = 1,
                        wellSelection= None,
                        LoopOptions = def_LoopOp,
                        RackName    = None,
                        Well        = None,
                        arm         = Pipette.LiHa1):
        Pipetting.__init__(self, 'Dispense',
                            tipMask,
                            liquidClass,
                            volume,
                            labware,
                            spacing,
                            wellSelection,
                            LoopOptions,
                            RackName,
                            Well,
                            arm )

    def action(self):
        return Robot.Robot.Arm.Dispense


class mix(Pipetting):
    """ A.15.4.3 Mix (Worklist: Mix)
    """
    def __init__(self,  tipMask     = curTipMask,
                        liquidClass = def_liquidClass,
                        volume      = def_vol,
                        labware     = def_LabW,
                        spacing     = 1,
                        wellSelection= None,
                        cycles      = 3,
                        LoopOptions = def_LoopOp,
                        RackName    = None,
                        Well        = None,
                        arm         = Pipette.LiHa1):
        Pipetting.__init__(self, 'Mix',
                            tipMask,
                            liquidClass,
                            volume,
                            labware,
                            spacing,
                            wellSelection,
                            LoopOptions,
                            RackName,
                            Well,
                            arm )
        self.cycles = cycles

    def validateArg(self):
        Pipetting.validateArg(self)
        self.arg[18:18] = [self.cycles]                 # arg 19
        return True

class wash_tips(Pipette):                     # TODO revise def values of arg
    """ A.15.4.4 Wash Tips (Worklist: Wash)
    """
    def __init__(self,  tipMask     = curTipMask,
                        WashWaste   = def_WashWaste,
                        WashCleaner = def_WashCleaner,
                        wasteVol    = 100,
                        wasteDelay  = 50,
                        cleanerVol  = 10,
                        cleanerDelay= 50,
                        Airgap      = 0.0,
                        airgapSpeed = 50,
                        retractSpeed= 100,
                        FastWash    = False,
                        lowVolume   = False,
                        atFrequency = 0,
                        RackName    = None,
                        Well        = None,
                        arm         = Pipette.LiHa1):
        Pipette.__init__(self, 'Wash',
                            tipMask,
                            labware=WashWaste,
                            RackName=RackName,
                            Well=Well,
                            arm=arm )
        self.atFrequency = atFrequency
        self.lowVolume = lowVolume
        self.FastWash = FastWash
        self.retractSpeed = retractSpeed
        self.airgapSpeed = airgapSpeed
        self.Airgap = Airgap
        self.cleanerDelay = cleanerDelay
        self.cleanerVol = cleanerVol
        self.wasteDelay = wasteDelay
        self.wasteVol = wasteVol
        self.WashCleaner = WashCleaner
        #self.WashWaste = WashWaste

    def validateArg(self):
        Pipette.validateArg(self)
        self.arg[3:-1] = [integer(self.WashCleaner.location.grid),   # arg 4
                          integer(self.WashCleaner.location.site),   # arg 5
                          expression(self.wasteVol),                 # arg 6
                          integer(self.wasteDelay),
                          expression(self.cleanerVol),
                          integer(self.cleanerDelay),
                          floating_point(self.Airgap),
                          integer(self.airgapSpeed),
                          integer(self.retractSpeed),
                          integer(self.FastWash),
                          integer(self.lowVolume),
                          integer(self.atFrequency)]
        return True

    def __init__(self):
        Pipette.__init__(self, "Wash")
        assert False,"Wash() not implemented"

class getDITI(DITIs):
    def __init__(self,  tipMask, type, options=0, arm= Pipette.LiHa1):
        """ A.15.4.5 Get DITIs (Worklist: GetDITI) ...
            The Get DITIs command is used to pick up DITIs (disposable tips) of the specified
            type from a DITI rack. Freedom EVOware keeps track of their position on the
            worktable and automatically picks up the next available unused DITIs of the
            chosen type.
            When you choose a DITI type in a script command, the pull-down list all of the
            LiHa DITI types which are currently configured in the labware database. When
            you want to pick up a DiTi, Freedom EVOware searches the worktable for a DITI
            rack which contains the DITI type you have specified in the script command.
            To configure Freedom EVOware for a new DITI type, create a new DITI rack or
            duplicate an existing DITI rack and give the new labware a suitable name (e.g.
            “ZipTip”).
            DiTi Index:
            Freedom EVOware automatically assigns a unique numeric index to each
            DITI type. You cannot edit the index manually. The DITI index is used e.g. by
            the Set DITI Type command in worklists and in advanced worklists. The DITI
            index is shown in the Edit Labware dialog box for the DITI labware (Well
            Dimensions tab).
            This function is deprecated in favor of getDITI2 which do not use index
            Currently only use ... ?
        :param label:
        :param tipMask:
        :param type: int, 0-3. DITI index (see 9.4.5 “Labware Types and DITI Types”,  9-32, DITI Index).
        """
        DITIs.__init__(self, "GetDITI", tipMask, options, arm)
        self.type=type # todo Implement!! Find the correct rack in the worktable and the current position to pick.

    def validateArg(self):
        DITIs.validateArg(self)
        self.arg[1:1] = [integer(self.type)]
        return True

class getDITI2(DITIs):
    """ A.15.4.5 Get DITIs (Worklist: GetDITI)
    """
    def __init__(self,  tipMask=curTipMask, LabwareTypeName=None, options=0,
                          arm=Pipette.LiHa1, AirgapVolume=0,   AirgapSpeed=def_AirgapSpeed ):
        """

        :param tipMask:
        :param LabwareTypeName: string? DiTi labware name
        :param options:
        :param arm:
        :param AirgapVolume: int. used to specify a system trailing airgap (STAG) which will be aspirated after
                                  mounting the DITIs. Volume in μl
        :param AirgapSpeed: int. Speed for the airgap in μl/s
        """
        DITIs.__init__(self, "GetDITI2", tipMask, options, arm)
        self.LabwareTypeName = LabwareTypeName # todo Implement!! Find the rack and the current position to pick.
        self.AirgapSpeed = AirgapSpeed
        self.AirgapVolume = AirgapVolume

    def validateArg(self):
        DITIs.validateArg(self)

        ln= self.LabwareTypeName
        if   ln is None                     : ln = def_DiTi.type.name # = Labware.Type("DiTi 1000ul", 8, 12, maxVol=940)
        elif isinstance(ln, Lab.Labware)    : ln = ln.type.name
        elif isinstance(ln,Lab.Labware.Type): ln = ln.name

        self.arg[1:1] = [string1(ln)]                              # arg 2 TODO string1 or 2 ? expression?
        self.arg += [integer(self.AirgapVolume), integer(self.AirgapSpeed)]   # arg 5, 6

        return True

    def actualize_robot_state(self):
        maxVol = None                   # todo Implement all this in the iRobot or in the Labware !!!
        ln = self.LabwareTypeName
        if   ln is None                 :   ln = def_DiTi       # = Labware.Type("DiTi 1000ul", 8, 12, maxVol=940)
        elif isinstance(ln, str)        :   ln = Robot.current.worktable.labTypes[ln].type
        elif isinstance(ln, Lab.Labware):   ln = ln.type
        assert isinstance(ln, Lab.Labware.Type)
        maxVol = ln.maxVol
        self.tipMask = Robot.current.getTips(self.tipMask, maxVol)
        self.LabwareTypeName = ln.name


class dropDITI(Pipette):
    """ A.15.4.6 Drop DITIs command (Worklist: DropDITI) """

    def __init__(self,  tipMask= curTipMask, labware = def_DiTiWaste,
                AirgapVolume=0, AirgapSpeed=def_AirgapSpeed ,
                arm= Pipette.LiHa1): #, conditional=True):
        """


        :param conditional: exec only if there are some tip to droop.
        :param tipMask:
        :param labware:
        :param AirgapVolume: floating point, 0 - 100.  airgap in μl which is aspirated after dropping the DITIs
        :param AirgapSpeed: int 1-1000. Speed for the airgap in μl/s
        :param arm:
        """
        Pipette.__init__(self, "DropDITI",  tipMask, labware = labware, arm=arm)
#        self.conditional = conditional
        self.AirgapSpeed = AirgapSpeed
        self.AirgapVolume = AirgapVolume

    def validateArg(self):
        Pipette.validateArg(self)
        self.arg[3:-1] = [floating_point(self.AirgapVolume), self.AirgapSpeed]
        return True

#    def exec(self, mode=None):
#        if supportVirtualRobot:
#            global current
#            used=current.arms[self.arm].drop(self.tipMask)
#            if self.conditional and used:
#                Pipette.exec(self,mode)

class set_DITI_Counter(Pipette): # todo help determining the type,set other def_LabW
    """A.15.4.7 Set Diti Position (Worklist: Set_DITI_Counter)"""

    def __init__(self, type, posInRack=0, labware = def_LabW  ):
        Pipette.__init__(self, "Set_DITI_Counter" , labware = labware)
        self.type = type
        self.posInRack = posInRack

    def validateArg(self):
        self.arg = [integer(self.type), string1(self.labware.location.grid),
                                        string1(self.labware.location.site),
                                        string1(self.posInRack)] # todo extract from Location
        return True

class set_DITI_Counter2(Pipette): # todo  set other def_LabW
    """A.15.4.7 Set Diti Position (Worklist: Set_DITI_Counter)     NOT DOCUMENTED
        example: Set_DITI_Counter2("DiTi 1000ul","25","2","5",0);
    """

    def __init__(self, labware = def_LabW, posInRack=0, lastPos=False  ):
        Pipette.__init__(self, "Set_DITI_Counter2" , labware = labware)
        self.lastPos = lastPos #todo implement internally; how??
        self.posInRack = posInRack

    def validateArg(self):
        self.arg = [string1(self.labware.type.name),
                    string1(self.labware.location.grid),
                    string1(self.labware.location.site+1),
                    string1(self.posInRack+1),
                    integer(self.lastPos)] # todo extract from Location
        return True

class pickUp_DITIs(Pipette):
    """ A.15.4.8 Pick Up DITIs (Worklist: Pick Up_DITI)
    """
    def __init__(self, tipMask     = curTipMask,
                             labware     = def_LabW,
                             wellSelection= None,
                             LoopOptions = def_LoopOp,
                             type        = None,
                             arm         = Pipette.LiHa1,
                             RackName    = None,
                             Well        = None):
        Pipette.__init__(self, 'PickUp_DITIs',
                             tipMask     = tipMask,
                             labware     = labware,
                             wellSelection= wellSelection,
                             LoopOptions = LoopOptions,
                             RackName    = RackName,
                             Well        = Well,
                             arm         = arm)
        self.type = type

    def validateArg(self):
        Pipette.validateArg(self)
        self.arg[4:5] = []
        self.arg[-1:-1] = [integer(self.type)]
        return True

class set_DITIs_Back(Pipette):
    """ A.15.4.9 Set DITIs Back (Worklist: Set_DITIs_Back)
    """
    def __init__(self , tipMask     = curTipMask,
                             labware     = def_LabW,
                             wellSelection= None,
                             LoopOptions = def_LoopOp,
                             arm         = Pipette.LiHa1,
                             RackName    = None,
                             Well        = None):
        Pipette.__init__(self, 'Set_DITIs_Back',
                             tipMask     = tipMask,
                             labware     = labware,
                             wellSelection= wellSelection,
                             LoopOptions = LoopOptions,
                             RackName    = RackName,
                             Well        = Well,
                             arm         = arm)

    def validateArg(self):
        Pipette.validateArg(self)
        self.arg[4:5] = []
        return True

class pickUp_ZipTip(Pipette): # todo implement !!!
    """ A.15.4.10 Pickup ZipTip (Worklist: PickUp_ZipTip)
    """
    def __init__(self, tipMask = curTipMask ):
        Pipette.__init__(self, 'PickUp_ZipTip' )
        assert False, "PickUp_ZipTip not implemented"

class detect_Liquid(Pipetting):    # todo get the results !!!
    """ A.15.4.11 Detect Liquid (Worklist: Detect_Liquid)
    """
    def __init__(self ,      tipMask     = curTipMask,
                             liquidClass = def_liquidClass,
                             labware     = def_LabW,
                             spacing     = 1,
                             wellSelection= None,
                             LoopOptions = def_LoopOp,
                             arm         = Pipette.LiHa1,
                             RackName    = None,
                             Well        = None,
                             read        = False):
        Pipetting.__init__(self, 'Detect_Liquid',
                            tipMask,
                            liquidClass,
                            labware,
                            spacing,
                            wellSelection,
                            LoopOptions,
                            RackName,
                            Well,
                            arm )
        self.read = read

    def validateArg(self):
        Pipette.validateArg(self)
        self.arg[2:13] = []
        return True

    def exec(self, mode=None):
        Pipetting.exec(self,mode)
        if not self.read: return
        #todo introduce some variable and read into it the vols

class activate_PMP(Instruction):
    """ A.15.4.12 Activate PMP (Worklist: Activate_PMP)
    """
    def __init__(self, tipMask = curTipMask ):
        Instruction.__init__(self, "Activate_PMP")
        self.tipMask = tipMask

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [integer(self.tipMask)]
        return True

class deactivate_PMP(Instruction):
    """ A.15.4.13 Deactivate PMP (Worklist: Deactivate_PMP)
    """
    def __init__(self, tipMask = curTipMask ):
        Instruction.__init__(self, "Deactivate_PMP")
        self.tipMask = tipMask

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [integer(self.tipMask)]
        return True

class moveLiha(Pipette ): #todo convenient arg
    """ A.15.4.14 Move LiHa (Worklist: MoveLiha   - A - 135)
    """
    def __init__(self, zMove, zTarget, offset, speed  ):
        Pipette.__init__(self, 'MoveLiha' )
        self.speed = speed
        self.offset = offset
        self.zTarget = zTarget
        self.zMove = zMove

    def validateArg(self):
        Pipette.validateArg(self)
        self.arg[5:5] = [ self.zMove, self.zTarget, self.offset, self.speed]
        return True

class waste(Instruction):
    """ A.15.4.15 Waste (Worklist: Waste)
    """
    init_system       = 0
    activate_waste_1  = 1
    activate_waste_2  = 2
    activate_waste_3  = 3
    deactivate_all_wastes = 4
    deactivate_system = 5

    def __init__(self, action = init_system ):
        Instruction.__init__(self, "Waste")
        self.action = action

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [integer(self.action)]
        return True

class active_Wash(Instruction):
    """ A.15.4.16 Active WashStation (Worklist: Active_Wash)
    """

    def __init__(self, wait = True, time=None, arm=Pipette.LiHa1   ):
        Instruction.__init__(self, "Active_Wash")
        self.arm = arm
        self.time = time
        self.wait = wait

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [integer(self.wait ),integer(self.time),integer(self.arm)]
        return True

class export(Instruction):
    """ A.15.4.17 Export Data (Worklist: Export)
    """
    lotus  = 1
    dbase  = 2
    excel  = 4
    paradox = 8
    quattro = 16
    text_with_delimiters = 32

    def __init__(self, exportAll = True,
                       formats =  text_with_delimiters,
                       delete = False,
                       compress = False,
                       Raks=[],
                       significantStep = 1):
        Instruction.__init__(self, "Export")
        self.exportAll = exportAll
        self.formats = formats
        self.delete = delete
        self.compress = compress
        self.Raks = Raks
        self.significantStep = significantStep


    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [integer(self.exportAll), integer(self.formats),
                   integer(self.delete),    integer(self.compress)]
        self.arg +=  [integer(len(self.Raks))]                                         # arg 5
        for rk in self.Raks:
            self.arg += [integer(rk.location.grid), integer(rk.location.site) ]        # arg 6,7
        self.arg += [integer( self.significantStep) ]                                  # arg 8

        return True

class startTimer(Instruction):
    """ A.15.4.18 Start Timer (Worklist: StartTimer)
    """
    def __init__(self, timer = 1 ):
        """


        :type timer: expression
        :param timer: expression, 1 - 100. number of timer to re-start. 1-1000?
        """
        Instruction.__init__(self, "StartTimer")
        self.timer = timer

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [expression(self.timer)]

class waitTimer(Instruction):
    """ A.15.4.19 Wait for Timer (Worklist: WaitTimer)
    """
    def __init__(self, timer =1, timeSpan= None ):
        """

        :param timeSpan: expression, 0.02 - 86400. duration
        :type timer: expression
        :param timer: expression, 1 - 100. number of timer to re-start. 1-1000?
        """
        Instruction.__init__(self, "WaitTimer")
        self.timeSpan = timeSpan
        self.timer = timer

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [expression(self.timer),expression(self.timeSpan)]

class execute(Instruction): # todo declare const
    """ A.15.4.20 Execute Application (Worklist: Execute)
    """
    def __init__(self, application, options, responseVariable, scope =0  ):
        """
        """
        Instruction.__init__(self, "Execute")
        self.scope = scope
        self.responseVariable = responseVariable
        self.options = options
        self.application = application


    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [string1(self.application),      integer(self.options),
                   string1(self.responseVariable), integer(self.scope)   ]

class comment(Instruction):
    """ A.15.4.21 Comment (Worklist: Comment)
    """
    def __init__(self, text ):
        """
        """
        Instruction.__init__(self, "Comment")
        self.text = text

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [string1(self.text)]
        return True

class userPrompt(Instruction):    # todo declare const
    """ A.15.4.22 User Prompt (Worklist: UserPrompt)
    """
    def __init__(self, text, sound = 1, closeTime = -1 ):
        """
        """
        Instruction.__init__(self, "UserPrompt")
        self.closeTime = closeTime
        self.sound = sound
        self.text = text

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [string1(self.text), integer(self.sound), integer(self.closeTime)]
        return True

class variable(Instruction):    # todo declare const
    """ A.15.4.23 Set Variable (Worklist: Variable)
    """
    def __init__(self, name, default, queryFlag = False, queryString="", checkLimits  = False,
                 lowerLimit=0.0, upperLimit=0.0, type=0, scope=0,InitMode=0, QueryAtStart=False):
        """
        """
        Instruction.__init__(self, "Variable")
        self.QueryAtStart = QueryAtStart
        self.InitMode = InitMode
        self.scope = scope
        self.type = type
        self.upperLimit = upperLimit
        self.lowerLimit = lowerLimit
        self.checkLimits = checkLimits
        self.queryString = queryString
        self.name = name
        self.default = default
        self.queryFlag = queryFlag

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [string2(self.name), expression(self.default), integer(self.queryFlag)]
        self.arg += [string1( self.queryString), integer(string1.checkLimits), floating_point(self.lowerLimit) ]
        self.arg += [floating_point(self.upperLimit), integer(string1.type), integer(string1.scope)  ]
        self.arg += [  integer(string1.InitMode), integer(string1.QueryAtStart)  ]
        return True

class execute_VBscript(Instruction):
    """ A.15.4.24 Execute VB Script (Worklist: Execute_VBscript)
    """
    def __init__(self, filename, action  = 0 ):
        """

        :param filename: Path and filename of the defined VB script.
        :param action: Use Waits, Continues and Waits_previous defined in subroutine
        """
        Instruction.__init__(self, "Execute_VBscript")
        self.action = action
        self.filename = filename

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [string1(self.filename), integer(self.action) ]
        return True

class notification(Instruction):    # todo declare const
    """ A.15.4.25 Notification (Worklist: Notification)
    """
    def __init__(self,receiverGroup, AttachScreen_ShotFlag = False, emailSubject="",emailMessage="", action  = 0 ):
        """

        :param receiverGroup:
        :param AttachScreen_ShotFlag:
        :param emailSubject:
        :param action:
        """
        Instruction.__init__(self, "Notification")
        self.emailMessage = emailMessage
        self.emailSubject = emailSubject
        self.AttachScreen_ShotFlag = AttachScreen_ShotFlag
        self.action = action
        self.receiverGroup = receiverGroup

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [integer(self.AttachScreen_ShotFlag), string1(self.receiverGroup),  string1(self.emailSubject),
                    string1(self.emailMessage),integer(self.action) ]
        return True

class subroutine(ScriptONLY):
    """ UNDOCUMENTED
    """
    Waits     =0      # script waits for end of the called script
    Continues =1      # script continues
    Waits_previous= 2 # script waits for a previously started script

    def __init__(self, filename, action  = 0 ):
        """
        """
        Instruction.__init__(self, "Subroutine")
        self.action = action
        self.filename = filename

    def validateArg(self):
        Instruction.validateArg(self)
        self.arg= [string1(self.filename), integer(self.action) ]
        return True
