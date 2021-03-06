# Copyright (C) 2014-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2014-2019
"""
Robots and arms
===============

 - :py:class:`Arm`
 - :py:class:`Robot`: track state to make organizations previous to the actual instruction call, and change that state
 after each instruction.


---------

"""


__author__ = 'qPCR4vir'

import logging
import EvoScriPy.labware as labware
rep_sub = None      # rep_sub = br"C:\Prog\robotevo\EvoScriPy\repeat_subroutine.esc" .decode(mode.Mode.encoding) ??

mask_tip = []        # mask for one tip of index ...
mask_tips = []       # mask for all the first tips
for tip in range(13):
    mask_tip += [1 << tip]
    mask_tips += [2 ** tip - 1]


class Arm:

    DiTi        = 0         # DiTi types
    Fixed       = 1

    Aspirate    = 1        # Actions types
    Detect      = 0
    Dispense    = -1

    def __init__(self, n_tips, index, workingTips=None, tips_type=None): # index=Pipette.LiHa1
        """
        :param n_tips: the number of possible tips
        :param index: int. for example: index=Pipette.LiHa1
        :param workingTips: some tips maybe broken or permanently unused.
        :param tips_type: DITI or fixed (not implemented)
        """

        self.index = index
        self.workingTips = workingTips if workingTips is not None else mask_tips[n_tips] # todo implement
        self.tips_type = Arm.DiTi if tips_type is None else tips_type
        self.n_tips = n_tips
        tip = None
        if self.tips_type == Arm.Fixed:
            tip = labware.Tip(labware.Fixed_Tip)

        self.Tips = [tip] * n_tips

    def getTips_test(self, tip_mask=None) -> int:
        """ Simple test that the asked positions are free for mounting new tips.
                :rtype : int
                :param tip_mask:
                :return: the mask that can be used
                :raise "Tip already in position " + str(i):

                """
        if self.tips_type == Arm.Fixed:
            return 0

        if tip_mask is None:
            tip_mask = mask_tips[self.n_tips]

        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                if tp is not None:
                    raise BaseException("A Tip from rack type " + tp.type.name + " is already in position " + str(i))

        return tip_mask

    def mount_tips_executed(self, rack_type=None, tip_mask=None, tips=None) -> (int, list):
        """     Mount only one kind of new tip at a time or just the tips given in the list
        :param rack_type:
        :param tips:
        :rtype : int
        :param tip_mask:
        :return: the mask that can be used
        :raise "Tip already in position " + str(i):

        """
        if self.tips_type == Arm.Fixed:
            return 0

        if tip_mask is None:  tip_mask = mask_tips[self.n_tips]
        n = labware.count_tips(tip_mask)
        assert n <= self.n_tips
        t = 0
        if tips is None:   # deprecated

            assert isinstance(rack_type, labware.DITIrackType)
            tips = [labware.Tip(rack_type) for i in range(n)]
        else:
            assert n == len(tips)

        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                if tp is not None:
                    raise "A Tip from rack type " + tp.type.name + " is already in position " + str(i)
                self.Tips[i] = tips[t]
                t += 1
        return tip_mask, (tips[t:] if t < n else [])

    def getMoreTips_test(self, rack_type, tip_mask=None) -> int:
        """ Mount only the tips with are not already mounted.
            Mount only one kind of tip at a time, but not necessary the same of the already mounted.
                :rtype : int
                :param tip_mask: int
                :return: the mask that can be used
                """
        if self.tips_type == Arm.Fixed:
            return 0

        if tip_mask is None:
            tip_mask = mask_tips[self.n_tips]
        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                if tp:  # already in position
                    if tp.type is not rack_type:
                        raise "A Tip from rack type " + tp.type.name + " is already in position " + str(i) + \
                                " and we need " + rack_type.name
                    tip_mask ^= (1 << i)  # todo raise if dif max_vol? or if vol not 0?
                else:
                    pass # self.Tips[i] = labware.Tip(rack_type)
        return tip_mask

    def mount_more_tips_executed(self, rack_type, tip_mask=None, tips=None) ->(int, list):
        """ Mount only the tips with are not already mounted.
            Mount only one kind of tip at a time, but not necessary the same of the already mounted.
                :rtype : int
                :param tip_mask: int
                :return: the mask that can be used
                """
        if self.tips_type == Arm.Fixed:
            return 0

        if tip_mask is None:  tip_mask = mask_tips[self.n_tips]
        n = labware.count_tips(tip_mask)
        assert n <= self.n_tips
        t = 0
        if tips is None:   # deprecated
            assert isinstance(rack_type, labware.Labware.DITIrack)
            tips = [labware.Tip(rack_type) for i in range(n)]
        else:
            assert n == len(tips)

        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                if tp:  # already in position
                    if tp.type is not tips[t].type:
                        raise "A Tip from rack type " + tp.type.name + " is already in position " + str(i) + \
                                " and we need " + tips[t].type.name
                    tip_mask ^= (1 << i)  # todo raise if dif max_vol? or if vol not 0?
                else:
                    self.Tips[i] = tips[t]
                    t += 1
        return tip_mask, tips[t:] if t < n else []

    def eject_tips_test(self, tip_mask=None) -> (int, [int]):
        """ Return the mask and the tips index to be really used.
        :param tip_mask: int
        :return: the mask that can be used with, is "True" if tips actually ned to be drooped
        :rtype : int
        """
        logging.debug("eject_tips_test called with mask= " + str(tip_mask))

        if self.tips_type == Arm.Fixed:
            return 0, []

        if tip_mask is None:
            tip_mask = mask_tips[self.n_tips]
        tips_index = []
        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                if tp:  # in position
                    tips_index += [i] # tips += [tp]
                    # pass # self.Tips[i] = None
                else:
                    tip_mask -= (1 << i)  # already drooped
        logging.debug("eject_tips_test return mask= " + str(tip_mask))

        return tip_mask, tips_index

    def eject_tips_executed(self, tip_mask=None) -> (int, list):
        """ Drop tips only if needed. Return the mask and the tips really used.
        :param tip_mask: int
        :return: the mask that can be used with, is "True" if tips actually ned to be drooped
        :rtype : int
        """

        if self.tips_type == Arm.Fixed:          # todo call protocol wash ??
            return 0, []

        if tip_mask is None:
            tip_mask = mask_tips[self.n_tips]
        tips = []
        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                if tp:  # in position
                    tips += [tp]
                    self.Tips[i] = None
                else:
                    tip_mask -= (1 << i)  # already drooped
        return tip_mask, tips

    def pipette_executed(self, action, volume, tip_mask=None) -> (list, int):
        """ Check and actualize the robot Arm state to aspirate [vol]s with a tip mask.
        Using the tip mask will check that you are not trying to use an unmounted tip.
        `volume` values for unsettled tip mask are ignored.

        :rtype : (list, int)
        :param action: +1:aspirate, -1:dispense
        :param volume: one vol for all tips, or a list of vol
        :param tip_mask: -1:all tips
        :return: a lis of vol to pipette, and the mask
        """

        if isinstance(volume, (float, int)):
            vol  = [volume] * self.n_tips
        else:
            vol  = list(volume)
            d    = self.n_tips - len(vol)
            vol += [0]*(d if d > 0 else 0 )

        if tip_mask is None:
            tip_mask = mask_tips[self.n_tips]

        for i, tp in enumerate(self.Tips):
            if tip_mask & (1 << i):
                assert isinstance(tp, labware.Tip), "No tip in position " + str(i)
                nv = tp.vol + action * vol[i]
                if 0-0.001 <= nv <= tp.type.max_vol+0.001:
                    self.Tips[i].vol = nv                                   # <----  arm state changed
                    continue
                msg = str(i + 1) + " changing volume from " + str(tp.vol) + " to " + str(nv)
                if nv < 0-0.001:
                    raise BaseException('To few Vol in tip ' + msg)
                raise BaseException('To much Vol in tip ' + msg)
            else:
                pass # vol[i] = None
        return vol, tip_mask


class Robot:
    """ Maintain an intern state.
    Can have more than one arm in a dictionary that map an index with the actual arm.
    One of the arms can be set as "current" and is returned by cur_arm()
    Most of the changes in state are made by the implementation of the low level instructions, while the protocols can
    "observe" the state to make all kind of optimizations and organizations previous to the actual instruction call
    """
    current=None # use immediately, for a short time.

    def __init__(self,
                 index       = None,
                 arms        = None,
                 n_tips      = None,
                 workingTips = None,
                 tips_type   = Arm.DiTi,
                 templateFile= None): # index=Pipette.LiHa1
        """
        A Robot may have 1 or more Arms, indexes by key index in a dictionary of Arms.
        :param arms:
        :param n_tips:
        :param workingTips:
        :param tips_type:
        """


        # assert Robot.current is None
        Robot.current = self
        self.arms = arms              if isinstance(arms, dict     ) else \
                   {arms.index: arms} if isinstance(arms, Arm) else \
                   {     index: Arm(n_tips, index, workingTips, tips_type=tips_type)}
        self.worktable      = None
        #self.set_worktable(templateFile)
        self.def_arm        = index  # or Pipette.LiHa1
        self.droptips       = True
        self.reusetips      = False
        self.preservetips   = False
        self.usePreservedtips = False
        self.allow_air      = 0.2
        self.liquid_clases  = None
        self.set_as_current()
        # self.preservedtips = {} # order:well
        # self.last_preserved_tips = None # labware.DITIrack, offset

    # Functions to observe the iRobot status (intern-physical status, or user status with are modificators of future
    # physical actions), or to modify the user status, but not the physical status. It can be used by the protocol
    # instruction and even by the final user.

    def where_are_preserved_tips(self,
                                 selected_reagents: labware.Labware,
                                 TIP_MASK, type) -> list:   # [labware.DITIrack]
        """

        :param selected_reagents:
        :param TIP_MASK:
        :return:  Return a list of racks with the tips-wells already selected.
        """

        assert isinstance(selected_reagents, labware.Labware)

        selected_reagents = selected_reagents.selected_wells()

        TIP_MASK        = TIP_MASK if TIP_MASK is not None else mask_tips[self.cur_arm().n_tips]
        type            = type if type else self.worktable.def_DiTi_type
        where           = []
        n               = labware.count_tips(TIP_MASK)

        assert n == len(selected_reagents)

        for reagent_well in selected_reagents:
            assert reagent_well in type.preserved_tips, "There are no tip preserved for sample "+str(reagent_well)
            well_tip = type.preserved_tips[reagent_well]
            assert isinstance(well_tip, labware.Well)
            if well_tip.labware in where:
                well_tip.selFlag = True
            else:
                where += [well_tip.labware]
                well_tip.labware.selectOnly(well_tip.offset)
        return where

    def where_preserve_tips(self, TIP_MASK) -> list:
        """ 
        There are used tips in the arm, and we want to know were to put it back.
        Return a list of racks with the tips-wells already selected.
        (to set back the tips currently in the arm)
        
        :param TIP_MASK:
        :return:    list of racks with the tips-wells already selected.
        """                                                                         # todo this in Labware??

        TIP_MASK = TIP_MASK if TIP_MASK is not None else mask_tips[self.cur_arm().n_tips]
        types    = []
        t_masks  = []
        racks    = []
        tips     = []

        for i, tip in enumerate(self.cur_arm().Tips):       # determine the type of tips in Arm to preserve, to set back
            if TIP_MASK & (1 << i):                                                 # this was selected
                assert tip, "There are no tip mounted in position " + str(i)
                tips += [tip]
                if tip.type in types:
                    t_masks[types.index(tip.type)] |= (1 << i)
                else:
                    types += [tip.type]
                    t_masks += [(1 << i)]

        assert len(types)==1                                        # todo temporally assumed only one type of tips
        tpe = types[0]
        m = t_masks[0]

        if not self.usePreservedtips:                               # no re-back DiTi for multiple reuse  todo ??
            assert isinstance(tpe, labware.DITIrackType)
            series = self.worktable.get_DITI_series(tpe)
            rack   = series.current
            ip     = 0
            if series.last_preserved_tips:
                w = series.last_preserved_tips
                assert isinstance(w, labware.Well)
                cont = False
                rack = w.labware  # extract the rack from the last_preserved_tips well
                assert isinstance(rack, labware.DITIrack)
                ip = w.offset

            cont = False
            n = labware.count_tips(m)
            prev_rack = None
            rewind = True
            while n:
                if prev_rack is rack:
                    assert rewind, "Fatal error: no more free rack wells to preserve used tips"
                    rewind = False
                prev_rack = rack
                cont, fw = rack.find_free_wells(n, init_pos=ip)
                if fw:
                    if cont:
                        racks.append(rack)
                        n -= len(fw)
                        if not rewind:
                            fw = rack.selected_wells() + fw
                        rack.selectOnly([w.offset for w in fw])
                    else:
                        logging.warning("WARNING ! todo, use noncontiguos tips well to aet back?")
                rack, rotate = rack.series.show_next_to(rack)
                ip = 0

            return racks

        for tp in tips:                                             # todo revise   !!
            assert isinstance(tp, labware.usedTip)

            react_well = tp.origin.track  or tp.origin              # ??
            assert react_well.offset in tp.type.preserved_tips, "There are no tip preserved for sample "+str(i)

            tip_well = tp.type.preserved_tips[react_well.offset]
            assert isinstance(tip_well, labware.Well)

            if tip_well.labware in racks:
                tip_well.selFlag = True
            else:
                racks += [ tip_well.labware]
                tip_well.labware.selectOnly(tip_well.offset)
        return racks

    def getTips_test(self, rack_type, tip_mask=None) -> int:   # todo REVISE
        if self.reusetips:
            tip_mask = self.cur_arm().getMoreTips_test(rack_type, tip_mask)
        else:
            # self.drop_tips(tip_mask)  # todo REVISE  here ???
            tip_mask = self.cur_arm().getTips_test(tip_mask)
        return tip_mask

    # Functions to change the physical status, to model physical actions, or that directly
    # correspond to actions in the hardware.
    # It can be CALL ONLY FROM the official low level INSTRUCTIONS in the method instructions.actualize_robot_state(self):

    def get_tips_executed(self, rack_series, tip_mask=None) -> (int, list):   # (int, [labware.Tip])

        """ To be call from instructions.actualize_robot_state(self): actualize iRobot state (tip mounted and DiTi racks)
        Return the mask with will be really used taking into account the iRobot state, specially, the "reusetips"
        status and the number of tips already mounted.
        If it return mask = 0 no evo-instruction for the real robot will be generated in some cases.

        :param tip_mask:
        :param rack_series: the series of this king of tips.
        :return: (int, [labware.Tip])
        """

        tips = None
        tip_mask = self.getTips_test(rack_series.type, tip_mask)

        if tip_mask:
            tips = rack_series.retire_new_tips(tip_mask)
        return self.cur_arm().mount_tips_executed(rack_type=rack_series.type, tip_mask=tip_mask, tips=tips)

    def drop_tips_test(self, TIP_MASK=None):
        logging.debug("drop_tips_test called with mask= " + str(TIP_MASK))

        if not self.droptips: return 0

        TIP_MASK, tips = self.cur_arm().eject_tips_test(TIP_MASK)

        logging.debug("drop_tips_test return mask= " + str(TIP_MASK))

        return TIP_MASK

    def drop_tips_executed(self, TIP_MASK=None, waste=None):
        logging.debug("drop_tips_executed called with mask= " + str(TIP_MASK))

        if not self.droptips: return 0

        waste = waste if waste else self.worktable.def_DiTiWaste
        assert isinstance(waste, labware.DITIwaste)

        TIP_MASK, tips = self.cur_arm().eject_tips_executed(TIP_MASK)
        waste.waste(tips)
        logging.debug("drop_tips_executed return mask= " + str(TIP_MASK))

        return TIP_MASK

    def pipette_executed(self, action, volume, labware_selection, tip_mask=None) -> (list, int):

        volume, tip_mask = self.cur_arm().pipette_executed(action, volume, tip_mask)
        w = 0

        assert isinstance(labware_selection, labware.Labware)
        wells = labware_selection.selected_wells()
        for i, tp in enumerate(self.cur_arm().Tips):
                if tip_mask & (1 << i):
                    dv = action*volume[i]
                    if wells[w].reagent is None:
                        logging.warning("There is no reagent in well {:d} of rack {:s}"
                                        .format(wells[w].offset+1, labware_selection.type.name + ": " + labware_selection.label))
                    assert wells[w].vol is not None, ("Volume of "
                                                      + wells[w].reagent.name
                                                      + " in well {:d} of rack {:s} not initialized."
                                                      .format(wells[w].offset + 1,
                                                              labware_selection.label))
                    nv = wells[w].vol - dv

                    if nv > wells[w].labware.type.max_vol:
                        err = ("trying to change the volume of " + str(wells[w])
                               + " to " + str(nv) + " but the maximum volume is "
                               + str(wells[w].labware.type.max_vol))
                        logging.error(err)
                        raise RuntimeError(err)

                    assert nv > -self.allow_air, "Error !!! trying to change the volume of " + str (wells[w])   \
                            + " to " + str(nv) + "uL. But only " + str(self.allow_air) + "uL of air are allowed"

                    wells[w].vol -= dv
                    if wells[w].vol < 0:                                   # don't allow air to fake reagent.
                        wells[w].vol = 0
                    if    action == Arm.Aspirate:
                        self.cur_arm().Tips[i] = labware.usedTip(tp, wells[w])  # todo FIX for already used tips
                        wells[w].log(-dv)
                    elif  action == Arm.Dispense:
                        assert isinstance(tp, labware.usedTip)
                        wells[w].log(-dv, tp.origin)
                    w += 1
        return volume, tip_mask

    def set_tips_back_executed(self, TIP_MASK, labware_selection):
        """ The low level instruction have to be generated already with almost all the information needed.
        Here we don't check any more where we really need to put the tips.
        Be careful by manual creation of low level instructions: they are safe if they are generated
        by protocol instructions (drop_tips(), and preserve and usePreserved were previously set).
        :param TIP_MASK:
        :param labware:
        """
        # todo what if self.droptips: is False ???
        assert isinstance(labware_selection, labware.DITIrack)

        TIP_MASK, tips = self.cur_arm().eject_tips_executed(TIP_MASK)
        labware_selection.set_back(TIP_MASK, tips)
        return TIP_MASK

    def pick_up_tips_executed(self, TIP_MASK, labware_selection : labware.DITIrack) -> int:
        """ The low level instruction have to be generated already with almost all the information needed.
        Here we don't check any more from where we really need to pick the tips
        and assume they are all in the same rack.
        Be careful by manual creation of low level instructions: they are safe if they are generated
        by protocol instructions (drop_tips(), and preserve and usePreserved were previously set).
        :param labware_selection:
        :param TIP_MASK:
        """
        assert isinstance(labware_selection, labware.DITIrack)

        TIP_MASK = self.cur_arm().getTips_test(TIP_MASK)
        tips = labware_selection.pick_up(TIP_MASK)
        return self.cur_arm().mount_tips_executed(tip_mask=TIP_MASK, tips=tips)

    def use_tips_executed(self, tipMask, labware_selection):                      # todo Deprecated ??????

        mask, tips = self.cur_arm().eject_tips_test(tipMask)
        assert len(tips) == len(labware_selection.selected())
        for i, w in enumerate(labware_selection.selected_wells()):
            self.cur_arm().Tips[tips[i]] = labware.usedTip(self.cur_arm().Tips[tips[i]], w)

    def move_labware_executed(self, labware, destination):
        # assert isinstance(labware, labware.Labware)
        # assert isinstance(destination, labware.WorkTable.Location)
        self.worktable.add_labware(labware, destination)

    # relatively simple "setters" and "getters" of current default options

    def set_worktable(self, templateFile, robot_protocol):
        # w = labware.WorkTable.cur_worktable
        logging.debug("Going to set template: " + str(templateFile))
        if templateFile is None: return
        if isinstance(self.worktable, labware.WorkTable):  # todo temp? really to set
            assert self.worktable.template_file_name == templateFile, 'Attemp to reset wortable from ' \
                                                                      + self.worktable.template_file_name + ' into ' + templateFile
        else:
            self.worktable  = labware.WorkTable(templateFile, robot_protocol)

    def set_as_current(self):
        Robot.current = self
        labware.curWorkTable=self.worktable # todo inconsistent duplication? allow for manuall actions?

    def set_drop_tips(self, drop=True)->bool:
        '''
        Drops the tips at THE END of the whole action? like after distribute of the reagent into various target?
        :param drop:
        :return: the previous value
        '''
        self.droptips, drop = drop, self.droptips
        return drop

    def set_allow_air(self, allow_air=0.0)->float:
        self.allow_air, allow_air = allow_air, self.allow_air
        return allow_air

    def reuse_tips(self, reuse=True)->bool:
        self.reusetips, reuse = reuse, self.reusetips
        return reuse

    def preserve_tips(self, preserve=True)->bool:
        self.preservetips, preserve = preserve, self.preservetips
        return preserve

    def use_preserved_tips(self, usePreserved=True)->bool:
        self.usePreservedtips, usePreserved = usePreserved, self.usePreservedtips
        return usePreserved

    def cur_arm(self, arm=None):

        if isinstance(arm, Arm):
            assert arm.index in self.arms
            assert arm is self.arms[arm.index]
            self.def_arm = arm.index
        else:
            if isinstance(arm, int):
                assert arm in self.arms
                self.def_arm = arm
            else:
                assert arm is None

        return self.arms[self.def_arm]

