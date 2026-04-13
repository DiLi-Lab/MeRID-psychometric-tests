"""
WMC configuration module.

Based on the original python-wmc-battery: https://github.com/aeye-lab/python-wmc-battery
Original License: MIT (see LICENSE file)

Copyright (C) 2024-2026 MultiplEYE Project
"""

import yaml
from dotmap import DotMap
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class WMCConfig:
    def __init__(
            self, language,
            common_config_path=None,
            memory_update_config_path=None,
            operation_span_config_path=None,
            sentence_span_config_path=None,
            spatial_short_term_memory_config_path=None,
            language_config_path_pattern=None,
            # common_config_path='config/common.yaml',
            # memory_update_config_path='config/memory_update.yaml',
            # operation_span_config_path='config/operation_span.yaml',
            # sentence_span_config_path='config/sentence_span.yaml',
            # spatial_short_term_memory_config_path='config/spatial_short_term_memory.yaml',
            # language_config_path_pattern='../../languages/{language}/WMC/config.yaml',
    ):
        common_config_path = common_config_path or (PROJECT_ROOT / 'tasks' / 'WMC' / 'config' / 'common.yaml')
        memory_update_config_path = memory_update_config_path or (PROJECT_ROOT / 'tasks' / 'WMC' / 'config' / 'memory_update.yaml')
        operation_span_config_path = operation_span_config_path or (PROJECT_ROOT / 'tasks' / 'WMC' / 'config' / 'operation_span.yaml')
        sentence_span_config_path = sentence_span_config_path or (PROJECT_ROOT / 'tasks' / 'WMC' / 'config' / 'sentence_span.yaml')
        spatial_short_term_memory_config_path = spatial_short_term_memory_config_path or (
            PROJECT_ROOT / 'tasks' / 'WMC' / 'config' / 'spatial_short_term_memory.yaml'
        )
        language_config_path_pattern = language_config_path_pattern or str(
            PROJECT_ROOT / 'languages' / '{language}' / 'WMC' / 'config.yaml'
        )

        self.common = WMCConfig.load_config(common_config_path)
        self.memory_update = WMCConfig.load_config(
            memory_update_config_path)
        self.operation_span = WMCConfig.load_config(
            operation_span_config_path)
        self.sentence_span = WMCConfig.load_config(
            sentence_span_config_path)
        self.spatial_short_term_memory = WMCConfig.load_config(
            spatial_short_term_memory_config_path)

        language_config_path = language_config_path_pattern.format(
            language=language)
        language_config = WMCConfig.load_config(language_config_path)

        self.experiment_messages = language_config.experiment_messages
        self.merge_language_config(language_config)

    @staticmethod
    def load_config(filepath):
        with Path(filepath).open('r') as stream:
            return DotMap(yaml.safe_load(stream))

    def merge_language_config(self, language_config):
        if 'memory_update' in language_config.keys():
            self.merge_dict(self.memory_update,
                            language_config.memory_update)
        if 'operation_span' in language_config.keys():
            self.merge_dict(self.operation_span,
                            language_config.operation_span)
        if 'sentence_span' in language_config.keys():
            self.merge_dict(self.sentence_span,
                            language_config.sentence_span)
        if 'spatial_short_term_memory' in language_config.keys():
            self.merge_dict(self.spatial_short_term_memory,
                            language_config.spatial_short_term_memory)

    def merge_dict(self, base_dict, new_dict):
        for key in new_dict.keys():
            if hasattr(new_dict[key], 'keys'):
                self.merge_dict(base_dict[key], new_dict[key])
            else:
                base_dict[key] = new_dict[key]
