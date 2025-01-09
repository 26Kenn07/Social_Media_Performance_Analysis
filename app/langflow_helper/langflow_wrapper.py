import os
import json
from dotenv import load_dotenv
from astrapy import DataAPIClient
from astrapy.collection import Collection
from langflow.load import run_flow_from_json

load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')
TOKEN = os.getenv('TOKEN')
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

PROMPT = """
<DATA>
{context}
</Data>

<Post Type>
{question}
</Post Type>


Analyze the provided social media data to extract actionable insights based on the following criteria:
   - Evaluate which content type (posts, reels, stories) receives the highest engagement in terms of likes, comments, and shares.
   - Assess the performance impact of post type (e.g., image vs. carousel) on engagement metrics.
   - Determine which post typre generate the most engagement and interactions.
   - Analyze engagement patterns across different content formats: static images, carousels, and Reels.
   - Identify which type of content leads to traffic or engagements, focusing on likes, comments on post.
   - Detect posts or reels with significantly high or low engagement, exploring possible reasons for these anomalies.
 
*Expected Output:*
Provide a detailed textual analysis categorized under each point above. Include percentages, comparisons, and trends to ensure insights are actionable. No calculations or coding or explanation required; solely rely on data for insights.
"""

FLOW = {
  "id": "100d6a1e-60d1-4161-a5fe-097b8351aa0b",
  "data": {
    "nodes": [
      {
        "data": {
          "description": "Get chat inputs from the Playground.",
          "display_name": "Chat Input",
          "id": "ChatInput-3woz5",
          "node": {
            "base_classes": [
              "Message"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Get chat inputs from the Playground.",
            "display_name": "Chat Input",
            "documentation": "",
            "edited": False,
            "field_order": [
              "input_value",
              "should_store_message",
              "sender",
              "sender_name",
              "session_id",
              "files"
            ],
            "frozen": False,
            "icon": "MessagesSquare",
            "legacy": False,
            "lf_version": "1.1.1",
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Message",
                "method": "message_response",
                "name": "message",
                "selected": "Message",
                "types": [
                  "Message"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "background_color": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Background Color",
                "dynamic": False,
                "info": "The background color of the icon.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "background_color",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "chat_icon": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Icon",
                "dynamic": False,
                "info": "The icon of the message.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "chat_icon",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "from langflow.base.data.utils import IMG_FILE_TYPES, TEXT_FILE_TYPES\nfrom langflow.base.io.chat import ChatComponent\nfrom langflow.inputs import BoolInput\nfrom langflow.io import DropdownInput, FileInput, MessageTextInput, MultilineInput, Output\nfrom langflow.schema.message import Message\nfrom langflow.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_USER, MESSAGE_SENDER_USER\n\n\nclass ChatInput(ChatComponent):\n    display_name = \"Chat Input\"\n    description = \"Get chat inputs from the Playground.\"\n    icon = \"MessagesSquare\"\n    name = \"ChatInput\"\n\n    inputs = [\n        MultilineInput(\n            name=\"input_value\",\n            display_name=\"Text\",\n            value=\"\",\n            info=\"Message to be passed as input.\",\n        ),\n        BoolInput(\n            name=\"should_store_message\",\n            display_name=\"Store Messages\",\n            info=\"Store the message in the history.\",\n            value=True,\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"sender\",\n            display_name=\"Sender Type\",\n            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],\n            value=MESSAGE_SENDER_USER,\n            info=\"Type of sender.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"sender_name\",\n            display_name=\"Sender Name\",\n            info=\"Name of the sender.\",\n            value=MESSAGE_SENDER_NAME_USER,\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"session_id\",\n            display_name=\"Session ID\",\n            info=\"The session ID of the chat. If empty, the current session ID parameter will be used.\",\n            advanced=True,\n        ),\n        FileInput(\n            name=\"files\",\n            display_name=\"Files\",\n            file_types=TEXT_FILE_TYPES + IMG_FILE_TYPES,\n            info=\"Files to be sent with the message.\",\n            advanced=True,\n            is_list=True,\n        ),\n        MessageTextInput(\n            name=\"background_color\",\n            display_name=\"Background Color\",\n            info=\"The background color of the icon.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"chat_icon\",\n            display_name=\"Icon\",\n            info=\"The icon of the message.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"text_color\",\n            display_name=\"Text Color\",\n            info=\"The text color of the name\",\n            advanced=True,\n        ),\n    ]\n    outputs = [\n        Output(display_name=\"Message\", name=\"message\", method=\"message_response\"),\n    ]\n\n    def message_response(self) -> Message:\n        _background_color = self.background_color\n        _text_color = self.text_color\n        _icon = self.chat_icon\n        message = Message(\n            text=self.input_value,\n            sender=self.sender,\n            sender_name=self.sender_name,\n            session_id=self.session_id,\n            files=self.files,\n            properties={\"background_color\": _background_color, \"text_color\": _text_color, \"icon\": _icon},\n        )\n        if self.session_id and isinstance(message, Message) and self.should_store_message:\n            stored_message = self.send_message(\n                message,\n            )\n            self.message.value = stored_message\n            message = stored_message\n\n        self.status = message\n        return message\n"
              },
              "files": {
                "advanced": True,
                "display_name": "Files",
                "dynamic": False,
                "fileTypes": [
                  "txt",
                  "md",
                  "mdx",
                  "csv",
                  "json",
                  "yaml",
                  "yml",
                  "xml",
                  "html",
                  "htm",
                  "pdf",
                  "docx",
                  "py",
                  "sh",
                  "sql",
                  "js",
                  "ts",
                  "tsx",
                  "jpg",
                  "jpeg",
                  "png",
                  "bmp",
                  "image"
                ],
                "file_path": "",
                "info": "Files to be sent with the message.",
                "list": True,
                "name": "files",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "file",
                "value": ""
              },
              "input_value": {
                "advanced": False,
                "display_name": "Text",
                "dynamic": False,
                "info": "Message to be passed as input.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "input_value",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": "carousel"
              },
              "sender": {
                "advanced": True,
                "display_name": "Sender Type",
                "dynamic": False,
                "info": "Type of sender.",
                "name": "sender",
                "options": [
                  "Machine",
                  "User"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "User"
              },
              "sender_name": {
                "advanced": True,
                "display_name": "Sender Name",
                "dynamic": False,
                "info": "Name of the sender.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "sender_name",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": "User"
              },
              "session_id": {
                "advanced": True,
                "display_name": "Session ID",
                "dynamic": False,
                "info": "The session ID of the chat. If empty, the current session ID parameter will be used.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "session_id",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "should_store_message": {
                "advanced": True,
                "display_name": "Store Messages",
                "dynamic": False,
                "info": "Store the message in the history.",
                "list": False,
                "name": "should_store_message",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "bool",
                "value": True
              },
              "text_color": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Text Color",
                "dynamic": False,
                "info": "The text color of the name",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "text_color",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              }
            }
          },
          "type": "ChatInput"
        },
        "dragging": False,
        "height": 234,
        "id": "ChatInput-3woz5",
        "position": {
          "x": 743.9745420290319,
          "y": 463.6977510207854
        },
        "positionAbsolute": {
          "x": 743.9745420290319,
          "y": 463.6977510207854
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "description": "Convert Data into plain text following a specified template.",
          "display_name": "Parse Data",
          "id": "ParseData-5AalP",
          "node": {
            "base_classes": [
              "Message"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Convert Data into plain text following a specified template.",
            "display_name": "Parse Data",
            "documentation": "",
            "edited": False,
            "field_order": [
              "data",
              "template",
              "sep"
            ],
            "frozen": False,
            "icon": "braces",
            "legacy": False,
            "lf_version": "1.1.1",
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Text",
                "method": "parse_data",
                "name": "text",
                "selected": "Message",
                "types": [
                  "Message"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "from langflow.custom import Component\nfrom langflow.helpers.data import data_to_text\nfrom langflow.io import DataInput, MultilineInput, Output, StrInput\nfrom langflow.schema.message import Message\n\n\nclass ParseDataComponent(Component):\n    display_name = \"Parse Data\"\n    description = \"Convert Data into plain text following a specified template.\"\n    icon = \"braces\"\n    name = \"ParseData\"\n\n    inputs = [\n        DataInput(name=\"data\", display_name=\"Data\", info=\"The data to convert to text.\"),\n        MultilineInput(\n            name=\"template\",\n            display_name=\"Template\",\n            info=\"The template to use for formatting the data. \"\n            \"It can contain the keys {text}, {data} or any other key in the Data.\",\n            value=\"{text}\",\n        ),\n        StrInput(name=\"sep\", display_name=\"Separator\", advanced=True, value=\"\\n\"),\n    ]\n\n    outputs = [\n        Output(display_name=\"Text\", name=\"text\", method=\"parse_data\"),\n    ]\n\n    def parse_data(self) -> Message:\n        data = self.data if isinstance(self.data, list) else [self.data]\n        template = self.template\n\n        result_string = data_to_text(template, data, sep=self.sep)\n        self.status = result_string\n        return Message(text=result_string)\n"
              },
              "data": {
                "advanced": False,
                "display_name": "Data",
                "dynamic": False,
                "info": "The data to convert to text.",
                "input_types": [
                  "Data"
                ],
                "list": False,
                "name": "data",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "other",
                "value": ""
              },
              "sep": {
                "advanced": True,
                "display_name": "Separator",
                "dynamic": False,
                "info": "",
                "list": False,
                "load_from_db": False,
                "name": "sep",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "\n"
              },
              "template": {
                "advanced": False,
                "display_name": "Template",
                "dynamic": False,
                "info": "The template to use for formatting the data. It can contain the keys {text}, {data} or any other key in the Data.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "template",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": "{text}"
              }
            }
          },
          "type": "ParseData"
        },
        "dragging": False,
        "height": 302,
        "id": "ParseData-5AalP",
        "position": {
          "x": 1606.0595305373527,
          "y": 751.4473696960695
        },
        "positionAbsolute": {
          "x": 1606.0595305373527,
          "y": 751.4473696960695
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "description": "Create a prompt template with dynamic variables.",
          "display_name": "Prompt",
          "id": "Prompt-nAHMf",
          "node": {
            "template": {
              "_type": "Component",
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "from langflow.base.prompts.api_utils import process_prompt_template\nfrom langflow.custom import Component\nfrom langflow.inputs.inputs import DefaultPromptField\nfrom langflow.io import Output, PromptInput\nfrom langflow.schema.message import Message\nfrom langflow.template.utils import update_template_values\n\n\nclass PromptComponent(Component):\n    display_name: str = \"Prompt\"\n    description: str = \"Create a prompt template with dynamic variables.\"\n    icon = \"prompts\"\n    trace_type = \"prompt\"\n    name = \"Prompt\"\n\n    inputs = [\n        PromptInput(name=\"template\", display_name=\"Template\"),\n    ]\n\n    outputs = [\n        Output(display_name=\"Prompt Message\", name=\"prompt\", method=\"build_prompt\"),\n    ]\n\n    async def build_prompt(self) -> Message:\n        prompt = Message.from_template(**self._attributes)\n        self.status = prompt.text\n        return prompt\n\n    def _update_template(self, frontend_node: dict):\n        prompt_template = frontend_node[\"template\"][\"template\"][\"value\"]\n        custom_fields = frontend_node[\"custom_fields\"]\n        frontend_node_template = frontend_node[\"template\"]\n        _ = process_prompt_template(\n            template=prompt_template,\n            name=\"template\",\n            custom_fields=custom_fields,\n            frontend_node_template=frontend_node_template,\n        )\n        return frontend_node\n\n    def post_code_processing(self, new_frontend_node: dict, current_frontend_node: dict):\n        \"\"\"This function is called after the code validation is done.\"\"\"\n        frontend_node = super().post_code_processing(new_frontend_node, current_frontend_node)\n        template = frontend_node[\"template\"][\"template\"][\"value\"]\n        # Kept it duplicated for backwards compatibility\n        _ = process_prompt_template(\n            template=template,\n            name=\"template\",\n            custom_fields=frontend_node[\"custom_fields\"],\n            frontend_node_template=frontend_node[\"template\"],\n        )\n        # Now that template is updated, we need to grab any values that were set in the current_frontend_node\n        # and update the frontend_node with those values\n        update_template_values(new_template=frontend_node, previous_template=current_frontend_node[\"template\"])\n        return frontend_node\n\n    def _get_fallback_input(self, **kwargs):\n        return DefaultPromptField(**kwargs)\n"
              },
              "context": {
                "field_type": "str",
                "required": False,
                "placeholder": "",
                "list": False,
                "show": True,
                "multiline": True,
                "value": "",
                "fileTypes": [],
                "file_path": "",
                "name": "context",
                "display_name": "context",
                "advanced": False,
                "input_types": [
                  "Message",
                  "Text"
                ],
                "dynamic": False,
                "info": "",
                "load_from_db": False,
                "title_case": False,
                "type": "str"
              },
              "question": {
                "field_type": "str",
                "required": False,
                "placeholder": "",
                "list": False,
                "show": True,
                "multiline": True,
                "value": "",
                "fileTypes": [],
                "file_path": "",
                "name": "question",
                "display_name": "question",
                "advanced": False,
                "input_types": [
                  "Message",
                  "Text"
                ],
                "dynamic": False,
                "info": "",
                "load_from_db": False,
                "title_case": False,
                "type": "str"
              },
              "template": {
                "advanced": False,
                "display_name": "Template",
                "dynamic": False,
                "info": "",
                "list": False,
                "load_from_db": False,
                "name": "template",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "type": "prompt",
                "value": "{context}\n\n---\n\nAccepts post types (e.g., carousel, reels, static images) as input.\n\nQueries the dataset in Astra DB to calculate average engagement metrics for each\npost type.\n\nExample outputs:\n● Carousel posts have 20% higher engagement than static posts.\n● Reels drive 2x more comments compared to other formats.\n\nQuestion: {question}\n\nAnswer: "
              }
            },
            "description": "Create a prompt template with dynamic variables.",
            "icon": "prompts",
            "is_input": None,
            "is_output": None,
            "is_composition": None,
            "base_classes": [
              "Message"
            ],
            "name": "",
            "display_name": "Prompt",
            "documentation": "",
            "custom_fields": {
              "template": [
                "context",
                "question"
              ]
            },
            "output_types": [],
            "full_path": None,
            "pinned": False,
            "conditional_paths": [],
            "frozen": False,
            "outputs": [
              {
                "types": [
                  "Message"
                ],
                "selected": "Message",
                "name": "prompt",
                "hidden": None,
                "display_name": "Prompt Message",
                "method": "build_prompt",
                "value": "__UNDEFINED__",
                "cache": True,
                "required_inputs": None
              }
            ],
            "field_order": [
              "template"
            ],
            "beta": False,
            "legacy": False,
            "error": None,
            "edited": False,
            "metadata": {},
            "tool_mode": False
          },
          "type": "Prompt"
        },
        "dragging": False,
        "height": 427,
        "id": "Prompt-nAHMf",
        "position": {
          "x": 1977.9097981422992,
          "y": 640.5656416923846
        },
        "positionAbsolute": {
          "x": 1977.9097981422992,
          "y": 640.5656416923846
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "description": "Split text into chunks based on specified criteria.",
          "display_name": "Split Text",
          "id": "SplitText-RuKuP",
          "node": {
            "base_classes": [
              "Data"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Split text into chunks based on specified criteria.",
            "display_name": "Split Text",
            "documentation": "",
            "edited": False,
            "field_order": [
              "data_inputs",
              "chunk_overlap",
              "chunk_size",
              "separator"
            ],
            "frozen": False,
            "icon": "scissors-line-dashed",
            "legacy": False,
            "lf_version": "1.1.1",
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Chunks",
                "method": "split_text",
                "name": "chunks",
                "selected": "Data",
                "types": [
                  "Data"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "chunk_overlap": {
                "advanced": False,
                "display_name": "Chunk Overlap",
                "dynamic": False,
                "info": "Number of characters to overlap between chunks.",
                "list": False,
                "name": "chunk_overlap",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": 200
              },
              "chunk_size": {
                "advanced": False,
                "display_name": "Chunk Size",
                "dynamic": False,
                "info": "The maximum number of characters in each chunk.",
                "list": False,
                "name": "chunk_size",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": 1000
              },
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "from langchain_text_splitters import CharacterTextSplitter\n\nfrom langflow.custom import Component\nfrom langflow.io import HandleInput, IntInput, MessageTextInput, Output\nfrom langflow.schema import Data\nfrom langflow.utils.util import unescape_string\n\n\nclass SplitTextComponent(Component):\n    display_name: str = \"Split Text\"\n    description: str = \"Split text into chunks based on specified criteria.\"\n    icon = \"scissors-line-dashed\"\n    name = \"SplitText\"\n\n    inputs = [\n        HandleInput(\n            name=\"data_inputs\",\n            display_name=\"Data Inputs\",\n            info=\"The data to split.\",\n            input_types=[\"Data\"],\n            is_list=True,\n        ),\n        IntInput(\n            name=\"chunk_overlap\",\n            display_name=\"Chunk Overlap\",\n            info=\"Number of characters to overlap between chunks.\",\n            value=200,\n        ),\n        IntInput(\n            name=\"chunk_size\",\n            display_name=\"Chunk Size\",\n            info=\"The maximum number of characters in each chunk.\",\n            value=1000,\n        ),\n        MessageTextInput(\n            name=\"separator\",\n            display_name=\"Separator\",\n            info=\"The character to split on. Defaults to newline.\",\n            value=\"\\n\",\n        ),\n    ]\n\n    outputs = [\n        Output(display_name=\"Chunks\", name=\"chunks\", method=\"split_text\"),\n    ]\n\n    def _docs_to_data(self, docs):\n        return [Data(text=doc.page_content, data=doc.metadata) for doc in docs]\n\n    def split_text(self) -> list[Data]:\n        separator = unescape_string(self.separator)\n\n        documents = [_input.to_lc_document() for _input in self.data_inputs if isinstance(_input, Data)]\n\n        splitter = CharacterTextSplitter(\n            chunk_overlap=self.chunk_overlap,\n            chunk_size=self.chunk_size,\n            separator=separator,\n        )\n        docs = splitter.split_documents(documents)\n        data = self._docs_to_data(docs)\n        self.status = data\n        return data\n"
              },
              "data_inputs": {
                "advanced": False,
                "display_name": "Data Inputs",
                "dynamic": False,
                "info": "The data to split.",
                "input_types": [
                  "Data"
                ],
                "list": True,
                "name": "data_inputs",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "other",
                "value": ""
              },
              "separator": {
                "advanced": False,
                "display_name": "Separator",
                "dynamic": False,
                "info": "The character to split on. Defaults to newline.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "separator",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              }
            }
          },
          "type": "SplitText"
        },
        "dragging": False,
        "height": 475,
        "id": "SplitText-RuKuP",
        "position": {
          "x": 1683.4543896546102,
          "y": 1350.7871623588553
        },
        "positionAbsolute": {
          "x": 1683.4543896546102,
          "y": 1350.7871623588553
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "id": "note-LDUgj",
          "node": {
            "description": "## 🐕 2. Retriever Flow\n\nThis flow answers your questions with contextual data retrieved from your vector database.\n\nOpen the **Playground** and ask, \n\n```\nWhat is this document about?\n```\n",
            "display_name": "",
            "documentation": "",
            "template": {
              "backgroundColor": "neutral"
            }
          },
          "type": "note"
        },
        "dragging": False,
        "height": 324,
        "id": "note-LDUgj",
        "position": {
          "x": 374.388314931542,
          "y": 486.18094072679895
        },
        "positionAbsolute": {
          "x": 374.388314931542,
          "y": 486.18094072679895
        },
        "resizing": False,
        "selected": False,
        "style": {
          "height": 324,
          "width": 324
        },
        "type": "noteNode",
        "width": 324
      },
      {
        "data": {
          "id": "note-tMOxa",
          "node": {
            "description": "## 📖 README\n\nLoad your data into a vector database with the 📚 **Load Data** flow, and then use your data as chat context with the 🐕 **Retriever** flow.\n\n**🚨 Add your OpenAI API key as a global variable to easily add it to all of the OpenAI components in this flow.** \n\n**Quick start**\n1. Run the 📚 **Load Data** flow.\n2. Run the 🐕 **Retriever** flow.\n\n**Next steps** \n\n- Experiment by changing the prompt and the loaded data to see how the bot's responses change. \n\nFor more info, see the [Langflow docs](https://docs.langflow.org/starter-projects-vector-store-rag).",
            "display_name": "Read Me",
            "documentation": "",
            "template": {
              "backgroundColor": "neutral"
            }
          },
          "type": "note"
        },
        "dragging": False,
        "id": "note-tMOxa",
        "position": {
          "x": 94.28986613312418,
          "y": 907.6428043837066
        },
        "positionAbsolute": {
          "x": 94.28986613312418,
          "y": 907.6428043837066
        },
        "resizing": False,
        "selected": False,
        "style": {
          "height": 527,
          "width": 600
        },
        "type": "noteNode",
        "width": 600,
        "height": 527
      },
      {
        "data": {
          "description": "Display a chat message in the Playground.",
          "display_name": "Chat Output",
          "id": "ChatOutput-V2YFg",
          "node": {
            "base_classes": [
              "Message"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Display a chat message in the Playground.",
            "display_name": "Chat Output",
            "documentation": "",
            "edited": False,
            "field_order": [
              "input_value",
              "should_store_message",
              "sender",
              "sender_name",
              "session_id",
              "data_template",
              "background_color",
              "chat_icon",
              "text_color"
            ],
            "frozen": False,
            "icon": "MessagesSquare",
            "legacy": False,
            "lf_version": "1.1.1",
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Message",
                "method": "message_response",
                "name": "message",
                "selected": "Message",
                "types": [
                  "Message"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "background_color": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Background Color",
                "dynamic": False,
                "info": "The background color of the icon.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "background_color",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "chat_icon": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Icon",
                "dynamic": False,
                "info": "The icon of the message.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "chat_icon",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "from langflow.base.io.chat import ChatComponent\nfrom langflow.inputs import BoolInput\nfrom langflow.io import DropdownInput, MessageInput, MessageTextInput, Output\nfrom langflow.schema.message import Message\nfrom langflow.schema.properties import Source\nfrom langflow.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_AI, MESSAGE_SENDER_USER\n\n\nclass ChatOutput(ChatComponent):\n    display_name = \"Chat Output\"\n    description = \"Display a chat message in the Playground.\"\n    icon = \"MessagesSquare\"\n    name = \"ChatOutput\"\n\n    inputs = [\n        MessageInput(\n            name=\"input_value\",\n            display_name=\"Text\",\n            info=\"Message to be passed as output.\",\n        ),\n        BoolInput(\n            name=\"should_store_message\",\n            display_name=\"Store Messages\",\n            info=\"Store the message in the history.\",\n            value=True,\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"sender\",\n            display_name=\"Sender Type\",\n            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],\n            value=MESSAGE_SENDER_AI,\n            advanced=True,\n            info=\"Type of sender.\",\n        ),\n        MessageTextInput(\n            name=\"sender_name\",\n            display_name=\"Sender Name\",\n            info=\"Name of the sender.\",\n            value=MESSAGE_SENDER_NAME_AI,\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"session_id\",\n            display_name=\"Session ID\",\n            info=\"The session ID of the chat. If empty, the current session ID parameter will be used.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"data_template\",\n            display_name=\"Data Template\",\n            value=\"{text}\",\n            advanced=True,\n            info=\"Template to convert Data to Text. If left empty, it will be dynamically set to the Data's text key.\",\n        ),\n        MessageTextInput(\n            name=\"background_color\",\n            display_name=\"Background Color\",\n            info=\"The background color of the icon.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"chat_icon\",\n            display_name=\"Icon\",\n            info=\"The icon of the message.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"text_color\",\n            display_name=\"Text Color\",\n            info=\"The text color of the name\",\n            advanced=True,\n        ),\n    ]\n    outputs = [\n        Output(\n            display_name=\"Message\",\n            name=\"message\",\n            method=\"message_response\",\n        ),\n    ]\n\n    def _build_source(self, _id: str | None, display_name: str | None, source: str | None) -> Source:\n        source_dict = {}\n        if _id:\n            source_dict[\"id\"] = _id\n        if display_name:\n            source_dict[\"display_name\"] = display_name\n        if source:\n            source_dict[\"source\"] = source\n        return Source(**source_dict)\n\n    def message_response(self) -> Message:\n        _source, _icon, _display_name, _source_id = self.get_properties_from_source_component()\n        _background_color = self.background_color\n        _text_color = self.text_color\n        if self.chat_icon:\n            _icon = self.chat_icon\n        message = self.input_value if isinstance(self.input_value, Message) else Message(text=self.input_value)\n        message.sender = self.sender\n        message.sender_name = self.sender_name\n        message.session_id = self.session_id\n        message.flow_id = self.graph.flow_id if hasattr(self, \"graph\") else None\n        message.properties.source = self._build_source(_source_id, _display_name, _source)\n        message.properties.icon = _icon\n        message.properties.background_color = _background_color\n        message.properties.text_color = _text_color\n        if self.session_id and isinstance(message, Message) and self.should_store_message:\n            stored_message = self.send_message(\n                message,\n            )\n            self.message.value = stored_message\n            message = stored_message\n\n        self.status = message\n        return message\n"
              },
              "data_template": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Data Template",
                "dynamic": False,
                "info": "Template to convert Data to Text. If left empty, it will be dynamically set to the Data's text key.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "data_template",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": "{text}"
              },
              "input_value": {
                "_input_type": "MessageInput",
                "advanced": False,
                "display_name": "Text",
                "dynamic": False,
                "info": "Message to be passed as output.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "input_value",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "sender": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Sender Type",
                "dynamic": False,
                "info": "Type of sender.",
                "name": "sender",
                "options": [
                  "Machine",
                  "User"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Machine"
              },
              "sender_name": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Sender Name",
                "dynamic": False,
                "info": "Name of the sender.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "sender_name",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": "AI"
              },
              "session_id": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Session ID",
                "dynamic": False,
                "info": "The session ID of the chat. If empty, the current session ID parameter will be used.",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "session_id",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "should_store_message": {
                "_input_type": "BoolInput",
                "advanced": True,
                "display_name": "Store Messages",
                "dynamic": False,
                "info": "Store the message in the history.",
                "list": False,
                "name": "should_store_message",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "bool",
                "value": True
              },
              "text_color": {
                "_input_type": "MessageTextInput",
                "advanced": True,
                "display_name": "Text Color",
                "dynamic": False,
                "info": "The text color of the name",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "name": "text_color",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              }
            },
            "tool_mode": False
          },
          "type": "ChatOutput"
        },
        "dragging": False,
        "height": 234,
        "id": "ChatOutput-V2YFg",
        "position": {
          "x": 2734.385670401691,
          "y": 808.2967893015561
        },
        "positionAbsolute": {
          "x": 2734.385670401691,
          "y": 808.2967893015561
        },
        "selected": True,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "id": "AstraDB-gHvII",
          "node": {
            "base_classes": [
              "Data",
              "Retriever"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Implementation of Vector Store using Astra DB with search capabilities",
            "display_name": "Astra DB",
            "documentation": "https://docs.langflow.org/starter-projects-vector-store-rag",
            "edited": False,
            "field_order": [
              "token",
              "api_endpoint",
              "collection_name",
              "search_input",
              "ingest_data",
              "namespace",
              "embedding_choice",
              "embedding_model",
              "metric",
              "batch_size",
              "bulk_insert_batch_concurrency",
              "bulk_insert_overwrite_concurrency",
              "bulk_delete_concurrency",
              "setup_mode",
              "pre_delete_collection",
              "metadata_indexing_include",
              "metadata_indexing_exclude",
              "collection_indexing_policy",
              "number_of_results",
              "search_type",
              "search_score_threshold",
              "search_filter"
            ],
            "frozen": False,
            "icon": "AstraDB",
            "legacy": False,
            "lf_version": "1.1.1",
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Retriever",
                "method": "build_base_retriever",
                "name": "base_retriever",
                "required_inputs": [],
                "selected": "Retriever",
                "types": [
                  "Retriever"
                ],
                "value": "__UNDEFINED__"
              },
              {
                "cache": True,
                "display_name": "Search Results",
                "method": "search_documents",
                "name": "search_results",
                "required_inputs": [
                  "api_endpoint",
                  "collection_name",
                  "token"
                ],
                "selected": "Data",
                "types": [
                  "Data"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "advanced_search_filter": {
                "_input_type": "NestedDictInput",
                "advanced": True,
                "display_name": "Search Metadata Filter",
                "dynamic": False,
                "info": "Optional dictionary of filters to apply to the search query.",
                "list": False,
                "name": "advanced_search_filter",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "NestedDict",
                "value": {}
              },
              "api_endpoint": {
                "_input_type": "SecretStrInput",
                "advanced": False,
                "display_name": "API Endpoint",
                "dynamic": False,
                "info": "API endpoint URL for the Astra DB service.",
                "input_types": [
                  "Message"
                ],
                "load_from_db": False,
                "name": "api_endpoint",
                "password": True,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "str",
                "value": API_ENDPOINT
              },
              "batch_size": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Batch Size",
                "dynamic": False,
                "info": "Optional number of data to process in a single batch.",
                "list": False,
                "name": "batch_size",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "bulk_delete_concurrency": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Bulk Delete Concurrency",
                "dynamic": False,
                "info": "Optional concurrency level for bulk delete operations.",
                "list": False,
                "name": "bulk_delete_concurrency",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "bulk_insert_batch_concurrency": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Bulk Insert Batch Concurrency",
                "dynamic": False,
                "info": "Optional concurrency level for bulk insert operations.",
                "list": False,
                "name": "bulk_insert_batch_concurrency",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "bulk_insert_overwrite_concurrency": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Bulk Insert Overwrite Concurrency",
                "dynamic": False,
                "info": "Optional concurrency level for bulk insert operations that overwrite existing data.",
                "list": False,
                "name": "bulk_insert_overwrite_concurrency",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "import os\nfrom collections import defaultdict\n\nimport orjson\nfrom astrapy import DataAPIClient\nfrom astrapy.admin import parse_api_endpoint\nfrom langchain_astradb import AstraDBVectorStore\n\nfrom langflow.base.vectorstores.model import LCVectorStoreComponent, check_cached_vector_store\nfrom langflow.helpers import docs_to_data\nfrom langflow.inputs import DictInput, FloatInput, MessageTextInput, NestedDictInput\nfrom langflow.io import (\n    BoolInput,\n    DataInput,\n    DropdownInput,\n    HandleInput,\n    IntInput,\n    MultilineInput,\n    SecretStrInput,\n    StrInput,\n)\nfrom langflow.schema import Data\n\n\nclass AstraVectorStoreComponent(LCVectorStoreComponent):\n    display_name: str = \"Astra DB\"\n    description: str = \"Implementation of Vector Store using Astra DB with search capabilities\"\n    documentation: str = \"https://docs.langflow.org/starter-projects-vector-store-rag\"\n    name = \"AstraDB\"\n    icon: str = \"AstraDB\"\n\n    _cached_vector_store: AstraDBVectorStore | None = None\n\n    VECTORIZE_PROVIDERS_MAPPING = defaultdict(\n        list,\n        {\n            \"Azure OpenAI\": [\n                \"azureOpenAI\",\n                [\"text-embedding-3-small\", \"text-embedding-3-large\", \"text-embedding-ada-002\"],\n            ],\n            \"Hugging Face - Dedicated\": [\"huggingfaceDedicated\", [\"endpoint-defined-model\"]],\n            \"Hugging Face - Serverless\": [\n                \"huggingface\",\n                [\n                    \"sentence-transformers/all-MiniLM-L6-v2\",\n                    \"intfloat/multilingual-e5-large\",\n                    \"intfloat/multilingual-e5-large-instruct\",\n                    \"BAAI/bge-small-en-v1.5\",\n                    \"BAAI/bge-base-en-v1.5\",\n                    \"BAAI/bge-large-en-v1.5\",\n                ],\n            ],\n            \"Jina AI\": [\n                \"jinaAI\",\n                [\n                    \"jina-embeddings-v2-base-en\",\n                    \"jina-embeddings-v2-base-de\",\n                    \"jina-embeddings-v2-base-es\",\n                    \"jina-embeddings-v2-base-code\",\n                    \"jina-embeddings-v2-base-zh\",\n                ],\n            ],\n            \"Mistral AI\": [\"mistral\", [\"mistral-embed\"]],\n            \"NVIDIA\": [\"nvidia\", [\"NV-Embed-QA\"]],\n            \"OpenAI\": [\"openai\", [\"text-embedding-3-small\", \"text-embedding-3-large\", \"text-embedding-ada-002\"]],\n            \"Upstage\": [\"upstageAI\", [\"solar-embedding-1-large\"]],\n            \"Voyage AI\": [\n                \"voyageAI\",\n                [\"voyage-large-2-instruct\", \"voyage-law-2\", \"voyage-code-2\", \"voyage-large-2\", \"voyage-2\"],\n            ],\n        },\n    )\n\n    inputs = [\n        SecretStrInput(\n            name=\"token\",\n            display_name=\"Astra DB Application Token\",\n            info=\"Authentication token for accessing Astra DB.\",\n            value=\"ASTRA_DB_APPLICATION_TOKEN\",\n            required=True,\n            advanced=os.getenv(\"ASTRA_ENHANCED\", \"False\").lower() == \"True\",\n        ),\n        SecretStrInput(\n            name=\"api_endpoint\",\n            display_name=\"Database\" if os.getenv(\"ASTRA_ENHANCED\", \"False\").lower() == \"True\" else \"API Endpoint\",\n            info=\"API endpoint URL for the Astra DB service.\",\n            value=\"ASTRA_DB_API_ENDPOINT\",\n            required=True,\n        ),\n        StrInput(\n            name=\"collection_name\",\n            display_name=\"Collection Name\",\n            info=\"The name of the collection within Astra DB where the vectors will be stored.\",\n            required=True,\n        ),\n        MultilineInput(\n            name=\"search_input\",\n            display_name=\"Search Input\",\n        ),\n        DataInput(\n            name=\"ingest_data\",\n            display_name=\"Ingest Data\",\n            is_list=True,\n        ),\n        StrInput(\n            name=\"keyspace\",\n            display_name=\"Keyspace\",\n            info=\"Optional keyspace within Astra DB to use for the collection.\",\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"embedding_choice\",\n            display_name=\"Embedding Model or Astra Vectorize\",\n            info=\"Determines whether to use Astra Vectorize for the collection.\",\n            options=[\"Embedding Model\", \"Astra Vectorize\"],\n            real_time_refresh=True,\n            value=\"Embedding Model\",\n        ),\n        HandleInput(\n            name=\"embedding_model\",\n            display_name=\"Embedding Model\",\n            input_types=[\"Embeddings\"],\n            info=\"Allows an embedding model configuration.\",\n        ),\n        DropdownInput(\n            name=\"metric\",\n            display_name=\"Metric\",\n            info=\"Optional distance metric for vector comparisons in the vector store.\",\n            options=[\"cosine\", \"dot_product\", \"euclidean\"],\n            value=\"cosine\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"batch_size\",\n            display_name=\"Batch Size\",\n            info=\"Optional number of data to process in a single batch.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"bulk_insert_batch_concurrency\",\n            display_name=\"Bulk Insert Batch Concurrency\",\n            info=\"Optional concurrency level for bulk insert operations.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"bulk_insert_overwrite_concurrency\",\n            display_name=\"Bulk Insert Overwrite Concurrency\",\n            info=\"Optional concurrency level for bulk insert operations that overwrite existing data.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"bulk_delete_concurrency\",\n            display_name=\"Bulk Delete Concurrency\",\n            info=\"Optional concurrency level for bulk delete operations.\",\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"setup_mode\",\n            display_name=\"Setup Mode\",\n            info=\"Configuration mode for setting up the vector store, with options like 'Sync' or 'Off'.\",\n            options=[\"Sync\", \"Off\"],\n            advanced=True,\n            value=\"Sync\",\n        ),\n        BoolInput(\n            name=\"pre_delete_collection\",\n            display_name=\"Pre Delete Collection\",\n            info=\"Boolean flag to determine whether to delete the collection before creating a new one.\",\n            advanced=True,\n        ),\n        StrInput(\n            name=\"metadata_indexing_include\",\n            display_name=\"Metadata Indexing Include\",\n            info=\"Optional list of metadata fields to include in the indexing.\",\n            is_list=True,\n            advanced=True,\n        ),\n        StrInput(\n            name=\"metadata_indexing_exclude\",\n            display_name=\"Metadata Indexing Exclude\",\n            info=\"Optional list of metadata fields to exclude from the indexing.\",\n            is_list=True,\n            advanced=True,\n        ),\n        StrInput(\n            name=\"collection_indexing_policy\",\n            display_name=\"Collection Indexing Policy\",\n            info='Optional JSON string for the \"indexing\" field of the collection. '\n            \"See https://docs.datastax.com/en/astra-db-serverless/api-reference/collections.html#the-indexing-option\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"number_of_results\",\n            display_name=\"Number of Results\",\n            info=\"Number of results to return.\",\n            advanced=True,\n            value=4,\n        ),\n        DropdownInput(\n            name=\"search_type\",\n            display_name=\"Search Type\",\n            info=\"Search type to use\",\n            options=[\"Similarity\", \"Similarity with score threshold\", \"MMR (Max Marginal Relevance)\"],\n            value=\"Similarity\",\n            advanced=True,\n        ),\n        FloatInput(\n            name=\"search_score_threshold\",\n            display_name=\"Search Score Threshold\",\n            info=\"Minimum similarity score threshold for search results. \"\n            \"(when using 'Similarity with score threshold')\",\n            value=0,\n            advanced=True,\n        ),\n        NestedDictInput(\n            name=\"advanced_search_filter\",\n            display_name=\"Search Metadata Filter\",\n            info=\"Optional dictionary of filters to apply to the search query.\",\n            advanced=True,\n        ),\n        DictInput(\n            name=\"search_filter\",\n            display_name=\"[DEPRECATED] Search Metadata Filter\",\n            info=\"Deprecated: use advanced_search_filter. Optional dictionary of filters to apply to the search query.\",\n            advanced=True,\n            is_list=True,\n        ),\n    ]\n\n    def del_fields(self, build_config, field_list):\n        for field in field_list:\n            if field in build_config:\n                del build_config[field]\n\n        return build_config\n\n    def insert_in_dict(self, build_config, field_name, new_parameters):\n        # Insert the new key-value pair after the found key\n        for new_field_name, new_parameter in new_parameters.items():\n            # Get all the items as a list of tuples (key, value)\n            items = list(build_config.items())\n\n            # Find the index of the key to insert after\n            idx = len(items)\n            for i, (key, _) in enumerate(items):\n                if key == field_name:\n                    idx = i + 1\n                    break\n\n            items.insert(idx, (new_field_name, new_parameter))\n\n            # Clear the original dictionary and update with the modified items\n            build_config.clear()\n            build_config.update(items)\n\n        return build_config\n\n    def update_providers_mapping(self):\n        # If we don't have token or api_endpoint, we can't fetch the list of providers\n        if not self.token or not self.api_endpoint:\n            self.log(\"Astra DB token and API endpoint are required to fetch the list of Vectorize providers.\")\n\n            return self.VECTORIZE_PROVIDERS_MAPPING\n\n        try:\n            self.log(\"Dynamically updating list of Vectorize providers.\")\n\n            # Get the admin object\n            client = DataAPIClient(token=self.token)\n            admin = client.get_admin()\n\n            # Get the embedding providers\n            db_admin = admin.get_database_admin(self.api_endpoint)\n            embedding_providers = db_admin.find_embedding_providers().as_dict()\n\n            vectorize_providers_mapping = {}\n\n            # Map the provider display name to the provider key and models\n            for provider_key, provider_data in embedding_providers[\"embeddingProviders\"].items():\n                display_name = provider_data[\"displayName\"]\n                models = [model[\"name\"] for model in provider_data[\"models\"]]\n\n                vectorize_providers_mapping[display_name] = [provider_key, models]\n\n            # Sort the resulting dictionary\n            return defaultdict(list, dict(sorted(vectorize_providers_mapping.items())))\n        except Exception as e:  # noqa: BLE001\n            self.log(f\"Error fetching Vectorize providers: {e}\")\n\n            return self.VECTORIZE_PROVIDERS_MAPPING\n\n    def update_build_config(self, build_config: dict, field_value: str, field_name: str | None = None):\n        if field_name == \"embedding_choice\":\n            if field_value == \"Astra Vectorize\":\n                self.del_fields(build_config, [\"embedding_model\"])\n\n                # Update the providers mapping\n                vectorize_providers = self.update_providers_mapping()\n\n                new_parameter = DropdownInput(\n                    name=\"embedding_provider\",\n                    display_name=\"Embedding Provider\",\n                    options=vectorize_providers.keys(),\n                    value=\"\",\n                    required=True,\n                    real_time_refresh=True,\n                ).to_dict()\n\n                self.insert_in_dict(build_config, \"embedding_choice\", {\"embedding_provider\": new_parameter})\n            else:\n                self.del_fields(\n                    build_config,\n                    [\n                        \"embedding_provider\",\n                        \"model\",\n                        \"z_01_model_parameters\",\n                        \"z_02_api_key_name\",\n                        \"z_03_provider_api_key\",\n                        \"z_04_authentication\",\n                    ],\n                )\n\n                new_parameter = HandleInput(\n                    name=\"embedding_model\",\n                    display_name=\"Embedding Model\",\n                    input_types=[\"Embeddings\"],\n                    info=\"Allows an embedding model configuration.\",\n                ).to_dict()\n\n                self.insert_in_dict(build_config, \"embedding_choice\", {\"embedding_model\": new_parameter})\n\n        elif field_name == \"embedding_provider\":\n            self.del_fields(\n                build_config,\n                [\"model\", \"z_01_model_parameters\", \"z_02_api_key_name\", \"z_03_provider_api_key\", \"z_04_authentication\"],\n            )\n\n            # Update the providers mapping\n            vectorize_providers = self.update_providers_mapping()\n            model_options = vectorize_providers[field_value][1]\n\n            new_parameter = DropdownInput(\n                name=\"model\",\n                display_name=\"Model\",\n                info=\"The embedding model to use for the selected provider. Each provider has a different set of \"\n                \"models available (full list at \"\n                \"https://docs.datastax.com/en/astra-db-serverless/databases/embedding-generation.html):\\n\\n\"\n                f\"{', '.join(model_options)}\",\n                options=model_options,\n                value=None,\n                required=True,\n                real_time_refresh=True,\n            ).to_dict()\n\n            self.insert_in_dict(build_config, \"embedding_provider\", {\"model\": new_parameter})\n\n        elif field_name == \"model\":\n            self.del_fields(\n                build_config,\n                [\"z_01_model_parameters\", \"z_02_api_key_name\", \"z_03_provider_api_key\", \"z_04_authentication\"],\n            )\n\n            new_parameter_1 = DictInput(\n                name=\"z_01_model_parameters\",\n                display_name=\"Model Parameters\",\n                is_list=True,\n            ).to_dict()\n\n            new_parameter_2 = MessageTextInput(\n                name=\"z_02_api_key_name\",\n                display_name=\"API Key Name\",\n                info=\"The name of the embeddings provider API key stored on Astra. \"\n                \"If set, it will override the 'ProviderKey' in the authentication parameters.\",\n            ).to_dict()\n\n            new_parameter_3 = SecretStrInput(\n                load_from_db=False,\n                name=\"z_03_provider_api_key\",\n                display_name=\"Provider API Key\",\n                info=\"An alternative to the Astra Authentication that passes an API key for the provider \"\n                \"with each request to Astra DB. \"\n                \"This may be used when Vectorize is configured for the collection, \"\n                \"but no corresponding provider secret is stored within Astra's key management system.\",\n            ).to_dict()\n\n            new_parameter_4 = DictInput(\n                name=\"z_04_authentication\",\n                display_name=\"Authentication Parameters\",\n                is_list=True,\n            ).to_dict()\n\n            self.insert_in_dict(\n                build_config,\n                \"model\",\n                {\n                    \"z_01_model_parameters\": new_parameter_1,\n                    \"z_02_api_key_name\": new_parameter_2,\n                    \"z_03_provider_api_key\": new_parameter_3,\n                    \"z_04_authentication\": new_parameter_4,\n                },\n            )\n\n        return build_config\n\n    def build_vectorize_options(self, **kwargs):\n        for attribute in [\n            \"embedding_provider\",\n            \"model\",\n            \"z_01_model_parameters\",\n            \"z_02_api_key_name\",\n            \"z_03_provider_api_key\",\n            \"z_04_authentication\",\n        ]:\n            if not hasattr(self, attribute):\n                setattr(self, attribute, None)\n\n        # Fetch values from kwargs if any self.* attributes are None\n        provider_value = self.VECTORIZE_PROVIDERS_MAPPING.get(self.embedding_provider, [None])[0] or kwargs.get(\n            \"embedding_provider\"\n        )\n        model_name = self.model or kwargs.get(\"model\")\n        authentication = {**(self.z_04_authentication or kwargs.get(\"z_04_authentication\", {}))}\n        parameters = self.z_01_model_parameters or kwargs.get(\"z_01_model_parameters\", {})\n\n        # Set the API key name if provided\n        api_key_name = self.z_02_api_key_name or kwargs.get(\"z_02_api_key_name\")\n        provider_key = self.z_03_provider_api_key or kwargs.get(\"z_03_provider_api_key\")\n        if api_key_name:\n            authentication[\"providerKey\"] = api_key_name\n\n        # Set authentication and parameters to None if no values are provided\n        if not authentication:\n            authentication = None\n        if not parameters:\n            parameters = None\n\n        return {\n            # must match astrapy.info.CollectionVectorServiceOptions\n            \"collection_vector_service_options\": {\n                \"provider\": provider_value,\n                \"modelName\": model_name,\n                \"authentication\": authentication,\n                \"parameters\": parameters,\n            },\n            \"collection_embedding_api_key\": provider_key,\n        }\n\n    @check_cached_vector_store\n    def build_vector_store(self, vectorize_options=None):\n        try:\n            from langchain_astradb import AstraDBVectorStore\n            from langchain_astradb.utils.astradb import SetupMode\n        except ImportError as e:\n            msg = (\n                \"Could not import langchain Astra DB integration package. \"\n                \"Please install it with `pip install langchain-astradb`.\"\n            )\n            raise ImportError(msg) from e\n\n        try:\n            if not self.setup_mode:\n                self.setup_mode = self._inputs[\"setup_mode\"].options[0]\n\n            setup_mode_value = SetupMode[self.setup_mode.upper()]\n        except KeyError as e:\n            msg = f\"Invalid setup mode: {self.setup_mode}\"\n            raise ValueError(msg) from e\n\n        if self.embedding_choice == \"Embedding Model\":\n            embedding_dict = {\"embedding\": self.embedding_model}\n        else:\n            from astrapy.info import CollectionVectorServiceOptions\n\n            # Fetch values from kwargs if any self.* attributes are None\n            dict_options = vectorize_options or self.build_vectorize_options()\n\n            # Set the embedding dictionary\n            embedding_dict = {\n                \"collection_vector_service_options\": CollectionVectorServiceOptions.from_dict(\n                    dict_options.get(\"collection_vector_service_options\")\n                ),\n                \"collection_embedding_api_key\": dict_options.get(\"collection_embedding_api_key\"),\n            }\n\n        try:\n            vector_store = AstraDBVectorStore(\n                collection_name=self.collection_name,\n                token=self.token,\n                api_endpoint=self.api_endpoint,\n                namespace=self.keyspace or None,\n                environment=parse_api_endpoint(self.api_endpoint).environment if self.api_endpoint else None,\n                metric=self.metric or None,\n                batch_size=self.batch_size or None,\n                bulk_insert_batch_concurrency=self.bulk_insert_batch_concurrency or None,\n                bulk_insert_overwrite_concurrency=self.bulk_insert_overwrite_concurrency or None,\n                bulk_delete_concurrency=self.bulk_delete_concurrency or None,\n                setup_mode=setup_mode_value,\n                pre_delete_collection=self.pre_delete_collection,\n                metadata_indexing_include=[s for s in self.metadata_indexing_include if s] or None,\n                metadata_indexing_exclude=[s for s in self.metadata_indexing_exclude if s] or None,\n                collection_indexing_policy=orjson.dumps(self.collection_indexing_policy)\n                if self.collection_indexing_policy\n                else None,\n                **embedding_dict,\n            )\n        except Exception as e:\n            msg = f\"Error initializing AstraDBVectorStore: {e}\"\n            raise ValueError(msg) from e\n\n        self._add_documents_to_vector_store(vector_store)\n\n        return vector_store\n\n    def _add_documents_to_vector_store(self, vector_store) -> None:\n        documents = []\n        for _input in self.ingest_data or []:\n            if isinstance(_input, Data):\n                documents.append(_input.to_lc_document())\n            else:\n                msg = \"Vector Store Inputs must be Data objects.\"\n                raise TypeError(msg)\n\n        if documents:\n            self.log(f\"Adding {len(documents)} documents to the Vector Store.\")\n            try:\n                vector_store.add_documents(documents)\n            except Exception as e:\n                msg = f\"Error adding documents to AstraDBVectorStore: {e}\"\n                raise ValueError(msg) from e\n        else:\n            self.log(\"No documents to add to the Vector Store.\")\n\n    def _map_search_type(self) -> str:\n        if self.search_type == \"Similarity with score threshold\":\n            return \"similarity_score_threshold\"\n        if self.search_type == \"MMR (Max Marginal Relevance)\":\n            return \"mmr\"\n        return \"similarity\"\n\n    def _build_search_args(self):\n        query = self.search_input if isinstance(self.search_input, str) and self.search_input.strip() else None\n        search_filter = (\n            {k: v for k, v in self.search_filter.items() if k and v and k.strip()} if self.search_filter else None\n        )\n\n        if query:\n            args = {\n                \"query\": query,\n                \"search_type\": self._map_search_type(),\n                \"k\": self.number_of_results,\n                \"score_threshold\": self.search_score_threshold,\n            }\n        elif self.advanced_search_filter or search_filter:\n            args = {\n                \"n\": self.number_of_results,\n            }\n        else:\n            return {}\n\n        filter_arg = self.advanced_search_filter or {}\n\n        if search_filter:\n            self.log(self.log(f\"`search_filter` is deprecated. Use `advanced_search_filter`. Cleaned: {search_filter}\"))\n            filter_arg.update(search_filter)\n\n        if filter_arg:\n            args[\"filter\"] = filter_arg\n\n        return args\n\n    def search_documents(self, vector_store=None) -> list[Data]:\n        vector_store = vector_store or self.build_vector_store()\n\n        self.log(f\"Search input: {self.search_input}\")\n        self.log(f\"Search type: {self.search_type}\")\n        self.log(f\"Number of results: {self.number_of_results}\")\n\n        try:\n            search_args = self._build_search_args()\n        except Exception as e:\n            msg = f\"Error in AstraDBVectorStore._build_search_args: {e}\"\n            raise ValueError(msg) from e\n\n        if not search_args:\n            self.log(\"No search input or filters provided. Skipping search.\")\n            return []\n\n        docs = []\n        search_method = \"search\" if \"query\" in search_args else \"metadata_search\"\n\n        try:\n            self.log(f\"Calling vector_store.{search_method} with args: {search_args}\")\n            docs = getattr(vector_store, search_method)(**search_args)\n        except Exception as e:\n            msg = f\"Error performing {search_method} in AstraDBVectorStore: {e}\"\n            raise ValueError(msg) from e\n\n        self.log(f\"Retrieved documents: {len(docs)}\")\n\n        data = docs_to_data(docs)\n        self.log(f\"Converted documents to data: {len(data)}\")\n        self.status = data\n        return data\n\n    def get_retriever_kwargs(self):\n        search_args = self._build_search_args()\n        return {\n            \"search_type\": self._map_search_type(),\n            \"search_kwargs\": search_args,\n        }\n"
              },
              "collection_indexing_policy": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Collection Indexing Policy",
                "dynamic": False,
                "info": "Optional JSON string for the \"indexing\" field of the collection. See https://docs.datastax.com/en/astra-db-serverless/api-reference/collections.html#the-indexing-option",
                "list": False,
                "load_from_db": False,
                "name": "collection_indexing_policy",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "collection_name": {
                "_input_type": "StrInput",
                "advanced": False,
                "display_name": "Collection Name",
                "dynamic": False,
                "info": "The name of the collection within Astra DB where the vectors will be stored.",
                "list": False,
                "load_from_db": False,
                "name": "collection_name",
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "test"
              },
              "embedding_choice": {
                "_input_type": "DropdownInput",
                "advanced": False,
                "combobox": False,
                "display_name": "Embedding Model or Astra Vectorize",
                "dynamic": False,
                "info": "Determines whether to use Astra Vectorize for the collection.",
                "name": "embedding_choice",
                "options": [
                  "Embedding Model",
                  "Astra Vectorize"
                ],
                "placeholder": "",
                "real_time_refresh": True,
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Embedding Model"
              },
              "embedding_model": {
                "_input_type": "HandleInput",
                "advanced": False,
                "display_name": "Embedding Model",
                "dynamic": False,
                "info": "Allows an embedding model configuration.",
                "input_types": [
                  "Embeddings"
                ],
                "list": False,
                "name": "embedding_model",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "other",
                "value": ""
              },
              "ingest_data": {
                "_input_type": "DataInput",
                "advanced": False,
                "display_name": "Ingest Data",
                "dynamic": False,
                "info": "",
                "input_types": [
                  "Data"
                ],
                "list": True,
                "name": "ingest_data",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "other",
                "value": ""
              },
              "keyspace": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Keyspace",
                "dynamic": False,
                "info": "Optional keyspace within Astra DB to use for the collection.",
                "list": False,
                "load_from_db": False,
                "name": "keyspace",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "metadata_indexing_exclude": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Metadata Indexing Exclude",
                "dynamic": False,
                "info": "Optional list of metadata fields to exclude from the indexing.",
                "list": True,
                "load_from_db": False,
                "name": "metadata_indexing_exclude",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "metadata_indexing_include": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Metadata Indexing Include",
                "dynamic": False,
                "info": "Optional list of metadata fields to include in the indexing.",
                "list": True,
                "load_from_db": False,
                "name": "metadata_indexing_include",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "metric": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Metric",
                "dynamic": False,
                "info": "Optional distance metric for vector comparisons in the vector store.",
                "name": "metric",
                "options": [
                  "cosine",
                  "dot_product",
                  "euclidean"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "cosine"
              },
              "number_of_results": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Number of Results",
                "dynamic": False,
                "info": "Number of results to return.",
                "list": False,
                "name": "number_of_results",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": 4
              },
              "pre_delete_collection": {
                "_input_type": "BoolInput",
                "advanced": True,
                "display_name": "Pre Delete Collection",
                "dynamic": False,
                "info": "Boolean flag to determine whether to delete the collection before creating a new one.",
                "list": False,
                "name": "pre_delete_collection",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "bool",
                "value": False
              },
              "search_filter": {
                "_input_type": "DictInput",
                "advanced": True,
                "display_name": "[DEPRECATED] Search Metadata Filter",
                "dynamic": False,
                "info": "Deprecated: use advanced_search_filter. Optional dictionary of filters to apply to the search query.",
                "list": True,
                "name": "search_filter",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "type": "dict",
                "value": {}
              },
              "search_input": {
                "_input_type": "MultilineInput",
                "advanced": False,
                "display_name": "Search Input",
                "dynamic": False,
                "info": "",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "search_input",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "search_score_threshold": {
                "_input_type": "FloatInput",
                "advanced": True,
                "display_name": "Search Score Threshold",
                "dynamic": False,
                "info": "Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')",
                "list": False,
                "name": "search_score_threshold",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "float",
                "value": 0
              },
              "search_type": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Search Type",
                "dynamic": False,
                "info": "Search type to use",
                "name": "search_type",
                "options": [
                  "Similarity",
                  "Similarity with score threshold",
                  "MMR (Max Marginal Relevance)"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Similarity"
              },
              "setup_mode": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Setup Mode",
                "dynamic": False,
                "info": "Configuration mode for setting up the vector store, with options like 'Sync' or 'Off'.",
                "name": "setup_mode",
                "options": [
                  "Sync",
                  "Off"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Sync"
              },
              "token": {
                "_input_type": "SecretStrInput",
                "advanced": False,
                "display_name": "Astra DB Application Token",
                "dynamic": False,
                "info": "Authentication token for accessing Astra DB.",
                "input_types": [
                  "Message"
                ],
                "load_from_db": False,
                "name": "token",
                "password": True,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "str",
                "value": TOKEN
              }
            },
            "tool_mode": False
          },
          "type": "AstraDB"
        },
        "dragging": False,
        "height": 745,
        "id": "AstraDB-gHvII",
        "position": {
          "x": 1225.8151138573664,
          "y": 369.2727294042354
        },
        "positionAbsolute": {
          "x": 1225.8151138573664,
          "y": 369.2727294042354
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "id": "AstraDB-cu7xm",
          "node": {
            "base_classes": [
              "Data",
              "Retriever"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Implementation of Vector Store using Astra DB with search capabilities",
            "display_name": "Astra DB",
            "documentation": "https://docs.langflow.org/starter-projects-vector-store-rag",
            "edited": False,
            "field_order": [
              "token",
              "api_endpoint",
              "collection_name",
              "search_input",
              "ingest_data",
              "namespace",
              "embedding_choice",
              "embedding_model",
              "metric",
              "batch_size",
              "bulk_insert_batch_concurrency",
              "bulk_insert_overwrite_concurrency",
              "bulk_delete_concurrency",
              "setup_mode",
              "pre_delete_collection",
              "metadata_indexing_include",
              "metadata_indexing_exclude",
              "collection_indexing_policy",
              "number_of_results",
              "search_type",
              "search_score_threshold",
              "search_filter"
            ],
            "frozen": False,
            "icon": "AstraDB",
            "legacy": False,
            "lf_version": "1.1.1",
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Retriever",
                "method": "build_base_retriever",
                "name": "base_retriever",
                "required_inputs": [],
                "selected": "Retriever",
                "types": [
                  "Retriever"
                ],
                "value": "__UNDEFINED__"
              },
              {
                "cache": True,
                "display_name": "Search Results",
                "method": "search_documents",
                "name": "search_results",
                "required_inputs": [
                  "api_endpoint",
                  "collection_name",
                  "token"
                ],
                "selected": "Data",
                "types": [
                  "Data"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "advanced_search_filter": {
                "_input_type": "NestedDictInput",
                "advanced": True,
                "display_name": "Search Metadata Filter",
                "dynamic": False,
                "info": "Optional dictionary of filters to apply to the search query.",
                "list": False,
                "name": "advanced_search_filter",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "NestedDict",
                "value": {}
              },
              "api_endpoint": {
                "_input_type": "SecretStrInput",
                "advanced": False,
                "display_name": "API Endpoint",
                "dynamic": False,
                "info": "API endpoint URL for the Astra DB service.",
                "input_types": [
                  "Message"
                ],
                "load_from_db": False,
                "name": "api_endpoint",
                "password": True,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "str",
                "value": API_ENDPOINT
              },
              "batch_size": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Batch Size",
                "dynamic": False,
                "info": "Optional number of data to process in a single batch.",
                "list": False,
                "name": "batch_size",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "bulk_delete_concurrency": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Bulk Delete Concurrency",
                "dynamic": False,
                "info": "Optional concurrency level for bulk delete operations.",
                "list": False,
                "name": "bulk_delete_concurrency",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "bulk_insert_batch_concurrency": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Bulk Insert Batch Concurrency",
                "dynamic": False,
                "info": "Optional concurrency level for bulk insert operations.",
                "list": False,
                "name": "bulk_insert_batch_concurrency",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "bulk_insert_overwrite_concurrency": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Bulk Insert Overwrite Concurrency",
                "dynamic": False,
                "info": "Optional concurrency level for bulk insert operations that overwrite existing data.",
                "list": False,
                "name": "bulk_insert_overwrite_concurrency",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": ""
              },
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "import os\nfrom collections import defaultdict\n\nimport orjson\nfrom astrapy import DataAPIClient\nfrom astrapy.admin import parse_api_endpoint\nfrom langchain_astradb import AstraDBVectorStore\n\nfrom langflow.base.vectorstores.model import LCVectorStoreComponent, check_cached_vector_store\nfrom langflow.helpers import docs_to_data\nfrom langflow.inputs import DictInput, FloatInput, MessageTextInput, NestedDictInput\nfrom langflow.io import (\n    BoolInput,\n    DataInput,\n    DropdownInput,\n    HandleInput,\n    IntInput,\n    MultilineInput,\n    SecretStrInput,\n    StrInput,\n)\nfrom langflow.schema import Data\n\n\nclass AstraVectorStoreComponent(LCVectorStoreComponent):\n    display_name: str = \"Astra DB\"\n    description: str = \"Implementation of Vector Store using Astra DB with search capabilities\"\n    documentation: str = \"https://docs.langflow.org/starter-projects-vector-store-rag\"\n    name = \"AstraDB\"\n    icon: str = \"AstraDB\"\n\n    _cached_vector_store: AstraDBVectorStore | None = None\n\n    VECTORIZE_PROVIDERS_MAPPING = defaultdict(\n        list,\n        {\n            \"Azure OpenAI\": [\n                \"azureOpenAI\",\n                [\"text-embedding-3-small\", \"text-embedding-3-large\", \"text-embedding-ada-002\"],\n            ],\n            \"Hugging Face - Dedicated\": [\"huggingfaceDedicated\", [\"endpoint-defined-model\"]],\n            \"Hugging Face - Serverless\": [\n                \"huggingface\",\n                [\n                    \"sentence-transformers/all-MiniLM-L6-v2\",\n                    \"intfloat/multilingual-e5-large\",\n                    \"intfloat/multilingual-e5-large-instruct\",\n                    \"BAAI/bge-small-en-v1.5\",\n                    \"BAAI/bge-base-en-v1.5\",\n                    \"BAAI/bge-large-en-v1.5\",\n                ],\n            ],\n            \"Jina AI\": [\n                \"jinaAI\",\n                [\n                    \"jina-embeddings-v2-base-en\",\n                    \"jina-embeddings-v2-base-de\",\n                    \"jina-embeddings-v2-base-es\",\n                    \"jina-embeddings-v2-base-code\",\n                    \"jina-embeddings-v2-base-zh\",\n                ],\n            ],\n            \"Mistral AI\": [\"mistral\", [\"mistral-embed\"]],\n            \"NVIDIA\": [\"nvidia\", [\"NV-Embed-QA\"]],\n            \"OpenAI\": [\"openai\", [\"text-embedding-3-small\", \"text-embedding-3-large\", \"text-embedding-ada-002\"]],\n            \"Upstage\": [\"upstageAI\", [\"solar-embedding-1-large\"]],\n            \"Voyage AI\": [\n                \"voyageAI\",\n                [\"voyage-large-2-instruct\", \"voyage-law-2\", \"voyage-code-2\", \"voyage-large-2\", \"voyage-2\"],\n            ],\n        },\n    )\n\n    inputs = [\n        SecretStrInput(\n            name=\"token\",\n            display_name=\"Astra DB Application Token\",\n            info=\"Authentication token for accessing Astra DB.\",\n            value=\"ASTRA_DB_APPLICATION_TOKEN\",\n            required=True,\n            advanced=os.getenv(\"ASTRA_ENHANCED\", \"False\").lower() == \"True\",\n        ),\n        SecretStrInput(\n            name=\"api_endpoint\",\n            display_name=\"Database\" if os.getenv(\"ASTRA_ENHANCED\", \"False\").lower() == \"True\" else \"API Endpoint\",\n            info=\"API endpoint URL for the Astra DB service.\",\n            value=\"ASTRA_DB_API_ENDPOINT\",\n            required=True,\n        ),\n        StrInput(\n            name=\"collection_name\",\n            display_name=\"Collection Name\",\n            info=\"The name of the collection within Astra DB where the vectors will be stored.\",\n            required=True,\n        ),\n        MultilineInput(\n            name=\"search_input\",\n            display_name=\"Search Input\",\n        ),\n        DataInput(\n            name=\"ingest_data\",\n            display_name=\"Ingest Data\",\n            is_list=True,\n        ),\n        StrInput(\n            name=\"keyspace\",\n            display_name=\"Keyspace\",\n            info=\"Optional keyspace within Astra DB to use for the collection.\",\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"embedding_choice\",\n            display_name=\"Embedding Model or Astra Vectorize\",\n            info=\"Determines whether to use Astra Vectorize for the collection.\",\n            options=[\"Embedding Model\", \"Astra Vectorize\"],\n            real_time_refresh=True,\n            value=\"Embedding Model\",\n        ),\n        HandleInput(\n            name=\"embedding_model\",\n            display_name=\"Embedding Model\",\n            input_types=[\"Embeddings\"],\n            info=\"Allows an embedding model configuration.\",\n        ),\n        DropdownInput(\n            name=\"metric\",\n            display_name=\"Metric\",\n            info=\"Optional distance metric for vector comparisons in the vector store.\",\n            options=[\"cosine\", \"dot_product\", \"euclidean\"],\n            value=\"cosine\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"batch_size\",\n            display_name=\"Batch Size\",\n            info=\"Optional number of data to process in a single batch.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"bulk_insert_batch_concurrency\",\n            display_name=\"Bulk Insert Batch Concurrency\",\n            info=\"Optional concurrency level for bulk insert operations.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"bulk_insert_overwrite_concurrency\",\n            display_name=\"Bulk Insert Overwrite Concurrency\",\n            info=\"Optional concurrency level for bulk insert operations that overwrite existing data.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"bulk_delete_concurrency\",\n            display_name=\"Bulk Delete Concurrency\",\n            info=\"Optional concurrency level for bulk delete operations.\",\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"setup_mode\",\n            display_name=\"Setup Mode\",\n            info=\"Configuration mode for setting up the vector store, with options like 'Sync' or 'Off'.\",\n            options=[\"Sync\", \"Off\"],\n            advanced=True,\n            value=\"Sync\",\n        ),\n        BoolInput(\n            name=\"pre_delete_collection\",\n            display_name=\"Pre Delete Collection\",\n            info=\"Boolean flag to determine whether to delete the collection before creating a new one.\",\n            advanced=True,\n        ),\n        StrInput(\n            name=\"metadata_indexing_include\",\n            display_name=\"Metadata Indexing Include\",\n            info=\"Optional list of metadata fields to include in the indexing.\",\n            is_list=True,\n            advanced=True,\n        ),\n        StrInput(\n            name=\"metadata_indexing_exclude\",\n            display_name=\"Metadata Indexing Exclude\",\n            info=\"Optional list of metadata fields to exclude from the indexing.\",\n            is_list=True,\n            advanced=True,\n        ),\n        StrInput(\n            name=\"collection_indexing_policy\",\n            display_name=\"Collection Indexing Policy\",\n            info='Optional JSON string for the \"indexing\" field of the collection. '\n            \"See https://docs.datastax.com/en/astra-db-serverless/api-reference/collections.html#the-indexing-option\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"number_of_results\",\n            display_name=\"Number of Results\",\n            info=\"Number of results to return.\",\n            advanced=True,\n            value=4,\n        ),\n        DropdownInput(\n            name=\"search_type\",\n            display_name=\"Search Type\",\n            info=\"Search type to use\",\n            options=[\"Similarity\", \"Similarity with score threshold\", \"MMR (Max Marginal Relevance)\"],\n            value=\"Similarity\",\n            advanced=True,\n        ),\n        FloatInput(\n            name=\"search_score_threshold\",\n            display_name=\"Search Score Threshold\",\n            info=\"Minimum similarity score threshold for search results. \"\n            \"(when using 'Similarity with score threshold')\",\n            value=0,\n            advanced=True,\n        ),\n        NestedDictInput(\n            name=\"advanced_search_filter\",\n            display_name=\"Search Metadata Filter\",\n            info=\"Optional dictionary of filters to apply to the search query.\",\n            advanced=True,\n        ),\n        DictInput(\n            name=\"search_filter\",\n            display_name=\"[DEPRECATED] Search Metadata Filter\",\n            info=\"Deprecated: use advanced_search_filter. Optional dictionary of filters to apply to the search query.\",\n            advanced=True,\n            is_list=True,\n        ),\n    ]\n\n    def del_fields(self, build_config, field_list):\n        for field in field_list:\n            if field in build_config:\n                del build_config[field]\n\n        return build_config\n\n    def insert_in_dict(self, build_config, field_name, new_parameters):\n        # Insert the new key-value pair after the found key\n        for new_field_name, new_parameter in new_parameters.items():\n            # Get all the items as a list of tuples (key, value)\n            items = list(build_config.items())\n\n            # Find the index of the key to insert after\n            idx = len(items)\n            for i, (key, _) in enumerate(items):\n                if key == field_name:\n                    idx = i + 1\n                    break\n\n            items.insert(idx, (new_field_name, new_parameter))\n\n            # Clear the original dictionary and update with the modified items\n            build_config.clear()\n            build_config.update(items)\n\n        return build_config\n\n    def update_providers_mapping(self):\n        # If we don't have token or api_endpoint, we can't fetch the list of providers\n        if not self.token or not self.api_endpoint:\n            self.log(\"Astra DB token and API endpoint are required to fetch the list of Vectorize providers.\")\n\n            return self.VECTORIZE_PROVIDERS_MAPPING\n\n        try:\n            self.log(\"Dynamically updating list of Vectorize providers.\")\n\n            # Get the admin object\n            client = DataAPIClient(token=self.token)\n            admin = client.get_admin()\n\n            # Get the embedding providers\n            db_admin = admin.get_database_admin(self.api_endpoint)\n            embedding_providers = db_admin.find_embedding_providers().as_dict()\n\n            vectorize_providers_mapping = {}\n\n            # Map the provider display name to the provider key and models\n            for provider_key, provider_data in embedding_providers[\"embeddingProviders\"].items():\n                display_name = provider_data[\"displayName\"]\n                models = [model[\"name\"] for model in provider_data[\"models\"]]\n\n                vectorize_providers_mapping[display_name] = [provider_key, models]\n\n            # Sort the resulting dictionary\n            return defaultdict(list, dict(sorted(vectorize_providers_mapping.items())))\n        except Exception as e:  # noqa: BLE001\n            self.log(f\"Error fetching Vectorize providers: {e}\")\n\n            return self.VECTORIZE_PROVIDERS_MAPPING\n\n    def update_build_config(self, build_config: dict, field_value: str, field_name: str | None = None):\n        if field_name == \"embedding_choice\":\n            if field_value == \"Astra Vectorize\":\n                self.del_fields(build_config, [\"embedding_model\"])\n\n                # Update the providers mapping\n                vectorize_providers = self.update_providers_mapping()\n\n                new_parameter = DropdownInput(\n                    name=\"embedding_provider\",\n                    display_name=\"Embedding Provider\",\n                    options=vectorize_providers.keys(),\n                    value=\"\",\n                    required=True,\n                    real_time_refresh=True,\n                ).to_dict()\n\n                self.insert_in_dict(build_config, \"embedding_choice\", {\"embedding_provider\": new_parameter})\n            else:\n                self.del_fields(\n                    build_config,\n                    [\n                        \"embedding_provider\",\n                        \"model\",\n                        \"z_01_model_parameters\",\n                        \"z_02_api_key_name\",\n                        \"z_03_provider_api_key\",\n                        \"z_04_authentication\",\n                    ],\n                )\n\n                new_parameter = HandleInput(\n                    name=\"embedding_model\",\n                    display_name=\"Embedding Model\",\n                    input_types=[\"Embeddings\"],\n                    info=\"Allows an embedding model configuration.\",\n                ).to_dict()\n\n                self.insert_in_dict(build_config, \"embedding_choice\", {\"embedding_model\": new_parameter})\n\n        elif field_name == \"embedding_provider\":\n            self.del_fields(\n                build_config,\n                [\"model\", \"z_01_model_parameters\", \"z_02_api_key_name\", \"z_03_provider_api_key\", \"z_04_authentication\"],\n            )\n\n            # Update the providers mapping\n            vectorize_providers = self.update_providers_mapping()\n            model_options = vectorize_providers[field_value][1]\n\n            new_parameter = DropdownInput(\n                name=\"model\",\n                display_name=\"Model\",\n                info=\"The embedding model to use for the selected provider. Each provider has a different set of \"\n                \"models available (full list at \"\n                \"https://docs.datastax.com/en/astra-db-serverless/databases/embedding-generation.html):\\n\\n\"\n                f\"{', '.join(model_options)}\",\n                options=model_options,\n                value=None,\n                required=True,\n                real_time_refresh=True,\n            ).to_dict()\n\n            self.insert_in_dict(build_config, \"embedding_provider\", {\"model\": new_parameter})\n\n        elif field_name == \"model\":\n            self.del_fields(\n                build_config,\n                [\"z_01_model_parameters\", \"z_02_api_key_name\", \"z_03_provider_api_key\", \"z_04_authentication\"],\n            )\n\n            new_parameter_1 = DictInput(\n                name=\"z_01_model_parameters\",\n                display_name=\"Model Parameters\",\n                is_list=True,\n            ).to_dict()\n\n            new_parameter_2 = MessageTextInput(\n                name=\"z_02_api_key_name\",\n                display_name=\"API Key Name\",\n                info=\"The name of the embeddings provider API key stored on Astra. \"\n                \"If set, it will override the 'ProviderKey' in the authentication parameters.\",\n            ).to_dict()\n\n            new_parameter_3 = SecretStrInput(\n                load_from_db=False,\n                name=\"z_03_provider_api_key\",\n                display_name=\"Provider API Key\",\n                info=\"An alternative to the Astra Authentication that passes an API key for the provider \"\n                \"with each request to Astra DB. \"\n                \"This may be used when Vectorize is configured for the collection, \"\n                \"but no corresponding provider secret is stored within Astra's key management system.\",\n            ).to_dict()\n\n            new_parameter_4 = DictInput(\n                name=\"z_04_authentication\",\n                display_name=\"Authentication Parameters\",\n                is_list=True,\n            ).to_dict()\n\n            self.insert_in_dict(\n                build_config,\n                \"model\",\n                {\n                    \"z_01_model_parameters\": new_parameter_1,\n                    \"z_02_api_key_name\": new_parameter_2,\n                    \"z_03_provider_api_key\": new_parameter_3,\n                    \"z_04_authentication\": new_parameter_4,\n                },\n            )\n\n        return build_config\n\n    def build_vectorize_options(self, **kwargs):\n        for attribute in [\n            \"embedding_provider\",\n            \"model\",\n            \"z_01_model_parameters\",\n            \"z_02_api_key_name\",\n            \"z_03_provider_api_key\",\n            \"z_04_authentication\",\n        ]:\n            if not hasattr(self, attribute):\n                setattr(self, attribute, None)\n\n        # Fetch values from kwargs if any self.* attributes are None\n        provider_value = self.VECTORIZE_PROVIDERS_MAPPING.get(self.embedding_provider, [None])[0] or kwargs.get(\n            \"embedding_provider\"\n        )\n        model_name = self.model or kwargs.get(\"model\")\n        authentication = {**(self.z_04_authentication or kwargs.get(\"z_04_authentication\", {}))}\n        parameters = self.z_01_model_parameters or kwargs.get(\"z_01_model_parameters\", {})\n\n        # Set the API key name if provided\n        api_key_name = self.z_02_api_key_name or kwargs.get(\"z_02_api_key_name\")\n        provider_key = self.z_03_provider_api_key or kwargs.get(\"z_03_provider_api_key\")\n        if api_key_name:\n            authentication[\"providerKey\"] = api_key_name\n\n        # Set authentication and parameters to None if no values are provided\n        if not authentication:\n            authentication = None\n        if not parameters:\n            parameters = None\n\n        return {\n            # must match astrapy.info.CollectionVectorServiceOptions\n            \"collection_vector_service_options\": {\n                \"provider\": provider_value,\n                \"modelName\": model_name,\n                \"authentication\": authentication,\n                \"parameters\": parameters,\n            },\n            \"collection_embedding_api_key\": provider_key,\n        }\n\n    @check_cached_vector_store\n    def build_vector_store(self, vectorize_options=None):\n        try:\n            from langchain_astradb import AstraDBVectorStore\n            from langchain_astradb.utils.astradb import SetupMode\n        except ImportError as e:\n            msg = (\n                \"Could not import langchain Astra DB integration package. \"\n                \"Please install it with `pip install langchain-astradb`.\"\n            )\n            raise ImportError(msg) from e\n\n        try:\n            if not self.setup_mode:\n                self.setup_mode = self._inputs[\"setup_mode\"].options[0]\n\n            setup_mode_value = SetupMode[self.setup_mode.upper()]\n        except KeyError as e:\n            msg = f\"Invalid setup mode: {self.setup_mode}\"\n            raise ValueError(msg) from e\n\n        if self.embedding_choice == \"Embedding Model\":\n            embedding_dict = {\"embedding\": self.embedding_model}\n        else:\n            from astrapy.info import CollectionVectorServiceOptions\n\n            # Fetch values from kwargs if any self.* attributes are None\n            dict_options = vectorize_options or self.build_vectorize_options()\n\n            # Set the embedding dictionary\n            embedding_dict = {\n                \"collection_vector_service_options\": CollectionVectorServiceOptions.from_dict(\n                    dict_options.get(\"collection_vector_service_options\")\n                ),\n                \"collection_embedding_api_key\": dict_options.get(\"collection_embedding_api_key\"),\n            }\n\n        try:\n            vector_store = AstraDBVectorStore(\n                collection_name=self.collection_name,\n                token=self.token,\n                api_endpoint=self.api_endpoint,\n                namespace=self.keyspace or None,\n                environment=parse_api_endpoint(self.api_endpoint).environment if self.api_endpoint else None,\n                metric=self.metric or None,\n                batch_size=self.batch_size or None,\n                bulk_insert_batch_concurrency=self.bulk_insert_batch_concurrency or None,\n                bulk_insert_overwrite_concurrency=self.bulk_insert_overwrite_concurrency or None,\n                bulk_delete_concurrency=self.bulk_delete_concurrency or None,\n                setup_mode=setup_mode_value,\n                pre_delete_collection=self.pre_delete_collection,\n                metadata_indexing_include=[s for s in self.metadata_indexing_include if s] or None,\n                metadata_indexing_exclude=[s for s in self.metadata_indexing_exclude if s] or None,\n                collection_indexing_policy=orjson.dumps(self.collection_indexing_policy)\n                if self.collection_indexing_policy\n                else None,\n                **embedding_dict,\n            )\n        except Exception as e:\n            msg = f\"Error initializing AstraDBVectorStore: {e}\"\n            raise ValueError(msg) from e\n\n        self._add_documents_to_vector_store(vector_store)\n\n        return vector_store\n\n    def _add_documents_to_vector_store(self, vector_store) -> None:\n        documents = []\n        for _input in self.ingest_data or []:\n            if isinstance(_input, Data):\n                documents.append(_input.to_lc_document())\n            else:\n                msg = \"Vector Store Inputs must be Data objects.\"\n                raise TypeError(msg)\n\n        if documents:\n            self.log(f\"Adding {len(documents)} documents to the Vector Store.\")\n            try:\n                vector_store.add_documents(documents)\n            except Exception as e:\n                msg = f\"Error adding documents to AstraDBVectorStore: {e}\"\n                raise ValueError(msg) from e\n        else:\n            self.log(\"No documents to add to the Vector Store.\")\n\n    def _map_search_type(self) -> str:\n        if self.search_type == \"Similarity with score threshold\":\n            return \"similarity_score_threshold\"\n        if self.search_type == \"MMR (Max Marginal Relevance)\":\n            return \"mmr\"\n        return \"similarity\"\n\n    def _build_search_args(self):\n        query = self.search_input if isinstance(self.search_input, str) and self.search_input.strip() else None\n        search_filter = (\n            {k: v for k, v in self.search_filter.items() if k and v and k.strip()} if self.search_filter else None\n        )\n\n        if query:\n            args = {\n                \"query\": query,\n                \"search_type\": self._map_search_type(),\n                \"k\": self.number_of_results,\n                \"score_threshold\": self.search_score_threshold,\n            }\n        elif self.advanced_search_filter or search_filter:\n            args = {\n                \"n\": self.number_of_results,\n            }\n        else:\n            return {}\n\n        filter_arg = self.advanced_search_filter or {}\n\n        if search_filter:\n            self.log(self.log(f\"`search_filter` is deprecated. Use `advanced_search_filter`. Cleaned: {search_filter}\"))\n            filter_arg.update(search_filter)\n\n        if filter_arg:\n            args[\"filter\"] = filter_arg\n\n        return args\n\n    def search_documents(self, vector_store=None) -> list[Data]:\n        vector_store = vector_store or self.build_vector_store()\n\n        self.log(f\"Search input: {self.search_input}\")\n        self.log(f\"Search type: {self.search_type}\")\n        self.log(f\"Number of results: {self.number_of_results}\")\n\n        try:\n            search_args = self._build_search_args()\n        except Exception as e:\n            msg = f\"Error in AstraDBVectorStore._build_search_args: {e}\"\n            raise ValueError(msg) from e\n\n        if not search_args:\n            self.log(\"No search input or filters provided. Skipping search.\")\n            return []\n\n        docs = []\n        search_method = \"search\" if \"query\" in search_args else \"metadata_search\"\n\n        try:\n            self.log(f\"Calling vector_store.{search_method} with args: {search_args}\")\n            docs = getattr(vector_store, search_method)(**search_args)\n        except Exception as e:\n            msg = f\"Error performing {search_method} in AstraDBVectorStore: {e}\"\n            raise ValueError(msg) from e\n\n        self.log(f\"Retrieved documents: {len(docs)}\")\n\n        data = docs_to_data(docs)\n        self.log(f\"Converted documents to data: {len(data)}\")\n        self.status = data\n        return data\n\n    def get_retriever_kwargs(self):\n        search_args = self._build_search_args()\n        return {\n            \"search_type\": self._map_search_type(),\n            \"search_kwargs\": search_args,\n        }\n"
              },
              "collection_indexing_policy": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Collection Indexing Policy",
                "dynamic": False,
                "info": "Optional JSON string for the \"indexing\" field of the collection. See https://docs.datastax.com/en/astra-db-serverless/api-reference/collections.html#the-indexing-option",
                "list": False,
                "load_from_db": False,
                "name": "collection_indexing_policy",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "collection_name": {
                "_input_type": "StrInput",
                "advanced": False,
                "display_name": "Collection Name",
                "dynamic": False,
                "info": "The name of the collection within Astra DB where the vectors will be stored.",
                "list": False,
                "load_from_db": False,
                "name": "collection_name",
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "test"
              },
              "embedding_choice": {
                "_input_type": "DropdownInput",
                "advanced": False,
                "combobox": False,
                "display_name": "Embedding Model or Astra Vectorize",
                "dynamic": False,
                "info": "Determines whether to use Astra Vectorize for the collection.",
                "name": "embedding_choice",
                "options": [
                  "Embedding Model",
                  "Astra Vectorize"
                ],
                "placeholder": "",
                "real_time_refresh": True,
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Embedding Model"
              },
              "embedding_model": {
                "_input_type": "HandleInput",
                "advanced": False,
                "display_name": "Embedding Model",
                "dynamic": False,
                "info": "Allows an embedding model configuration.",
                "input_types": [
                  "Embeddings"
                ],
                "list": False,
                "name": "embedding_model",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "other",
                "value": ""
              },
              "ingest_data": {
                "_input_type": "DataInput",
                "advanced": False,
                "display_name": "Ingest Data",
                "dynamic": False,
                "info": "",
                "input_types": [
                  "Data"
                ],
                "list": True,
                "name": "ingest_data",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "other",
                "value": ""
              },
              "keyspace": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Keyspace",
                "dynamic": False,
                "info": "Optional keyspace within Astra DB to use for the collection.",
                "list": False,
                "load_from_db": False,
                "name": "keyspace",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "metadata_indexing_exclude": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Metadata Indexing Exclude",
                "dynamic": False,
                "info": "Optional list of metadata fields to exclude from the indexing.",
                "list": True,
                "load_from_db": False,
                "name": "metadata_indexing_exclude",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "metadata_indexing_include": {
                "_input_type": "StrInput",
                "advanced": True,
                "display_name": "Metadata Indexing Include",
                "dynamic": False,
                "info": "Optional list of metadata fields to include in the indexing.",
                "list": True,
                "load_from_db": False,
                "name": "metadata_indexing_include",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "metric": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Metric",
                "dynamic": False,
                "info": "Optional distance metric for vector comparisons in the vector store.",
                "name": "metric",
                "options": [
                  "cosine",
                  "dot_product",
                  "euclidean"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "cosine"
              },
              "number_of_results": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Number of Results",
                "dynamic": False,
                "info": "Number of results to return.",
                "list": False,
                "name": "number_of_results",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": 4
              },
              "pre_delete_collection": {
                "_input_type": "BoolInput",
                "advanced": True,
                "display_name": "Pre Delete Collection",
                "dynamic": False,
                "info": "Boolean flag to determine whether to delete the collection before creating a new one.",
                "list": False,
                "name": "pre_delete_collection",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "bool",
                "value": False
              },
              "search_filter": {
                "_input_type": "DictInput",
                "advanced": True,
                "display_name": "[DEPRECATED] Search Metadata Filter",
                "dynamic": False,
                "info": "Deprecated: use advanced_search_filter. Optional dictionary of filters to apply to the search query.",
                "list": True,
                "name": "search_filter",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_input": True,
                "type": "dict",
                "value": {}
              },
              "search_input": {
                "_input_type": "MultilineInput",
                "advanced": False,
                "display_name": "Search Input",
                "dynamic": False,
                "info": "",
                "input_types": [
                  "Message"
                ],
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "search_input",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "type": "str",
                "value": ""
              },
              "search_score_threshold": {
                "_input_type": "FloatInput",
                "advanced": True,
                "display_name": "Search Score Threshold",
                "dynamic": False,
                "info": "Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')",
                "list": False,
                "name": "search_score_threshold",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "float",
                "value": 0
              },
              "search_type": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Search Type",
                "dynamic": False,
                "info": "Search type to use",
                "name": "search_type",
                "options": [
                  "Similarity",
                  "Similarity with score threshold",
                  "MMR (Max Marginal Relevance)"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Similarity"
              },
              "setup_mode": {
                "_input_type": "DropdownInput",
                "advanced": True,
                "combobox": False,
                "display_name": "Setup Mode",
                "dynamic": False,
                "info": "Configuration mode for setting up the vector store, with options like 'Sync' or 'Off'.",
                "name": "setup_mode",
                "options": [
                  "Sync",
                  "Off"
                ],
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "tool_mode": False,
                "trace_as_metadata": True,
                "type": "str",
                "value": "Sync"
              },
              "token": {
                "_input_type": "SecretStrInput",
                "advanced": False,
                "display_name": "Astra DB Application Token",
                "dynamic": False,
                "info": "Authentication token for accessing Astra DB.",
                "input_types": [
                  "Message"
                ],
                "load_from_db": False,
                "name": "token",
                "password": True,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "str",
                "value": TOKEN
              }
            },
            "tool_mode": False
          },
          "type": "AstraDB"
        },
        "dragging": False,
        "height": 745,
        "id": "AstraDB-cu7xm",
        "position": {
          "x": 2090.491421890006,
          "y": 1351.6194724621473
        },
        "positionAbsolute": {
          "x": 2090.491421890006,
          "y": 1351.6194724621473
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "id": "note-mC3tw",
          "node": {
            "description": "## 📚 1. Load Data Flow\n\nRun this first! Load data from a local file and embed it into the vector database.\n\nSelect a Database and a Collection, or create new ones. \n\nClick ▶️ **Run component** on the **Astra DB** component to load your data.\n\n* If you're using OSS Langflow, add your Astra DB Application Token to the Astra DB component.\n\n#### Next steps:\n Experiment by changing the prompt and the contextual data to see how the retrieval flow's responses change.",
            "display_name": "",
            "documentation": "",
            "template": {
              "backgroundColor": "neutral"
            }
          },
          "type": "note"
        },
        "dragging": False,
        "id": "note-mC3tw",
        "position": {
          "x": 955.3277857006676,
          "y": 1552.171191793604
        },
        "positionAbsolute": {
          "x": 955.3277857006676,
          "y": 1552.171191793604
        },
        "selected": False,
        "style": {
          "height": 50,
          "width": 325
        },
        "type": "noteNode",
        "width": 325,
        "height": 50
      },
      {
        "data": {
          "id": "File-2Z8Wc",
          "node": {
            "base_classes": [
              "Data"
            ],
            "beta": False,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Load a file to be used in your project.",
            "display_name": "File",
            "documentation": "",
            "edited": False,
            "field_order": [
              "path",
              "silent_errors",
              "use_multithreading",
              "concurrency_multithreading"
            ],
            "frozen": False,
            "icon": "file-text",
            "legacy": False,
            "metadata": {},
            "output_types": [],
            "outputs": [
              {
                "cache": True,
                "display_name": "Data",
                "method": "load_file",
                "name": "data",
                "selected": "Data",
                "types": [
                  "Data"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": False,
            "template": {
              "_type": "Component",
              "code": {
                "advanced": True,
                "dynamic": True,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": False,
                "load_from_db": False,
                "multiline": True,
                "name": "code",
                "password": False,
                "placeholder": "",
                "required": True,
                "show": True,
                "title_case": False,
                "type": "code",
                "value": "from pathlib import Path\nfrom tempfile import NamedTemporaryFile\nfrom zipfile import ZipFile, is_zipfile\n\nfrom langflow.base.data.utils import TEXT_FILE_TYPES, parallel_load_data, parse_text_file_to_data\nfrom langflow.custom import Component\nfrom langflow.io import BoolInput, FileInput, IntInput, Output\nfrom langflow.schema import Data\n\n\nclass FileComponent(Component):\n    \"\"\"Handles loading of individual or zipped text files.\n\n    Processes multiple valid files within a zip archive if provided.\n\n    Attributes:\n        display_name: Display name of the component.\n        description: Brief component description.\n        icon: Icon to represent the component.\n        name: Identifier for the component.\n        inputs: Inputs required by the component.\n        outputs: Output of the component after processing files.\n    \"\"\"\n\n    display_name = \"File\"\n    description = \"Load a file to be used in your project.\"\n    icon = \"file-text\"\n    name = \"File\"\n\n    inputs = [\n        FileInput(\n            name=\"path\",\n            display_name=\"Path\",\n            file_types=[*TEXT_FILE_TYPES, \"zip\"],\n            info=f\"Supported file types: {', '.join([*TEXT_FILE_TYPES, 'zip'])}\",\n        ),\n        BoolInput(\n            name=\"silent_errors\",\n            display_name=\"Silent Errors\",\n            advanced=True,\n            info=\"If True, errors will not raise an exception.\",\n        ),\n        BoolInput(\n            name=\"use_multithreading\",\n            display_name=\"Use Multithreading\",\n            advanced=True,\n            info=\"If True, parallel processing will be enabled for zip files.\",\n        ),\n        IntInput(\n            name=\"concurrency_multithreading\",\n            display_name=\"Multithreading Concurrency\",\n            advanced=True,\n            info=\"The maximum number of workers to use, if concurrency is enabled\",\n            value=4,\n        ),\n    ]\n\n    outputs = [Output(display_name=\"Data\", name=\"data\", method=\"load_file\")]\n\n    def load_file(self) -> Data:\n        \"\"\"Load and parse file(s) from a zip archive.\n\n        Raises:\n            ValueError: If no file is uploaded or file path is invalid.\n\n        Returns:\n            Data: Parsed data from file(s).\n        \"\"\"\n        # Check if the file path is provided\n        if not self.path:\n            self.log(\"File path is missing.\")\n            msg = \"Please upload a file for processing.\"\n\n            raise ValueError(msg)\n\n        resolved_path = Path(self.resolve_path(self.path))\n        try:\n            # Check if the file is a zip archive\n            if is_zipfile(resolved_path):\n                self.log(f\"Processing zip file: {resolved_path.name}.\")\n\n                return self._process_zip_file(\n                    resolved_path,\n                    silent_errors=self.silent_errors,\n                    parallel=self.use_multithreading,\n                )\n\n            self.log(f\"Processing single file: {resolved_path.name}.\")\n\n            return self._process_single_file(resolved_path, silent_errors=self.silent_errors)\n        except FileNotFoundError:\n            self.log(f\"File not found: {resolved_path.name}.\")\n\n            raise\n\n    def _process_zip_file(self, zip_path: Path, *, silent_errors: bool = False, parallel: bool = False) -> Data:\n        \"\"\"Process text files within a zip archive.\n\n        Args:\n            zip_path: Path to the zip file.\n            silent_errors: Suppresses errors if True.\n            parallel: Enables parallel processing if True.\n\n        Returns:\n            list[Data]: Combined data from all valid files.\n\n        Raises:\n            ValueError: If no valid files found in the archive.\n        \"\"\"\n        data: list[Data] = []\n        with ZipFile(zip_path, \"r\") as zip_file:\n            # Filter file names based on extensions in TEXT_FILE_TYPES and ignore hidden files\n            valid_files = [\n                name\n                for name in zip_file.namelist()\n                if (\n                    any(name.endswith(ext) for ext in TEXT_FILE_TYPES)\n                    and not name.startswith(\"__MACOSX\")\n                    and not name.startswith(\".\")\n                )\n            ]\n\n            # Raise an error if no valid files found\n            if not valid_files:\n                self.log(\"No valid files in the zip archive.\")\n\n                # Return empty data if silent_errors is True\n                if silent_errors:\n                    return data  # type: ignore[return-value]\n\n                # Raise an error if no valid files found\n                msg = \"No valid files in the zip archive.\"\n                raise ValueError(msg)\n\n            # Define a function to process each file\n            def process_file(file_name, silent_errors=silent_errors):\n                with NamedTemporaryFile(delete=False) as temp_file:\n                    temp_path = Path(temp_file.name).with_name(file_name)\n                    with zip_file.open(file_name) as file_content:\n                        temp_path.write_bytes(file_content.read())\n                try:\n                    return self._process_single_file(temp_path, silent_errors=silent_errors)\n                finally:\n                    temp_path.unlink()\n\n            # Process files in parallel if specified\n            if parallel:\n                self.log(\n                    f\"Initializing parallel Thread Pool Executor with max workers: \"\n                    f\"{self.concurrency_multithreading}.\"\n                )\n\n                # Process files in parallel\n                initial_data = parallel_load_data(\n                    valid_files,\n                    silent_errors=silent_errors,\n                    load_function=process_file,\n                    max_concurrency=self.concurrency_multithreading,\n                )\n\n                # Filter out empty data\n                data = list(filter(None, initial_data))\n            else:\n                # Sequential processing\n                data = [process_file(file_name) for file_name in valid_files]\n\n        self.log(f\"Successfully processed zip file: {zip_path.name}.\")\n\n        return data  # type: ignore[return-value]\n\n    def _process_single_file(self, file_path: Path, *, silent_errors: bool = False) -> Data:\n        \"\"\"Process a single file.\n\n        Args:\n            file_path: Path to the file.\n            silent_errors: Suppresses errors if True.\n\n        Returns:\n            Data: Parsed data from the file.\n\n        Raises:\n            ValueError: For unsupported file formats.\n        \"\"\"\n        # Check if the file type is supported\n        if not any(file_path.suffix == ext for ext in [\".\" + f for f in TEXT_FILE_TYPES]):\n            self.log(f\"Unsupported file type: {file_path.suffix}\")\n\n            # Return empty data if silent_errors is True\n            if silent_errors:\n                return Data()\n\n            msg = f\"Unsupported file type: {file_path.suffix}\"\n            raise ValueError(msg)\n\n        try:\n            # Parse the text file as appropriate\n            data = parse_text_file_to_data(str(file_path), silent_errors=silent_errors)  # type: ignore[assignment]\n            if not data:\n                data = Data()\n\n            self.log(f\"Successfully processed file: {file_path.name}.\")\n        except Exception as e:\n            self.log(f\"Error processing file {file_path.name}: {e}\")\n\n            # Return empty data if silent_errors is True\n            if not silent_errors:\n                raise\n\n            data = Data()\n\n        return data\n"
              },
              "concurrency_multithreading": {
                "_input_type": "IntInput",
                "advanced": True,
                "display_name": "Multithreading Concurrency",
                "dynamic": False,
                "info": "The maximum number of workers to use, if concurrency is enabled",
                "list": False,
                "name": "concurrency_multithreading",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "int",
                "value": 4
              },
              "path": {
                "_input_type": "FileInput",
                "advanced": False,
                "display_name": "Path",
                "dynamic": False,
                "fileTypes": [
                  "txt",
                  "md",
                  "mdx",
                  "csv",
                  "json",
                  "yaml",
                  "yml",
                  "xml",
                  "html",
                  "htm",
                  "pdf",
                  "docx",
                  "py",
                  "sh",
                  "sql",
                  "js",
                  "ts",
                  "tsx",
                  "zip"
                ],
                "file_path": "100d6a1e-60d1-4161-a5fe-097b8351aa0b/2025-01-02_19-39-00_social_media_data.csv",
                "info": "Supported file types: txt, md, mdx, csv, json, yaml, yml, xml, html, htm, pdf, docx, py, sh, sql, js, ts, tsx, zip",
                "list": False,
                "name": "path",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "file",
                "value": ""
              },
              "silent_errors": {
                "_input_type": "BoolInput",
                "advanced": True,
                "display_name": "Silent Errors",
                "dynamic": False,
                "info": "If True, errors will not raise an exception.",
                "list": False,
                "name": "silent_errors",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "bool",
                "value": False
              },
              "use_multithreading": {
                "_input_type": "BoolInput",
                "advanced": True,
                "display_name": "Use Multithreading",
                "dynamic": False,
                "info": "If True, parallel processing will be enabled for zip files.",
                "list": False,
                "name": "use_multithreading",
                "placeholder": "",
                "required": False,
                "show": True,
                "title_case": False,
                "trace_as_metadata": True,
                "type": "bool",
                "value": False
              }
            },
            "tool_mode": False,
            "lf_version": "1.1.1"
          },
          "type": "File"
        },
        "dragging": False,
        "height": 232,
        "id": "File-2Z8Wc",
        "position": {
          "x": 1318.9043936921921,
          "y": 1486.3263312921847
        },
        "positionAbsolute": {
          "x": 1318.9043936921921,
          "y": 1486.3263312921847
        },
        "selected": False,
        "type": "genericNode",
        "width": 320
      },
      {
        "data": {
          "id": "note-8bkoF",
          "node": {
            "description": "### 💡 Add your OpenAI API key here 👇",
            "display_name": "",
            "documentation": "",
            "template": {
              "backgroundColor": "transparent"
            }
          },
          "type": "note"
        },
        "dragging": False,
        "height": 324,
        "id": "note-8bkoF",
        "position": {
          "x": 824.1003268813427,
          "y": 698.6951695764802
        },
        "positionAbsolute": {
          "x": 824.1003268813427,
          "y": 698.6951695764802
        },
        "selected": False,
        "type": "noteNode",
        "width": 324
      },
      {
        "data": {
          "id": "note-H0kPc",
          "node": {
            "description": "### 💡 Add your OpenAI API key here 👇",
            "display_name": "",
            "documentation": "",
            "template": {
              "backgroundColor": "transparent"
            }
          },
          "type": "note"
        },
        "dragging": False,
        "height": 324,
        "id": "note-H0kPc",
        "position": {
          "x": 2350.297636215281,
          "y": 525.0687902842766
        },
        "positionAbsolute": {
          "x": 2350.297636215281,
          "y": 525.0687902842766
        },
        "selected": False,
        "type": "noteNode",
        "width": 324
      },
      {
        "id": "HuggingFaceInferenceAPIEmbeddings-bRxhe",
        "type": "genericNode",
        "position": {
          "x": 1683.7208892634467,
          "y": 1898.449637585206
        },
        "data": {
          "node": {
            "template": {
              "_type": "Component",
              "api_key": {
                "load_from_db": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "api_key",
                "value": TOKEN,
                "display_name": "API Key",
                "advanced": True,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "Required for non-local inference endpoints. Local inference does not require an API Key.",
                "title_case": False,
                "password": True,
                "type": "str",
                "_input_type": "SecretStrInput"
              },
              "code": {
                "type": "code",
                "required": True,
                "placeholder": "",
                "list": False,
                "show": True,
                "multiline": True,
                "value": "from urllib.parse import urlparse\n\nimport requests\nfrom langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings\nfrom pydantic.v1.types import SecretStr\nfrom tenacity import retry, stop_after_attempt, wait_fixed\n\nfrom langflow.base.embeddings.model import LCEmbeddingsModel\nfrom langflow.field_typing import Embeddings\nfrom langflow.io import MessageTextInput, Output, SecretStrInput\n\n\nclass HuggingFaceInferenceAPIEmbeddingsComponent(LCEmbeddingsModel):\n    display_name = \"HuggingFace Embeddings Inference\"\n    description = \"Generate embeddings using HuggingFace Text Embeddings Inference (TEI)\"\n    documentation = \"https://huggingface.co/docs/text-embeddings-inference/index\"\n    icon = \"HuggingFace\"\n    name = \"HuggingFaceInferenceAPIEmbeddings\"\n\n    inputs = [\n        SecretStrInput(\n            name=\"api_key\",\n            display_name=\"API Key\",\n            advanced=True,\n            info=\"Required for non-local inference endpoints. Local inference does not require an API Key.\",\n        ),\n        MessageTextInput(\n            name=\"inference_endpoint\",\n            display_name=\"Inference Endpoint\",\n            required=True,\n            value=\"https://api-inference.huggingface.co/models/\",\n            info=\"Custom inference endpoint URL.\",\n        ),\n        MessageTextInput(\n            name=\"model_name\",\n            display_name=\"Model Name\",\n            value=\"BAAI/bge-large-en-v1.5\",\n            info=\"The name of the model to use for text embeddings.\",\n        ),\n    ]\n\n    outputs = [\n        Output(display_name=\"Embeddings\", name=\"embeddings\", method=\"build_embeddings\"),\n    ]\n\n    def validate_inference_endpoint(self, inference_endpoint: str) -> bool:\n        parsed_url = urlparse(inference_endpoint)\n        if not all([parsed_url.scheme, parsed_url.netloc]):\n            msg = (\n                f\"Invalid inference endpoint format: '{self.inference_endpoint}'. \"\n                \"Please ensure the URL includes both a scheme (e.g., 'http://' or 'https://') and a domain name. \"\n                \"Example: 'http://localhost:8080' or 'https://api.example.com'\"\n            )\n            raise ValueError(msg)\n\n        try:\n            response = requests.get(f\"{inference_endpoint}/health\", timeout=5)\n        except requests.RequestException as e:\n            msg = (\n                f\"Inference endpoint '{inference_endpoint}' is not responding. \"\n                \"Please ensure the URL is correct and the service is running.\"\n            )\n            raise ValueError(msg) from e\n\n        if response.status_code != requests.codes.ok:\n            msg = f\"HuggingFace health check failed: {response.status_code}\"\n            raise ValueError(msg)\n        # returning True to solve linting error\n        return True\n\n    def get_api_url(self) -> str:\n        if \"huggingface\" in self.inference_endpoint.lower():\n            return f\"{self.inference_endpoint}{self.model_name}\"\n        return self.inference_endpoint\n\n    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))\n    def create_huggingface_embeddings(\n        self, api_key: SecretStr, api_url: str, model_name: str\n    ) -> HuggingFaceInferenceAPIEmbeddings:\n        return HuggingFaceInferenceAPIEmbeddings(api_key=api_key, api_url=api_url, model_name=model_name)\n\n    def build_embeddings(self) -> Embeddings:\n        api_url = self.get_api_url()\n\n        is_local_url = api_url.startswith((\"http://localhost\", \"http://127.0.0.1\"))\n\n        if not self.api_key and is_local_url:\n            self.validate_inference_endpoint(api_url)\n            api_key = SecretStr(\"DummyAPIKeyForLocalDeployment\")\n        elif not self.api_key:\n            msg = \"API Key is required for non-local inference endpoints\"\n            raise ValueError(msg)\n        else:\n            api_key = SecretStr(self.api_key).get_secret_value()\n\n        try:\n            return self.create_huggingface_embeddings(api_key, api_url, self.model_name)\n        except Exception as e:\n            msg = \"Could not connect to HuggingFace Inference API.\"\n            raise ValueError(msg) from e\n",
                "fileTypes": [],
                "file_path": "",
                "password": False,
                "name": "code",
                "advanced": True,
                "dynamic": True,
                "info": "",
                "load_from_db": False,
                "title_case": False
              },
              "inference_endpoint": {
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": True,
                "placeholder": "",
                "show": True,
                "name": "inference_endpoint",
                "value": "https://api-inference.huggingface.co/models/",
                "display_name": "Inference Endpoint",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "Custom inference endpoint URL.",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageTextInput"
              },
              "model_name": {
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "model_name",
                "value": "BAAI/bge-large-en-v1.5",
                "display_name": "Model Name",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "The name of the model to use for text embeddings.",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageTextInput"
              }
            },
            "description": "Generate embeddings using HuggingFace Text Embeddings Inference (TEI)",
            "icon": "HuggingFace",
            "base_classes": [
              "Embeddings"
            ],
            "display_name": "HuggingFace Embeddings Inference",
            "documentation": "https://huggingface.co/docs/text-embeddings-inference/index",
            "custom_fields": {},
            "output_types": [],
            "pinned": False,
            "conditional_paths": [],
            "frozen": False,
            "outputs": [
              {
                "types": [
                  "Embeddings"
                ],
                "selected": "Embeddings",
                "name": "embeddings",
                "display_name": "Embeddings",
                "method": "build_embeddings",
                "value": "__UNDEFINED__",
                "cache": True
              }
            ],
            "field_order": [
              "api_key",
              "inference_endpoint",
              "model_name"
            ],
            "beta": False,
            "legacy": False,
            "edited": False,
            "metadata": {},
            "tool_mode": False,
            "lf_version": "1.1.1"
          },
          "type": "HuggingFaceInferenceAPIEmbeddings",
          "id": "HuggingFaceInferenceAPIEmbeddings-bRxhe"
        },
        "selected": False,
        "width": 320,
        "height": 340,
        "positionAbsolute": {
          "x": 1683.7208892634467,
          "y": 1898.449637585206
        },
        "dragging": False
      },
      {
        "id": "HuggingFaceInferenceAPIEmbeddings-7rcWz",
        "type": "genericNode",
        "position": {
          "x": 822.7460206839855,
          "y": 812.0547998009067
        },
        "data": {
          "node": {
            "template": {
              "_type": "Component",
              "api_key": {
                "load_from_db": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "api_key",
                "value": TOKEN,
                "display_name": "API Key",
                "advanced": True,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "Required for non-local inference endpoints. Local inference does not require an API Key.",
                "title_case": False,
                "password": True,
                "type": "str",
                "_input_type": "SecretStrInput"
              },
              "code": {
                "type": "code",
                "required": True,
                "placeholder": "",
                "list": False,
                "show": True,
                "multiline": True,
                "value": "from urllib.parse import urlparse\n\nimport requests\nfrom langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings\nfrom pydantic.v1.types import SecretStr\nfrom tenacity import retry, stop_after_attempt, wait_fixed\n\nfrom langflow.base.embeddings.model import LCEmbeddingsModel\nfrom langflow.field_typing import Embeddings\nfrom langflow.io import MessageTextInput, Output, SecretStrInput\n\n\nclass HuggingFaceInferenceAPIEmbeddingsComponent(LCEmbeddingsModel):\n    display_name = \"HuggingFace Embeddings Inference\"\n    description = \"Generate embeddings using HuggingFace Text Embeddings Inference (TEI)\"\n    documentation = \"https://huggingface.co/docs/text-embeddings-inference/index\"\n    icon = \"HuggingFace\"\n    name = \"HuggingFaceInferenceAPIEmbeddings\"\n\n    inputs = [\n        SecretStrInput(\n            name=\"api_key\",\n            display_name=\"API Key\",\n            advanced=True,\n            info=\"Required for non-local inference endpoints. Local inference does not require an API Key.\",\n        ),\n        MessageTextInput(\n            name=\"inference_endpoint\",\n            display_name=\"Inference Endpoint\",\n            required=True,\n            value=\"https://api-inference.huggingface.co/models/\",\n            info=\"Custom inference endpoint URL.\",\n        ),\n        MessageTextInput(\n            name=\"model_name\",\n            display_name=\"Model Name\",\n            value=\"BAAI/bge-large-en-v1.5\",\n            info=\"The name of the model to use for text embeddings.\",\n        ),\n    ]\n\n    outputs = [\n        Output(display_name=\"Embeddings\", name=\"embeddings\", method=\"build_embeddings\"),\n    ]\n\n    def validate_inference_endpoint(self, inference_endpoint: str) -> bool:\n        parsed_url = urlparse(inference_endpoint)\n        if not all([parsed_url.scheme, parsed_url.netloc]):\n            msg = (\n                f\"Invalid inference endpoint format: '{self.inference_endpoint}'. \"\n                \"Please ensure the URL includes both a scheme (e.g., 'http://' or 'https://') and a domain name. \"\n                \"Example: 'http://localhost:8080' or 'https://api.example.com'\"\n            )\n            raise ValueError(msg)\n\n        try:\n            response = requests.get(f\"{inference_endpoint}/health\", timeout=5)\n        except requests.RequestException as e:\n            msg = (\n                f\"Inference endpoint '{inference_endpoint}' is not responding. \"\n                \"Please ensure the URL is correct and the service is running.\"\n            )\n            raise ValueError(msg) from e\n\n        if response.status_code != requests.codes.ok:\n            msg = f\"HuggingFace health check failed: {response.status_code}\"\n            raise ValueError(msg)\n        # returning True to solve linting error\n        return True\n\n    def get_api_url(self) -> str:\n        if \"huggingface\" in self.inference_endpoint.lower():\n            return f\"{self.inference_endpoint}{self.model_name}\"\n        return self.inference_endpoint\n\n    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))\n    def create_huggingface_embeddings(\n        self, api_key: SecretStr, api_url: str, model_name: str\n    ) -> HuggingFaceInferenceAPIEmbeddings:\n        return HuggingFaceInferenceAPIEmbeddings(api_key=api_key, api_url=api_url, model_name=model_name)\n\n    def build_embeddings(self) -> Embeddings:\n        api_url = self.get_api_url()\n\n        is_local_url = api_url.startswith((\"http://localhost\", \"http://127.0.0.1\"))\n\n        if not self.api_key and is_local_url:\n            self.validate_inference_endpoint(api_url)\n            api_key = SecretStr(\"DummyAPIKeyForLocalDeployment\")\n        elif not self.api_key:\n            msg = \"API Key is required for non-local inference endpoints\"\n            raise ValueError(msg)\n        else:\n            api_key = SecretStr(self.api_key).get_secret_value()\n\n        try:\n            return self.create_huggingface_embeddings(api_key, api_url, self.model_name)\n        except Exception as e:\n            msg = \"Could not connect to HuggingFace Inference API.\"\n            raise ValueError(msg) from e\n",
                "fileTypes": [],
                "file_path": "",
                "password": False,
                "name": "code",
                "advanced": True,
                "dynamic": True,
                "info": "",
                "load_from_db": False,
                "title_case": False
              },
              "inference_endpoint": {
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": True,
                "placeholder": "",
                "show": True,
                "name": "inference_endpoint",
                "value": "https://api-inference.huggingface.co/models/",
                "display_name": "Inference Endpoint",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "Custom inference endpoint URL.",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageTextInput"
              },
              "model_name": {
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "model_name",
                "value": "BAAI/bge-large-en-v1.5",
                "display_name": "Model Name",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "The name of the model to use for text embeddings.",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageTextInput"
              }
            },
            "description": "Generate embeddings using HuggingFace Text Embeddings Inference (TEI)",
            "icon": "HuggingFace",
            "base_classes": [
              "Embeddings"
            ],
            "display_name": "HuggingFace Embeddings Inference",
            "documentation": "https://huggingface.co/docs/text-embeddings-inference/index",
            "custom_fields": {},
            "output_types": [],
            "pinned": False,
            "conditional_paths": [],
            "frozen": False,
            "outputs": [
              {
                "types": [
                  "Embeddings"
                ],
                "selected": "Embeddings",
                "name": "embeddings",
                "display_name": "Embeddings",
                "method": "build_embeddings",
                "value": "__UNDEFINED__",
                "cache": True
              }
            ],
            "field_order": [
              "api_key",
              "inference_endpoint",
              "model_name"
            ],
            "beta": False,
            "legacy": False,
            "edited": False,
            "metadata": {},
            "tool_mode": False,
            "lf_version": "1.1.1"
          },
          "type": "HuggingFaceInferenceAPIEmbeddings",
          "id": "HuggingFaceInferenceAPIEmbeddings-7rcWz"
        },
        "selected": False,
        "width": 320,
        "height": 340,
        "positionAbsolute": {
          "x": 822.7460206839855,
          "y": 812.0547998009067
        },
        "dragging": False
      },
      {
        "id": "GroqModel-V8Dm2",
        "type": "genericNode",
        "position": {
          "x": 2352.0688828198176,
          "y": 566.1385367527583
        },
        "data": {
          "node": {
            "template": {
              "_type": "Component",
              "output_parser": {
                "trace_as_metadata": True,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "output_parser",
                "value": "",
                "display_name": "Output Parser",
                "advanced": True,
                "input_types": [
                  "OutputParser"
                ],
                "dynamic": False,
                "info": "The parser to use to parse the output of the model",
                "title_case": False,
                "type": "other",
                "_input_type": "HandleInput"
              },
              "code": {
                "type": "code",
                "required": True,
                "placeholder": "",
                "list": False,
                "show": True,
                "multiline": True,
                "value": "import requests\nfrom pydantic.v1 import SecretStr\nfrom typing_extensions import override\n\nfrom langflow.base.models.groq_constants import GROQ_MODELS\nfrom langflow.base.models.model import LCModelComponent\nfrom langflow.field_typing import LanguageModel\nfrom langflow.inputs.inputs import HandleInput\nfrom langflow.io import DropdownInput, FloatInput, IntInput, MessageTextInput, SecretStrInput\n\n\nclass GroqModel(LCModelComponent):\n    display_name: str = \"Groq\"\n    description: str = \"Generate text using Groq.\"\n    icon = \"Groq\"\n    name = \"GroqModel\"\n\n    inputs = [\n        *LCModelComponent._base_inputs,\n        SecretStrInput(name=\"groq_api_key\", display_name=\"Groq API Key\", info=\"API key for the Groq API.\"),\n        MessageTextInput(\n            name=\"groq_api_base\",\n            display_name=\"Groq API Base\",\n            info=\"Base URL path for API requests, leave blank if not using a proxy or service emulator.\",\n            advanced=True,\n            value=\"https://api.groq.com\",\n        ),\n        IntInput(\n            name=\"max_tokens\",\n            display_name=\"Max Output Tokens\",\n            info=\"The maximum number of tokens to generate.\",\n            advanced=True,\n        ),\n        FloatInput(\n            name=\"temperature\",\n            display_name=\"Temperature\",\n            info=\"Run inference with this temperature. Must by in the closed interval [0.0, 1.0].\",\n            value=0.1,\n        ),\n        IntInput(\n            name=\"n\",\n            display_name=\"N\",\n            info=\"Number of chat completions to generate for each prompt. \"\n            \"Note that the API may not return the full n completions if duplicates are generated.\",\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"model_name\",\n            display_name=\"Model\",\n            info=\"The name of the model to use.\",\n            options=GROQ_MODELS,\n            value=\"llama-3.1-8b-instant\",\n            refresh_button=True,\n        ),\n        HandleInput(\n            name=\"output_parser\",\n            display_name=\"Output Parser\",\n            info=\"The parser to use to parse the output of the model\",\n            advanced=True,\n            input_types=[\"OutputParser\"],\n        ),\n    ]\n\n    def get_models(self) -> list[str]:\n        api_key = self.groq_api_key\n        base_url = self.groq_api_base or \"https://api.groq.com\"\n        url = f\"{base_url}/openai/v1/models\"\n\n        headers = {\"Authorization\": f\"Bearer {api_key}\", \"Content-Type\": \"application/json\"}\n\n        try:\n            response = requests.get(url, headers=headers, timeout=10)\n            response.raise_for_status()\n            model_list = response.json()\n            return [model[\"id\"] for model in model_list.get(\"data\", [])]\n        except requests.RequestException as e:\n            self.status = f\"Error fetching models: {e}\"\n            return GROQ_MODELS\n\n    @override\n    def update_build_config(self, build_config: dict, field_value: str, field_name: str | None = None):\n        if field_name in {\"groq_api_key\", \"groq_api_base\", \"model_name\"}:\n            models = self.get_models()\n            build_config[\"model_name\"][\"options\"] = models\n        return build_config\n\n    def build_model(self) -> LanguageModel:  # type: ignore[type-var]\n        try:\n            from langchain_groq import ChatGroq\n        except ImportError as e:\n            msg = \"langchain-groq is not installed. Please install it with `pip install langchain-groq`.\"\n            raise ImportError(msg) from e\n\n        groq_api_key = self.groq_api_key\n        model_name = self.model_name\n        max_tokens = self.max_tokens\n        temperature = self.temperature\n        groq_api_base = self.groq_api_base\n        n = self.n\n        stream = self.stream\n\n        return ChatGroq(\n            model=model_name,\n            max_tokens=max_tokens or None,\n            temperature=temperature,\n            base_url=groq_api_base,\n            n=n or 1,\n            api_key=SecretStr(groq_api_key).get_secret_value(),\n            streaming=stream,\n        )\n",
                "fileTypes": [],
                "file_path": "",
                "password": False,
                "name": "code",
                "advanced": True,
                "dynamic": True,
                "info": "",
                "load_from_db": False,
                "title_case": False
              },
              "groq_api_base": {
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "groq_api_base",
                "value": "https://api.groq.com",
                "display_name": "Groq API Base",
                "advanced": True,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "Base URL path for API requests, leave blank if not using a proxy or service emulator.",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageTextInput"
              },
              "groq_api_key": {
                "load_from_db": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "groq_api_key",
                "value": GROQ_API_KEY,
                "display_name": "Groq API Key",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "API key for the Groq API.",
                "title_case": False,
                "password": True,
                "type": "str",
                "_input_type": "SecretStrInput"
              },
              "input_value": {
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "input_value",
                "value": "",
                "display_name": "Input",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageInput"
              },
              "max_tokens": {
                "trace_as_metadata": True,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "max_tokens",
                "value": "",
                "display_name": "Max Output Tokens",
                "advanced": True,
                "dynamic": False,
                "info": "The maximum number of tokens to generate.",
                "title_case": False,
                "type": "int",
                "_input_type": "IntInput"
              },
              "model_name": {
                "tool_mode": False,
                "trace_as_metadata": True,
                "options": [
                  "distil-whisper-large-v3-en",
                  "gemma2-9b-it",
                  "gemma-7b-it",
                  "llama3-groq-70b-8192-tool-use-preview",
                  "llama3-groq-8b-8192-tool-use-preview",
                  "llama-3.1-70b-versatile",
                  "llama-3.1-8b-instant",
                  "llama-3.2-1b-preview",
                  "llama-3.2-3b-preview",
                  "llama-3.2-11b-vision-preview",
                  "llama-3.2-90b-vision-preview",
                  "llama-guard-3-8b",
                  "llama3-70b-8192",
                  "llama3-8b-8192",
                  "mixtral-8x7b-32768",
                  "whisper-large-v3",
                  "whisper-large-v3-turbo"
                ],
                "combobox": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "model_name",
                "value": "llama-3.1-8b-instant",
                "display_name": "Model",
                "advanced": False,
                "dynamic": False,
                "info": "The name of the model to use.",
                "refresh_button": True,
                "title_case": False,
                "type": "str",
                "_input_type": "DropdownInput"
              },
              "n": {
                "trace_as_metadata": True,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "n",
                "value": "",
                "display_name": "N",
                "advanced": True,
                "dynamic": False,
                "info": "Number of chat completions to generate for each prompt. Note that the API may not return the full n completions if duplicates are generated.",
                "title_case": False,
                "type": "int",
                "_input_type": "IntInput"
              },
              "stream": {
                "trace_as_metadata": True,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "stream",
                "value": False,
                "display_name": "Stream",
                "advanced": False,
                "dynamic": False,
                "info": "Stream the response from the model. Streaming works only in Chat.",
                "title_case": False,
                "type": "bool",
                "_input_type": "BoolInput"
              },
              "system_message": {
                "tool_mode": False,
                "trace_as_input": True,
                "trace_as_metadata": True,
                "load_from_db": False,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "system_message",
                "value": "",
                "display_name": "System Message",
                "advanced": False,
                "input_types": [
                  "Message"
                ],
                "dynamic": False,
                "info": "System message to pass to the model.",
                "title_case": False,
                "type": "str",
                "_input_type": "MessageTextInput"
              },
              "temperature": {
                "trace_as_metadata": True,
                "list": False,
                "required": False,
                "placeholder": "",
                "show": True,
                "name": "temperature",
                "value": 0.1,
                "display_name": "Temperature",
                "advanced": False,
                "dynamic": False,
                "info": "Run inference with this temperature. Must by in the closed interval [0.0, 1.0].",
                "title_case": False,
                "type": "float",
                "_input_type": "FloatInput"
              }
            },
            "description": "Generate text using Groq.",
            "icon": "Groq",
            "base_classes": [
              "LanguageModel",
              "Message"
            ],
            "display_name": "Groq",
            "documentation": "",
            "custom_fields": {},
            "output_types": [],
            "pinned": False,
            "conditional_paths": [],
            "frozen": False,
            "outputs": [
              {
                "types": [
                  "Message"
                ],
                "selected": "Message",
                "name": "text_output",
                "display_name": "Text",
                "method": "text_response",
                "value": "__UNDEFINED__",
                "cache": True,
                "required_inputs": []
              },
              {
                "types": [
                  "LanguageModel"
                ],
                "selected": "LanguageModel",
                "name": "model_output",
                "display_name": "Language Model",
                "method": "build_model",
                "value": "__UNDEFINED__",
                "cache": True,
                "required_inputs": []
              }
            ],
            "field_order": [
              "input_value",
              "system_message",
              "stream",
              "groq_api_key",
              "groq_api_base",
              "max_tokens",
              "temperature",
              "n",
              "model_name",
              "output_parser"
            ],
            "beta": False,
            "legacy": False,
            "edited": False,
            "metadata": {},
            "tool_mode": False,
            "lf_version": "1.1.1"
          },
          "type": "GroqModel",
          "id": "GroqModel-V8Dm2"
        },
        "selected": False,
        "width": 320,
        "height": 672,
        "positionAbsolute": {
          "x": 2352.0688828198176,
          "y": 566.1385367527583
        },
        "dragging": False
      }
    ],
    "edges": [
      {
        "animated": False,
        "className": "not-running",
        "data": {
          "sourceHandle": {
            "dataType": "ParseData",
            "id": "ParseData-5AalP",
            "name": "text",
            "output_types": [
              "Message"
            ]
          },
          "targetHandle": {
            "fieldName": "context",
            "id": "Prompt-nAHMf",
            "inputTypes": [
              "Message",
              "Text"
            ],
            "type": "str"
          }
        },
        "id": "reactflow__edge-ParseData-5AalP{œdataTypeœ:œParseDataœ,œidœ:œParseData-5AalPœ,œnameœ:œtextœ,œoutput_typesœ:[œMessageœ]}-Prompt-nAHMf{œfieldNameœ:œcontextœ,œidœ:œPrompt-nAHMfœ,œinputTypesœ:[œMessageœ,œTextœ],œtypeœ:œstrœ}",
        "source": "ParseData-5AalP",
        "sourceHandle": "{œdataTypeœ:œParseDataœ,œidœ:œParseData-5AalPœ,œnameœ:œtextœ,œoutput_typesœ:[œMessageœ]}",
        "target": "Prompt-nAHMf",
        "targetHandle": "{œfieldNameœ:œcontextœ,œidœ:œPrompt-nAHMfœ,œinputTypesœ:[œMessageœ,œTextœ],œtypeœ:œstrœ}"
      },
      {
        "animated": True,
        "className": "running",
        "data": {
          "sourceHandle": {
            "dataType": "AstraDB",
            "id": "AstraDB-gHvII",
            "name": "search_results",
            "output_types": [
              "Data"
            ]
          },
          "targetHandle": {
            "fieldName": "data",
            "id": "ParseData-5AalP",
            "inputTypes": [
              "Data"
            ],
            "type": "other"
          }
        },
        "id": "reactflow__edge-AstraDB-gHvII{œdataTypeœ:œAstraDBœ,œidœ:œAstraDB-gHvIIœ,œnameœ:œsearch_resultsœ,œoutput_typesœ:[œDataœ]}-ParseData-5AalP{œfieldNameœ:œdataœ,œidœ:œParseData-5AalPœ,œinputTypesœ:[œDataœ],œtypeœ:œotherœ}",
        "source": "AstraDB-gHvII",
        "sourceHandle": "{œdataTypeœ:œAstraDBœ,œidœ:œAstraDB-gHvIIœ,œnameœ:œsearch_resultsœ,œoutput_typesœ:[œDataœ]}",
        "target": "ParseData-5AalP",
        "targetHandle": "{œfieldNameœ:œdataœ,œidœ:œParseData-5AalPœ,œinputTypesœ:[œDataœ],œtypeœ:œotherœ}"
      },
      {
        "animated": False,
        "className": "ran",
        "data": {
          "sourceHandle": {
            "dataType": "ChatInput",
            "id": "ChatInput-3woz5",
            "name": "message",
            "output_types": [
              "Message"
            ]
          },
          "targetHandle": {
            "fieldName": "search_input",
            "id": "AstraDB-gHvII",
            "inputTypes": [
              "Message"
            ],
            "type": "str"
          }
        },
        "id": "reactflow__edge-ChatInput-3woz5{œdataTypeœ:œChatInputœ,œidœ:œChatInput-3woz5œ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}-AstraDB-gHvII{œfieldNameœ:œsearch_inputœ,œidœ:œAstraDB-gHvIIœ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}",
        "source": "ChatInput-3woz5",
        "sourceHandle": "{œdataTypeœ:œChatInputœ,œidœ:œChatInput-3woz5œ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}",
        "target": "AstraDB-gHvII",
        "targetHandle": "{œfieldNameœ:œsearch_inputœ,œidœ:œAstraDB-gHvIIœ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}"
      },
      {
        "animated": False,
        "className": "not-running",
        "data": {
          "sourceHandle": {
            "dataType": "ChatInput",
            "id": "ChatInput-3woz5",
            "name": "message",
            "output_types": [
              "Message"
            ]
          },
          "targetHandle": {
            "fieldName": "question",
            "id": "Prompt-nAHMf",
            "inputTypes": [
              "Message",
              "Text"
            ],
            "type": "str"
          }
        },
        "id": "reactflow__edge-ChatInput-3woz5{œdataTypeœ:œChatInputœ,œidœ:œChatInput-3woz5œ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}-Prompt-nAHMf{œfieldNameœ:œquestionœ,œidœ:œPrompt-nAHMfœ,œinputTypesœ:[œMessageœ,œTextœ],œtypeœ:œstrœ}",
        "source": "ChatInput-3woz5",
        "sourceHandle": "{œdataTypeœ:œChatInputœ,œidœ:œChatInput-3woz5œ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}",
        "target": "Prompt-nAHMf",
        "targetHandle": "{œfieldNameœ:œquestionœ,œidœ:œPrompt-nAHMfœ,œinputTypesœ:[œMessageœ,œTextœ],œtypeœ:œstrœ}"
      },
      {
        "animated": False,
        "className": "not-running",
        "data": {
          "sourceHandle": {
            "dataType": "SplitText",
            "id": "SplitText-RuKuP",
            "name": "chunks",
            "output_types": [
              "Data"
            ]
          },
          "targetHandle": {
            "fieldName": "ingest_data",
            "id": "AstraDB-cu7xm",
            "inputTypes": [
              "Data"
            ],
            "type": "other"
          }
        },
        "id": "reactflow__edge-SplitText-RuKuP{œdataTypeœ:œSplitTextœ,œidœ:œSplitText-RuKuPœ,œnameœ:œchunksœ,œoutput_typesœ:[œDataœ]}-AstraDB-cu7xm{œfieldNameœ:œingest_dataœ,œidœ:œAstraDB-cu7xmœ,œinputTypesœ:[œDataœ],œtypeœ:œotherœ}",
        "source": "SplitText-RuKuP",
        "sourceHandle": "{œdataTypeœ:œSplitTextœ,œidœ:œSplitText-RuKuPœ,œnameœ:œchunksœ,œoutput_typesœ:[œDataœ]}",
        "target": "AstraDB-cu7xm",
        "targetHandle": "{œfieldNameœ:œingest_dataœ,œidœ:œAstraDB-cu7xmœ,œinputTypesœ:[œDataœ],œtypeœ:œotherœ}"
      },
      {
        "className": "not-running",
        "data": {
          "sourceHandle": {
            "dataType": "File",
            "id": "File-2Z8Wc",
            "name": "data",
            "output_types": [
              "Data"
            ]
          },
          "targetHandle": {
            "fieldName": "data_inputs",
            "id": "SplitText-RuKuP",
            "inputTypes": [
              "Data"
            ],
            "type": "other"
          }
        },
        "id": "reactflow__edge-File-2Z8Wc{œdataTypeœ:œFileœ,œidœ:œFile-2Z8Wcœ,œnameœ:œdataœ,œoutput_typesœ:[œDataœ]}-SplitText-RuKuP{œfieldNameœ:œdata_inputsœ,œidœ:œSplitText-RuKuPœ,œinputTypesœ:[œDataœ],œtypeœ:œotherœ}",
        "source": "File-2Z8Wc",
        "sourceHandle": "{œdataTypeœ:œFileœ,œidœ:œFile-2Z8Wcœ,œnameœ:œdataœ,œoutput_typesœ:[œDataœ]}",
        "target": "SplitText-RuKuP",
        "targetHandle": "{œfieldNameœ:œdata_inputsœ,œidœ:œSplitText-RuKuPœ,œinputTypesœ:[œDataœ],œtypeœ:œotherœ}",
        "animated": False
      },
      {
        "source": "HuggingFaceInferenceAPIEmbeddings-bRxhe",
        "sourceHandle": "{œdataTypeœ:œHuggingFaceInferenceAPIEmbeddingsœ,œidœ:œHuggingFaceInferenceAPIEmbeddings-bRxheœ,œnameœ:œembeddingsœ,œoutput_typesœ:[œEmbeddingsœ]}",
        "target": "AstraDB-cu7xm",
        "targetHandle": "{œfieldNameœ:œembedding_modelœ,œidœ:œAstraDB-cu7xmœ,œinputTypesœ:[œEmbeddingsœ],œtypeœ:œotherœ}",
        "data": {
          "targetHandle": {
            "fieldName": "embedding_model",
            "id": "AstraDB-cu7xm",
            "inputTypes": [
              "Embeddings"
            ],
            "type": "other"
          },
          "sourceHandle": {
            "dataType": "HuggingFaceInferenceAPIEmbeddings",
            "id": "HuggingFaceInferenceAPIEmbeddings-bRxhe",
            "name": "embeddings",
            "output_types": [
              "Embeddings"
            ]
          }
        },
        "id": "reactflow__edge-HuggingFaceInferenceAPIEmbeddings-bRxhe{œdataTypeœ:œHuggingFaceInferenceAPIEmbeddingsœ,œidœ:œHuggingFaceInferenceAPIEmbeddings-bRxheœ,œnameœ:œembeddingsœ,œoutput_typesœ:[œEmbeddingsœ]}-AstraDB-cu7xm{œfieldNameœ:œembedding_modelœ,œidœ:œAstraDB-cu7xmœ,œinputTypesœ:[œEmbeddingsœ],œtypeœ:œotherœ}",
        "animated": False,
        "className": "not-running"
      },
      {
        "source": "HuggingFaceInferenceAPIEmbeddings-7rcWz",
        "sourceHandle": "{œdataTypeœ:œHuggingFaceInferenceAPIEmbeddingsœ,œidœ:œHuggingFaceInferenceAPIEmbeddings-7rcWzœ,œnameœ:œembeddingsœ,œoutput_typesœ:[œEmbeddingsœ]}",
        "target": "AstraDB-gHvII",
        "targetHandle": "{œfieldNameœ:œembedding_modelœ,œidœ:œAstraDB-gHvIIœ,œinputTypesœ:[œEmbeddingsœ],œtypeœ:œotherœ}",
        "data": {
          "targetHandle": {
            "fieldName": "embedding_model",
            "id": "AstraDB-gHvII",
            "inputTypes": [
              "Embeddings"
            ],
            "type": "other"
          },
          "sourceHandle": {
            "dataType": "HuggingFaceInferenceAPIEmbeddings",
            "id": "HuggingFaceInferenceAPIEmbeddings-7rcWz",
            "name": "embeddings",
            "output_types": [
              "Embeddings"
            ]
          }
        },
        "id": "reactflow__edge-HuggingFaceInferenceAPIEmbeddings-7rcWz{œdataTypeœ:œHuggingFaceInferenceAPIEmbeddingsœ,œidœ:œHuggingFaceInferenceAPIEmbeddings-7rcWzœ,œnameœ:œembeddingsœ,œoutput_typesœ:[œEmbeddingsœ]}-AstraDB-gHvII{œfieldNameœ:œembedding_modelœ,œidœ:œAstraDB-gHvIIœ,œinputTypesœ:[œEmbeddingsœ],œtypeœ:œotherœ}",
        "animated": False,
        "className": "ran"
      },
      {
        "source": "Prompt-nAHMf",
        "sourceHandle": "{œdataTypeœ:œPromptœ,œidœ:œPrompt-nAHMfœ,œnameœ:œpromptœ,œoutput_typesœ:[œMessageœ]}",
        "target": "GroqModel-V8Dm2",
        "targetHandle": "{œfieldNameœ:œinput_valueœ,œidœ:œGroqModel-V8Dm2œ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}",
        "data": {
          "targetHandle": {
            "fieldName": "input_value",
            "id": "GroqModel-V8Dm2",
            "inputTypes": [
              "Message"
            ],
            "type": "str"
          },
          "sourceHandle": {
            "dataType": "Prompt",
            "id": "Prompt-nAHMf",
            "name": "prompt",
            "output_types": [
              "Message"
            ]
          }
        },
        "id": "reactflow__edge-Prompt-nAHMf{œdataTypeœ:œPromptœ,œidœ:œPrompt-nAHMfœ,œnameœ:œpromptœ,œoutput_typesœ:[œMessageœ]}-GroqModel-V8Dm2{œfieldNameœ:œinput_valueœ,œidœ:œGroqModel-V8Dm2œ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}",
        "animated": False,
        "className": "not-running"
      },
      {
        "source": "GroqModel-V8Dm2",
        "sourceHandle": "{œdataTypeœ:œGroqModelœ,œidœ:œGroqModel-V8Dm2œ,œnameœ:œtext_outputœ,œoutput_typesœ:[œMessageœ]}",
        "target": "ChatOutput-V2YFg",
        "targetHandle": "{œfieldNameœ:œinput_valueœ,œidœ:œChatOutput-V2YFgœ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}",
        "data": {
          "targetHandle": {
            "fieldName": "input_value",
            "id": "ChatOutput-V2YFg",
            "inputTypes": [
              "Message"
            ],
            "type": "str"
          },
          "sourceHandle": {
            "dataType": "GroqModel",
            "id": "GroqModel-V8Dm2",
            "name": "text_output",
            "output_types": [
              "Message"
            ]
          }
        },
        "id": "reactflow__edge-GroqModel-V8Dm2{œdataTypeœ:œGroqModelœ,œidœ:œGroqModel-V8Dm2œ,œnameœ:œtext_outputœ,œoutput_typesœ:[œMessageœ]}-ChatOutput-V2YFg{œfieldNameœ:œinput_valueœ,œidœ:œChatOutput-V2YFgœ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}",
        "animated": False,
        "className": "not-running"
      }
    ],
    "viewport": {
      "x": -1284.4805388511318,
      "y": -241.20878340329637,
      "zoom": 0.7182762288606254
    }
  },
  "description": "Load your data for chat context with Retrieval Augmented Generation.",
  "name": "Vector Store RAG",
  "last_tested_version": "1.1.1",
  "endpoint_name": None,
  "is_component": False
}

class LangFlow_Helper:
    
    def __init__(self, query, file_path):
        self.query = query
        self.file_path = file_path
        self.client = DataAPIClient(token=TOKEN)
        self.db = self.client.get_database_by_api_endpoint(
          api_endpoint=API_ENDPOINT
        )

    def get_response(self):
      TWEAKS = {
        "ChatInput-3woz5": {
          "background_color": "",
          "chat_icon": "",
          "files": "",
          "input_value": "carousel",
          "sender": "User",
          "sender_name": "User",
          "session_id": "",
          "should_store_message": True,
          "text_color": ""
        },
        "ParseData-5AalP": {
          "sep": "\n",
          "template": "{text}"
        },
        "Prompt-nAHMf": {
          "context": "",
          "question": "",
          "template": PROMPT,
        },
        "SplitText-RuKuP": {
          "chunk_overlap": 200,
          "chunk_size": 1000,
          "separator": ""
        },
        "ChatOutput-V2YFg": {
          "background_color": "",
          "chat_icon": "",
          "data_template": "{text}",
          "input_value": "",
          "sender": "Machine",
          "sender_name": "AI",
          "session_id": "",
          "should_store_message": True,
          "text_color": ""
        },
        "AstraDB-gHvII": {
          "advanced_search_filter": "{}",
          "api_endpoint": API_ENDPOINT,
          "batch_size": None,
          "bulk_delete_concurrency": None,
          "bulk_insert_batch_concurrency": None,
          "bulk_insert_overwrite_concurrency": None,
          "collection_indexing_policy": "",
          "collection_name": "test",
          "embedding_choice": "Embedding Model",
          "keyspace": "",
          "metadata_indexing_exclude": "",
          "metadata_indexing_include": "",
          "metric": "cosine",
          "number_of_results": 4,
          "pre_delete_collection": False,
          "search_filter": {},
          "search_input": "",
          "search_score_threshold": 0,
          "search_type": "Similarity",
          "setup_mode": "Sync",
          "token": TOKEN
        },
        "AstraDB-cu7xm": {
          "advanced_search_filter": "{}",
          "api_endpoint": API_ENDPOINT,
          "batch_size": None,
          "bulk_delete_concurrency": None,
          "bulk_insert_batch_concurrency": None,
          "bulk_insert_overwrite_concurrency": None,
          "collection_indexing_policy": "",
          "collection_name": "test",
          "embedding_choice": "Embedding Model",
          "keyspace": "",
          "metadata_indexing_exclude": "",
          "metadata_indexing_include": "",
          "metric": "cosine",
          "number_of_results": 4,
          "pre_delete_collection": False,
          "search_filter": {},
          "search_input": "",
          "search_score_threshold": 0,
          "search_type": "Similarity",
          "setup_mode": "Sync",
          "token": TOKEN,
        },
        "File-2Z8Wc": {
          "concurrency_multithreading": 4,
          "path": self.file_path,
          "silent_errors": False,
          "use_multithreading": False
        },
        "HuggingFaceInferenceAPIEmbeddings-bRxhe": {
          "api_key": HUGGING_FACE_TOKEN,
          "inference_endpoint": "https://api-inference.huggingface.co/models/",
          "model_name": "BAAI/bge-large-en-v1.5"
        },
        "HuggingFaceInferenceAPIEmbeddings-7rcWz": {
          "api_key": HUGGING_FACE_TOKEN,
          "inference_endpoint": "https://api-inference.huggingface.co/models/",
          "model_name": "BAAI/bge-large-en-v1.5"
        },
        "GroqModel-V8Dm2": {
          "groq_api_base": "https://api.groq.com",
          "groq_api_key": GROQ_API_KEY,
          "input_value": "",
          "max_tokens": None,
          "model_name": "llama-3.1-8b-instant",
          "n": None,
          "stream": False,
          "system_message": "",
          "temperature": 0.1
        }
      }

      result = run_flow_from_json(input_value=self.query,
                          flow=FLOW,
                          fallback_to_env_vars=True, 
                          tweaks=TWEAKS)
      
      return result[0].outputs[0].messages[0].message
    
    def delete_data(self):
      obj = Collection(database=self.db,name="test")
      
      obj.delete_all()
      
      return "Deleted Successfully"
    
    # def data_ingestion(self):