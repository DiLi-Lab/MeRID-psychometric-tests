from datetime import datetime, timedelta
from itertools import product, permutations
import pandas as pd
from psychopy import data
import pytest
import warnings

from common.config import WMCConfig
import tasks.spatial_short_term_memory as sstm


score_filenames = [
    'tests/SSTM-01-1-1975.txt',
]

def load_score_file(filename, nrows_trials, nrows_dots, skiprows):
    index_cols = ['ID', 'Trial']
    df_trials = pd.read_csv(filename, sep=r'\s+', header=1,
                            nrows=nrows_trials, index_col=index_cols)

    dot_cols = ['Dot', 'ResRow', 'ResCol', 'TrasfResRow', 'TrasfResCol',
                'AnsRow', 'AnsCol', 'Score', 'InTrial#']
    index_cols = ['InTrial#', 'Dot']
    df_dots = pd.read_csv(filename, sep=r'\s+', header=None,
                          names=dot_cols, index_col=index_cols,
                          nrows=nrows_dots, skiprows=skiprows)

    return df_trials, df_dots


def extract_dot_sequences(df):
    sequences = []
    for _, trial_group in df.groupby(level='InTrial#'):
        sequence_rows = trial_group['AnsRow']
        sequence_cols = trial_group['AnsCol']
        trial_sequence = list(zip(sequence_rows, sequence_cols))
        sequences.append(trial_sequence)
    return sequences


def extract_dot_responses(df):
    responses = []
    for _, trial_group in df.groupby(level='InTrial#'):
        response_rows = trial_group['ResRow']
        response_cols = trial_group['ResCol']
        response = list(zip(response_rows, response_cols))
        responses.append(response)
    return responses


def create_trials(sequences, response_times):
    config = WMCConfig('English').spatial_short_term_memory
    grid = sstm.SpatialShortTermMemoryGrid(
        window=None,
        n_rows=config['grid']['n_rows'],
        n_cols=config['grid']['n_cols'],
        cell_height=config['cell']['height'],
        cell_width=config['cell']['width'])

    trials = [sstm.SpatialShortTermMemoryTrial(sequence, grid)
              for sequence in sequences]

    for trial, response_time in zip(trials, response_times):
        trial.response_time = response_time

    return trials


def get_simple_permutations(sequences):
    sequence_permutators = [permutations(sequence) for sequence in sequences]

    # we don't need a full product of each single permutation
    # it's sufficient to have each sequence permutation at least once

    sequence_permutation = [list(next(sp)) for sp in sequence_permutators]
    sequence_permutations = [sequence_permutation]

    for i, this_sequence_permutator in enumerate(sequence_permutators):
        while True:
            try:
                this_sequence_permutation = next(this_sequence_permutator)
            except StopIteration:
                break

            sequence_permutation = sequence_permutation.copy()
            sequence_permutation[i] = list(this_sequence_permutation)
            sequence_permutations.append(sequence_permutation)

    return sequence_permutations


def df_diff(df1, df2):
    df_l = df1.copy()
    df_r = df2.copy()
    for (index, row_l), (_, row_r) in zip(df1.iterrows(), df2.iterrows()):
        if row_l.equals(row_r):
            df_l.drop(index, axis='index', inplace=True)
            df_r.drop(index, axis='index', inplace=True)

    return df_l, df_r


def get_trials_with_unequivalent_dot_score_sum(df1, df2):
    trial_id_col = 'InTrial#'
    
    df_l = df1.copy()
    df_r = df2.copy()

    df_l_groupby = df_l.groupby(level=trial_id_col)
    df_r_groupby = df_r.groupby(level=trial_id_col)

    corr_trials = df_l_groupby['Score'].sum() == df_r_groupby['Score'].sum()
    drop_trials = corr_trials[corr_trials].index

    df_l.drop(index=drop_trials, inplace=True)
    df_r.drop(index=drop_trials, inplace=True)

    return df_l, df_r


def set_trial_responses(trials, responses):
    for trial, response in zip(trials, responses):
        trial.response_dots = response
    return trials


def generate_all_equivalence_parameters(filename):
    parameters = []
    
    df_trials_example, df_dots_example = load_score_file(
        filename, nrows_trials=14, nrows_dots=52, skiprows=20)

    assert df_trials_example.shape == (14, 3)
    assert df_dots_example.shape == (52, 7)

    example_sequences = extract_dot_sequences(df_dots_example)
    assert len(example_sequences) == 14
    example_responses = extract_dot_responses(df_dots_example)
    assert len(example_responses) == 14

    correct_dots_permutations = get_simple_permutations(example_sequences)
    for correct_dots_permutation in correct_dots_permutations:
        #response_permutations = get_simple_permutations(example_responses)
        # it's sufficient to permutate the correct dot sequences
        response_permutations = [example_responses]
        for response_permutation in response_permutations:
            parameter = {
                'df_trials_example': df_trials_example,
                'df_dots_example': df_dots_example,
                'correct_dots': correct_dots_permutation,
                'response_dots': response_permutation,
            }
            parameters.append(parameter)

    return parameters

parameter_dicts = [d for filename in score_filenames
                   for d in generate_all_equivalence_parameters(filename)]

@pytest.mark.parametrize("parameter_dict", parameter_dicts)
def test_example_score_file_equivalence(parameter_dict):
    df_trials_example = parameter_dict['df_trials_example']
    df_dots_example = parameter_dict['df_dots_example']
    correct_dots = parameter_dict['correct_dots']
    response_dots = parameter_dict['response_dots']
    
    trials = create_trials(correct_dots, df_trials_example.RT)
    trials = set_trial_responses(trials, response_dots)
    
    for trial in trials:
        assert len(trial.sequence) == len(trial.response_dots)

    subject_id = df_trials_example.index.get_level_values('ID')[0]
    experiment_data = data.ExperimentHandler(
        name='test',
        extraInfo={'Subject ID': subject_id,
                   'date': None,
                   'datetime': datetime.now()}
    )
    
    scorer = sstm.SpatialShortTermMemoryScorer(trials, experiment_data)
    scorer.compute_scores()

    assert df_dots_example.index.equals(scorer.dot_scores.index), (
        r'dot score index does not match!'
    )
    
    dot_diff_l, dot_diff_r = get_trials_with_unequivalent_dot_score_sum(
        df_dots_example, scorer.dot_scores)

    assert len(dot_diff_l) == len(dot_diff_r) == 0 , (
        f'dot scores do not match! \r\n\r\n'
        f'example: \r\n{dot_diff_l}\r\n\r\n'
        f'but computed scores are: \r\n{dot_diff_r}\r\n\r\n'
    )

    assert df_trials_example.index.equals(scorer.trial_scores.index), (
        r'trial score index does not match!'
    )
    
    trial_diff_l, trial_diff_r = df_diff(df_trials_example,
                                         scorer.trial_scores)

    assert len(trial_diff_l) == len(trial_diff_r) == 0 , (
        f'trial scores do not match! \r\n\r\n'
        f'example: \r\n{trial_diff_l}\r\n\r\n'
        f'but computed scores are: \r\n{trial_diff_r}\r\n\r\n'
    )


def test_single_trial_sequence():
    sequence = [(2, 9), (5, 9), (8, 7), (4, 2), (5, 5)]
    response_dots = [(4, 9), (2, 9), (8, 6), (3, 2), (6, 9)]
    response_time = 4.7139999999999995

    config = WMCConfig('English').spatial_short_term_memory
    grid = sstm.SpatialShortTermMemoryGrid(
        window=None,
        n_rows=config['grid']['n_rows'],
        n_cols=config['grid']['n_cols'],
        cell_height=config['cell']['height'],
        cell_width=config['cell']['width'])

    trial = sstm.SpatialShortTermMemoryTrial(sequence, grid)
    trial.response_dots = response_dots
    trial.response_time = response_time
    trials = [trial]

    experiment_data = data.ExperimentHandler(
        name='test', extraInfo={'Subject ID': 1,
                                'date': None,
                                'datetime': datetime.now()}
    )
    
    scorer = sstm.SpatialShortTermMemoryScorer(trials, experiment_data)
    scorer.compute_scores()

    assert scorer.dot_scores.Score.sum() == 6, (
        f'{scorer.dot_scores}')


def test_scoring_computation_duration():
    max_duration = timedelta(seconds=1)
    filename = 'tests/SSTM-2.dat'
    df_trials_example, df_dots_example = load_score_file(
        filename, nrows_trials=30, nrows_dots=120, skiprows=36)

    correct_dots = extract_dot_sequences(df_dots_example)
    response_dots = extract_dot_responses(df_dots_example)

    print(correct_dots)
    print(response_dots)

    trials = create_trials(correct_dots, df_trials_example.RT)
    trials = set_trial_responses(trials, response_dots)
    
    for trial in trials:
        assert len(trial.sequence) == len(trial.response_dots)

    subject_id = df_trials_example.index.get_level_values('ID')[0]
    
    experiment_data = data.ExperimentHandler(
        name='test', extraInfo={'Subject ID': subject_id,
                                'date': None,
                                'datetime': datetime.now()}
    )

    start_time = datetime.now()
    
    scorer = sstm.SpatialShortTermMemoryScorer(trials, experiment_data)
    scorer.compute_scores()

    duration = datetime.now() - start_time
    assert duration <= max_duration
