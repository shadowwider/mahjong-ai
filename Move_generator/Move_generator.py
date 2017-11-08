from __future__ import print_function
import six, abc
import Tile
from timeit import default_timer as timer

@six.add_metaclass(abc.ABCMeta)
class Move_generator:
	def __init__(self, player_name):
		self.__player_name = player_name
		self.__start_time = None
		self.__avg_drop_tile_time = 0
		self.__avg_decision_time = 0
		self.__decision_count = 0
		self.__drop_tile_count = 0

	@property
	def avg_drop_tile_time(self):
		return self.__avg_drop_tile_time

	@property
	def avg_decision_time(self):
		return self.__avg_decision_time

	@property
	def player_name(self):
		return self.__player_name

	@abc.abstractmethod
	def decide_chow(self, player, new_tile, choices, neighbors, game):
		pass

	@abc.abstractmethod
	def decide_kong(self, player, new_tile, kong_tile, location, src, neighbors, game):
		pass

	@abc.abstractmethod
	def decide_pong(self, player, new_tile, neighbors, game):
		pass
	
	@abc.abstractmethod
	def decide_drop_tile(self, player, new_tile, neighbors, game):
		pass

	@abc.abstractmethod
	def decide_win(self, player, grouped_hand, new_tile, src, score, neighbors, game):
		pass

	@abc.abstractmethod
	def reset_new_game(self):
		pass

	def begin_decision(self):
		self.__start_time = timer()

	def end_decision(self, is_drop_tile = False):
		if self.__start_time is None:
			raise Exception("Have not started a decision yet")

		time_elapsed = timer() - self.__start_time
		self.__start_time = None

		self.__avg_decision_time = (self.__avg_decision_time * self.__decision_count + time_elapsed)/(self.__decision_count + 1)
		self.__decision_count += 1

		if is_drop_tile:
			self.__avg_drop_tile_time = (self.__avg_drop_tile_time * self.__drop_tile_count + time_elapsed)/(self.__drop_tile_count + 1)
			self.__drop_tile_count += 1

	def print_game_board(self, fixed_hand, hand, neighbors, game, new_tile = None, print_stolen_tiles = False):
		line_format_left = u"|{next:<20s}|{opposite:<20s}|{prev:<20s}|"
		line_format_right = u"|{next:>20s}|{opposite:>20s}|{prev:>20s}|"
		line_merged_format_left = u"|{msg:<62s}|"
		line_merged_format_right = u"|{msg:>62s}|"

		horizontal_line = line_merged_format_left.format(msg = '-'*62)

		print("Wake up %s!"%self.player_name)

		print(horizontal_line)
		print(line_merged_format_right.format(msg = "Game of %s wind [%d]"%(game.game_wind, game.deck_size)))
		print(horizontal_line)
		print(line_format_left.format(next = "Next Player", opposite = "Opposite Player", prev = "Previous Player"))
		print(line_format_left.format(next = "(%s)"%neighbors[0].name, opposite = "(%s)"%neighbors[1].name, prev = "(%s)"%neighbors[2].name))
		print(horizontal_line)

		fixed_hands_strs = []
		hand_sizes = []
		disposed_tiles_symbols = []
		filter_state = None if print_stolen_tiles else "unstolen"

		for neighbor in neighbors:
			fixed_hand_str = ""
			for meld_type, is_secret, tiles in neighbor.fixed_hand:
				if is_secret:
					fixed_hand_str += Tile.tile_back_symbol + tiles[0].symbol + tiles[0].symbol + Tile.tile_back_symbol
				else:
					fixed_hand_str += "".join([tile.symbol for tile in tiles])
			fixed_hands_strs.append(fixed_hand_str)
			hand_sizes.append(neighbor.hand_size)

			disposed_tiles = neighbor.get_discarded_tiles(filter_state)
			disposed_tiles_symbols.append(''.join([tile.symbol for tile in disposed_tiles]))

		print(line_format_left.format(next = fixed_hands_strs[0], opposite = fixed_hands_strs[1], prev = fixed_hands_strs[2]))
		print(line_format_right.format(next = "%s -%d"%(Tile.tile_back_symbol*hand_sizes[0], hand_sizes[0]), opposite =  "%s -%d"%(Tile.tile_back_symbol*hand_sizes[1], hand_sizes[1]), prev =  "%s -%d"%(Tile.tile_back_symbol*hand_sizes[2], hand_sizes[2])))

		print(horizontal_line)
		is_continue_print = True

		while is_continue_print:
			print(line_format_left.format(next = disposed_tiles_symbols[0][0:20], opposite = disposed_tiles_symbols[1][0:20], prev = disposed_tiles_symbols[2][0:20]))
			is_continue_print = False
			for i in range(3):
				disposed_tiles_symbols[i] = disposed_tiles_symbols[i][20:]
				if len(disposed_tiles_symbols[i]) > 0:
					is_continue_print = True

		print(horizontal_line)
		print(line_merged_format_left.format(msg = "%s's tiles:"%(self.player_name)))
		fixed_hand_str = ""
		for meld_type, is_secret, tiles in fixed_hand:
			if is_secret:
				fixed_hand_str += "".join([Tile.tile_back_symbol, tiles[0].symbol, tiles[0].symbol, Tile.tile_back_symbol])
			else:
				fixed_hand_str += "".join([tile.symbol for tile in tiles])
		print(line_merged_format_left.format(msg = fixed_hand_str))

		line_1, line_2 = "", ""
		i = 0
		for tile in hand:
			line_1 += "%s  "%(tile.symbol)
			line_2 += "{digit:<3s}".format(digit = str(i))
			i += 1
		print(line_merged_format_right.format(msg = line_1))
		print(line_merged_format_right.format(msg = line_2))

		if new_tile is not None:
			print(line_merged_format_right.format(msg = "%d: %s  "%(i, new_tile.symbol)))
		print(horizontal_line)
