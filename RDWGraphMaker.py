# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:31:18 2019

@author: messinjf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.stats.multicomp

PATH = "C:\\Users\\messinjf\\Desktop\\Results April 8th\\"
APF_RS = PATH + "APF-RS.csv"
APF_GA = PATH + "APF-GA.csv"
APF_GAU = PATH + "APF-GAU.csv"
STC = PATH + "STC.csv"
CONTROL = PATH + "CONTROL.csv"

IDX_TO_ROOM_CONDITION = ["2 User 25x25", "3 user 30x30", "5 user 40x40",
                         "Rectangle", "L-shape", "Cross", "Trapezoid"]


def CreateBarGraph(df1, df2, columnName='totalResets'):
    avgs1, sems1 = GetAveragesForEachRoom(df1, columnName=columnName)
    avgs2, sems2 = GetAveragesForEachRoom(df2, columnName=columnName)
    # create plot
    fig, ax = plt.subplots(figsize=(8, 5))
    index = np.arange(len(IDX_TO_ROOM_CONDITION))
    bar_width = 0.35
    opacity = 0.8
     
    rects1 = plt.bar(index, avgs1, bar_width,
    alpha=opacity,
    color='b',
    label='Old')
    plt.errorbar(index, avgs1, yerr=sems1, c='black', fmt='o')
     
    rects2 = plt.bar(index + bar_width, avgs2, bar_width,
    alpha=opacity,
    color='g',
    label='New')
    plt.errorbar(index + bar_width, avgs2, yerr=sems2, c='black', fmt='o')
     
    plt.xlabel('Condition')
    plt.ylabel(columnName)
    #plt.title('TODO')
    plt.xticks(index + bar_width, IDX_TO_ROOM_CONDITION)
    plt.legend()
     
    plt.tight_layout()
    plt.show()
    
def CreateBarGraph2(df_dict, attribute='totalResets', ylabel=None, title=None, combine=False):
    
    # Use attribute as y label if none is given.
    if(ylabel == None):
        ylabel = attribute
    fig = None
    ax = None
    index = np.arange(len(IDX_TO_ROOM_CONDITION))
    bar_width = 0.75 / len(df_dict)
    if(combine):
        fig, ax = plt.subplots(figsize=(4, 6))
        bar_width *= len(IDX_TO_ROOM_CONDITION)
    else:
        fig, ax = plt.subplots(figsize=(9, 6))
    opacity = 0.8
    
    for i, key in enumerate(df_dict):
        df = df_dict[key]
        
        if(not combine):
            avgs, sems = GetAveragesForEachRoom(df, columnName=attribute)
         
            rects = plt.bar(index + i * bar_width, avgs, bar_width,
            alpha=opacity,
            label=key)
            plt.errorbar(index + i * bar_width, avgs, yerr=sems, fmt='o')
            for j in range(len(avgs)):
                #print("{} {} {}\n\tMean: {} +/- {}".format(key, IDX_TO_ROOM_CONDITION[j], attribute, round(avgs[j],3), round(sems[j],3)))
                pass
            
        else:
            
            avg_all = np.average(df[attribute])
            sem_all = sem(df[attribute])
            rects = plt.bar(i * bar_width, avg_all, bar_width,
            alpha=opacity,
            label=key)
            plt.errorbar(i * bar_width, avg_all, yerr=sem_all, fmt='o')
            
    #rects2 = plt.bar(index + bar_width, avgs2, bar_width,
    #alpha=opacity,
    #color='g',
    #label='New')
    #plt.errorbar(index + bar_width, avgs2, yerr=sems2, c='black', fmt='o')
    plt.ylabel(ylabel)
    if(title != None):
        plt.title(title)
    
    # Determines where to place the tick that labels the condition.
    if(not combine):
        plt.xticks(rotation=-45)
        plt.xlabel('Condition')
        tick_slot = (len(df_dict) - 1) / 2
        plt.xticks(index + tick_slot * bar_width, IDX_TO_ROOM_CONDITION)
        ax.legend(loc='upper center', shadow=True, ncol=5)
    else:
        # Use ticks instead of legend
        plt.xticks(rotation=-45)
        index = np.arange(len(df_dict))
        plt.xticks(index * bar_width, df_dict.keys())
    #plt.legend()
    lower_ylim, upper_ylim = ax.get_ylim()
    ax.set_ylim(lower_ylim, 1.05 * upper_ylim)
     
    plt.tight_layout()
    #plt.show()
    plt.savefig("C:\\Users\\messinjf\\Desktop\\Results April 8th\\{}.png".format(title))


def DisplayComparison(df1, df2):
    CreateBarGraph(df1, df2, columnName='wallResets')
    CreateBarGraph(df1, df2, columnName='userResets')
    CreateBarGraph(df1, df2, columnName='totalResets')
    #CreateBarGraph(df1, df2, columnName='physDistToCenter')
    #CreateBarGraph(df1, df2, columnName='totalVirtTime')
    #CreateBarGraph(df1, df2, columnName='totalVirtDist')
    
    
def ConcatenateResults(df_dict):
    df_concat_list = []
    for k, df in df_dict.items():
        trials = df.shape[0]
        temp_df = df.drop(['subNum', 'condition', 'totalVirtDist', 'largestPosJump', 'numJumpsGreaterThanOneMeter'], axis='columns')
        #print(temp_df.columns)
        temp_df['algorithm'] = [k for i in range(trials)]
        
        assert(trials % len(IDX_TO_ROOM_CONDITION) == 0)
        stepSize = trials // len(IDX_TO_ROOM_CONDITION)
        temp_df['room_condition']= [IDX_TO_ROOM_CONDITION[i // stepSize] for i in range(trials)]
        #print(temp_df['condition'].value_counts())
        df_concat_list.append(temp_df)
    df = pd.concat(df_concat_list, ignore_index=True)
    print(df['room_condition'].value_counts())
    print(df)
    return(df)
    
def RunAnova(df):
    
    print(df.columns)
    
    # Fits the model with the interaction term
    # This will also automatically include the main effects for each factor
    model = ols('totalResets ~ C(algorithm)*C(room_condition)', df).fit()

    # Seeing if the overall model is significant
    print(f"Overall model F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}, p = {model.f_pvalue: .4f}")
    print(model.summary())
    
    # Creates the ANOVA table
    res = sm.stats.anova_lm(model, typ= 2)
    pd.set_option('display.expand_frame_repr', False)
    print(res)
    
    def anova_table(aov):
        aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']
        
        aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
        
        aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])
        
        cols = ['sum_sq', 'mean_sq', 'df', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
        aov = aov[cols]
        return aov

    print(anova_table(res))

def GetAveragesForEachRoom(df, columnName='totalResets', split=7):
    
    # Assert that the number of columns is divisible by split
    assert(df.shape[0] % split == 0)
    stepSize = df.shape[0] // split
    values = df[columnName].values
    averages = [np.average(values[i*stepSize:(i+1)*stepSize]) for i in range(split)]
    sems = [sem(values[i*stepSize:(i+1)*stepSize]) for i in range(split)]
    return averages, sems

if __name__ == "__main__":
    df_rs = pd.read_csv(APF_RS, skipinitialspace=True)
    df_ga = pd.read_csv(APF_GA, skipinitialspace=True)
    df_gau = pd.read_csv(APF_GAU, skipinitialspace=True)
    df_stc = pd.read_csv(STC, skipinitialspace=True)
    df_ctr = pd.read_csv(CONTROL, skipinitialspace=True)
    
    df_dict = {"Control" :df_ctr,
               "STC" : df_stc,
               "APF-GAU" : df_gau,
               "APF-RS" : df_rs,
               "APF-GA" :df_ga
            }
    
    
#    print(df_old.head())
#    print("df shape: {}".format(df_old.shape))
    print("column names: {}".format(df_ga.columns))
#    avgs, stds = GetAveragesForEachRoom(df_old)
#    print("averages: {}".format(avgs))
#    print("stds: {}".format(stds))
    DisplayComparison(df_rs, df_ga)
    CreateBarGraph2(df_dict, attribute='totalResets', ylabel = 'Total Resets', title='Effect of Condition and Algorithm on Total Resets')
    CreateBarGraph2(df_dict, attribute='wallResets', ylabel = 'Wall Resets', title='Effect of Condition and Algorithm on Wall Resets')
    CreateBarGraph2(df_dict, attribute='userResets', ylabel = 'User Resets', title='Effect of Condition and Algorithm on User Resets')
    CreateBarGraph2(df_dict, attribute='totalPhysDist', ylabel = 'Total Distance Traveled (m)', title='Effect of Condition and Algorithm on Distance Traveled')
    CreateBarGraph2({"APF-GAU (no scaling)" : df_gau, "APF-GA (scaling)" :df_ga}, attribute='steeringRateAvg', ylabel = 'Redirection Rate ($^\circ$/sec)', title='Effect of Proximity Scaling on Redirection Rate', combine=True)
    CreateBarGraph2({"APF-GAU (no scaling)" : df_gau, "APF-GA (scaling)" :df_ga}, attribute='totalResets', ylabel = 'Redirection Rate ($^\circ$/sec)', title='Effect of Proximity Scaling on Total Resets', combine=True)
    df = ConcatenateResults(df_dict)
    RunAnova(df)