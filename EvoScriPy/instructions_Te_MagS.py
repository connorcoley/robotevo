# Copyright (C) 2014-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2014-2019
__author__ = 'Ariel'

""" A.15.10 Advanced Worklist Commands for the Te-MagS """

import logging
import EvoScriPy.evo_mode
import EvoScriPy.labware
from EvoScriPy.Instruction_Base import *



class Te_MagS_MoveToPosition(TMagInstr):
    """
    A.15.10.1 MoveToPosition (Worklist: Te-MagS_MoveToPosition)
    """
    Dispense    = 0
    Aspirate    = 1
    Re_suspension = 2
    Incubation  = 3

    def __init__(self,  position, z_pos=31, needs_allwd_lw=0, allowed_labware="" ):

        """

        :param position: Aspirate Position  - Carrier above the magnet block, magnet block raised.
                         Dispense Position - Carrier above the magnet block, magnet block lowered.
                         Incubation Position - Carrier above the heating block, heating block raised.
                         Re-suspension Position - Carrier above the heating block, heating block lowered.
                             Use this position to carry out re-suspension by mixing the liquid with
                             the pipetting tips (e.g. with the LiHa - Mix script command).
        :param z_pos:
        :param needs_allwd_lw:
        :param allowed_labware:
        """
        TMagInstr.__init__(self, "Te-MagS_MoveToPosition")

        self.allowed_labware = allowed_labware
        self.needs_allwd_lw = needs_allwd_lw
        self.z_pos = z_pos
        self.position = position

    def validate_arg(self):
        TMagInstr.validate_arg(self)
        assert self.needs_allwd_lw == 0
        assert self.allowed_labware == ""

        pos = int(self.position)
        if pos == Te_MagS_MoveToPosition.Aspirate:
            pos = "{:d} {:d}".format( pos, int(self.z_pos) )

        self.arg += [ Expression(pos), Expression(self.needs_allwd_lw), Expression(self.allowed_labware)]
        return True


class Te_MagS_ActivateHeater(TMagInstr):
    """
    A.15.10.2 ActivateHeater (Worklist: Te-MagS_ActivateHeater)
    """

    def __init__(self,  temperature, needs_allwd_lw=0, allowed_labware="" ):

        TMagInstr.__init__(self, "Te-MagS_ActivateHeater")

        self.temperature = temperature
        self.allowed_labware = allowed_labware
        self.needs_allwd_lw = needs_allwd_lw


    def validate_arg(self):
        TMagInstr.validate_arg(self)
        assert self.needs_allwd_lw == 0
        assert self.allowed_labware == ""

        self.arg += [ Expression(self.temperature), Expression(self.needs_allwd_lw), Expression(self.allowed_labware)]
        return True


class Te_MagS_DeactivateHeater(TMagInstr):
    """
    A.15.10.3 DeactivateHeater (Worklist: Te-MagS_DeactivateHeater)
    """

    def __init__(self,  exec_parameters="", needs_allwd_lw=0, allowed_labware="" ):

        TMagInstr.__init__(self, "Te-MagS_DeactivateHeater")

        self.exec_parameters = exec_parameters
        self.allowed_labware = allowed_labware
        self.needs_allwd_lw = needs_allwd_lw


    def validate_arg(self):
        TMagInstr.validate_arg(self)

        assert self.needs_allwd_lw == 0
        assert self.allowed_labware == ""
        assert self.exec_parameters == ""

        self.arg += [ Expression(self.exec_parameters), Expression(self.needs_allwd_lw), Expression(self.allowed_labware)]
        return True



class Te_MagS_Execution(TMagInstr):
    """
    A.15.10.4 Execution (Worklist: Te-MagS_Execution)
    """
    class Parametr:
        def __init__(self, num):
            self.num=num

        def __str__(self):
            return "{:d}:".format(int(self.num))


    class mix: #(Parametr):
        def __init__(self, cycles, hh, mm, ss, z_pos=31):
            self.z_pos = z_pos
            self.ss = ss
            self.mm = mm
            self.hh = hh
            self.cycles = cycles
        def __str__(self):
            return "1:{:d} {:d} {:d} {:d} {:d}".format(int(self.cycles),
                                                       int(self.hh), int(self.mm), int(self.ss),
                                                       int(self.z_pos) )

    class incub: #(Parametr):
        def __init__(self, hh, mm, ss):
            self.ss = ss
            self.mm = mm
            self.hh = hh
        def __str__(self):
            return "2:{:d} {:d} {:d}".format(int(self.hh), int(self.mm), int(self.ss))

    class wait: #(Parametr):
        def __init__(self, hh, mm, ss):
            self.ss = ss
            self.mm = mm
            self.hh = hh
        def __str__(self):
            return "3:{:d} {:d} {:d}".format(int(self.hh), int(self.mm), int(self.ss))

    class move: #(Parametr):
        def __init__(self,position, z_pos):
            self.z_pos = z_pos
            self.position=position + 1

        def __str__(self):
            return "4:{:d} {:d}".format(int(self.position), int(self.z_pos))

    class command: #(Parametr):
        def __init__(self,firmware_command):     # example ="RPZ1" ???????
            self.firmware_command = firmware_command

        def __str__(self):
            return "5:"+ self.firmware_command



    def __init__(self,  exec_parameters=[], needs_allwd_lw=0, allowed_labware="" ):

        TMagInstr.__init__(self, "Te-MagS_Execution")

        self.exec_parameters = exec_parameters
        self.allowed_labware = allowed_labware
        self.needs_allwd_lw = needs_allwd_lw


    def validate_arg(self):
        TMagInstr.validate_arg(self)

        assert self.needs_allwd_lw == 0
        assert self.allowed_labware == ""

        pr=self.exec_parameters     #  + [Te_MagS_Execution.command()]
        pr = ','.join( [str(cm) for cm in pr] )

        self.arg += [ Expression(pr) , Expression(self.needs_allwd_lw), Expression(self.allowed_labware)]
        return True
