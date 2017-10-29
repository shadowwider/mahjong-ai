#include <map>
#include <string>
#include <vector>
#include <utility>
#include <tuple>
#include "../CppTile.h"
using namespace std;

class CppMCTGroupAction;
class CppMCTSwapTileNode;
typedef pair<string, CppMCTSwapTileNode*> UCBResult;
typedef map<string, int> TMap;
typedef vector< vector<string> > FHand;

class CppMCTGroupAction{
public:
	int count_visit;
	double avg_score, sum_rollout_prob;
	vector <CppMCTSwapTileNode*> actions;
	CppMCTGroupAction();
	CppMCTSwapTileNode* expand(string drop_tile, TMap& map_hand, TMap& map_remaining, int tile_remaining, int round_remaining, double prev_prior);
};

class CppMCTSwapTileNode{
public:
	map<string, CppMCTGroupAction> grouped_actions;

	CppMCTSwapTileNode();
	CppMCTSwapTileNode(TMap& map_hand, TMap& map_remaining, int tile_remaining, int round_remaining, double prior);
	string search(FHand& fixed_hand, int max_iter, double ucb_policy);
	void new_visit(double prior, double score, string& action);
	pair<double, double>  rollout(FHand& fixed_hand);
	pair<string, CppMCTSwapTileNode*> argmax_ucb(double ucb_policy, bool is_root);
	void add_branch_action(string identifier, CppMCTSwapTileNode* node);
private:
	TMap map_hand, map_remaining;
	int tile_remaining, round_remaining;
	double prior, sum_rollout_prob, avg_score, count_visit, max_action_avg_score, min_action_avg_score;

	void expand();
};

double map_hand_eval_func(FHand fixed_hand, TMap map_hand);