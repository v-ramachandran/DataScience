#!/usr/bin/python
"""
CS194-16 Data Science Assignment 1
UC Berkeley

Venketaram Ramachandran
v.ramachandran28@berkeley.edu

"""

from __future__ import division
import math
import sys

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

def num_donation_records(df):
    """Return the total number of donation records.
    
    Args:
        df: A DataFrame generated from the campaign finance data csv file.

    Returns:
        An integer count of the number of donation records.
    """
    
    # Count the Total number of donation records
    return df['contb_receipt_amt'].count()

def num_refund_records(df):
    """Return the number of refund records.
    
    Args:
        df: A DataFrame generated from the campaign finance data csv file.

    Returns:
        An integer count of the number of refund records.
    """
    # Select amounts that are less than zero and count the total remaining amounts
    return df[df['contb_receipt_amt'] < 0].count()['contb_receipt_amt']
    pass


def num_donors(df, state):
    """Return the number of people that have donated in the given state.
    
    Assume people have unique names (i.e. no two person share the same name).
    Do not count the same person twice.

    Args:
        df: A DataFrame generated from the campaign finance data csv file.
        state: The state of interest in capitalized two-letter format,
            e.g. "CA".

    Returns:
        An integer count of the number of donors.
    """
    # Select only rows with the appropriate state, and clean duplicates since we want distinct donors.
    return df[(df['contbr_st']==state)].drop_duplicates('contbr_nm')['contbr_nm'].count()

def top_candidate_by_num_donors(df, state):
    """Find the candidate that received the most donations (by the number of
    donation records) in a given state.

    Args:
        df: A DataFrame generated from the campaign finance data csv file.
        state: The state of interest in capitalized two-letter format,
            e.g. "CA".

    Returns:
        A tuple consisting of a pair of values. The first value should be the
        name of the candidate, and the second value should be the fraction of
        the number of donations he received compared with all candidates.
        E.g. ('Cain, Herman', 0.115).
    """
    
    # Obtain the filtered version of the DF with correspondence to state and clean duplicate candidate, contributor pairs
    filtered=df[(df['contbr_st']==state)][['contbr_nm','cand_nm']].drop_duplicates(['contbr_nm','cand_nm'])
    
    # Get the state total, counting one for each candidate, contributor pair
    stateTotal = filtered['contbr_nm'].count()
    
    # Group by candidate name Aggregate the total count of donors.
    temp=filtered.groupby("cand_nm").agg(lambda x: x.count())['contbr_nm']

    # Return max value and appropriate fraction
    return (temp.idxmax(), temp.max()/stateTotal) 

def top_candidate_by_amount(df, state):
    """Find the candidate that received the highest amount of donations in
    a given state.

    Args:
        df: A DataFrame generated from the campaign finance data csv file.
        state: The state of interest in capitalized two-letter format,
            e.g. "CA".

    Returns:
        A tuple consisting of a pair of values. The first value should be the
        name of the candidate, and the second value should be the fraction of
        donations he received compared with all candidates.
        E.g. ('Cain, Herman', 0.05).
    """
    
    # Filter the DF based on state match and restrict the DF to relevant columns
    stFilterd=df[(df['contbr_st']==state)][['cand_nm', 'contb_receipt_amt']]
    
    # Sum out the total money from the filtered DF for this state
    stateTotal=stFilterd['contb_receipt_amt'].sum()
    
    # Group by the candidates
    candGrps=stFilterd.groupby("cand_nm")
    
    # Aggregate the total money based on the candidate groups
    temp=candGrps.agg(lambda x: x.sum())['contb_receipt_amt']
    
    # REturn the appropriate value and fraction
    return (temp.idxmax(), temp.max()/stateTotal) 

    # TODO: Implement this function.
    pass


def top_party_by_num_donors(df, state):
    """Find the party that received the most donations (by the number of
    donation records) in a given state.

    Args:
        df: A DataFrame generated from the campaign finance data csv file
            with the column "party" added.
        state: The state of interest in capitalized two-letter format,
            e.g. "CA".

    Returns:
        A tuple consisting of a pair of values. The first value should be the
        name of the party, as defined in add_party_column(df), and the second
        value should be the fraction of the number of donations the party
        received compared with other parties. E.g. ('Democrat', 0.115).
    """
    
    # Filter the DF by appropriate state and drop all contributor, party duplicates
    filtered=df[(df['contbr_st']==state)][['contbr_nm','party']].drop_duplicates(['contbr_nm','party'])
    
    # Count all of the different possible contributor, party pairs
    stateTotal = filtered['contbr_nm'].count()
    
    # Aggregate
    temp=filtered.groupby("party").agg(lambda x: x.count())['contbr_nm']
    return (temp.idxmax(), temp.max()/stateTotal) 

    pass


def top_party_by_amount(df, state):
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
    stFilterd=df[(df['contbr_st']==state)][['party', 'contb_receipt_amt']]
    stateTotal=stFilterd['contb_receipt_amt'].sum()
    candGrps=stFilterd.groupby("party")
    temp=candGrps.agg(lambda x: x.sum())['contb_receipt_amt']
    return (temp.idxmax(), temp.max()/stateTotal) 

    # TODO: Implement this function.
    pass


def num_bipartisan_donors(df):
    """Find the number of people that have donated to more than one parties.
    
    Args:
        df: A DataFrame generated from the campaign finance data csv file
            with the column "party" added.

    Returns:
        An integer count of the number of people that have donated to more than
        one parties.
    
    Initial Approach:
        Select only contb amts > 0 (i.e. it is a donation)
        Select only people, parties.
        Group by people.
        aggregate number of parties
        select > 1
        Count

        
        '''
        bipartyAgg= df[df['contb_receipt_amt']>0][['contbr_nm','party']].drop_duplicates(['contbr_nm','party']).groupby('contbr_nm', as_index=False).agg(lambda x: x.count())
        bipartySet= bipartyAgg[bipartyAgg['party']>1]
        return bipartySet['contbr_nm'].count()
        # TODO: Implement this function.
        '''

    """
    
    # Obtain the set of unique contributor, party pairs
    pplSet= df[df['contb_receipt_amt']>0][['contbr_nm','party']].drop_duplicates(['contbr_nm','party']) 
    
    # Obtain all of the democrat info
    democ_d = np.array(pplSet[pplSet['party']=="Democrat"]["contbr_nm"])
    
    # Obtain the republican subset
    repub_d = np.array(pplSet[pplSet['party']=="Republican"]["contbr_nm"])
    
    # OBtain the libertarian subset
    liber_d = np.array(pplSet[pplSet['party']=="Libertarian"]["contbr_nm"])
    
    # Intersect democrat set with republican
    dr = np.intersect1d(democ_d, repub_d)
    
    # Intersect republican set with libertarian
    rl = np.intersect1d(repub_d, liber_d)
    
    # Intersect democrat set with libertarian
    ld = np.intersect1d(liber_d, democ_d)

    # Return the union of all three intersections
    retVal = np.union1d(dr, np.union1d(rl, ld))    
    return retVal
    
    pass

def bucketize_donation_amounts(df):
    """Generate a histogram for the donation amount.

    Put donation amount into buckets and generate a histogram for these buckets.
    The buckets are: (0, 1], (1, 10], (10, 100], (100, 1000], (1000, 10000],
    (10000, 100000], (100000, 1000000], (1000000, 10000000].

    Args:
        df: A DataFrame generated from the campaign finance data csv file.

    Returns:
        A list containing 8 integers. The Nth integer is the count of donation
        amounts that fall into the Nth bucket. E.g. [2, 3, 4, 5, 4, 3, 1, 1].
    """
    # Obtain the necessary values in an array
    vals = np.array(df[df['contb_receipt_amt']>0]['contb_receipt_amt'])
    
    # Set up the buckets
    buckets = np.array([0.000000000000000000000000000000000000000001, 1.000000000000000000000000000000000000000001, 10.000000000000000000000000000000000000000001, 100.000000000000000000000000000000000000000001, 1000.000000000000000000000000000000000000000001, 10000.000000000000000000000000000000000000000001, 100000.000000000000000000000000000000000000000001, 1000000.000000000000000000000000000000000000000001, 10000000.000000000000000000000000000000000000000001])
    
    # Digitize the values into buckets
    temp = np.digitize(vals, buckets)
    
    # Return the bincounts
    bincounts = np.bincount(np.digitize(vals, buckets)-1, minlength=8)
    return bincounts
    # TODO: Implement this function.
    pass


def main(*args):
    ##################################
    # Data Set Query Variables #######
    ##################################
    sampleruns = False
    state = "CA"
    qa_1 = True
    qa_2 = False
    qa_34 = False
    qa_5 = False

    ##################################
    
    df = read_csv('P00000001-ALL.txt')
    
    #print len(df.drop_duplicates('contbr_st')['contbr_st'])
    
    df = add_party_column(df)

    stFilterd=df[(df['contb_receipt_amt']>0)][['party', 'contb_receipt_amt']]
    stateTotal=stFilterd['contb_receipt_amt'].sum()
    candGrps=stFilterd.groupby("party")
    temp=candGrps.agg(lambda x: x.sum())['contb_receipt_amt']
    
    
    # My sanity check cases
    if (sampleruns):
      print "Party Column Addition:"
      print df['party']
      print "Donation Records:"
      print num_donation_records(df)
      print "Refund Records:"
      print num_refund_records(df)
      print "Number of Donors: CA"
      print num_donors(df, state)
      print "Top Candidate by # Donors: CA"
      print top_candidate_by_num_donors(df, state)
      print "Top Party by # Donors: CA"
      print top_party_by_num_donors(df, state)
      print "Top Candidate by Amount: CA"
      print top_candidate_by_amount(df, state)
      print "Top Party by Amount: CA"
      print top_party_by_amount(df, state)
      print "# Bipartisan Donors:"
      print num_bipartisan_donors(df)
      print "Histogram"
      print bucketize_donation_amounts(df)
      # TODO: Put the code you used to explore the data set here.
    
    if (qa_1):
    
      # Should obtain a fair bit of general descriptiveness in terms of spread and center via this...
      print df['contb_receipt_amt'].describe()
      
      # Knowing the mean, median, and std. dev. from the previous line, the histogram will help us approximate further outliers
      print bucketize_donation_amounts(df)
      
      # Compute what is at the 99th percentile      
      vals = np.array(df['contb_receipt_amt'])      
      from scipy import stats
      print stats.scoreatpercentile(vals, 99.9)

    if (qa_2):
    
      # Query for people grouped by name trying to see if more than one residence exists
      pplSet= df[df['contb_receipt_amt']>0][['contbr_nm','contbr_zip']].drop_duplicates(['contbr_nm','contbr_zip'])['contbr_nm']
      pplArr= list(pplSet)
      
      # Compute and print difference counts
      temp= list(np.unique(pplArr))
      print "Count Difference:", (len(pplArr) -len(temp))
    
    if (qa_34):
    
      """
      Approach:
        Select [state, cand_nm, amount]
        GroupBy [state, cand_nm]:
          Sum over the amount
        GroupBy [state].max() 
        GroupBy
      """ 
      # Total Number of Parties
      print "Total Parties", len(df.drop_duplicates('party')['party'])

      # Find the total aggregations of sum, grouped by state, candidate
      groupedSums=df[['contbr_st', 'cand_nm', 'contb_receipt_amt']].groupby(['contbr_st', 'cand_nm'], as_index=False).agg(np.sum)
      groupedSums=groupedSums.sort_index(by="contb_receipt_amt", ascending=False).drop_duplicates('contbr_st')
                  
      # How many states did Republicans win?
      states_won = groupedSums [(groupedSums['cand_nm']!="Obama, Barack") & (groupedSums['cand_nm']!="Johnson, Gary Earl")]
      print "States Won Republicans:", len(states_won)
      
      # How many states did Obama win?
      states_won = groupedSums [groupedSums['cand_nm']=="Obama, Barack"]['contbr_st']
      print "States Won Democrats:", len(states_won)
      
      # How many states did the Libertarians win?
      states_won = groupedSums [groupedSums['cand_nm']=="Johnson, Gary Earl"]['contbr_st']
      print "States Won Libertarians:", len(states_won)      
          
      pass
    if (qa_5):

      #-----------------------
      # Interesting thing No.1
      #-----------------------
      
      numZero = len(df[df["contb_receipt_amt"]==0])      
      print "Total Records with a ZERO contribution:", numZero
      print "-----------------------------------------------------"      

      #-----------------------
      # Interesting thing No.2
      #-----------------------

      # Find impact of unemployed on the donation amounts
      unempDf = df[(df["contbr_occupation"]=="NOT EMPLOYED")|(df["contbr_employer"]=="NOT EMPLOYED")]

      print "Count of Not Employed Donors:", len(unempDf.drop_duplicates('contbr_nm')["contbr_nm"])

      contbr=(unempDf["contb_receipt_amt"].sum())
      
      print "Total Contributed:", contbr

      print "Percentage of all Contributions:", (contbr/(df["contb_receipt_amt"].sum()))
      splits = unempDf[["contb_receipt_amt", "party"]].groupby('party').sum()
      print "Party Splits:", splits
      
      print "-----------------------------------------------------"      

      #-----------------------
      # Interesting thing No.3
      #-----------------------
      
      # Get a Df for only Obama, only Republicans, and only Libertarians
      repubDf = df[(df['cand_nm']!="Obama, Barack") & (df['cand_nm']!="Johnson, Gary Earl")]
      obamaDf = df[df['cand_nm']=="Obama, Barack"]
      liberDf = df[df['cand_nm']=="Johnson, Gary Earl"]
      
      # Compute their histograms
      oHist = bucketize_donation_amounts(obamaDf)
      rHist = bucketize_donation_amounts(repubDf)
      lHist = bucketize_donation_amounts(liberDf)

      print "Obama Histogram"
      print oHist
      print "Republican Histogram"
      print rHist
      print "Libertarian Histogram"
      print lHist
      
      donations = df[(df["contb_receipt_amt"]!=0) & (df["contb_receipt_amt"]>0)]
    
      pass
if __name__ =='__main__':
    sys.exit(main(*sys.argv[1:]))

