import numpy as np
from universe import Universe

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
    new_universe = Universe(PARTICIPANTS, AVG_VOTING_RATE, WEALTH, TOKENS_AMOUNT, WEALTH_DISTRIBUTION)

if __name__ == '__main__':
    main()