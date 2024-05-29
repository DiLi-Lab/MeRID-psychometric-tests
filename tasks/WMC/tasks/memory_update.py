import operator as op
import random
from psychopy import visual
import pandas as pd

from tasks.generic_task import GenericTask, GenericTrial


operator_string_map = {
    op.add: '+',
    op.sub: '-',
}

class MemoryUpdateOperation:
    def __init__(self, operator, operand_right, location):
        self.operator_str = operator_string_map[operator]
        self.operator = operator
        self.operand_right = operand_right
        self.location = location

    def get_location(self):
        return self.location

    def compute(self, operand_left):
        return self.operator(operand_left, self.operand_right)

    def __repr__(self):
        return f'{self.operator_str}{self.operand_right}'


class MemoryUpdateOperationFactory:
    def __init__(self):
        self.operators = [op.add, op.sub]
        self.operands_right = list(range(1, 9))

    def generate(self, digits, n_operations):
        locations = list(range(len(digits)))
        operations = []

        values = digits.copy()
        prev_operation = MemoryUpdateOperation(op.add, 0, 0)
        for _ in range(n_operations):
            location = random.choice(locations)
            # omit operand value from previous operation
            operator, operand_right = self.generate_operation(
                values[location], prev_operation.operand_right)

            operation = MemoryUpdateOperation(operator, operand_right, location)
            operations.append(operation)

            values[location] = operation.operator(values[location], operand_right)
            prev_operation = operation
            
        return operations

    def generate_operation(self, operand_left, omit):
        operands_right = [o for o in self.operands_right if o != omit]
        while True:
            operand_right = random.choice(operands_right)
            operator = random.choice(self.operators)

            # all (temporary) results need to be between 0 and 10
            result = operator(operand_left, operand_right)
            if result > 0 and result < 10:
                return operator, operand_right


class MemoryUpdateTrial(GenericTrial):
    def __init__(self, digits, operations, locations):
        super().__init__()
        
        self.digits = digits
        self.operations = operations
        self.locations = locations
        
        self.recall_order = list(range(len(digits)))
        random.shuffle(self.recall_order)
        self.results = self.compute_results(digits, operations)
        self.responses = [None] * len(digits)
        self.is_correct = [None] * len(digits)

        self.current_digit = -1
        self.current_operation = -1
        self.current_recall = -1

    def compute_results(self, digits, operations):
        results = digits.copy()

        for operation in operations:
            location = operation.get_location()
            results[location] = operation.compute(results[location])
        
        return results

    def get_n_digits(self):
        return len(self.digits)

    def get_n_operations(self):
        return len(self.operations)

    def get_next_digit(self):
        assert self.current_digit + 1 < len(self.digits)
        self.current_digit += 1

        digit = self.digits[self.current_digit]
        location = self.locations[self.current_digit]
        return digit, location

    def get_next_operation(self):
        assert self.current_operation + 1 < len(self.operations)
        self.current_operation += 1

        operation = self.operations[self.current_operation]
        location = self.locations[operation.location]
        
        return operation, location

    def get_operation_sequence_string(self, location_id):
        sequence_string = str(self.digits[location_id])
        for operation in self.operations:
            if operation.location == location_id:
                sequence_string += ' ' + str(operation)
        return sequence_string

    def get_next_recall(self):
        assert self.current_recall + 1 < len(self.digits)
        self.current_recall += 1

        result = self.results[self.recall_order[self.current_recall]]
        location = self.locations[self.recall_order[self.current_recall]]
        location_id = self.recall_order[self.current_recall]
        operation_sequence = self.get_operation_sequence_string(
            self.recall_order[self.current_recall])

        recall = {
            'result': result,
            'position': location,
            'position_id': location_id,
            'operation_sequence': operation_sequence,
        }
        return recall

    def get_left_recalls(self):
        return len(self.digits) - self.current_recall - 1

    def save_response(self, digit):
        try:
            digit = int(str(digit).replace('num_', ''))
        except ValueError:
            digit = -1
        self.responses[self.current_recall] = digit
        correct_result = self.results[self.recall_order[self.current_recall]]
        self.is_correct[self.current_recall] = int(digit == correct_result)


class MemoryUpdateTrialFactory:
    def __init__(self, locations):
        self.locations = locations
        self.valid_digits = list(range(1, 10))
        
    def generate(self, set_sizes, n_operations):
        assert len(set_sizes) == len(n_operations)
        assert all(set_size <= max(self.locations.keys()) for set_size in set_sizes)

        trials = []
        operation_factory = MemoryUpdateOperationFactory()
        for i in range(len(set_sizes)):
            trial_set_size = set_sizes[i]
            trial_n_operations = n_operations[i]
            
            trial_digits = random.sample(self.valid_digits, trial_set_size)
            trial_locations = self.locations[trial_set_size]
            trial_operations = operation_factory.generate(
                trial_digits, trial_n_operations)

            trial = MemoryUpdateTrial(
                trial_digits, trial_operations, trial_locations)
            trials.append(trial)

        return trials


class MemoryUpdateTask(GenericTask):
    def __init__(self, window, seed, config):
        super().__init__()
        random.seed(seed)
        self.name = 'MU'
        
        self.config = config
        self.init_frames(window, config)
        self.init_trials(config)
        self.init_results(config)

    def init_frames(self, window, config):
        frame_width = config['frames']['width']
        frame_height = config['frames']['height']
        frame_locations = config['frames']['locations']
        frame_units = config['frames']['units']

        self.frames = {n_frames: [] for n_frames in frame_locations.keys()}
        
        for n_frames, frame_positions in frame_locations.items():
            for frame_position in frame_positions:
                this_frame = visual.Rect(
                    win=window, name='frame',
                    width=frame_width,
                    height=frame_height,
                    ori=0, pos=frame_position,
                    lineWidth=1, lineColor='black', lineColorSpace='rgb',
                    fillColor=[1,1,1], fillColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=True,
                    units=frame_units)
                self.frames[n_frames].append(this_frame)

    def init_trials(self, config):
        trial_factory = MemoryUpdateTrialFactory(config['frames']['locations'])

        self.practice_trials = trial_factory.generate(
            set_sizes=config['practice']['set_sizes'],
            n_operations=config['practice']['n_operations'])

        self.trials = trial_factory.generate(
            set_sizes=config['trials']['set_sizes'],
            n_operations=config['trials']['n_operations'])

    def init_results(self, config):
        result_idx = range(len(config['trials']['set_sizes']))

        set_size = config['trials']['max_set_size']
        self.response_cols = [f'response_{i}' for i in range(set_size)]
        self.is_correct_cols = [f'is_correct_{i}' for i in range(set_size)]
        result_cols = self.response_cols + self.is_correct_cols

        self.results = pd.DataFrame(data=-1,
                                    index=result_idx,
                                    columns=result_cols)
        self.results.index.name = 'trial_id'

        self.results[self.response_cols] = 0
        self.results[self.is_correct_cols] = -1


    def start_new_trial(self):
        trial = super().start_new_trial()
        self.show_frames(trial.get_n_digits(), show=True)
        return trial

    def finish_trial(self):
        if self.current_trial is not None:
            self.copy_trial_results(self.current_trial)
        super().finish_trial()

    def copy_trial_results(self, trial):
        trial_row = self.results.iloc[self.current_trial_id]
        responses = trial.responses
        trial_row.loc[self.response_cols[:len(responses)]] = responses
        is_correct = trial.is_correct
        trial_row.loc[self.is_correct_cols[:len(is_correct)]] = is_correct

    def hide_frames(self):
        for n_frames in self.frames.keys():
            self.show_frames(n_frames, show=False)

    def show_frames(self, n_frames, show=True):
        assert n_frames in self.frames.keys()

        for frame in self.frames[n_frames]:
            frame.setAutoDraw(show)
