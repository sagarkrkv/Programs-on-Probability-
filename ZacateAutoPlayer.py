# Automatic Zacate game player
# B551 Fall 2015
# Vidya Sagar Kalvakunta (vkalvaku)
#
# Based on skeleton code by D. Crandall
#
# PUT YOUR REPORT HERE!
'''
I approached this problem by writing a function named logic

the function is called in the first and second roll of the dice, the function first 
checks all the remaining Categories available in the present round.

Then it calls individual functions  for each of the individual states, each function 
returns a list of dice that need to be changed to achieve the goal state.

Now we calculate a score for each of the function based on the number of dice to be 
changed and the score of the goal state 

				score = (1 / float(6 ** len(dice_to_be_changed))) *score_of_goal

After checking the scores for all the available states, we select the moves required to
reach the state with the max score

these moves are then passed on to a function that retrieves the index of these dice.


The function in the third roll is basically the same function that is given in the 
ZacateState.py, it returns the state with the best score.

This program returns an average mean score of 185-190.It can be improved 




'''
#
#
# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from ZacateState import Dice
from ZacateState import Scorecard
import random
from itertools import groupby
from operator import itemgetter
import copy

class ZacateAutoPlayer:

  	def __init__(self):
  		pass

  	def first_roll(self, dice, scorecard):
  		rolls_remain =2
  		return logic(dice,scorecard,rolls_remain)
  		
  	def second_roll(self, dice, scorecard):
		rolls_remain = 1
		return logic(dice,scorecard,rolls_remain)
  
  	def third_roll(self, dice, scorecard):
		avail_cat=list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
		cat_score={}
		key_count = [dice.dice.count(i) for i in range(1,7)]
		for cat in avail_cat:
			if cat in Scorecard.Numbers:
				cat_score[cat] = key_count[Scorecard.Numbers[cat]-1] * Scorecard.Numbers[cat]
				if cat_score[cat] > Scorecard.Numbers[cat]*4:
					cat_score[cat] = 40
			elif cat == "pupusa de queso":
			    cat_score[cat] = 40 if sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6] else 0
			elif cat == "pupusa de frijol":
			    cat_score[cat]  = 30 if (len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) else 0
			elif cat == "elote":
			    cat_score[cat]  = 25 if (2 in key_count) and (3 in key_count) else 0
			elif cat == "triple":
			    cat_score[cat]  = sum(dice.dice) if max(key_count) >= 3 else 0
			elif cat == "cuadruple":
			    cat_score[cat]  = sum(dice.dice) if max(key_count) >= 4 else 0
			elif cat == "quintupulo":
			    cat_score[cat]  = 50 if max(key_count) == 5 else 0
			elif cat == "tamal" and len(avail_cat) == 1:
			    cat_score[cat]  = sum(dice.dice)
		return max(cat_score, key=cat_score.get)

def logic(dice,scorecard,rolls_remain):
	avail_cat=list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
	tmp_list1  = list(dice.dice)
	tmp_list = copy.copy(tmp_list1)
	tmp_list.sort()
	dice_no = {}        #used to store the no of times each value appears
	for i in range (1,7):
		dice_no[i] = tmp_list.count(i)
	max_value = max(dice_no.values())
	key_list = [dice.dice.count(i) for i in range(1,7)]
	diff_dice = key_list.count(1)
	no_of_same_dice = 5 - diff_dice
	same_dice_1 = 0
	same_dice = {}
	same_dice = { key:value for key, value in dice_no.items() if value > 1 }
	if no_of_same_dice > 0:
		same_dice_1 = get_key(max_value,dice_no)
		if max_value != no_of_same_dice:
			same_dice_2 = get_key(no_of_same_dice-max_value,dice_no)
	bestmove = []
	bestscore = -999
	
	for cat in avail_cat:
		score = 0
		k = []
		if cat == "quintupulo":
			k = quintuplo(tmp_list,same_dice_1)
			score = (1 / float(6 ** len(k))) * 50
		elif cat == "pupusa de frijol":	
			k = pupusa1(tmp_list,same_dice)
			score = (1 / float(6 ** len(k))) * 30
		elif cat == "pupusa de queso" :
			k = pupusa(tmp_list,same_dice)
			score = (1 / float(6 ** len(k))) * 40
		elif cat == "elote":
			k = elote(dice_no)
			score = (1 / float(6 ** len(k))) * 25
		elif cat == "cuadruple" :
			k = cuadruple_triple(dice_no,same_dice)
			score = (1 / float(6 ** len(k))) * 22
		elif cat == "triple":
			k = cuadruple_triple(dice_no,same_dice)
			score = (1 / float(6 ** len(k))) * 18
		elif (cat == "tamal") and len(avail_cat) == 1:
			k = tamal(dice_no)
			score = (1 / float(6 ** len(k))) * 10
		elif cat in Scorecard.Numbers: 
			cat_no = Scorecard.Numbers[cat]
			k = numbers(dice_no,cat_no)
			score = (1 / float(6 ** len(k)))
			if len(k) <= 2:
				score = score*50
			elif len(k) == 3:
				score = score*25
			else:
				score = score*cat_no*2
		score = score*rolls_remain
		if score > bestscore:
			bestscore = score
			bestmove = k
			print cat
	final_move = []

	if len(bestmove) > 0:
		visited = []
		for n in bestmove:
			if bestmove.count(n) == 1:
			 	final_move.append(dice.dice.index(n))
			elif n not in visited:
				temp = get_index_same_value(n,dice.dice)
				count = bestmove.count(n)
				while count > 0:
					final_move.append(temp.pop())
					count-=1
				visited.append(n)

	else : final_move.append(7)
	final_move.sort()
	return final_move

	

def quintuplo(list,same_dice_1):
	if same_dice_1 != 0:
		return [x for x in list if x != same_dice_1]
	else: return list


def pupusa(list,same_dice):
	tlist = []
	rlist = copy.copy(list)
	final_list = []
	se_list =[]
	if len(same_dice) > 0:
		for key, value in same_dice.items():
			while value > 1:
				tlist.append(key)
				rlist.remove(key)
				value-=1
		if (len(rlist)) > 1:
			for k, g in groupby(enumerate(rlist), lambda (i, x): i-x):
				final_list.append(map(itemgetter(1), g))
			
			if len(final_list) > 1:
				list1 = min(final_list,key = len)
				for i in list1:
					tlist.append(i)
	elif 1 in rlist:
		if 6 in rlist:
			tlist.append(1)
	return tlist
	
def pupusa1(list,same_dice):
	tlist = []
	rlist = copy.copy(list)
	final_list = []
	se_list=[]
	for k, g in groupby(enumerate(rlist), lambda (i, x): i-x):
				se_list.append(map(itemgetter(1), g))
	if len(max(se_list,key = len)) in (4,5):
				tlist = []
	elif len(same_dice) > 0:
	
		for key, value in same_dice.items():
			while value > 1:
				tlist.append(key)
				rlist.remove(key)
				value-=1
	elif (len(rlist)) > 1:
		for k, g in groupby(enumerate(rlist), lambda (i, x): i-x):
			final_list.append(map(itemgetter(1), g))
		
		if len(final_list) > 1:
			list1 = min(final_list,key = len)
			for i in list1:
				tlist.append(i)
	
	return tlist
def elote(dice_no):
	key_pair =[]
	for key , value in dice_no.items():
		if value in (1,4):
			key_pair.append(key)
	return key_pair

def tamal(dice_no):
	key_pair =[]
	for key , value in dice_no.items():
		if value != 0 and key < 4:
			while value > 0:
				key_pair.append(key)
				value-=1
	return key_pair

def cuadruple_triple(dice_no,same_dice):
	key_pair =[]
	for key , value in dice_no.items():
		if value == 1 :
			key_pair.append(key)
	if len(same_dice) > 1:
		key_pair.append(min(same_dice,key = same_dice.get))
	return key_pair

def numbers(dice_no,cat_no):
	key_pair = []
	for key , value in dice_no.items():
		if cat_no != key and value != 0:
			while value > 0:
				key_pair.append(key)
				value-=1
	return key_pair

def get_key(val,dict):
	for key, value in dict.items():
			if value == val:
				return key
def get_index_same_value(val,list):
	index_list = []
	for index, value in enumerate(list):
		if value == val:
			index_list.append(index)
	return index_list