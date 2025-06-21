import json
from typing import Dict, Callable, Any
from pydantic import BaseModel
from .chat_agent import llm
from .functions import get_order, get_orders, update_profile




class Agent:
    def __init__(
            self,
            user_id: str,
            message: str,
            function_descriptions: Dict[str, str],
            function_schemas: Dict[str, BaseModel],
            function_inputs: Dict[str, Dict[str, str]],
            function_registry: Dict[str, Callable[..., Any]]
    ):
        self.user_id = user_id
        self.message = message
        self.function_descriptions = function_descriptions
        self.function_schemas = function_schemas
        self.function_inputs = function_inputs
        self.function_registry = function_registry
        self.full_prompt = f"{message}"
        self.user_id = user_id
        self.function_name = ""
        self.inputs = {}
        self.initial_prompt = ""
        self.function_result = {}
        self.error = ""

    def run(self) -> dict:
        """
        Run the agent to process the message and return the response data.
        """
        self._log("Received request", self.full_prompt)
        if not self._detect_intent():
            return self._response()

        if not self._extract_inputs():
            return self._response()

        if not self._validate_inputs():
            return self._response()

        if not self._execute_function():
            return self._response()

        return self._response()
        
    def _log(self, label, data):
        """
        Log messages for debugging purposes.
        """
        print(f"[CHAT] {label}: {json.dumps(data, indent=2) if not isinstance(data, str) else data}", flush=True)


    def _detect_intent(self) -> bool:
        """
        Detect the intent of the user message.
        """
        result = self.get_intent(self.full_prompt)
        self._log("Intent detected", result)

        try:
            result = json.loads(result)
            self.function_name = result.get("function")
            return self.function_name in self.function_descriptions
        except json.JSONDecodeError as e:
            self.error = f"JSON decode error: {e}"
            return False
        
    def _extract_inputs(self) -> bool:
        """
        Extract function inputs from the user message.
        """
        inputs_result = self.get_function_inputs(self.full_prompt, self.function_name)
        self._log("Function inputs", inputs_result)

        try:
            self.inputs = json.loads(inputs_result)
            return True
        except json.JSONDecodeError as e:
            self.error = f"JSON decode error: {e}"
            return False
        
    def _validate_inputs(self) -> bool:
        """
        Validate the extracted inputs against the function schema.
        """
        is_valid = self.check_inputs(self.function_name, self.inputs)
        if not is_valid:
            self.error = "Invalid inputs for the function"
        return is_valid
    
    def _execute_function(self) -> bool:
        """
        Execute the function with the validated inputs.
        """
        try:
            self.function_result = self.execute_function(self.function_name, self.inputs)
            self._log("Function result", self.function_result)
            return True
        except Exception as e:
            self.error = f"Error executing function: {e}"
            return False
        
    def _response(self) -> dict:
        """
        Generate the final response data.
        """
        response_data = {
            "function_name": self.function_name,
            "inputs": self.inputs,
            "initial_prompt": self.initial_prompt,
            "function_result": self.function_result,
            "error": self.error
        }
        print(response_data, flush=True)
        response = self.final_ai_output(
            self.function_name,
            self.inputs,
            self.initial_prompt,
            self.function_result,
            self.error
        )
        return response


    def get_intent(self, prompt: str)->dict:
        """
        Determine the intent of the user input based on the provided prompt.
        """
        system_instruction = (
        "You are an AI assistant that helps route user queries to backend functions. "
        "Your job is to extract the correct function name from the user's message "
        "based on the available functions. Respond only with a JSON like: "
        "{\"function\": \"function_name\"}."
        )
        full_prompt = (
        f"{system_instruction}\n\n"
        f"User input: {prompt}\n\n"
        f"Available functions:\n{json.dumps(self.function_descriptions, indent=2)}"
        )
        try:
            response = llm.invoke(full_prompt)
            print(f"[DEBUG] Response from LLM: {response.content}")
            return response.content.strip()  # Assuming the response is a JSON string
        except Exception as e:
            print(f"[ERROR] Error determining intent: {e}")
            return {"error": str(e)}
        

    def get_function_inputs(self, prompt: str, function_name: str) -> dict:
        input_schema = json.dumps(self.function_inputs[function_name], indent=2)
        system_instruction = (
            "You are an AI assistant that extracts structured input data from user messages. "
            "Use the schema provided and return a valid JSON dictionary only. Do not explain. "
            "Do not mix up user_id with any other *_id. It is normal that the user may not provide complete or correct input."
        )
        input_prompt = (
            f"{system_instruction}\n\n"
            f"The user_id {self.user_id} said: \"{prompt}\"\n\n"
            f"The function to call is: {function_name}\n"
            f"The function expects the following inputs:\n{input_schema}\n\n"
            f"⚠️ If the function input schema is empty (i.e. the function does not require any inputs), then output ONLY this: {{}} — nothing else.\n"
            f"⚠️ DO NOT include any keys like 'user_id', 'args', 'input', 'input_args', or any others.\n"
            f"✅ If the function does require inputs, output them in a valid flat JSON object format (no explanation, no comments).\n\n"
            f"Now generate the input arguments in JSON format."
        )

        print("[DEBUG] Generating function inputs with prompt:", input_prompt)
        try:
            response = llm.invoke(input_prompt)
            print("[DEBUG] got inputs: ", response.content)
            
            return response.content.strip()  # Assuming the response is a JSON string
        except Exception as e:
            return {"error": f"Input extraction failed: {str(e)}"}



    def check_inputs(self, function_name: str, inputs: dict) -> bool:
        """
        Validate the inputs against the expected schema for the given function.
        """
        schema = self.function_schemas.get(function_name.strip())
        print(f"[DEBUG] Validating inputs for function '{function_name}': {inputs}")
        print(f"[DEBUG] Using schema: {schema}")
        # If no schema is found for the function, return False
        if not schema:
            return False
        
        try:
            schema(**inputs)  # This will raise an error if inputs are invalid
            return True
        except Exception as e:
            print(f"[ERROR] Input validation failed for {function_name}: {e}")
            return False
        

    def execute_function(self, function_name: str, inputs: dict) -> dict:
        """
        Execute a registered function using unpacked keyword arguments.
        """
        print(f"[DEBUG] Executing function '{function_name}' with inputs: {inputs}")
        
        func = self.function_registry.get(function_name)
        if not func:
            return {"error": f"Function '{function_name}' not found."}

        try:
            return func(**inputs)
        except TypeError as e:
            return {"error": f"Invalid arguments for function '{function_name}': {str(e)}"}
        

    def final_ai_output(self, function_name: str, inputs: dict, initial_prompt: str, function_result: dict, error: str) -> str:
        """
        Format the final AI output including function name, inputs, and response.
        """
        system_instruction = (
            "You are a helpful AI assistant. Based on the user's request, the system has determined the function to execute, "
            "its inputs, and the output from the backend. Now, write a natural, human-friendly message summarizing the result. "
            "If there was an error, politely explain it and suggest a rephrase, but only based on what the user said, do not mention the actual error "
        )

        prompt = f"{system_instruction}\n\n"
        prompt += f"User said: \"{initial_prompt}\"\n\n"
        prompt += f"Function to call: {function_name}\n"
        prompt += f"Inputs: {json.dumps(inputs, indent=2)}\n\n"
        prompt += f"Function result: {json.dumps(function_result, indent=2)}\n\n"
        
        if error:
            prompt += f"Error: {error}\n\n"

        prompt += "Now generate a final response for the user, in natural language."

        try:
            response = llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            return str(e)
