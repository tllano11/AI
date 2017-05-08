class HMM:
    """
    HMM (Hidden Markov Model), returns the processed Markov Model
    to get a value in order to shoot the enemy, this is the file
    that calculates the values that we need to process, the
    agent_none calls this file and "send" data in order to
    get it processed
    """
    def __init__(self, transition_probs, emission_probs):
      """
      Initialization of the class, it takes transition_probs that
      stores the possible transitions of the enemy so that it can
      calculate where it might move, emission_probs stores the
      probabilities that the enemy will do what we "said" it will do
      """
      self._transition_probs = transition_probs
      self._emission_probs = emission_probs

    def emission(self, emission):
      #Calculate and return the emission matrix
      return self._emission_probs[:, emission]

    @property                                       #@property is a build in python function that makes posible to create read-only properties.
    def num_states(self):                           #Calculates and return the states matrix.
        return self._transition_probs.shape[0]

    @property
    def transition_probabilities(self):             #Calculates and return the states matrix.
        return self._transition_probs