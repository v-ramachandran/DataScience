#!/usr/bin/python
"""
CS194-16 Data Science Assignment 2
UC Berkeley

Venketaram Ramachandran
v.ramachandran28@berkeley.edu

"""

from __future__ import division
import math
import sys
import re

import numpy as np
from pandas import *

def add_party_column(df):
    """Add a column representing the candidate's party to the data frame.

    Args:
        df: A DataFrame generated from the campaign finance data csv file.

    Returns:
        A DataFrame based on df with an additional column keyed "party" whose
        values represent the party of the candidates.
        For Democratic candidates, use value "Democrat".
        For Republicans, use "Republican".
        For Libertarian candidates, use value "Libertarian".
    """
    # Enter a party name value for each candidate name found according to the mapping in __getParty__
    df['party']= [__getParty__(n) for n in df['cand_nm']]
    
    # Return the modified DataFrame
    return df

def mapMonths(df):
    df['contb_receipt_dt']=[re.sub(r'[\d-]','',n) for n in df['contb_receipt_dt']]
    return df
 
def __getParty__(name):
    
    republicans = ["Bachmann, Michelle", "Cain, Herman", "Huntsman, Jon", "Paul, Ron", "Pawlenty, Timothy", "Romney, Mitt", "Santorum, Rick", "Perry, Rick", "Roemer, Charles E. 'Buddy' III", "Gingrich, Newt", "Huntsman, Jon", "McCotter, Thaddeus G"]
    democrats = ["Obama, Barack"]
    libertarians = ["Johnson, Gary Earl"]
    if name in libertarians:
      return "Libertarian"
    elif name in democrats:
      return "Democrat"
    elif name in republicans:
      return "Republican"
    else:
      return "ERROR"

def stats_by_donor(df):
    """Find the party that received the highest amount of donations in a given
    state.

    Args:
        df: A DataFrame generated from the campaign finance data csv file
            with the column "party" added.
        state: The state of interest in capitalized two-letter format,
            e.g. "CA".

    Returns:
        Return a tuple consisting of a pair of values. The first value should be
        the name of the party, as defined in add_party_column(df), and the
        second value should be the fraction of the amount of donations the party
        received compared with other parties. E.g. ('Democrat', 0.21).
    """
    
    rFilterd=df[(df['party']=="Republican")][['contbr_st', 'contbr_nm']].drop_duplicates(['contbr_st', 'contbr_nm'])
    dFilterd=df[(df['party']=="Democrat")][['contbr_st', 'contbr_nm']].drop_duplicates(['contbr_st', 'contbr_nm'])
    total=rFilterd['contbr_nm'].sum() + dFilterd['contbr_nm'].sum()
    candGrps=rFilterd.groupby("contbr_st")
    temp=candGrps.agg(lambda x: x.sum()/total)
#    print temp
#    candGrps=dFilterd.groupby("contbr_st")
#    temp=candGrps.agg(lambda x: x.sum()/total)
    print temp
    
    
    # TODO: Implement this function.
    pass

def getRefunds(df):
    df['receipt_desc']=[str(n).lower() for n in df['receipt_desc']]
    refunds = df[(df["receipt_desc"]=="refund")&(df['contb_receipt_amt']<0)][['party', 'contb_receipt_amt']]
    print len(refunds['party'])
    refunds=refunds.groupby('party').agg(lambda x: x.count())
    print refunds

def help(tf):
    if tf:
      return 1
    else:
      return 0

def getUnemp(df):
    df['contbr_occupation']=[str(n).lower() for n in df['contbr_occupation']]
    df['contbr_employer']=[str(n).lower() for n in df['contbr_employer']]
    unempDf = df[(df["contbr_occupation"]=="not employed")|(df["contbr_employer"]=="not employed")]
    print "Count of Not Employed Donors:", len(unempDf.drop_duplicates('contbr_nm')["contbr_nm"])
    contbr=(unempDf["contb_receipt_amt"].sum())
    print "Total Contributed:", contbr
    print "Percentage of all Contributions:", (contbr/(df["contb_receipt_amt"].sum()))
    splits = unempDf[["contb_receipt_amt", "party"]].groupby('party').sum()
    print "Party Splits:", splits
    
def getPartySplits(df):
    stFilterd=df[(df['contb_receipt_amt']>0)][['party', 'contb_receipt_amt']]
    candGrps=stFilterd.groupby("party")
    temp=candGrps.agg(lambda x: x.sum())
    return temp

def getDonorCounts(df):
    filtered=df[['contbr_nm','cand_nm']].drop_duplicates(['contbr_nm','cand_nm'])
    temp=filtered.groupby("cand_nm").agg(lambda x: x.count())
    return temp

def getOccupations(df):
    jobs=df.drop_duplicates(['contbr_nm', 'contbr_occupation'])
    jobs=jobs.groupby('contbr_occupation', as_index=False).agg(lambda x: x.count())['contbr_occupation']
    print jobs
    return

def getLeadingStates(df):
    groupedSums=df[['contbr_st', 'party', 'contb_receipt_amt']].groupby(['contbr_st', 'party'], as_index=False).agg(np.sum)
    groupedSums=groupedSums.sort_index(by="contb_receipt_amt", ascending=False).drop_duplicates('contbr_st')
                  
      # How many states did Republicans win?
    states_won = groupedSums [(groupedSums['party']=="Republican")]['contbr_st']
    print "States Won Republicans:", states_won
    print len(states_won)  
      # How many states did Obama win?
    states_won = groupedSums [groupedSums['party']=="Democrat"]['contbr_st']
    print "States Won Democrats:", states_won
    print len(states_won)
      # How many states did the Libertarians win?
    states_won = groupedSums [groupedSums['party']=="Libertarian"]['contbr_st']
    print "States Won Libertarians:", states_won
    print len(states_won)

def getTrend(df):
    df['contb_receipt_dt']=[re.sub(r'[\d-]','',n) for n in df['contb_receipt_dt']]
    rep=df[(df['party']=="Republican")][['contb_receipt_dt', 'contb_receipt_amt']]
    dem=df[df['party']=="Democrat"][['contb_receipt_dt', 'contb_receipt_amt']]
    lib=df[df['party']=="Libertarian"][['contb_receipt_dt', 'contb_receipt_amt']]
    
    rep=rep.groupby('contb_receipt_dt', sort = False).agg(np.sum)
    dem=dem.groupby('contb_receipt_dt', sort = False).agg(np.sum)    
    lib=lib.groupby('contb_receipt_dt', sort = False).agg(np.sum)
    
    
    rep.to_csv('repTrend.csv')
    dem.to_csv('demTrend.csv')
    lib.to_csv('libTrend.csv')
    
def printIQR(df):
    df=df[['cand_nm', 'contb_receipt_amt']]
    from scipy import stats
    temp = df[df['cand_nm'] == "Obama, Barack"]
    vals = np.array(temp['contb_receipt_amt'])
    print stats.scoreatpercentile(vals, 25)
    print stats.scoreatpercentile(vals, 50)
    print stats.scoreatpercentile(vals, 75)      


def main(*args):
    
    df = read_csv('P00000001-ALL.txt')    
    df = add_party_column(df)
    
    pass
if __name__ =='__main__':
    sys.exit(main(*sys.argv[1:]))

