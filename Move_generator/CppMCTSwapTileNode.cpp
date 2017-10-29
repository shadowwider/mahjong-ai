#include <cstdlib>
#include <string>
#include <vector>
#include <stack>
#include <utility>
#include <limits>
#include <algorithm>
#include <cmath>
#include "CppMCTSwapTileNode.h"
using namespace std;

//double (*map_hand_eval_func)(FHand, TMap)

CppMCTGroupAction::CppMCTGroupAction(){
	this->avg_score = 0;
	this->sum_rollout_prob = 0;
	this->avg_score = 0;
}

CppMCTSwapTileNode* CppMCTGroupAction::expand(string drop_tile, TMap& map_hand, TMap& map_remaining, int tile_remaining, int round_remaining, double prev_prior){
	if(this->actions.size() > 0) return NULL;

	CppMCTSwapTileNode* last_node;
	map_hand[drop_tile] -= 1;
	double prior;
	for (auto &new_tile_info: map_remaining){
		if(new_tile_info.second == 0) continue;
		prior = prev_prior * new_tile_info.second / tile_remaining;

		new_tile_info.second -= 1;
		map_hand[new_tile_info.first] += 1;
		last_node = new CppMCTSwapTileNode(map_hand, map_remaining, tile_remaining - 1, round_remaining - 1, prior);
		this->actions.push_back(last_node);
		map_hand[new_tile_info.first] -= 1;
		new_tile_info.second += 1;

	}
	map_hand[drop_tile] += 1;
	return last_node;
}

CppMCTSwapTileNode::CppMCTSwapTileNode(){

}

CppMCTSwapTileNode::CppMCTSwapTileNode(TMap& map_hand, TMap& map_remaining, int tile_remaining, int round_remaining, double prior){
	this->map_hand = map_hand;
	this->map_remaining = map_remaining;
	this->tile_remaining = tile_remaining;
	this->round_remaining = round_remaining;
	this->prior = prior;
	this->sum_rollout_prob = 0;
	this->avg_score = 0;
	this->count_visit = 0;
	this->max_action_avg_score = 0;
	this->min_action_avg_score = 0;
}

string CppMCTSwapTileNode::search(FHand& fixed_hand, int max_iter, double ucb_policy){
	stack <UCBResult> st;
	for(int i = 0; i < max_iter; i++){
		CppMCTSwapTileNode* current = this;
		UCBResult prev_result = make_pair("", this), result;
		while(current->grouped_actions.size() > 0 && current->count_visit > 0){
			result = current->argmax_ucb(ucb_policy, current == this);
			st.push(prev_result);
			if(result.first == "" || result.first == "stop")
				break;
			current = result.second;
			prev_result = result;
		}
		double score = 0, prior = 1;

		if(result.first == "stop"){
			if(current->grouped_actions["stop"].count_visit == 0){
				score = map_hand_eval_func(fixed_hand, current->map_hand);
			}else{
				score = current->grouped_actions["stop"].avg_score;
			}
			prior = current->prior;
		}else{
			pair<double, double> rollout_result = current->rollout(fixed_hand);
			prior = rollout_result.first;
			score = rollout_result.second;
		}

		while(st.size() > 0){
			UCBResult result = st.top();
			result.second->new_visit(prior, score, result.first);
			st.pop();
		}
	}

	double max_score = -1 * numeric_limits<float>::infinity();
	string max_action = "";
	for(auto const &ent: this->grouped_actions){
		if(ent.second.avg_score > max_score){
			max_score = ent.second.avg_score;
			max_action = ent.first;
		}
	}
	return max_action;
}

void CppMCTSwapTileNode::expand(){

	if(this->grouped_actions.size() > 0) return;

	for(auto const &dispose_tile_info: this->map_hand){
		if(dispose_tile_info.second == 0) continue;

		this->grouped_actions[dispose_tile_info.first] = CppMCTGroupAction();

	}
	this->grouped_actions["stop"] = CppMCTGroupAction();
}

void CppMCTSwapTileNode::new_visit(double prior, double score, string& action){
	this->avg_score = (this->sum_rollout_prob*this->avg_score + prior*score)/(this->sum_rollout_prob + prior);
	this->sum_rollout_prob += prior;
	this->count_visit += 1;
	if(action != ""){
		CppMCTGroupAction grouped_action = this->grouped_actions[action];

		this->max_action_avg_score = max(this->max_action_avg_score, score);
		this->min_action_avg_score = min(this->min_action_avg_score, score);

		grouped_action.avg_score = (grouped_action.sum_rollout_prob*grouped_action.avg_score + prior*score)/(grouped_action.sum_rollout_prob + prior);
		grouped_action.sum_rollout_prob += prior;
		grouped_action.count_visit += 1;
	}
}

pair<double, double> CppMCTSwapTileNode::rollout(FHand& fixed_hand){
	double prior = this->prior;
	int swapped_count = 0;
	vector <string> tiles, deck;
	map <string, int> used_count, final_map_hand;

	for(auto const& t_info: this->map_hand){
		for(int i = 0; i<t_info.second; i++){
			tiles.push_back(t_info.first);
		}
	}
	for(auto const& t_info: this->map_remaining){
		for(int i = 0; i<t_info.second; i++){
			deck.push_back(t_info.first);
		}
	}

	random_shuffle(deck.begin(), deck.end());

	while(this->round_remaining > swapped_count + 1){
		int dispose_tile_index = rand() % tiles.size();
		string new_tile = deck[deck.size() - 1];
		prior *= 1.0*(this->map_remaining[new_tile] - used_count[new_tile])/deck.size();

		tiles[dispose_tile_index] = new_tile;

		used_count[new_tile] += 1;
		deck.pop_back();
		++swapped_count;
	}

	for(unsigned long i = 0; i<tiles.size(); i++){
		final_map_hand[tiles[i]] += 1;
	}

	double score = map_hand_eval_func(fixed_hand, final_map_hand);
	string emptys = "";
	this->new_visit(prior, score, emptys);
	return make_pair(prior, score);
}

//Leaf node --> action ""
//Stopping --> action "stop"
UCBResult CppMCTSwapTileNode::argmax_ucb(double ucb_policy, bool is_root){
	if(this->round_remaining == 0){
		return make_pair("", (CppMCTSwapTileNode*) NULL);
	}
	this->expand();

	string max_action = "";
	double max_ucb_score = 0;
	for(auto& gaction_info: this->grouped_actions){
		if(gaction_info.first != "stop" && gaction_info.second.actions.size() == 0){
			CppMCTSwapTileNode* node = (gaction_info.second).expand(gaction_info.first, this->map_hand, this->map_remaining, this->tile_remaining, this->round_remaining, this->prior);
			return (UCBResult) make_pair(gaction_info.first, node);
		}

		if(gaction_info.second.count_visit == 0){
			return (UCBResult) make_pair(gaction_info.first, gaction_info.second.actions[0]);
		}

		double ucb_score = (gaction_info.second.avg_score - this->min_action_avg_score)/(this->max_action_avg_score - this->min_action_avg_score);
		ucb_score += ucb_policy*sqrt(log(this->count_visit)/gaction_info.second.count_visit);
		if(ucb_score > max_ucb_score){
			max_ucb_score = ucb_score;
			max_action = gaction_info.first;
		}
	}

	int conseq_index = rand() % this->grouped_actions[max_action].actions.size();
	return (UCBResult) make_pair(max_action, this->grouped_actions[max_action].actions[conseq_index]);
	
}

void CppMCTSwapTileNode::add_branch_action(string identifier, CppMCTSwapTileNode* node){
	CppMCTGroupAction gaction = CppMCTGroupAction();
	gaction.actions.push_back(node);
	this->grouped_actions[identifier] = gaction;
}