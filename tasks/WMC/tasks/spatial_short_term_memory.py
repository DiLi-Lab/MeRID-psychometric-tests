from itertools import product, permutations
import os
import random

import numpy as np
import pandas as pd

from psychopy.visual import Line, Polygon, Rect
from psychopy.event import Mouse

from tasks.generic_task import GenericTask, GenericTrial
from tasks.spatial_short_term_memory_scorer import SpatialShortTermMemoryScorer

class SpatialShortTermMemoryGrid:
    def __init__(self, window, n_rows, n_cols, grid_height, grid_width,
                 line_width):
        self.window = window
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.init_cells(window=window, n_cols=n_cols, n_rows=n_rows,
                        grid_height=grid_height, grid_width=grid_width,
                        line_width=line_width)

    def init_cells(self, window, n_cols, n_rows, grid_height, grid_width,
                   line_width):
        self.cells = [[0 for _ in range(self.n_cols)]
                      for _ in range(self.n_rows)]
        self.lines = {
            'horizontal': [0 for _ in range(self.n_rows + 1)],
            'vertical': [0 for _ in range(self.n_cols + 1)],
        }
        
        cell_height = grid_height / self.n_rows
        cell_width = grid_width / self.n_cols

        top_line = grid_height / 2
        bottom_line = -grid_height / 2
        left_line = -grid_width / 2
        right_line = grid_width / 2

        top_row = top_line - cell_height / 2
        left_col = left_line - cell_width / 2
        
        self.position_map = {
            (row, col): (0, 0)
            for col in range(self.n_cols)
            for row in range(self.n_rows)
        }

        # generate horizontal lines
        for i in range(self.n_rows + 1):
            line_y = (top_line - i * cell_height)
            start_position = (left_line, line_y)
            end_position = (right_line, line_y)
            
            if window is not None:  # None only for testing
                this_line = Line(
                    win=window, name=f'horizontal_line_{i}',
                    start=start_position,
                    end=end_position,
                    lineWidth=line_width,
                    lineColor='black', lineColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=False)
                self.lines['horizontal'][i] = this_line

        # generate vertical lines
        for i in range(self.n_cols + 1):
            line_x = (left_line + i * cell_width)
            start_position = (line_x, bottom_line)
            end_position = (line_x, top_line)
            
            if window is not None:  # None only for testing
                this_line = Line(
                    win=window, name=f'horizontal_line_{i}',
                    start=start_position,
                    end=end_position,
                    lineWidth=line_width,
                    lineColor='black', lineColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=False)
                self.lines['vertical'][i] = this_line

        # generate cells
        for row, col in product(range(self.n_rows), (range(self.n_cols))):
            cell_position = (left_col + (col + 1) * cell_width,
                             top_row - row * cell_height)
            self.position_map[(row, col)] = cell_position

            if window is not None:  # None only for testing
                this_cell = Rect(
                    win=window, name=f'cell_{row}_{col}',
                    width=cell_width,
                    height=cell_height,
                    ori=0, pos=cell_position,
                    lineWidth=0,
                    lineColor='white', lineColorSpace='rgb',
                    fillColor='white', fillColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=False)
                self.cells[row][col] = this_cell

    def get_grid_positions(self):
        row_col_product = product(range(self.n_rows), range(self.n_cols))
        grid_positions = [(row, col) for row, col in row_col_product]

        return grid_positions

    def get_position_map(self):
        return self.position_map

    def show(self, show=True):
        if self.window is None:  # None only for testing
            return
        
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                self.cells[row][col].setAutoDraw(show)

        for grid_line in self.lines['horizontal']:
            grid_line.setAutoDraw(show)
        for grid_line in self.lines['vertical']:
            grid_line.setAutoDraw(show)
        


class SpatialShortTermMemoryTrial(GenericTrial):
    def __init__(self, sequence, grid, dot_size):
        super().__init__()

        self.sequence = sequence
        self.grid = grid
        
        self.current_dot = -1
        self.was_pressed = None
        self.init_cell_selection(grid)
        self.init_dot_reserve(window=grid.window,
                              n_dots=len(sequence)+1,
                              dot_size=dot_size)
        self.response_dots = None
        self.response_time = None

    def init_dot_reserve(self, window, n_dots, dot_size):
        self.dot_reserve = []
        for i in range(n_dots):
            if window is not None:  # None only for Testing
                dot = Polygon(
                    win=window, name=f'selected_dot_{i}',
                    edges=128, size=(dot_size, dot_size),
                    ori=0, pos=[0,0],
                    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
                    fillColor='black', fillColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=False)
                dot.setAutoDraw(False)
                self.dot_reserve.append(dot)

    def init_cell_selection(self, grid):
        self.cell_selection = {
            (row, col): None
            for col in range(grid.n_cols)
            for row in range(grid.n_rows)
        }

    def get_presentation_count(self):
        return len(self.sequence)

    def get_next_presentation(self):
        assert self.current_dot + 1 < len(self.sequence)
        self.current_dot += 1
        dot_row, dot_col = self.sequence[self.current_dot]
        return self.grid.get_position_map()[(dot_row, dot_col)]

    def get_pressed_coordinates(self, mouse):
        for row, col in self.grid.get_grid_positions():
            if mouse.isPressedIn(shape=self.grid.cells[row][col]):
                return row, col
        return None

    def process_mouse_event(self, mouse):
        is_pressed = any(v != 0 for v in mouse.getPressed())

        if is_pressed and not self.was_pressed:
            self.update_selected_dots(mouse)
            self.was_pressed = True
        elif not is_pressed:
            self.was_pressed = False
            
    def selected_required_count(self):
        return self.get_selected_cell_count() == self.get_presentation_count()
    
    def update_selected_dots(self, mouse):
        grid_coordinates = self.get_pressed_coordinates(mouse)
        if grid_coordinates is None:
            return
        row, col = grid_coordinates

        if not self.is_cell_selected(row, col):
            if self.get_selected_cell_count() < self.get_presentation_count():
                self.select_cell(row, col)
        else:
            self.deselect_cell(row, col)

    def is_cell_selected(self, row, col):
        return self.cell_selection[(row, col)] is not None

    def select_cell(self, row, col):
        dot = self.dot_reserve.pop()
        dot.pos = self.grid.position_map[(row, col)]
        dot.setAutoDraw(True)
        self.cell_selection[(row, col)] = dot

    def deselect_cell(self, row, col):
        dot = self.cell_selection[(row, col)]
        dot.setAutoDraw(False)
        self.dot_reserve.append(dot)
        self.cell_selection[(row, col)] = None

    def get_selected_cells(self):
        return [(row, col) for (row, col), dot in self.cell_selection.items()
                if dot is not None]

    def get_selected_cell_count(self):
        return len(list(filter(None, self.cell_selection.values())))

    def save_response(self, response_time):
        self.response_dots = self.get_selected_cells()
        self.response_time = response_time

    def show(self, show=True):
        self.grid.show(show)
        
        dots = list(filter(None, self.cell_selection.values()))
        for dot in dots:
            dot.setAutoDraw(show)
            self.dot_reserve.append(dot)
        for coordinate in self.cell_selection.keys():
            self.cell_selection[coordinate] = None


class SpatialShortTermMemoryTrialFactory:
    def __init__(self, grid, padding, dot_size):
        self.grid = grid
        self.dot_size = dot_size
        grid_positions = self.grid.get_grid_positions()
        self.valid_positions = self.shrink_grid(grid_positions, padding)

    def generate(self, n_dots_list, n_far, n_near):
        trials = []
        for n_dots in n_dots_list:
            for _ in range(n_far):
                sequence = self.generate_far_stimuli(n_dots)
                trial = SpatialShortTermMemoryTrial(
                    sequence, self.grid, self.dot_size)
                trials.append(trial)

            for _ in range(n_near):
                sequence = self.generate_near_stimuli(n_dots)
                trial = SpatialShortTermMemoryTrial(
                    sequence, self.grid, self.dot_size)
                trials.append(trial)

        assert random.shuffle(trials) is None
        return trials

    def generate_far_stimuli(self, n_dots, min_distance=3):
        '''
        sequence = [None for _ in range(n_dots)]
        sequence[0] = random.choice(self.valid_positions)

        for i in range(1, n_dots):
            for _i in range(1000):
                sequence[i] = random.choice([p for p in self.valid_positions
                                         if p not in sequence])
                dot_distances = self.compute_dot_distances(sequence[:i+1])

                if np.min(dot_distances) <= min_distance:
                    sequence[i] = None
                else:
                    break
        '''

        sequence = [None for _ in range(n_dots)]
        sequence[0] = random.choice(self.valid_positions)

        spot = self.create_spot(sequence[0], min_distance-1, False)
        valid_positions = [p for p in self.valid_positions if p not in spot]

        for _i in range(10000):
            sequence = random.sample(valid_positions, n_dots)
            dot_distances = self.compute_dot_distances(sequence)

            if np.min(dot_distances) >= min_distance:
                break
        return sequence

    def generate_near_stimuli(self, n_dots, max_distance=2):
        '''
        for i in range(1, n_dots):
            for _i in range(1000):
                sequence[i] = random.choice([p for p in self.valid_positions
                                         if p != sequence[i-1]])
                dot_distances = self.compute_dot_distances(sequence[:i+1])

                if np.max(dot_distances) > max_distance:
                    sequence[i] = None
                else:
                    break

            assert sequence[i] is not None, f'{_i} {sequence} {n_dots}'
        '''
        origin_candidates = self.shrink_grid(self.valid_positions,
                                             by=max_distance)
        sequence = [None for _ in range(n_dots)]
        sequence[0] = random.choice(origin_candidates)

        spot = self.create_spot(sequence[0], 2 * max_distance, False)
        for _i in range(10000):
            sequence[1:] = random.sample(spot, n_dots - 1)
            dot_distances = self.compute_dot_distances(sequence)

            if np.max(dot_distances) <= 2 * max_distance:
                break
        return sequence

    def compute_dot_distances(self, dots, drop_diagonal=True):
        n_dots = len(dots)
        distances = [[0 for _ in range(n_dots)] for _ in range(n_dots)]

        for i, j in product(range(n_dots), range(n_dots)):
            dot_i, dot_j = dots[i], dots[j]
            dist_horizontal = abs(dots[i][0] - dots[j][0])
            dist_vertical = abs(dots[i][1] - dots[j][1])
            distances[i][j] = max(dist_horizontal, dist_vertical)

        distances = np.array(distances)
        if drop_diagonal:
            diagonal = np.eye(distances.shape[0], dtype=bool)
            distances = distances[~diagonal].reshape(distances.shape[0], -1)
            
        return distances

    def shrink_grid(self, positions, by):
        cols = [position[0] for position in positions]
        rows = [position[1] for position in positions]

        min_col, max_col = min(cols), max(cols)
        min_row, max_row = min(rows), max(rows)
        
        origin_rows = list(range(min_col + by, max_col - by + 1))
        origin_cols = list(range(min_row + by, max_row - by + 1))

        shrinked_grid = [position for position in product(origin_rows,
                                                          origin_cols)]
        return shrinked_grid

    def create_spot(self, origin, size, include_origin=False):
        origin_row, origin_col = origin
        grid_cols = list(range(origin_col - size // 2,
                               origin_col + size // 2 + 1))
        grid_rows = list(range(origin_row - size // 2,
                               origin_row + size // 2 + 1))

        spot = list(product(grid_rows, grid_cols))
        if not include_origin:
            spot = [p for p in spot if p != origin]
        return spot


class SpatialShortTermMemoryTask(GenericTask):
    def __init__(self, window, seed, experiment_data, config):
        super().__init__()
        random.seed(seed)
        self.name = 'SSTM'
        
        self.config = config

        self.grid = SpatialShortTermMemoryGrid(
            window=window,
            n_rows=config['grid']['n_rows'],
            n_cols=config['grid']['n_cols'],
            grid_height=config['grid']['height'],
            grid_width=config['grid']['width'],
            line_width=config['grid']['line_width'])

        self.date_format = config['date_format']
        
        self.init_trials(config)
        self.scorer = SpatialShortTermMemoryScorer(self.trials, experiment_data)

    def init_trials(self, config):
        trial_factory = SpatialShortTermMemoryTrialFactory(
            grid=self.grid,
            padding=config['sequences']['padding'],
            dot_size=config['dots']['size'])

        practice_dot_sequences = config['practice']
        self.practice_trials = [
            SpatialShortTermMemoryTrial(
                sequence=dot_sequence,
                grid=self.grid,
                dot_size=config['dots']['size'])
            for dot_sequence in practice_dot_sequences]

        self.trials = trial_factory.generate(
            n_dots_list=config['trials']['n_dots_list'],
            n_far=config['trials']['n_far'],
            n_near=config['trials']['n_near'])

    def show(self, show=True):
        self.grid.show(show)

        if self.current_trial is not None:
            self.current_trial.show(show)

    def write_results(self, filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        self.scorer.compute_scores()

        self.scorer.trial_scores['Score'] = pd.to_numeric(
            self.scorer.trial_scores['Score'], downcast='integer')
        self.scorer.trial_scores['NumDot'] = pd.to_numeric(
            self.scorer.trial_scores['NumDot'], downcast='integer')

        with open(filepath, 'w') as f:
            f.write(f'{self.scorer.date} Spatual Short-Term Memory Task data\n')

        self.scorer.trial_scores.to_csv(filepath, mode='a', sep=' ',
                                        float_format='%.3f')
        
        with open(filepath, 'a') as f:
            f.write('\n')
            f.write('------------------------------------------\n')
            f.write('\n')

        self.scorer.dot_scores.to_csv(filepath, mode='a', sep=' ')

    def write_overall_results(self, filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        max_possible_score = sum([len(trial.sequence)*2-2
                                  for trial in self.trials])

        with open(filepath, 'a') as f:
            f.write(f'SubID Score Date Time {max_possible_score}\n')
            f.write(f'{self.scorer.subject_id} '
                    f'{self.scorer.trial_scores.Score.sum()} '
                    f'{self.scorer.date.strftime(self.date_format)}\n')
