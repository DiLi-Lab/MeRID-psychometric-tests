from dotmap import DotMap
import yaml

class WMCConfig:
    def __init__(
            self, language,
            common_config_path='tasks/WMC/config/common.yaml',
            memory_update_config_path='tasks/WMC/config/memory_update.yaml',
            operation_span_config_path='tasks/WMC/config/operation_span.yaml',
            sentence_span_config_path='tasks/WMC/config/sentence_span.yaml',
            spatial_short_term_memory_config_path='tasks/WMC/config/spatial_short_term_memory.yaml',
            language_config_path_pattern='languages/{language}/WMC/config.yaml',
            # common_config_path='config/common.yaml',
            # memory_update_config_path='config/memory_update.yaml',
            # operation_span_config_path='config/operation_span.yaml',
            # sentence_span_config_path='config/sentence_span.yaml',
            # spatial_short_term_memory_config_path='config/spatial_short_term_memory.yaml',
            # language_config_path_pattern='../../languages/{language}/WMC/config.yaml',
    ):
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
        with open(filepath, 'r') as stream:
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
