from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer
from typing import Annotated, Dict, List, Any
from typing_extensions import TypedDict
from langgraph.types import interrupt
from pydantic import ValidationError
from dataclasses import dataclass
import logfire
import asyncio
import sys
import os
import uuid
import pandas as pd


# Import the message classes from Pydantic AI
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter
)

# Import the agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.info_gathering_agent import info_gathering_agent

from agents.final_planner_agent import final_planner_agent

from agents.sustainability_optimizer_agent import sustainability_agent, FarmingDeps
from agents.farmer_advisor_agent import farming_agent, FarmerDeps
from agents.market_intelligence_agent import market_agent, MarketDeps

logfire.configure(send_to_logfire='if-token-present')

import operator

# Define the state for our graph --  DONE
class FarmState(TypedDict):
    # Chat messages and details
    user_input: str
    all_details_given: bool
    farmer_advisor: List[Dict[str, Any]]
    market_researcher: List[Dict[str, Any]]
    messages: Annotated[List[bytes], operator.add]
    
    farming_details: Dict[str, Any]

    # User preferences
    user_id: str
    
    # Results from each agent
    sustainability_optimizer_results: str
    farmer_advisor_results: str
    market_intelligence_results: str
    
    # Final summary
    final_plan: str

# Node functions for the graph

def safe_write(writer, text: str):
    """Safely write to stream writer if available and callable."""
    if callable(writer):
        try:
            writer(text)
        except Exception:
            pass

# Info gathering node
async def gather_info(state: FarmState, writer=None) -> Dict[str, Any]:
    """Gather necessary information from the user and datasets."""
    print("Entering gather_info")
    user_input = state.get("user_input", "")
    all_details_given = state.get("all_details_given", False)

    # Auto-load sample datasets if not already provided (e.g. when testing in LangGraph Studio)
    farmer_advisor = state.get("farmer_advisor", [])
    market_researcher = state.get("market_researcher", [])

    if not farmer_advisor:
        sample_farm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_dataset", "farmer_advisory_dataset.csv")
        if os.path.exists(sample_farm_path):
            farmer_advisor = pd.read_csv(sample_farm_path).to_dict(orient="records")
            state["farmer_advisor"] = farmer_advisor

    if not market_researcher:
        sample_market_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_dataset", "market_research_dataset.csv")
        if os.path.exists(sample_market_path):
            market_researcher = pd.read_csv(sample_market_path).to_dict(orient="records")
            state["market_researcher"] = market_researcher

    if farmer_advisor and market_researcher:
        all_details_given = True
        state["all_details_given"] = True

    if not all_details_given:
        response_message = "Please upload both the Farmer Advisor and Market Researcher data files to proceed."
        print("Details not provided. Requesting more information.")
        return {
            "farming_details": {"response": response_message, "all_details_given": False},
            "messages": []
        }

    # Get the message history into the format for Pydantic AI
    message_history: list[ModelMessage] = []
    for message_row in state.get('messages', []):
        if isinstance(message_row, str):
            message_row = message_row.encode('utf-8')
        try:
            message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))
        except Exception:
            pass
    
    # Call the info gathering agent
    try:
        result = await info_gathering_agent.run(user_input, message_history=message_history)
        farming_details = result.data
        if hasattr(farming_details, "response") and farming_details.response:
            safe_write(writer, farming_details.response)
        farming_details_dict = farming_details.model_dump() if hasattr(farming_details, "model_dump") else {"response": str(farming_details)}
        new_msgs = [result.new_messages_json()]
    except Exception as e:
        print("Error during info_gathering_agent.run:", e)
        farming_details_dict = {"response": "All datasets and details loaded successfully."}
        new_msgs = []
        
    # Update the state with the gathered details
    state["farming_details"] = farming_details_dict
    state["all_details_given"] = True

    return {
        "farming_details": farming_details_dict,
        "farmer_advisor": state.get("farmer_advisor", []),
        "market_researcher": state.get("market_researcher", []),
        "all_details_given": True,
        "messages": new_msgs
    }



############################ AGENT CALLS #################################

# Sustainability recommendation node -- DONE
async def get_sustainability_optimization_recommendations(state: FarmState, writer=None) -> Dict[str, Any]:
    """Get sustainability_optimization recommendations based on provided details."""
    safe_write(writer, "\n#### Getting sustainability_optimization recommendations...\n")
    farming_details = state["farming_details"]
    farmer_advisor = state['farmer_advisor']
    reduction_target = 0.15

    # Prepare the prompt for the activity agent
    sustainability_dependencies = FarmingDeps(
            farm_data=farmer_advisor
        ) 
    # Create the user prompt
    user_prompt = f"""
    I need you to analyze farm data and provide sustainability optimization recommendations.    
    Then, analyze the correlations between different farming practices and sustainability scores. Take these details into consideration: {farming_details}

    Provide sustainability recommendations for all farms in the dataset.
    Aim for approximately {reduction_target * 100:.0f}% reduction in fertilizer and pesticide usage if possible,
    while maintaining crop yield.

    For each recommendation, include:
    1. Optimal fertilizer and pesticide usage levels
    2. Estimated impact on sustainability score and crop yield
    3. Soil management recommendations
    4. Clear rationale for your recommendations
    
    Please format your analysis as a structured report with clear sections.
    """
    # Run the agent
    results = await sustainability_agent.run(user_prompt, deps=sustainability_dependencies)
    
    # Print results
    return {"sustainability_optimizer_results": results.data}

# Farming recommendation node -- DONE
async def get_farmer_advisor_recommendations(state: FarmState, writer=None) -> Dict[str, Any]:
    """Get farming advisory recommendations based on travel details."""
    safe_write(writer, "\n#### Getting farming recommendations...\n")
    farming_details = state["farming_details"]
    farmer_advisor = state['farmer_advisor']

    # Create hotel dependencies (in a real app, this would come from user preferences)
    farm_df = pd.DataFrame(farmer_advisor) if isinstance(farmer_advisor, list) else farmer_advisor
    farming_dependencies = FarmerDeps(
            farm_data=farm_df
        )
    
    # Prepare the prompt for the hotel agent
    user_prompt = f"""
    Generate comprehensive recommendation using the provided data. Take these details into consideration: {farming_details}
    """
    # Call the farming_agent agent
    result = await farming_agent.run(user_prompt, deps=farming_dependencies)
    
    # Return the farming recommendations
    return {"farmer_advisor_results": result.data}

# Market_intelligence recommendation node -- DONEs
async def get_market_intelligence_recommendations(state: FarmState, writer=None) -> Dict[str, Any]:
    """Get market research recommendations based on travel details."""
    safe_write(writer, "\n#### Getting market research...\n")
    farming_details = state["farming_details"]
    market_researcher = state["market_researcher"]
    
    # Prepare the prompt for the activity agent
    market_df = pd.DataFrame(market_researcher) if isinstance(market_researcher, list) else market_researcher
    market_dependencies = MarketDeps(
            market_data=market_df
        )    
    
    user_prompt = f"""
    Give me extensive market research using the provided data. Take these details into consideration: {farming_details}
    """
    # Call the activity agent
    result = await market_agent.run(user_prompt, deps=market_dependencies)
    
    # Return the activity recommendations
    return {"market_intelligence_results": result.data}

###########################################################################



# Final planning node - DONE
async def create_final_plan(state: FarmState, writer=None) -> Dict[str, Any]:
    """Create a final agriculture plan based on all recommendations."""
    farming_details = state["farming_details"]
    sustainability_optimizer_results = state["sustainability_optimizer_results"]
    farmer_advisor_results = state["farmer_advisor_results"]
    market_intelligence_results = state["market_intelligence_results"]
    
    # Prepare the prompt for the final planner agent
    prompt = f"""
    I'm in need of innovative solutions that promote sustainability, optimize resource usage, and improve the livelihoods of farmers,
    bringing together different stakeholders in agriculture—farmers, weather stations, and agricultural experts—to work collaboratively 
    for the optimization of farming practices.
    Additional details: {farming_details}

    Here are the sustainability optimizer recommendations:
    {sustainability_optimizer_results}
    
    Here are the enhanced farmer advisor recommendations:
    {farmer_advisor_results}
    
    Here are the market intelligence recommendations:
    {market_intelligence_results}
    
    The goals is to reduce environmental impact of farming: Promote practices that lower the carbon footprint, minimize water consumption,
    and reduce soil erosion
    Please create a comprehensive plan based on these recommendations.
    """
    
    # Call the final planner agent
    async with final_planner_agent.run_stream(prompt) as result:
        # Stream partial text as it arrives
        async for chunk in result.stream_text(delta=True):
            safe_write(writer, chunk)
    
    # Return the final plan
    data = await result.get_data()
    return {"final_plan": data}

# Conditional edge function to determine next steps after info gathering - DONE
def route_after_info_gathering(state: FarmState):
    """Determine what to do after gathering information."""
    # farming_details = state["farming_details"]
    
    # If all details are not given, we need more information
    print("all_details_given for loop decision: ",state.get("all_details_given", False))
    if not state.get("all_details_given", False):
        return "get_next_user_message"
    # if not state["all_details_given"]:
    #     return "get_next_user_message"
    # If all details are given, we can proceed to parallel recommendations
    # Return a list of Send objects to fan out to multiple nodes
    return ["get_sustainability_optimization_recommendations", "get_farmer_advisor_recommendations", "get_market_intelligence_recommendations"]

# Interrupt the graph to get the user's next message - DONE
def get_next_user_message(state: FarmState):
    value = interrupt({})

    # Set the user's latest message for the LLM to continue the conversation
    return {
        "user_input": value
    }    

# Build the graph - DONE
def build_farming_agent_graph():
    """Build and return the agent graph."""
    # Create the graph with our state
    graph = StateGraph(FarmState)
    
    # Add nodes
    graph.add_node("gather_info", gather_info)
    graph.add_node("get_next_user_message", get_next_user_message)
    graph.add_node("get_sustainability_optimization_recommendations", get_sustainability_optimization_recommendations)
    graph.add_node("get_farmer_advisor_recommendations", get_farmer_advisor_recommendations)
    graph.add_node("get_market_intelligence_recommendations", get_market_intelligence_recommendations)
    graph.add_node("create_final_plan", create_final_plan)
    
    # Add edges
    graph.add_edge(START, "gather_info")
    
    # Conditional edge after info gathering
    graph.add_conditional_edges(
        "gather_info",
        route_after_info_gathering,
        ["get_next_user_message", "get_sustainability_optimization_recommendations", 
         "get_farmer_advisor_recommendations", "get_market_intelligence_recommendations"]
    )

    # After getting a user message (required if not enough details given), route back to the info gathering agent
    graph.add_edge("get_next_user_message", "gather_info")
    
    # Connect all recommendation nodes to the final planning node
    graph.add_edge("get_sustainability_optimization_recommendations", "create_final_plan")
    graph.add_edge("get_farmer_advisor_recommendations", "create_final_plan")
    graph.add_edge("get_market_intelligence_recommendations", "create_final_plan")
    
    # Connect final planning to END
    graph.add_edge("create_final_plan", END)
    
    # Compile the graph
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

# Create the agent graph - DONE
farming_agent_graph = build_farming_agent_graph()

# Function to run the agent - DONE
async def run_farm_agent(user_input: str):
    """Run the agent with the given user input."""
    # Initialize the state with user input
    initial_state = {
        "user_input": user_input,
        "all_details_given": False,
        "farmer_advisor": [],
        "market_researcher": [],
        "messages": [],
        "farming_details": {},
        "user_id": str(uuid.uuid4()),
        "sustainability_optimizer_results": "",
        "farmer_advisor_results": "",
        "market_intelligence_results": "",
        "final_plan": ""
    }
    
    # Run the graph
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = await farming_agent_graph.ainvoke(initial_state, config=config)
    
    # Return the final plan
    return result.get("final_plan", "")

async def main():
    # Example user input
    user_input = "I want a data driven solution for sustainable farming. Please provide a curated plan according to the data provided."
    
    # Run the agent
    final_plan = await run_farm_agent(user_input)
    
    # Print the final plan
    print("Final Plan:")
    print(final_plan)

# Example usage
if __name__ == "__main__":
    asyncio.run(main())
