
def functions_format() -> list:
	
	my_execution_tools = glm.Tool(
	    function_declarations = [
	        glm.FunctionDeclaration(
	            name='question',
	            description="""A Python shell. Use this to execute python commands. Input should be a valid python
            command and you should print result with `print(...)` to see the output.""",
	            parameters=glm.Schema(
	                type=glm.Type.OBJECT,
	                properties={
	                	'command': glm.Schema(type=glm.Type.STRING)
	                },
	                required=['command']
	            )
	        ),

	        glm.FunctionDeclaration(
	            name='search',
	            description="The action will search this entity name on Wikipedia and returns the first 10 sentences if it exists. If not, it will return some related entities to search next.",
	            parameters=glm.Schema(
	                type=glm.Type.OBJECT,
	                properties={
	                    'entity': glm.Schema(type=glm.Type.STRING),
	                    'count': glm.Schema(type=glm.Type.NUMBER)
	                },
	                required=["entity"],
	            )
	        ),

	        glm.FunctionDeclaration(
	        name="finish",
	        description="""use this to signal that you have finished all your goals and remember show your
	        results""",
	        parameters=glm.Schema(
	          type=glm.Type.OBJECT,
	          properties={
	            'response': glm.Schema(type=glm.Type.STRING),
	          },
	          required=["response"]
	        )
	      )
	    ]
	)

	return my_execution_tools