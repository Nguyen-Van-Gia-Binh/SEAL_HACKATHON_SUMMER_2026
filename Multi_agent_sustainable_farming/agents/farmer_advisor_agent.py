from typing import List, Dict, Optional, Any, Callable
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from pydantic_ai import Agent, RunContext
import os
from dataclasses import dataclass
import sys
import logfire
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_model

logfire.configure(send_to_logfire='if-token-present')

model = get_model()

# Define the data models
class FarmData(BaseModel):
    """Farm agricultural data model"""
    Farm_ID: int
    Soil_pH: float
    Soil_Moisture: float
    Temperature_C: float
    Rainfall_mm: float
    Crop_Type: str
    Fertilizer_Usage_kg: float
    Pesticide_Usage_kg: float
    Crop_Yield_ton: float
    Sustainability_Score: float

class FarmerInput(BaseModel):
    """Input data provided by the farmer"""
    farm_id: Optional[int] = None
    soil_ph: Optional[float] = None
    soil_moisture: Optional[float] = None
    local_temperature: Optional[float] = None
    typical_rainfall: Optional[float] = None
    current_crop: Optional[str] = None
    land_size_hectares: Optional[float] = None
    financial_goal: Optional[str] = None
    sustainability_priority: Optional[int] = Field(None, description="Priority level for sustainability on scale 1-10")

class CropRecommendation(BaseModel):
    """Crop recommendation with expected performance"""
    crop_type: str
    suitability_score: float = Field(..., description="Score from 0-100 indicating how suitable this crop is")
    expected_yield_per_hectare: float = Field(..., description="Expected yield in tons per hectare")
    estimated_profit_per_hectare: float = Field(..., description="Estimated profit in $ per hectare")
    sustainability_impact: str = Field(..., description="Impact on sustainability (Low/Medium/High)")
    resource_requirements: Dict[str, Any] = Field(..., description="Required resources for this crop")
    implementation_plan: str = Field(..., description="Steps to implement this recommendation")

class ResourcePlan(BaseModel):
    """Resource usage plan for a recommended crop"""
    fertilizer_kg_per_hectare: float
    pesticide_kg_per_hectare: float
    water_requirements_mm: float
    labor_days_per_hectare: float
    estimated_costs_per_hectare: float

class FarmerAdvisorRecommendation(BaseModel):
    """Complete recommendation set for a farmer"""
    farm_id: Optional[int]
    land_assessment: Dict[str, Any] = Field(..., description="Assessment of land conditions")
    primary_crop_recommendation: CropRecommendation
    alternative_crop_recommendations: List[CropRecommendation]
    soil_management_plan: str
    seasonal_considerations: str
    risk_assessment: str

@dataclass
class FarmerDeps:
    farm_data: pd.DataFrame

# Define the system prompt for the agent
system_prompt = """
You are a farming advisor specializing in sustainable agriculture. Your role is to provide personalized recommendations to farmers based on their inputs, land conditions, and goals.

Use the tools provided to:
1. Process farmer inputs about land conditions and goals.
2. Suggest optimal crop types based on soil conditions and local climate.
3. Recommend precise fertilizer and pesticide application rates.
4. Provide a comprehensive recommendation combining all insights.

Ensure your recommendations are practical, sustainable, and tailored to the farmer's priorities.
"""

# Initialize the farming advisor agent
farming_agent = Agent(
    model=model,
    system_prompt=system_prompt,
    deps_type=FarmerDeps,
    retries=2
)

@farming_agent.tool
def process_farmer_inputs(ctx: RunContext[FarmerDeps], farmer_input: Dict[str, Any]) -> str:
    """
    Process farmer inputs to assess land conditions and goals.
    """
    farm_data = ctx.deps.farm_data
    if isinstance(farmer_input, str):
        try:
            farmer_input = json.loads(farmer_input)
        except Exception:
            farmer_input = {}
    farm_id = farmer_input.get("farm_id") if isinstance(farmer_input, dict) else None
    if farm_id is not None and not farm_data.empty and "Farm_ID" in farm_data:
        historical_data = farm_data[farm_data["Farm_ID"] == farm_id].to_dict(orient="records")
    else:
        historical_data = []
    return json.dumps({"farmer_input": farmer_input, "historical_data": historical_data})

@farming_agent.tool
def suggest_optimal_crops(ctx: RunContext[FarmerDeps], land_conditions: Dict[str, Any]) -> str:
    """
    Suggest optimal crop types based on soil conditions and local climate.
    """
    farm_data = ctx.deps.farm_data
    if isinstance(land_conditions, str):
        try:
            parsed = json.loads(land_conditions)
            land_conditions = parsed.get("farmer_input", parsed) if isinstance(parsed, dict) else {}
        except Exception:
            land_conditions = {}
    if not isinstance(land_conditions, dict):
        land_conditions = {}
    soil_ph = land_conditions.get("soil_ph", 6.5)
    soil_moisture = land_conditions.get("soil_moisture", 30.0)
    suitable_crops = []

    if not farm_data.empty:
        for _, row in farm_data.iterrows():
            crop = row["Crop_Type"]
            if 5.5 <= soil_ph <= 7.5 and 20 <= soil_moisture <= 50:  # Example conditions
                suitable_crops.append({
                    "crop_type": crop,
                    "fertilizer_usage": row["Fertilizer_Usage_kg"],
                    "pesticide_usage": row["Pesticide_Usage_kg"],
                    "sustainability_score": row["Sustainability_Score"]
                })
    return json.dumps(suitable_crops)

@farming_agent.tool
def recommend_application_rates(ctx: RunContext[FarmerDeps], crop_type: str, land_size: float) -> str:
    """
    Recommend precise fertilizer and pesticide application rates for a crop.
    """
    farm_data = ctx.deps.farm_data
    if farm_data.empty or "Crop_Type" not in farm_data:
        return json.dumps({"error": f"No data available for crop type: {crop_type}"})
    crop_data = farm_data[farm_data["Crop_Type"] == crop_type]
    if crop_data.empty:
        return json.dumps({"error": f"No data available for crop type: {crop_type}"})

    avg_fertilizer = crop_data["Fertilizer_Usage_kg"].mean()
    avg_pesticide = crop_data["Pesticide_Usage_kg"].mean()
    return json.dumps({
        "crop_type": crop_type,
        "fertilizer_rate_per_hectare": round(float(avg_fertilizer), 2),
        "pesticide_rate_per_hectare": round(float(avg_pesticide), 2),
        "total_fertilizer": round(float(avg_fertilizer * land_size), 2),
        "total_pesticide": round(float(avg_pesticide * land_size), 2)
    })

@farming_agent.tool
def generate_comprehensive_recommendation(ctx: RunContext[FarmerDeps], farmer_input: Dict[str, Any]) -> str:
    """
    Generate a comprehensive recommendation for the farmer.
    """
    if isinstance(farmer_input, str):
        try:
            farmer_input = json.loads(farmer_input)
        except Exception:
            farmer_input = {}
    if not isinstance(farmer_input, dict):
        farmer_input = {}

    # Process farmer inputs
    land_conditions_str = process_farmer_inputs(ctx, farmer_input)

    # Suggest optimal crops
    crop_recommendations_str = suggest_optimal_crops(ctx, farmer_input)
    try:
        crop_recs = json.loads(crop_recommendations_str)
    except Exception:
        crop_recs = []

    # Recommend application rates for the top crop
    if crop_recs:
        top_crop = crop_recs[0]["crop_type"]
        application_rates = recommend_application_rates(ctx, top_crop, float(farmer_input.get("land_size_hectares", 1.0)))
    else:
        application_rates = json.dumps({"error": "No suitable crops found"})

    return json.dumps({
        "land_conditions": json.loads(land_conditions_str),
        "crop_recommendations": crop_recs,
        "application_rates": json.loads(application_rates)
    }, indent=4)

# Example usage
# if __name__ == "__main__":
#     # Load data from the relevant CSV file
#     farm_data = pd.read_csv("d:\\Pet_projects\\Multiagent_Accenture\\Sustainable_farming_AI\\fad_tiny.csv")

#     # Initialize the agent with dependencies
#     agent = farming_agent.with_deps(FarmerDeps(farm_data=farm_data))

#     # Example farmer input
#     farmer_input = {
#         "farm_id": 1,
#         "soil_ph": 6.8,
#         "soil_moisture": 35.0,
#         "land_size_hectares": 10.0,
#         "financial_goal": "Maximize profit"
#     }

#     # Run the comprehensive recommendation tool
#     recommendation = agent.run_tool("generate_comprehensive_recommendation", farmer_input=farmer_input)

#     # Print the recommendation
#     print(json.dumps(recommendation, indent=4))