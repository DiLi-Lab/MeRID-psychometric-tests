import operator as op
import random
import pandas as pd

from tasks.generic_task import GenericTask, GenericTrial


operator_map = {
    '+': op.add,
    '-': op.sub,
}


class Equation:
    def __init__(self, operator, operand_left, operand_right, result, correct):
        self.operator = operator
        self.operand_left = operand_left
        self.operand_right = operand_right
        self.result = result
        self.correct = correct
        
    def __str__(self):
        return (f'{self.operand_left}{self.operator}{self.operand_right}'
                f'={self.result}')


class EquationFactory:
    def __init__(self, operators, operands_left, operands_right, valid_results):
        self.operators = operators
        self.operands_left = operands_left
        self.operands_right = operands_right
        self.valid_results = valid_results
        
    def generate_equation(self, correct):
        operator = random.choice(self.operators)

        result = None
        while result not in self.valid_results:
            operand_left = random.choice(self.operands_left)
            operand_right = random.choice(self.operands_right)
            result = operator_map[operator](operand_left, operand_right)
            
        if not correct:
            false_results = [r for r in self.valid_results if r != result]
            result = random.choice(false_results)

        return Equation(operator, operand_left, operand_right, result, correct)
        
    def generate_equations(self, n_correct, n_false, shuffle=True):
        equations = []
        for _ in range(n_correct):
            equations.append(self.generate_equation(correct=True))
        for _ in range(n_false):
            equations.append(self.generate_equation(correct=False))
        if shuffle:
            random.shuffle(equations)
        return equations


class OperationSpanTrial(GenericTrial):
    def __init__(self, letters, equations):
        assert len(letters) == len(equations)
        
        super().__init__()
        self.letters = letters
        self.equations = equations

        self.current_presentation_step = -1
        self.current_recall_step = -1

        self.letter_resps = [None] * len(letters)
        self.letter_rts = [None] * len(letters)
        self.equation_resps = [None] * len(equations)
        self.equation_rts = [None] * len(equations)

    def get_presentation_count(self):
        return len(self.letters)

    def get_next_letter(self):
        return self.letters[self.current_presentation_step]

    def get_next_equation(self):
        self.current_presentation_step += 1
        return self.equations[self.current_presentation_step]

    def get_next_recall_letter(self):
        self.current_recall_step += 1
        return self.letters[self.current_recall_step]

    def save_letter_response(self, response, response_time):
        self.letter_resps[self.current_recall_step] = response
        self.letter_rts[self.current_recall_step] = response_time

    def save_equation_response(self, response, response_time):
        self.equation_resps[self.current_presentation_step] = int(response)
        self.equation_rts[self.current_presentation_step] = response_time

    
class OperationSpanTrialFactory():
    def __init__(self, alphabet, operators, operand_left_min,
                 operand_left_max, operand_right_min, operand_right_max,
                 valid_result_min, valid_result_max):
        self.alphabet = alphabet
        
        operands_left = list(range(operand_left_min, operand_left_max + 1))
        operands_right = list(range(operand_right_min, operand_right_max + 1))
        valid_results = list(range(valid_result_min, valid_result_max + 1))

        self.equation_factory = EquationFactory(operators, operands_left,
                                                operands_right, valid_results)

    def generate(self, list_lengths, n_trials_per_condition, shuffle=True):
        n_trials = len(list_lengths) * n_trials_per_condition
        trial_list_lengths = list_lengths * n_trials_per_condition

        if shuffle:
            random.shuffle(trial_list_lengths)

        trials = []
        for list_length in trial_list_lengths:
            trial_letters = self.alphabet.copy()
            random.shuffle(trial_letters)
            trial_letters = trial_letters[:list_length]

            # on odd list lengths there will be one correct equation more
            n_correct = list_length // 2 + list_length % 2
            n_false = list_length // 2
        
            trial_equations = self.equation_factory.generate_equations(
                n_correct, n_false, shuffle=True)

            trial = OperationSpanTrial(trial_letters, trial_equations)
            trials.append(trial)
        return trials


class OperationSpanTask(GenericTask):
    def __init__(self, seed, config):
        super().__init__()
        
        random.seed(seed)
        self.name = 'OS'

        self.config = config
        
        self.key_map = config['key_map']
        self.inv_key_map = {v: k for k, v in config['key_map'].items()}

        self.init_trials(config)
        self.init_results(config)
        
    def init_trials(self, config):
        trial_factory = OperationSpanTrialFactory(
            alphabet=config['alphabet'],
            operators=config['equations']['operators'],
            operand_left_min=config['equations']['operand_left_min'],
            operand_left_max=config['equations']['operand_left_max'],
            operand_right_min=config['equations']['operand_right_min'],
            operand_right_max=config['equations']['operand_right_max'],
            valid_result_min=config['equations']['valid_result_min'],
            valid_result_max=config['equations']['valid_result_max'],
        )
        
        self.practice_trials = trial_factory.generate(
            list_lengths=config['practice']['list_lengths'],
            n_trials_per_condition=config['practice']['n_trials_per_condition'],
            shuffle=config['practice']['shuffle'],
        )
        
        self.trials = trial_factory.generate(
            list_lengths=config['trials']['list_lengths'],
            n_trials_per_condition=config['trials']['n_trials_per_condition'],
            shuffle=config['trials']['shuffle'],
        )

    def init_results(self, config):
        result_idx = range(len(self.trials))

        list_length = config['trials']['max_list_length']

        self.letter_cols = [f'letter_correct{i}'
                            for i in range(list_length)]
        self.letter_resp_cols = [f'letter_response_{i}'
                                 for i in range(list_length)]
        self.letter_rt_cols = [f'letter_rt_{i}' for i in range(list_length)]

        self.equation_correct_cols = [f'equation_correct_{i}'
                                      for i in range(list_length)]
        self.equation_resp_cols = [f'equation_response_{i}'
                                   for i in range(list_length)]
        self.equation_rt_cols = [f'equation_rt_{i}'
                                 for i in range(list_length)]

        result_cols = (['list_length']
                       + self.letter_cols
                       + self.letter_resp_cols
                       + self.letter_rt_cols
                       + self.equation_correct_cols
                       + self.equation_resp_cols
                       + self.equation_rt_cols)

        self.results = pd.DataFrame(data='?',
                                    index=result_idx,
                                    columns=result_cols,
                                    dtype=str)
        self.results.index.name = 'trial_id'

        self.results[self.letter_cols] = '%'
        self.results[self.letter_resp_cols] = '%'
        self.results[self.letter_rt_cols] = '-1.000'

        self.results[self.equation_correct_cols] = '-1'
        self.results[self.equation_resp_cols] = '-1'
        self.results[self.equation_rt_cols] = '-1.000'

    def finish_trial(self):
        if self.current_trial is not None:
            self.copy_trial_results(self.current_trial,
                                    self.current_trial_id)
        super().finish_trial()

    def copy_trial_results(self, trial, trial_id):
        trial_row = self.results.iloc[trial_id]
        list_length = trial.get_presentation_count()
        trial_row.loc['list_length'] = list_length

        letters = [l.upper() for l in trial.letters]
        trial_row.loc[self.letter_cols[:list_length]] = letters
        letter_resps = [l.upper() for l in trial.letter_resps]
        trial_row.loc[self.letter_resp_cols[:list_length]] = letter_resps
        letter_rts = trial.letter_rts
        trial_row.loc[self.letter_rt_cols[:list_length]] = letter_rts

        equations = trial.equations
        equations_correct = [int(e.correct) for e in equations]
        trial_row.loc[self.equation_correct_cols[:list_length]] = equations_correct
        equation_resps = trial.equation_resps
        trial_row.loc[self.equation_resp_cols[:list_length]] = equation_resps
        equation_rts = trial.equation_rts
        trial_row.loc[self.equation_rt_cols[:list_length]] = equation_rts

    def get_equation_keys(self):
        return list(self.key_map.values())
