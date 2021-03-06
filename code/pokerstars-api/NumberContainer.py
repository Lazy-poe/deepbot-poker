#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2

@author: cyril
"""

from functools import reduce
import os
import pyautogui

from ScreenItem import ScreenItem
from Number import Number
import math
from extra_functions import angle_between

import constants
#import glob_file

my_verbose = False

class NumberContainer(ScreenItem):
    def __init__(self, id_, type):
        #ScreenItem.__init__(self,id_,image_file,detection_confidence)
        self.id=id_
        self.type=type
        self.numbers = []
        self.value = 0
        self.corresponding_entity = None

    def addNumber(self, number):
        self.numbers.append(number)
        return

    def computeValue(self):
        numbers_string = [number.value for number in self.numbers]
        value = int(reduce(lambda x,y: x+str(y), numbers_string, ''))
        self.value = value
        return

    def attributeEntity(self, players, table_center):
        if ((self.numbers[0].left-table_center[0])**2 + (self.numbers[0].top-table_center[1])**2)**(1/2)<constants.POT_ZONE_LENGTH:
            self.corresponding_entity = 'POT'
        else:
            vect_number_cont = [self.numbers[0].left-table_center[0],self.numbers[0].top-table_center[1]]
            deg_number_cont = angle_between([1,0],vect_number_cont)
            if(deg_number_cont<=0):
                deg_number_cont+=360
            for i in range(constants.NB_PLAYERS):
                if((deg_number_cont>constants.DEG_PLAYERS[i]['left'] and deg_number_cont<=constants.DEG_PLAYERS[i]['right'])
                    or ((constants.DEG_PLAYERS[i]['left']>constants.DEG_PLAYERS[i]['right'])  #special case to complete circle
                    and (deg_number_cont>constants.DEG_PLAYERS[i]['left'] or deg_number_cont<=constants.DEG_PLAYERS[i]['right']))):
                    self.corresponding_entity = i
                    break
            
        if self.corresponding_entity!='POT':
            players[self.corresponding_entity].bet_value = self.value

        if(my_verbose):
            print('[NumberContainer] Attributing '+str(self.type)+' of size '+str(self.value)+' to '+str(self.corresponding_entity))


        return
        """
        #old implementation
        min_norm_2 = math.inf
        corresponding_entity_id = -1
        entity_is_player = None
        #searching for closest player
        for player in players:
            norm_2 = (self.numbers[0].left-player.center_pos[0])**2 + (self.numbers[0].top-player.center_pos[1])**2
            if norm_2<min_norm_2:
                min_norm_2 = norm_2
                corresponding_entity_id = player.id
                entity_is_player = True
        #checkin wether pot (center of table) is closer
        if not(entity_is_player): norm_2 = ((self.numbers[0].left-table_center[0])**2 + (self.numbers[0].top-table_center[1])**2)*2
        else: norm_2 = ((self.numbers[0].left-table_center[0])**2 + (self.numbers[0].top-table_center[1])**2)*2.5

        if norm_2<min_norm_2:
            min_norm_2 = norm_2
            corresponding_entity_id = 'POT'
            entity_is_player = False

        if(my_verbose):
            if(entity_is_player==None):
                print('[Error] Could not attribute entity to number container '+ self.id)
            elif(entity_is_player==True):
                print('[NumberContainer] Attributing '+str(self.type)+' of size '+str(self.value)+' to '+str(corresponding_entity_id))
                players[corresponding_entity_id].setCorrespondingNumbers(type=self.type, value=self.value)
            elif(entity_is_player ==False):
                print('[NumberContainer] Attributing '+str(self.type)+' of size '+str(self.value)+' to '+str(corresponding_entity_id))

        self.corresponding_entity = corresponding_entity_id
        return #corresponding_entity_id
        """

