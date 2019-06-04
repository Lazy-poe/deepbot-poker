#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:40:29 2019

@author: cyril
"""

import csv
from collections import OrderedDict as OrderedDict
import torch
import re
import os
import pickle

def write_declare_action_state(action_id, round_id, valid_actions, hole_card, round_state, strat, action, amount, csv_file = './test_declare_action.csv'):
    state_row = [{'round_id': round_id, 'action_id': action_id, 'hole_card':hole_card, 'valid_actions':valid_actions, 
                  'round_state':round_state, 'strat':strat, 'action':action, 'amount':amount}]
    with open(csv_file,'a') as hand_data_csv:
        f_csv = csv.DictWriter(hand_data_csv, ['round_id','action_id','hole_card','valid_actions','round_state','strat','action','amount'])
        
        if(action_id==0):
            f_csv.writeheader()
        f_csv.writerows(state_row)
    return

def write_round_start_state(round_id, seats, csv_file = './test_round_start.csv'):
    state_row = [{'round_id': round_id, 'seats': seats}]
    with open(csv_file,'a') as hand_data_csv:
        f_csv = csv.DictWriter(hand_data_csv, ['round_id','seats'])
        if(round_id==0):
            f_csv.writeheader()
        f_csv.writerows(state_row)
    return

def write_round_result_state(round_id, winners, hand_info, round_state, csv_file = './test_round_results.csv'):
    state_row = [{'round_id': round_id, 'winners':winners, 'hand_info':hand_info, 'round_state':round_state}]
    with open(csv_file,'a') as hand_data_csv:
        f_csv = csv.DictWriter(hand_data_csv, ['round_id','winners','hand_info','round_state'])
        if(round_id==0):
            f_csv.writeheader()
        f_csv.writerows(state_row)
    return


def find_action_id(csv_file = './test_declare_action.csv'):
    try:
        with open(csv_file, 'r') as hand_data_csv:
            next_action_id = int(list(csv.reader(hand_data_csv))[-1][1])+1
    except:
        next_action_id = 0
    return next_action_id


def find_round_id(csv_file = './test_round_results.csv'):
    try:
        with open(csv_file, 'r') as hand_data_csv:
            next_round_id = int(list(csv.reader(hand_data_csv))[-1][0])+1
    except:
        next_round_id = 0
    return next_round_id

def prep_gen_dirs(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_) 
    if not os.path.exists(dir_+'/bots'):
        os.makedirs(dir_+'/bots') 
        
        
def get_all_gen_dicts(dir_, nb_bots = 50):
    all_dicts = []
    for bot_id in range(1,nb_bots+1):
        with open(dir_+'/bots/'+str(bot_id)+'/bot_'+str(bot_id)+'_dict.pkl', 'rb') as f:  
            full_dict = pickle.load(f)
            all_dicts.append(full_dict)
    return all_dicts