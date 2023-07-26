import numpy as np
from universe import universe_development
from voting import voting_development

PARTICIPANTS = 1000
VOTING_METHOD = 'simple_majority'
VOTING_INCENTIVE = 'none'
WEALTH_DISTRIBUTION = 'uniform'
AVG_VOTING_RATE = 0.5
WEALTH = 1000000
TOKENS_AMOUNT = 1000000
RANDOM_SEED = 42


def main():
    
    np.random.seed(RANDOM_SEED)
    # Create new universe
    universe = universe_development.build_universe()
    print("Participants: ", len(universe.participants))
    proposals = voting_development.define_proposals(num_proposals=120, distrib_per_group=(0.2, 0.2, 0.2), preference_methodology="binary")
    print("Proposals: ", len(proposals))

if __name__ == '__main__':
    main()