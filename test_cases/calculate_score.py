import Tile
import Scoring_rules
import unittest

def test():
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(Calculate_score_test)
	unittest.TextTestRunner().run(suite)

class Calculate_score_test(unittest.TestCase):
	def test_all_pongs(self):
		character_1 = Tile.Tile("characters", 1)
		bamboo_2 = Tile.Tile("bamboo", 2)
		dots_5 = Tile.Tile("dots", 5)
		character_7 = Tile.Tile("characters", 7)
		dots_9 = Tile.Tile("dots", 9)
		hand = [character_1, character_1, character_1, bamboo_2, bamboo_2, bamboo_2, dots_5, dots_5, dots_5, character_7, character_7, character_7, dots_9]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, dots_9)
		score = Scoring_rules.HK_rules.score_all_pongs([], grouped_hands[0])
		self.assertEqual(score, 3)

	def test_one_nines(self):
		bamboo_1 = Tile.Tile("bamboo", 1)
		bamboo_9 = Tile.Tile("bamboo", 9)
		dots_1 = Tile.Tile("dots", 1)
		east = Tile.Tile("honor", "east")
		character_9 = Tile.Tile("characters", 9)

		hand = [bamboo_1, bamboo_1, bamboo_1, bamboo_9, bamboo_9, bamboo_9, dots_1, dots_1, dots_1, east, east, east, character_9]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, character_9)
		score = Scoring_rules.HK_rules.score_ones_nines([], grouped_hands[0])
		self.assertEqual(score, 1)

	def test_mixed_suit(self):
		east = Tile.Tile("honor", "east")
		dots_1 = Tile.Tile("dots", 1)
		dots_2 = Tile.Tile("dots", 2)
		dots_3 = Tile.Tile("dots", 3)
		dots_4 = Tile.Tile("dots", 4)
		dots_5 = Tile.Tile("dots", 5)
		dots_6 = Tile.Tile("dots", 6)
		dots_8 = Tile.Tile("dots", 8)
		white = Tile.Tile("honor", "white")
		hand = [east, east, east, dots_1, dots_2, dots_3, dots_4, dots_5, dots_6, dots_8, dots_8, dots_8, white]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, white)
		score = Scoring_rules.HK_rules.score_one_suit([], grouped_hands[0])
		self.assertEqual(score, 3)

	def test_small_honors(self):
		bamboo_1 = Tile.Tile("bamboo", 1)
		bamboo_2 = Tile.Tile("bamboo", 2)
		bamboo_3 = Tile.Tile("bamboo", 3)
		character_1 = Tile.Tile("characters", 1)
		red = Tile.Tile("honor", "red")
		green = Tile.Tile("honor", "green")
		white = Tile.Tile("honor", "white")

		hand = [bamboo_1, bamboo_2, bamboo_3, character_1, character_1, character_1, red, red, red, green, green, green, white]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, white)
		score = Scoring_rules.HK_rules.score_honor_tiles([], grouped_hands[0])
		self.assertEqual(score, 5)

	def test_one_suit_wo_honor(self):
		dots_1 = Tile.Tile("dots", 1)
		dots_2 = Tile.Tile("dots", 2)
		dots_6 = Tile.Tile("dots", 6)
		dots_7 = Tile.Tile("dots", 7)
		dots_9 = Tile.Tile("dots", 9)
		hand = [dots_1, dots_1, dots_1, dots_2, dots_2, dots_2, dots_6, dots_6, dots_6, dots_7, dots_7, dots_7, dots_9]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, dots_9)
		score = Scoring_rules.HK_rules.score_one_suit([], grouped_hands[0])
		self.assertEqual(score, 7)

	def test_small_four_winds(self):
		east = Tile.Tile("honor", "east")
		south = Tile.Tile("honor", "south")
		west = Tile.Tile("honor", "west")
		north = Tile.Tile("honor", "north")
		bamboo_1 = Tile.Tile("bamboo", 1)
		bamboo_2 = Tile.Tile("bamboo", 2)
		bamboo_3 = Tile.Tile("bamboo", 3)
		hand = [east, east, east, south, south, south, west, west, west, bamboo_1, bamboo_2, bamboo_3, north]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, north)
		score = Scoring_rules.HK_rules.score_four_winds([], grouped_hands[0])
		self.assertEqual(score, Scoring_rules.HK_rules.get_score_upper_limit())

	def test_big_honors(self):
		dots_1 = Tile.Tile("dots", 1)
		dots_2 = Tile.Tile("dots", 2)
		red = Tile.Tile("honor", "red")
		green = Tile.Tile("honor", "green")
		white = Tile.Tile("honor", "white")

		hand = [red, red, red, green, green, green, white, white, white, dots_1, dots_1, dots_1, dots_2]
		grouped_hands = Scoring_rules.HK_rules.validate_hand([], hand, dots_2)
		score = Scoring_rules.HK_rules.score_honor_tiles([], grouped_hands[0])
		self.assertEqual(score, Scoring_rules.HK_rules.get_score_upper_limit())