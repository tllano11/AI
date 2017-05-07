class HMM:
    def __init__(self, transition_probs, emission_probs):
        self._transition_probs = transition_probs
        self._emission_probs = emission_probs

    def emission(self, emission):
        return self._emission_probs[:, emission]

    @property                                                                                                                                                                           
    def num_states(self):
        return self._transition_probs.shape[0]

    @property                                                                                                                                                                           
    def transition_probabilities(self):
        return self._transition_probs