import yaml
from dotmap import DotMap
from pathlib import Path


class ExperimentMessages(DotMap):
    def __init__(self, language, encoding):
        project_root = Path(__file__).resolve().parents[3]
        filepath = project_root / 'languages' / language / 'WMC' / f'experiment_messages_{language.lower()}.yaml'
        with filepath.open(mode='r', encoding=encoding) as stream:
            super().__init__(yaml.safe_load(stream))
