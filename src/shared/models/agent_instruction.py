from abc import ABC


class AgentInstruction(ABC):
    """Base class to handle and construct agent instructions."""

    def __init__(self, system_instruction: str):
        self.system_instruction = system_instruction

    def __str__(self):
        return self.system_instruction


class AgentFewShotInstruction(AgentInstruction):
    """
    Class to handle few-shot learning instructions for agents.
    **Few Shot Prompt Structure:**
    ------------------------
    {Base Instruction}

    Examples:
    Input: {Example Input 1}
    Output: {Example Output 1}

    Input: {Example Input 2}
    Output: {Example Output 2}

    ... etc.
    """

    def __init__(self, system_instruction: str, examples: list[tuple[str, str]]):
        super().__init__(system_instruction)
        # self.system_instruction = system_instruction
        self.examples = examples

    def __str__(self):
        out = self.system_instruction
        out += "\n\nExamples:\n"
        out += "\n\n".join(
            f"Input: {input}\nOutput: {output}" for input, output in self.examples
        )
        return out
