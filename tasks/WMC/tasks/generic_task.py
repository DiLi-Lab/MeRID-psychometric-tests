import os
import pandas as pd

class GenericTrial:
    def __init__(self):
        pass

    def finish(self):
        pass

class GenericTask:
    def __init__(self):
        self.name = 'generic'
        
        self.practice_trials = []
        self.trials = []

        self.current_practice_trial_id = -1
        self.current_trial_id = -1

        self.did_practice = False
        self.do_practice = True

        self.current_trial = None

        self.results = pd.DataFrame()

    def get_trial_count(self):
        if self.do_practice:
            return self.get_practice_trial_count()
        else:
            return self.get_real_trial_count()

    def get_real_trial_count(self):
        return len(self.trials)

    def get_practice_trial_count(self):
        return len(self.practice_trials)

    def has_pause(self):
        # no pause if uninitialized
        if self.current_trial_id == -1:
            return False
        # no pause if last trial
        elif self.current_trial_id >= self.get_trial_count() - 1:
            return False
        # pause every three trials
        elif (self.current_trial_id + 1) % 3 == 0:
            return True
        else:
            return False

    def start_new_trial(self):
        if self.do_practice:
            return self.start_new_practice_trial()
        else:
            return self.start_new_real_trial()
        
    def start_new_real_trial(self):
        assert self.current_trial_id + 1 < len(self.trials)
        self.current_trial_id += 1
        self.current_trial = self.trials[self.current_trial_id]

        return self.current_trial

    def start_new_practice_trial(self):
        assert self.current_practice_trial_id + 1 < len(self.practice_trials)
        self.current_practice_trial_id += 1
        self.current_trial = self.practice_trials[
            self.current_practice_trial_id]

        return self.current_trial

    def get_left_trials(self):
        if self.do_practice:
            n_trials = len(self.practice_trials)
            current_trial_id = self.current_practice_trial_id
        else:
            n_trials = len(self.trials)
            current_trial_id = self.current_trial_id

        return n_trials - current_trial_id - 1

    def finish_trial(self):
        if self.current_trial is not None:
            self.current_trial.finish()
        
        if self.get_left_trials() == 0:
            self.do_practice = False
            self.did_practice = True

        self.current_trial = None

    def write_results(self, filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        self.results.to_csv(filepath, sep=' ', header=False,
                            float_format='%.3f')
