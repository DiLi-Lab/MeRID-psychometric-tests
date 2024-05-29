import os
import random
import pandas as pd
import yaml

from tasks.generic_task import GenericTask, GenericTrial


class SentenceSpanTrial(GenericTrial):
    def __init__(self, letters, sentences):
        assert len(letters) == len(sentences)
        
        super().__init__()
        self.letters = letters
        self.sentences = sentences

        self.current_presentation_step = -1
        self.current_recall_step = -1

        self.letter_resps = [None] * len(letters)
        self.letter_rts = [None] * len(letters)
        self.sentence_resps = [None] * len(sentences)
        self.sentence_rts = [None] * len(sentences)

    def get_presentation_count(self):
        return len(self.letters)

    def get_next_letter(self):
        return self.letters[self.current_presentation_step]

    def get_next_sentence(self):
        self.current_presentation_step += 1
        return self.sentences[self.current_presentation_step]

    def get_next_recall_letter(self):
        self.current_recall_step += 1
        return self.letters[self.current_recall_step]

    def save_letter_response(self, response, response_time):
        self.letter_resps[self.current_recall_step] = response
        self.letter_rts[self.current_recall_step] = response_time

    def save_sentence_response(self, response, response_time):
        self.sentence_resps[self.current_presentation_step] = int(response)
        self.sentence_rts[self.current_presentation_step] = response_time


class SentenceSpanSentence:
    def __init__(self, sentence_string, correct):
        self.sentence_string = sentence_string
        self.correct = correct

    def __str__(self):
        return self.sentence_string

    
class SentenceSpanTrialFactory:
    def __init__(self, alphabet, true_sentences, false_sentences):
        self.alphabet = alphabet
        self.true_sentences = true_sentences
        self.false_sentences = false_sentences
        random.shuffle(self.true_sentences)
        random.shuffle(self.false_sentences)

    def generate(self, list_lengths, n_trials_per_condition):
        n_trials = len(list_lengths) * n_trials_per_condition
        trial_list_lengths = list_lengths * n_trials_per_condition

        extra_true = False    # these extra values will be toggled to
        extra_false = True    # balance sampling on uneven list lengths
        
        trials = []
        for list_length in trial_list_lengths:
            trial_letters = random.sample(self.alphabet, k=list_length)

            if list_length % 2:  # toggle extra value sampling
                extra_true = not(extra_true)
                extra_false = not(extra_false)
            
            n_true = list_length // 2 + extra_true * list_length % 2
            n_false = list_length // 2 + extra_false * list_length % 2

            true_sentences = self.true_sentences.copy()
            false_sentences = self.false_sentences.copy()
            trial_sentences = []
            for _ in range(n_true):
                sentence_string = true_sentences.pop()
                sentence = SentenceSpanSentence(sentence_string, True)
                trial_sentences.append(sentence)
            for _ in range(n_false):
                sentence_string = false_sentences.pop()
                sentence = SentenceSpanSentence(sentence_string, False)
                trial_sentences.append(sentence)
            # print('trial_sentences:', trial_sentences)

            random.shuffle(trial_sentences)

            trial = SentenceSpanTrial(trial_letters, trial_sentences)
            trials.append(trial)

        random.shuffle(trials)
        return trials


class SentenceSpanTask(GenericTask):
    def __init__(self, language, seed, config):
        super().__init__()

        random.seed(seed)
        self.name = 'SS'
        self.language = language

        self.config = config
        
        self.key_map = config['key_map']
        self.inv_key_map = {v: k for k, v in config['key_map'].items()}
        
        self.load_sentences(language, config.encoding)
        self.init_trials(config)
        self.init_results(config)

    def load_sentences(self, language, encoding):
        filepath = os.path.join('languages/', f'{language}/WMC/sentence_span_sentences_{language.lower()}.yaml')
        with open(filepath, mode='r', encoding=encoding) as f:
            self.sentences = yaml.safe_load(f)

        self.sentences['practice'][True] = SentenceSpanTask.strip_sentences(
            self.sentences['practice'][True])
        self.sentences['practice'][False] = SentenceSpanTask.strip_sentences(
            self.sentences['practice'][False])
        self.sentences['trials'][True] = SentenceSpanTask.strip_sentences(
            self.sentences['trials'][True])
        self.sentences['trials'][False] = SentenceSpanTask.strip_sentences(
            self.sentences['trials'][False])

    @staticmethod
    def strip_sentences(sentences):
        sentences = [sentence.lstrip().rstrip() for sentence in sentences]
        sentences = [sentence for sentence in sentences if len(sentence) > 0]
        return sentences
        
    def init_trials(self, config):
        practice_trial_factory = SentenceSpanTrialFactory(
            alphabet=config['alphabet'],
            true_sentences=self.sentences['practice'][True],
            false_sentences=self.sentences['practice'][False],
        )
        
        self.practice_trials = practice_trial_factory.generate(
            list_lengths=config['practice']['list_lengths'],
            n_trials_per_condition=config['practice']['n_trials_per_condition']
        )
        
        trial_factory = SentenceSpanTrialFactory(
            alphabet=config['alphabet'],
            true_sentences=self.sentences['trials'][True],
            false_sentences=self.sentences['trials'][False],
        )
        
        self.trials = trial_factory.generate(
            list_lengths=config['trials']['list_lengths'],
            n_trials_per_condition=config['trials']['n_trials_per_condition']
        )

    def init_results(self, config):
        result_idx = range(len(self.trials))

        list_length = config['trials']['max_list_length']

        self.letter_cols = [f'letter_correct{i}'
                            for i in range(list_length)]
        self.letter_resp_cols = [f'letter_response_{i}'
                                 for i in range(list_length)]
        self.letter_rt_cols = [f'letter_rt_{i}' for i in range(list_length)]

        self.sentence_correct_cols = [f'sentence_correct_{i}'
                                      for i in range(list_length)]
        self.sentence_resp_cols = [f'sentence_response_{i}'
                                   for i in range(list_length)]
        self.sentence_rt_cols = [f'sentence_rt_{i}'
                                 for i in range(list_length)]

        result_cols = (['list_length']
                       + self.letter_cols
                       + self.letter_resp_cols
                       + self.letter_rt_cols
                       + self.sentence_correct_cols
                       + self.sentence_resp_cols
                       + self.sentence_rt_cols)

        self.results = pd.DataFrame(data='?',
                                    index=result_idx,
                                    columns=result_cols,
                                    dtype=str)
        self.results.index.name = 'trial_id'

        self.results[self.letter_cols] = '%'
        self.results[self.letter_resp_cols] = '%'
        self.results[self.letter_rt_cols] = '-1.000'

        self.results[self.sentence_correct_cols] = '-1'
        self.results[self.sentence_resp_cols] = '-1'
        self.results[self.sentence_rt_cols] = '-1.000'

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

        sentences = trial.sentences
        sentences_correct = [int(s.correct) for s in sentences]
        trial_row.loc[self.sentence_correct_cols[:list_length]] = sentences_correct
        sentence_resps = trial.sentence_resps
        trial_row.loc[self.sentence_resp_cols[:list_length]] = sentence_resps
        sentence_rts = trial.sentence_rts
        trial_row.loc[self.sentence_rt_cols[:list_length]] = sentence_rts

    def get_sentence_keys(self):
        return list(self.key_map.values())
