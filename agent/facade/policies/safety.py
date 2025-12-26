import re
from typing import Optional, Callable, List

class InputGuardrail:
    def __init__(self):
        self.max_length_input = 1000
        self._pipeline: List[Callable[[str], Optional[str]]] = [
            self.check_policy_violation,
            self.check_prompt_injection,
            self.check_prompt_too_long,
        ]

    def __call__(self, texto: str) -> Optional[str]:
        result = texto
        for check in self._pipeline:
            result, obs = check(result)
            if result is not None:
                break
        return result, obs

    @staticmethod
    def check_policy_violation(text: str) -> Optional[str]:
        forbidden = ["hack","violencia"]
        if any(word in text.lower() for word in forbidden):
            return None,"policy-violation"
        return text, None

    @staticmethod
    def check_prompt_injection(text: str) -> Optional[str]:
        _INJECTION_PATTERNS = [
            r"ignore\s+all\s+previous\s+instructions",
            r"ignore\s+the\s+above",
            r"forget\s+the\s+system\s+prompt",
            r"disregard\s+previous",
            r"act\s+as\s+.*",
            r"you\s+are\s+now\s+.*",
            r"reveal\s+the\s+system\s+prompt",
            r"show\s+your\s+instructions",
            r"jailbreak",
            r"bypass",
            r"override",
            r"execute\s+code",
            r"system\s*:",
            r"assistant\s*:",
            r"developer\s*:",
            r"agora\s+você\s+é\s+.*",
            r"ignore\s+todas\s+as\s+instruções\s+anteriores"
        ]
        text = text.lower()
        for pattern in _INJECTION_PATTERNS:
            if re.search(pattern, text):
                return None, "prompt-injection"
        return text, None
    
    def check_prompt_too_long(self, text: str) -> Optional[str]:
        if len(text)>self.max_length_input:
            return text[:self.max_length_input], "prompt-too-long"
        return text, None

class InnerGuardrail:
    pass

class OutputGuardrail:
    @staticmethod
    def clean_llm_output(text: str) -> str:
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        text = re.sub(r"</?think>", "", text)
        return text.strip()