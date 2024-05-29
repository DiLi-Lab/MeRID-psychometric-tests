from itertools import product
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow


class SpatialShortTermMemoryScoreCandidate:
    def __init__(self, correct_dots, response_dots):
        self.correct_dots = correct_dots
        self.response_dots = response_dots
        
        # offset between first correct dot and first response dot
        offset = tuple(a - b for a, b in zip(correct_dots[0], response_dots[0]))
        self.shifted_response_dots = [
            tuple(a + b for a, b in zip(response_dot, offset))
            for response_dot in response_dots
        ]
        self.offset = offset

    def compute_trial_score(self):
        score_matrix = np.array(self.get_score_matrix())
        resp_ass, corr_ass = linear_sum_assignment(score_matrix, maximize=True)
        score_matrix -= 1  # no we subtract one from each score position
        score = (score_matrix)[resp_ass, corr_ass].sum()

        self.response_dots = np.array(self.response_dots)[resp_ass]
        self.shifted_response_dots = np.array(
            self.shifted_response_dots)[resp_ass]
        self.dot_scores = score_matrix[resp_ass, corr_ass]
        return score
        
    def are_neighbours(self, a, b):
        if abs(a[0] - b[0]) > 1 or abs(a[1] - b[1]) > 1:
            return False
        else:
            return True

    def get_score_matrix(self):
        # scipy package does not support 0 as weight
        # but we can add 1 and subtract afterwards
        matrix = [[1 for _ in enumerate(self.correct_dots)]
                  for _ in enumerate(self.shifted_response_dots)]

        # now set weights between response and correct nodes
        product_iterator = product(enumerate(self.shifted_response_dots),
                                   enumerate(self.correct_dots))
        for (i_resp, resp_dot), (i_corr, corr_dot) in product_iterator:
            if resp_dot == corr_dot:
                matrix[i_resp][i_corr] = 3
            elif self.are_neighbours(resp_dot, corr_dot):
                matrix[i_resp][i_corr] = 2
        return matrix
            
class SpatialShortTermMemoryScorer:
    def __init__(self, trials, experiment_data):
        self.trials = trials
        self.experiment_data = experiment_data
        
        self.init_dot_scores(trials)
        self.init_trial_scores(trials, experiment_data)
        self.date = experiment_data.extraInfo['datetime']
        
    def init_dot_scores(self, trials):
        columns = ['ResRow', 'ResCol',
                   'TrasfResRow', 'TrasfResCol',
                   'AnsRow', 'AnsCol', 'Score']
        index_names = ['InTrial#', 'Dot']
        # index values start with 1
        index_tuples = [(trial_id + 1, dot_id + 1)
                        for trial_id, trial in enumerate(trials)
                        for dot_id in range(len((trial.sequence)))]
        index = pd.MultiIndex.from_tuples(index_tuples,
                                          names=index_names)

        self.dot_scores = pd.DataFrame(index=index,
                                       columns=columns,
                                       data=-1, dtype=int)
        
        dot_scores_ans = [(row, col) for trial in trials
                          for row, col in trial.sequence]
        self.dot_scores['AnsRow'] = [ds[0] for ds in dot_scores_ans]
        self.dot_scores['AnsCol'] = [ds[1] for ds in dot_scores_ans]

    def init_trial_scores(self, trials, experiment_data):
        self.subject_id = experiment_data.extraInfo['participant_id']
        
        columns = ['Score', 'RT', 'NumDot']
        index_names = ['ID', 'Trial']
        # index values start with 1
        index_tuples = [(self.subject_id, trial_id + 1)
                        for trial_id in range(len((trials)))]
        index = pd.MultiIndex.from_tuples(index_tuples,
                                          names=index_names)

        self.trial_scores = pd.DataFrame(index=index,
                                         columns=columns,
                                         data=-1)
        self.trial_scores['NumDot'] = [len(t.sequence) for t in trials]
        self.trial_scores['RT'] = 0.1

    def compute_trial_score(self, trial_id):
        trial = self.trials[trial_id]
            
        trial_score = self.trial_scores.loc[self.subject_id, trial_id + 1].copy()
        trial_score.loc['RT'] = trial.response_time
        trial_dot_scores = self.dot_scores.loc[trial_id + 1, :]
        trial_score.loc['Score'] = trial_dot_scores['Score'].sum()
        self.trial_scores.loc[self.subject_id, trial_id + 1] = trial_score


    def compute_dot_scores(self, trial_id):
        trial = self.trials[trial_id]
        response_dots = trial.response_dots
        correct_dots = trial.sequence

        candidates = self.get_candidates(response_dots, correct_dots)
        best_candidate = self.get_best_candidate(candidates)
                
        # we now have found the best candidate with a corresponding permutation
        # now save the information into the dot score data frame
        # remember, trial ids start with 1 for legacy reasons
        self.dot_scores.loc[trial_id + 1, 'Score'] = best_candidate.dot_scores
        
        correct_dots_rows = [dot[0] for dot in best_candidate.correct_dots]
        correct_dots_cols = [dot[1] for dot in best_candidate.correct_dots]
        self.dot_scores.loc[trial_id + 1, 'AnsRow'] = correct_dots_rows
        self.dot_scores.loc[trial_id + 1, 'AnsCol'] = correct_dots_cols

        response_rows = [dot[0] for dot in best_candidate.response_dots]
        response_cols = [dot[1] for dot in best_candidate.response_dots]
        self.dot_scores.loc[trial_id + 1, 'ResRow'] = response_rows
        self.dot_scores.loc[trial_id + 1, 'ResCol'] = response_cols

        shifted_response_dots = best_candidate.shifted_response_dots
        shifted_resp_rows = [dot[0] for dot in shifted_response_dots]
        shifted_resp_cols = [dot[1] for dot in shifted_response_dots]
        self.dot_scores.loc[trial_id + 1, 'TrasfResRow'] = shifted_resp_rows
        self.dot_scores.loc[trial_id + 1, 'TrasfResCol'] = shifted_resp_cols

    def get_candidates(self, response_dots, correct_dots):
        # each swap first positions of response and correct dots
        # because scoring is done for relative positioning not absolute
        candidates = [None for _ in range(len(response_dots)*len(correct_dots))]
        i = 0
        for j in range(len(correct_dots)):
            corr_candidate = correct_dots.copy()
            if j > 0: # swap first positions
                corr_candidate[0] = correct_dots[j]
                corr_candidate[j] = correct_dots[0]

            for k in range(len(response_dots)):
                resp_candidate = response_dots.copy()
                if k > 0: # swap first positions
                    resp_candidate[0] = response_dots[k]
                    resp_candidate[k] = response_dots[0]

                candidate = SpatialShortTermMemoryScoreCandidate(
                    corr_candidate, resp_candidate)
                candidates[i] = candidate
                i += 1

        return candidates
        
    def get_best_candidate(self, candidates):
        best_trial_score = -1
        best_candidate = None
        for candidate in candidates:
            trial_score = candidate.compute_trial_score()

            if trial_score > best_trial_score:
                best_trial_score = trial_score
                best_candidate = candidate

        return best_candidate

    def compute_scores(self):
        for trial_id, trial in enumerate(self.trials):
            self.compute_dot_scores(trial_id)
            self.compute_trial_score(trial_id)
