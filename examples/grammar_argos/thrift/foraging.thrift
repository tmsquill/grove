// Terminal Expansions
enum IdState {
  STATE_0 = 0,
  STATE_1 = 1,
  STATE_2 = 2
}

enum IdPrecondition {
	PRECONDITION_0 = 0,
	PRECONDITION_1 = 1,
	PRECONDITION_2 = 2,
	PRECONDITION_3 = 3,
	PRECONDITION_4 = 4,
	PRECONDITION_5 = 5,
	PRECONDITION_6 = 6,
	PRECONDITION_7 = 7
}

enum IdVar {
	VAR_0 = 0,
	VAR_1 = 1,
	VAR_2 = 2,
	VAR_3 = 3
}

enum Probability {
	PROB_0 = 0,
	PROB_1 = 1,
	PROB_2 = 2,
	PROB_3 = 3,
	PROB_4 = 4,
	PROB_5 = 5,
	PROB_6 = 6,
	PROB_7 = 7
}

enum ProbInitState {
	PROB_INIT_STATE_0 = 0,
	PROB_INIT_STATE_1 = 1,
	PROB_INIT_STATE_2 = 2,
	PROB_INIT_STATE_3 = 3,
	PROB_INIT_STATE_4 = 4,
	PROB_INIT_STATE_5 = 5,
	PROB_INIT_STATE_6 = 6,
	PROB_INIT_STATE_7 = 7,
	PROB_INIT_STATE_8 = 8,
	PROB_INIT_STATE_9 = 9
}



// Non-terminal Expansions
struct ActionCngVar {
	1: Probability prob,
	2: IdVar id_var
}

struct ActionCngState {
	1: Probability prob,
	2: IdState id_state
}

struct Action {
  1: ActionCngState cng_state,
  2: ActionCngVar cng_var
}

struct Precondition {
  1: IdPrecondition id_precondition
}

struct Behavior {
  1: IdState id_state
}

struct Rule {
  1: list<Precondition> preconditions,
  2: list<Behavior> behaviors,
  3: list<Action> actions
}

struct RuleSet {
  1: list<Rule> rule_list = []
}

struct Initialization {
  1: ProbInitState init_1,
  2: ProbInitState init_2,
  3: ProbInitState init_3
}

struct Root {
  1: Initialization init,
  2: RuleSet rules
}
