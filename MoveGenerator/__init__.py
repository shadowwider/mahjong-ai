from .Human import Human
from .MoveGenerator import MoveGenerator
from .Rule_based_ai_naive_baseline import RuleBasedAINaive
from .MCTSCpp import RuleBasedAINaiveMCTSCpp
from .MCTSPy import RuleBasedAINaiveMCTSPy
from .TGHuman import TGHuman
from .Rule_based_ai_q import RuleBasedAIQ

__models_map = {
	"RuleBasedAINaive": RuleBasedAINaive,
	"RuleBasedAINaiveMCTSCpp": RuleBasedAINaiveMCTSCpp,
	"RuleBasedAINaiveMCTSPy": RuleBasedAINaiveMCTSPy,
}

def get_model_by_id(model_id):
	if model_id in __models_map:
		return __models_map[model_id]
	raise Exception("Unknown model_id '%s'"%model_id)