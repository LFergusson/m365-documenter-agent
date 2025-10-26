from abc import ABC


class AgentInstruction(ABC):
    """Base class to handle and construct agent instructions."""

    def __init__(self, base_instruction: str):
        self.base_instruction = base_instruction

    def __str__(self):
        return self.base_instruction


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

    def __init__(self, base_instruction: str, examples: list[tuple[str, str]]):
        super().__init__(base_instruction)
        self.examples = examples

    def __str__(self):

        out = self.base_instruction
        out += "\n\nExamples:\n"
        out += "\n\n".join(
            f"Input: {input}\nOutput: {output}" for input, output in self.examples
        )
        return out
