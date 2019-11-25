#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:30:03 2019

@author: cyril
"""
import os
import pickle
import torch
from collections import OrderedDict

def flatten_list(list):
    return [x for sublist in list for x in sublist]

def get_flat_params(full_dict):
    params = torch.Tensor(0)
    for key in sorted(full_dict.keys()):
        params = torch.cat((params, full_dict[key].view(-1)),0)
    return params

def get_full_dict(all_params, m_sizes_ref):
    #dict_sizes=get_dict_sizes(m_sizes_ref.state_dict,m_sizes_ref.model.i_opp,m_sizes_ref.model.i_gen)
    dict_sizes=get_dict_sizes(m_sizes_ref.full_dict)
    full_dict = OrderedDict()
    i_start = 0
    for layer in sorted(dict_sizes.keys()):
        full_dict[layer] = torch.Tensor(all_params[i_start:i_start+dict_sizes[layer]['numel']]).view(dict_sizes[layer]['shape'])
        i_start+=dict_sizes[layer]['numel']
    return full_dict

def get_dict_sizes(all_dicts):
    dict_sizes = OrderedDict()
    #all_dicts = state_dict.copy()
    #all_dicts.update(i_opp), all_dicts.update(i_gen)
    for key in all_dicts.keys():
        dict_sizes[key] = {}
        dict_sizes[key]['numel'] = all_dicts[key].numel()
        dict_sizes[key]['shape'] = list(all_dicts[key].shape)
    return dict_sizes

def get_gen_flat_params(dir_):
    all_gen_flat = []
    for bot_id in os.listdir(dir_+'/bots'):
        with open(dir_+'/bots/'+str(bot_id)+'/bot_'+str(bot_id)+'_flat.pkl', 'rb') as f:
            params_flat = pickle.load(f)
            all_gen_flat.append(params_flat)
    return all_gen_flat

def prep_gen_dirs(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    if not os.path.exists(dir_+'/bots'):
        os.makedirs(dir_+'/bots')

def reduce_full_dict(full_dict):
    nb_opps=4
    nb_LSTM = 10
    for opp_id in range(1,nb_opps+1):
        for lstm_id in range(nb_LSTM):
            full_dict.pop('opp_round_h0_'+str(opp_id)+'_'+str(lstm_id),None)
            full_dict.pop('opp_round_c0_'+str(opp_id)+'_'+str(lstm_id),None)
            full_dict.pop('opp_game_h0_'+str(opp_id)+'_'+str(lstm_id),None)
            full_dict.pop('opp_game_c0_'+str(opp_id)+'_'+str(lstm_id),None)
    return full_dict

def extend_full_dict(full_dict):
    nb_opps=4
    nb_LSTM = 10
    for opp_id in range(1,nb_opps+1):
        for lstm_id in range(nb_LSTM):
            full_dict['opp_round_h0_'+str(opp_id)+'_'+str(lstm_id)] = full_dict['opp_round_h0_0_'+str(lstm_id)].clone()
            full_dict['opp_round_c0_'+str(opp_id)+'_'+str(lstm_id)] = full_dict['opp_round_c0_0_'+str(lstm_id)].clone()
            full_dict['opp_game_h0_'+str(opp_id)+'_'+str(lstm_id)] = full_dict['opp_game_h0_0_'+str(lstm_id)].clone()
            full_dict['opp_game_c0_'+str(opp_id)+'_'+str(lstm_id)] = full_dict['opp_game_c0_0_'+str(lstm_id)].clone()
    return full_dict
