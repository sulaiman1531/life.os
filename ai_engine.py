import os
from dotenv import load_dotenv
from memory_store import memory
import models

load_dotenv()

def process_intent_with_llm(user_input: str, db, user_id) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"response": "API Key missing. Cannot use agent.", "intent": "error"}

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        from langchain.tools import tool
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        
        @tool
        def create_task(title: str, priority: str = "medium") -> str:
            """Creates a new task in the user's todo list. Priority should be low, medium, or high."""
            db_task = models.Task(title=title, priority=priority, user_id=user_id)
            db.add(db_task)
            db.commit()
            return f"Task '{title}' created successfully."

        @tool
        def create_note(title: str, content: str) -> str:
            """Creates a new note."""
            db_note = models.Note(title=title, content=content, owner_id=user_id)
            db.add(db_note)
            db.commit()
            return f"Note '{title}' created successfully."
            
        @tool
        def log_finance(title: str, amount: float, tx_type: str) -> str:
            """Logs a financial transaction. tx_type must be 'in' or 'out'."""
            db_tx = models.FinanceTransaction(title=title, amount=amount, type=tx_type, owner_id=user_id)
            db.add(db_tx)
            db.commit()
            return f"Transaction '{title}' for ${amount} logged."

        @tool
        def schedule_block(title: str, start_time: str, end_time: str, date: str) -> str:
            """Schedules a time block in the planner. start_time and end_time format: HH:MM. date format: YYYY-MM-DD."""
            db_block = models.PlannerBlock(title=title, start_time=start_time, end_time=end_time, date=date, owner_id=user_id)
            db.add(db_block)
            db.commit()
            return f"Block '{title}' scheduled from {start_time} to {end_time}."

        # RAG Memory
        context_results = memory.search_memory(user_input, k=3)
        context_str = "\n".join(context_results) if context_results else "No relevant past memories."

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        
        tools = [create_task, create_note, log_finance, schedule_block]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are Jarvis, the advanced AI layer of 'LIFE OS'. Assist the user in managing their life. Use tools to create tasks, log finances, or schedule planner blocks if the user asks. If no tools are needed, answer conversationally. Be concise and friendly.\n\nPAST MEMORIES CONTEXT: {context_str}"),
            ("human", "{user_input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        result_output = agent_executor.invoke({
            "user_input": user_input,
            "context_str": context_str
        })
        
        result = result_output.get("output", str(result_output))
        
        # Save chat to memory implicitly
        memory.add_memory(f"User: {user_input}. Jarvis: {result}")
        
        return {"response": result, "intent": "agent_action"}

    except Exception as e:
        print("Agent Error:", e)
        return {"response": f"An error occurred: {str(e)}", "intent": "error"}
