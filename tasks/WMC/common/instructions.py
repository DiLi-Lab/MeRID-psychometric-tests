import yaml

class Instructions:
    def __init__(self, language):

        path_pattern = f'languages/{language}/WMC/' + '{}'
        filepath = f'languages/{language}/WMC/instructions_{language.lower()}.yaml'

        with open(filepath, 'r') as stream:
            instructions = yaml.safe_load(stream)
        
        for key in instructions.keys():
            instructions[key] = list(map(path_pattern.format,
                                         instructions[key]))
        self.instructions = instructions

    def get_instructions(self, task):
        return self.instructions[task]

    def get_instruction_page_count(self, task):
        return len(self.instructions[task])
