import logging
from typing import Any, Dict, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import (
    BaseChatModel,
)
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.pydantic_v1 import Field, SecretStr
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion, ChatCompletionMessage


logger = logging.getLogger(__name__)


def _convert_message_to_dict(message: BaseMessage) -> dict:
    message_dict: Dict[str, Any]
    if isinstance(message, ChatMessage):
        message_dict = {"role": message.role, "content": message.content}
    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        message_dict = {"role": "assistant", "content": message.content}
    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}
    else:
        raise TypeError(f"Got unknown type {message}")

    return message_dict


def _create_chat_result(response: ChatCompletion) -> ChatResult:
    generations = []
    for choice in response.choices:
        message = _convert_openai_response_to_message(choice.message)
        generations.append(ChatGeneration(message=message))

    token_usage = response.usage
    llm_output = {"token_usage": token_usage}
    return ChatResult(generations=generations, llm_output=llm_output)


def _convert_openai_response_to_message(
    _response: ChatCompletionMessage,
) -> BaseMessage:
    role = _response.role
    if role == "user":
        return HumanMessage(content=_response.content)
    elif role == "assistant":
        return AIMessage(content=_response.content or "")
    else:
        return ChatMessage(content=_response.content, role=role)


DEFAULT_API_BASE = "https://api.moonshot.cn/v1"


class ChatMoonshot(BaseChatModel):
    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {
            # "moonshot_api_key": "MOONSHOT_API_KEY",
            "moonshot_api_key": "sk-yrU5C6KyXyqXuII5vHy5tVrYPjUUCNg0iFOQWOASldwm8hoX",
        }

    @property
    def lc_serializable(self) -> bool:
        return True

    moonshot_api_base: str = Field(default=DEFAULT_API_BASE)
    """Moonshot custom endpoints"""

    moonshot_api_key: Optional[SecretStr] = None
    """Moonshot Api Key"""

    moonshot_model_name: str = "moonshot-v1-32k"
    """Moonshot Model Name"""

    temperature: float = 1.0
    """What sampling temperature to use."""

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.moonshot_api_key is None:
            raise ValueError("Moonshot secret key is not set.")

        client = OpenAI(
            api_key=self.moonshot_api_key.get_secret_value(),
            base_url=self.moonshot_api_base,
        )

        moonshot_messages = [_convert_message_to_dict(m) for m in messages]

        completion = client.chat.completions.create(
            model=self.moonshot_model_name,
            messages=moonshot_messages,
            temperature=self.temperature,
        )

        return _create_chat_result(completion)

    @property
    def _llm_type(self) -> str:
        return "moonshot-chat"
