import yaml
from pathlib import Path


class Instructions:
    def __init__(self, language):
        project_root = Path(__file__).resolve().parents[3]
        base_path = project_root / 'languages' / language / 'WMC'
        filepath = base_path / f'instructions_{language.lower()}.yaml'

        with filepath.open('r') as stream:
            instructions = yaml.safe_load(stream)

        for key in instructions.keys():
            instructions[key] = [str(base_path / item) for item in instructions[key]]
        self.instructions = instructions

    def get_instructions(self, task):
        return self.instructions[task]

    def get_instruction_page_count(self, task):
        return len(self.instructions[task])
