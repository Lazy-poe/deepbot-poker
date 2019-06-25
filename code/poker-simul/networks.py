#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 19:34:51 2019

@author: cyril
"""
from torch import nn
import torch
import numpy as np

class Net(nn.Module):
    def __init__(self, i_opp, i_gen):
        super(Net, self).__init__()
        self.LSTM_opp = nn.LSTM(input_size =8, hidden_size = 50, num_layers=1)
        self.LSTM_gen = []
        for i in range(10):
            self.LSTM_gen.append(nn.LSTM(8, 10))
        self.LSTM_gen = nn.ModuleList(self.LSTM_gen)
        self.lin_dec_1 = nn.Linear(150, 75)
        self.lin_dec_2 = nn.Linear(75, 1)
        self.i_opp = i_opp
        self.i_gen = i_gen
        self.u_opp = i_opp.copy()
        self.u_gen = i_gen.copy()

    def forward(self, x):
        x_opp_out, (self.u_opp['opp_h0'], self.u_opp['opp_c0']) = self.LSTM_opp(x, (self.u_opp['opp_h0'], self.u_opp['opp_c0']))
        #print('x_opp_out: '+str(x_opp_out[0][0][:20]))
        x_opp_out = self.LSTM_opp(x)
        x_gen_all, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']) = self.LSTM_gen[0](x, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']))
        for i in range(1,10):
            x_gen, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]) = self.LSTM_gen[i](x, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]))
            #x_gen_all = torch.cat((x_gen_all,self.LSTM_gen[i](x, (i_gen['h0_'+str(i)].view(1,1,10), i_gen['c0_'+str(i)].view(1,1,10)))[0].view(1,1,1,-1)),0)
            x_gen_all = torch.cat((x_gen_all,x_gen),0)

        x_gen_out = x_gen_all.view(1,1,-1)
        x_lin_h = torch.tanh(self.lin_dec_1(torch.cat((x_gen_out,x_opp_out[0]),2)))
        x_out = torch.tanh(self.lin_dec_2(x_lin_h))
        return x_out
    
    def reset_u_opp(self):
        self.u_opp = self.i_opp.copy()
    def reset_u_gen(self):
        self.u_gen = self.i_gen.copy()
    def reset(self):
        self.reset_u_opp()
        self.reset_u_gen()
        return
    
    
    
class Net_2(nn.Module):
    def __init__(self, i_opp, i_gen):
        super(Net_2, self).__init__()
        self.LSTM_opp = []
        for i in range(10):
            self.LSTM_opp.append(nn.LSTM(8, 10))
            self.LSTM_opp = nn.ModuleList(self.LSTM_opp)
        
        self.LSTM_gen = []
        for i in range(10):
            self.LSTM_gen.append(nn.LSTM(8, 10))
        self.LSTM_gen = nn.ModuleList(self.LSTM_gen)
        self.lin_dec_1 = nn.Linear(200, 50)
        self.lin_dec_2 = nn.Linear(50, 10)
        self.lin_dec_3 = nn.Linear(10, 1)
        self.i_opp = i_opp
        self.i_gen = i_gen
        self.u_opp = i_opp.copy()
        self.u_gen = i_gen.copy()

    def forward(self, x):
        #x_opp_out, (self.u_opp['h0'], self.u_opp['c0']) = self.LSTM_opp(x, (self.u_opp['h0'], self.u_opp['c0']))
        #print('x_opp_out: '+str(x_opp_out[0][0][:20]))
        #x_opp_out = self.LSTM_opp(x)
        
        #Opponent blocks
        x_opp_all, (self.u_opp['opp_h0_0'], self.u_opp['opp_c0_0']) = self.LSTM_opp[0](x, (self.u_opp['opp_h0_0'], self.u_opp['opp_c0_0']))
        for i in range(1,10):
            x_opp, (self.u_opp['opp_h0_'+str(i)], self.u_opp['opp_c0_'+str(i)]) = self.LSTM_opp[i](x, (self.u_opp['opp_h0_'+str(i)], self.u_opp['opp_c0_'+str(i)]))
            x_opp_all = torch.cat((x_opp_all,x_opp),0)
        x_opp_out = x_opp_all.view(1,1,-1) 
        #General blocks
        x_gen_all, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']) = self.LSTM_gen[0](x, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']))
        for i in range(1,10):
            x_gen, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]) = self.LSTM_gen[i](x, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]))
            #x_gen_all = torch.cat((x_gen_all,self.LSTM_gen[i](x, (i_gen['h0_'+str(i)].view(1,1,10), i_gen['c0_'+str(i)].view(1,1,10)))[0].view(1,1,1,-1)),0)
            x_gen_all = torch.cat((x_gen_all,x_gen),0)
        x_gen_out = x_gen_all.view(1,1,-1)
        
        #Linear layers
        x_lin_h_1 = torch.tanh(self.lin_dec_1(torch.cat((x_gen_out,x_opp_out),2)))
        x_lin_h_2 = torch.tanh(self.lin_dec_2(x_lin_h_1))
        x_out = torch.tanh(self.lin_dec_3(x_lin_h_2))
        return x_out
    
    def reset_u_opp(self):
        self.u_opp = self.i_opp.copy()
    def reset_u_gen(self):
        self.u_gen = self.i_gen.copy()
    def reset(self):
        self.reset_u_opp()
        self.reset_u_gen()
        return
    


class Net_6maxSingle(nn.Module):
    def __init__(self, i_gen):
        super(Net_6maxSingle, self).__init__()
        self.LSTM_gen = []
        for i in range(10):
            self.LSTM_gen.append(nn.LSTM(12, 10))
        self.LSTM_gen = nn.ModuleList(self.LSTM_gen)
        self.lin_dec_1 = nn.Linear(100, 50)
        self.lin_dec_2 = nn.Linear(50, 10)
        self.lin_dec_3 = nn.Linear(10, 1)
        self.i_gen = i_gen
        self.i_opp = dict()
        self.u_gen = i_gen.copy()

    def forward(self, x):        
        #General blocks
        x_gen_all, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']) = self.LSTM_gen[0](x, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']))
        for i in range(1,10):
            x_gen, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]) = self.LSTM_gen[i](x, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]))
            #x_gen_all = torch.cat((x_gen_all,self.LSTM_gen[i](x, (i_gen['h0_'+str(i)].view(1,1,10), i_gen['c0_'+str(i)].view(1,1,10)))[0].view(1,1,1,-1)),0)
            x_gen_all = torch.cat((x_gen_all,x_gen),0)
        x_gen_out = x_gen_all.view(1,1,-1)
        
        #Linear layers
        x_lin_h_1 = torch.tanh(self.lin_dec_1(x_gen_out))
        x_lin_h_2 = torch.tanh(self.lin_dec_2(x_lin_h_1))
        x_out = torch.tanh(self.lin_dec_3(x_lin_h_2))
        return x_out

    def reset_u_gen(self):
        self.u_gen = self.i_gen.copy()
    def reset(self):
        self.reset_u_gen()
        return
    
class Net_6maxFull(nn.Module):
    def __init__(self, i_opp, i_gen):
        super(Net_6maxFull, self).__init__()
        #general blocks
        self.LSTM_gen = []
        for i in range(10):
            self.LSTM_gen.append(nn.LSTM(12, 10))
        self.LSTM_gen = nn.ModuleList(self.LSTM_gen)
        #self.lin_dec_1 = nn.Linear(100, 50)
        
        #opponent blocks
        self.nb_opponents=5
        self.LSTM_opp_round = [[],[],[],[],[]]
        self.LSTM_opp_game = [[],[],[],[],[]]
        for opponent_id in range(self.nb_opponents):
            for i in range(10):
                self.LSTM_opp_round[opponent_id].append(nn.LSTM(4, 5))
            self.LSTM_opp_round[opponent_id] = nn.ModuleList(self.LSTM_opp_round[opponent_id])
            for i in range(10):
                self.LSTM_opp_game[opponent_id].append(nn.LSTM(4, 5))
            self.LSTM_opp_game[opponent_id] = nn.ModuleList(self.LSTM_opp_game[opponent_id])
        self.LSTM_opp_round=nn.ModuleList(self.LSTM_opp_round)
        self.LSTM_opp_game=nn.ModuleList(self.LSTM_opp_game)
        
        self.lin_dec_1 = nn.Linear(200,50)
        self.lin_dec_2 = nn.Linear(50, 10)
        self.lin_dec_3 = nn.Linear(10, 1)
        self.i_opp = i_opp
        self.i_gen = i_gen
        self.u_opp = i_opp.copy()
        self.u_gen = i_gen.copy()


    def forward(self, x):        
        #General blocks
        x_gen_in=x[:,:,:12]
        
        x_gen_all, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']) = self.LSTM_gen[0](x_gen_in, (self.u_gen['gen_h0_0'], self.u_gen['gen_c0_0']))
        for i in range(1,10):
            x_gen, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]) = self.LSTM_gen[i](x_gen_in, (self.u_gen['gen_h0_'+str(i)], self.u_gen['gen_c0_'+str(i)]))
            x_gen_all = torch.cat((x_gen_all,x_gen),0)
        x_gen_out = x_gen_all.view(1,1,-1)
        #linear layer
        #x_lin_h_1_gen = torch.tanh(self.lin_dec_1(x_gen_out))
        
        #Opponent blocks
        #x_opp_out=torch.Tensor([0,]*self.nb_opponents)
        x_opp_out=[]
        for opp_id in range(self.nb_opponents):
            x_opp = x[:,:,12+opp_id*5:12+(opp_id+1)*5]
            x_active = x_opp[:,:,0]
            x_opp_in = x_opp[:,:,1:]    
            
            ##opponent game lstms
            x_opp_single, (self.u_gen['opp_game_h0_'+str(opp_id)+'_0'], self.u_gen['opp_game_c0_'+str(opp_id)+'_0']) = self.LSTM_opp_game[opp_id][0](x_opp_in, (self.u_gen['opp_game_h0_'+str(opp_id)+'_0'], self.u_gen['opp_game_c0_'+str(opp_id)+'_0']))
            for i in range(1,10):
                x_opp_game, (self.u_gen['opp_game_h0_'+str(opp_id)+'_'+str(i)], self.u_gen['opp_game_c0_'+str(opp_id)+'_'+str(i)]) = self.LSTM_opp_game[opp_id][i](x_opp_in, (self.u_gen['opp_game_h0_'+str(opp_id)+'_'+str(i)], self.u_gen['opp_game_c0_'+str(opp_id)+'_'+str(i)]))
                x_opp_single = torch.cat((x_opp_single,x_opp_game),0)
            for i in range(0,10):
                x_opp_round, (self.u_opp['opp_round_h0_'+str(opp_id)+'_'+str(i)], self.u_opp['opp_round_c0_'+str(opp_id)+'_'+str(i)]) = self.LSTM_opp_round[opp_id][i](x_opp_in, (self.u_opp['opp_round_h0_'+str(opp_id)+'_'+str(i)], self.u_opp['opp_round_c0_'+str(opp_id)+'_'+str(i)]))
                x_opp_single = torch.cat((x_opp_single,x_opp_game),0)
                
            x_opp_single = x_opp_single.view(1,1,-1) 
            #linear layer
            #x_lin_h_1_opp = torch.tanh(self.lin_dec_1_opp(x_opp_out))
            if x_active==1:
                x_opp_out.append(x_opp_single)
            
        #Average of active opponent outputs
        x_opp_out_avg = torch.stack(x_opp_out).mean(0)
        test=torch.cat((x_gen_out,x_opp_out_avg),2)
        #final linear layers
        x_lin_h_1 = torch.tanh(self.lin_dec_1(test))
        x_lin_h_2 = torch.tanh(self.lin_dec_2(x_lin_h_1))
        x_out = torch.tanh(self.lin_dec_3(x_lin_h_2))
        return x_out

    def reset_u_opp(self):
        self.u_opp = self.i_opp.copy()
    def reset_u_gen(self):
        self.u_gen = self.i_gen.copy()
    def reset(self):
        self.reset_u_opp()
        self.reset_u_gen()
        return
    