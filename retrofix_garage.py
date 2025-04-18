"""RetroFix Garage - Vintage Machine Reverse Engineering Portal"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import random
import time
import datetime
import base64
import requests
import numpy as np
from io import BytesIO
from typing import List, Dict, Any, Optional
from database_models import get_db
import database_models as models
from sqlalchemy import func

# ------ Data Models & State Management ------

class VintageMachine:
    def __init__(
        self,
        id: str,
        name: str,
        era: str,
        category: str,
        manufacturer: str,
        year: int,
        description: str,
        technical_specs: Dict[str, Any],
        components: List[Dict[str, Any]],
        challenge_description: str,
        difficulty: str,
        model_url: str
    ):
        self.id = id
        self.name = name
        self.era = era
        self.category = category
        self.manufacturer = manufacturer
        self.year = year
        self.description = description
        self.technical_specs = technical_specs
        self.components = components
        self.challenge_description = challenge_description
        self.difficulty = difficulty
        self.model_url = model_url


class UserSubmission:
    def __init__(
        self,
        user_id: str,
        machine_id: str,
        submission_date: datetime.datetime,
        engineering_notes: str,
        identified_components: List[Dict[str, Any]],
        workflow_analysis: str,
        modernization_proposal: str,
        score: Optional[float] = None,
        feedback: Optional[str] = None
    ):
        self.user_id = user_id
        self.machine_id = machine_id
        self.submission_date = submission_date
        self.engineering_notes = engineering_notes
        self.identified_components = identified_components
        self.workflow_analysis = workflow_analysis
        self.modernization_proposal = modernization_proposal
        self.score = score
        self.feedback = feedback


# ------ Sample Data ------

def get_sample_machines() -> List[VintageMachine]:
    """Get sample vintage machines."""
    return [
        VintageMachine(
            id="typewriter-royal-1920",
            name="Royal 10 Typewriter",
            era="Early 20th Century",
            category="Office Equipment",
            manufacturer="Royal Typewriter Company",
            year=1920,
            description="""
            The Royal 10 is a classic manual typewriter known for its durability and reliability.
            It features a QWERTY keyboard, ribbon ink system, and mechanical linkages that transfer
            key presses to type bars, which strike an inked ribbon against paper. The carriage moves
            with each keystroke and returns with a lever action. It represents quintessential early
            20th century office technology.
            """,
            technical_specs={
                "dimensions": "12\" x 15\" x 9\"",
                "weight": "25 lbs",
                "typing_mechanism": "Type bar",
                "characters": "44 keys, 88 characters",
                "line_spacing": "Single, 1.5, and double",
                "color_options": "Black",
                "materials": "Steel, cast iron, rubber, enamel"
            },
            components=[
                {
                    "name": "Keyboard Assembly",
                    "function": "Translates finger presses into mechanical movement",
                    "materials": "Metal, spring mechanisms",
                    "engineering_principle": "Lever action"
                },
                {
                    "name": "Type Bars",
                    "function": "Contain character stamps that strike the paper",
                    "materials": "Hardened steel",
                    "engineering_principle": "Radial arrangement for space efficiency"
                },
                {
                    "name": "Ribbon System",
                    "function": "Provides ink for character impression",
                    "materials": "Cloth ribbon, metal spool",
                    "engineering_principle": "Continuous feed with reversing mechanism"
                },
                {
                    "name": "Carriage",
                    "function": "Moves paper horizontally during typing",
                    "materials": "Steel rails and rollers",
                    "engineering_principle": "Spring-loaded linear motion"
                },
                {
                    "name": "Escapement Mechanism",
                    "function": "Controls character spacing and carriage movement",
                    "materials": "Precision gears and ratchets",
                    "engineering_principle": "Incremental ratcheting"
                },
                {
                    "name": "Platen",
                    "function": "Provides surface against which type strikes",
                    "materials": "Rubber cylinder, metal core",
                    "engineering_principle": "Rotational paper feed"
                }
            ],
            challenge_description="""
            Reverse engineer the Royal 10 typewriter focusing on the escapement mechanism 
            that controls character spacing. Explain how a single keystroke translates into 
            a character appearing on paper and the carriage moving one space. Analyze the 
            efficiency of the design and propose how modern materials or techniques could 
            improve its function while maintaining the mechanical nature.
            """,
            difficulty="Intermediate",
            model_url="https://sketchfab.com/3d-models/royal-10-typewriter-high-res-42caf7f9fb4c41c1862c87d44d1887d6"
        ),
        VintageMachine(
            id="engine-hit-miss-1915",
            name="Hit-and-Miss Engine",
            era="Industrial Revolution",
            category="Power Generation",
            manufacturer="International Harvester",
            year=1915,
            description="""
            The Hit-and-Miss engine is a type of stationary internal combustion engine that was 
            popular in the late 19th and early 20th centuries. It's characterized by its unique 
            speed control mechanism, which causes the engine to fire ("hit") only when power is 
            needed and to "miss" when at proper operating speed. These engines were widely used 
            for agricultural purposes, powering equipment like water pumps, grain mills, and 
            workshop machinery before widespread electrification.
            """,
            technical_specs={
                "power": "3-5 horsepower",
                "rpm_range": "250-600 RPM",
                "ignition": "Hot tube or spark ignition",
                "cooling": "Open water hopper cooling",
                "fuel": "Kerosene, gasoline, or natural gas",
                "weight": "400-800 lbs",
                "flywheel_diameter": "24-36 inches"
            },
            components=[
                {
                    "name": "Flywheel",
                    "function": "Stores rotational energy and maintains momentum",
                    "materials": "Cast iron",
                    "engineering_principle": "Rotational inertia"
                },
                {
                    "name": "Governor Mechanism",
                    "function": "Controls engine speed by regulating valve operation",
                    "materials": "Steel, brass components",
                    "engineering_principle": "Centrifugal force regulation"
                },
                {
                    "name": "Combustion Chamber",
                    "function": "Where fuel-air mixture combusts to produce power",
                    "materials": "Cast iron, steel",
                    "engineering_principle": "Internal combustion"
                },
                {
                    "name": "Intake/Exhaust Valves",
                    "function": "Control gas flow into and out of the combustion chamber",
                    "materials": "Hardened steel, springs",
                    "engineering_principle": "Timed valve operation"
                },
                {
                    "name": "Water Hopper",
                    "function": "Provides cooling for the engine",
                    "materials": "Cast iron",
                    "engineering_principle": "Thermosiphon cooling"
                },
                {
                    "name": "Crankshaft & Connecting Rod",
                    "function": "Converts linear piston motion to rotational motion",
                    "materials": "Forged steel",
                    "engineering_principle": "Crank-slider mechanism"
                }
            ],
            challenge_description="""
            Reverse engineer the governor mechanism of the Hit-and-Miss engine. Explain how 
            this mechanical speed control system works to maintain a steady RPM despite varying 
            loads. Analyze the efficiency of this approach compared to modern engine governing 
            systems, and propose improvements that maintain the elegance of the mechanical design 
            while enhancing reliability or efficiency. Consider how modern materials could improve 
            the existing design.
            """,
            difficulty="Advanced",
            model_url="https://sketchfab.com/3d-models/hit-and-miss-engine-c46ad37feb6d472c851d1d58f8e7d89a"
        ),
        VintageMachine(
            id="phonograph-edison-1900",
            name="Edison Standard Phonograph",
            era="Victorian Era",
            category="Entertainment",
            manufacturer="Thomas A. Edison, Inc.",
            year=1900,
            description="""
            The Edison Standard Phonograph was a popular model of phonograph manufactured from 
            1898 through the 1910s. It used wax cylinders as recording medium and was sold as 
            a home entertainment device. The phonograph works through a purely mechanical process: 
            sound waves are captured by a horn, causing a diaphragm to vibrate. These vibrations 
            move a stylus that cuts grooves into a rotating wax cylinder. For playback, this 
            process is reversed, with the stylus following the grooves and transmitting vibrations 
            back through the diaphragm and horn.
            """,
            technical_specs={
                "recording_medium": "Wax cylinders (2 minutes of audio)",
                "playback_speed": "160 RPM (hand-cranked)",
                "horn_material": "Brass or painted tin",
                "dimensions": "10\" x 12\" x 14\" (without horn)",
                "amplification": "Purely acoustic (no electrical components)",
                "playing_time": "2 minutes per cylinder",
                "cylinder_size": "4\" length, 2.25\" diameter"
            },
            components=[
                {
                    "name": "Spring Motor",
                    "function": "Provides rotational power for cylinder playback",
                    "materials": "Steel springs, brass gears",
                    "engineering_principle": "Potential energy storage in wound spring"
                },
                {
                    "name": "Governor",
                    "function": "Maintains consistent rotation speed",
                    "materials": "Brass weights, steel shaft",
                    "engineering_principle": "Centrifugal speed regulation"
                },
                {
                    "name": "Mandrel",
                    "function": "Holds and rotates the wax cylinder",
                    "materials": "Steel, brass fittings",
                    "engineering_principle": "Precision rotational mounting"
                },
                {
                    "name": "Reproducer Assembly",
                    "function": "Converts groove vibrations into sound waves",
                    "materials": "Mica diaphragm, sapphire stylus",
                    "engineering_principle": "Mechanical amplification through leverage"
                },
                {
                    "name": "Horn",
                    "function": "Amplifies and directs sound waves",
                    "materials": "Brass or painted tin",
                    "engineering_principle": "Acoustic impedance matching"
                },
                {
                    "name": "Feed Screw",
                    "function": "Moves reproducer assembly along cylinder length",
                    "materials": "Threaded steel rod",
                    "engineering_principle": "Linear translation through screw thread"
                }
            ],
            challenge_description="""
            Reverse engineer the sound reproduction system of the Edison Standard Phonograph. 
            Analyze how mechanical energy is converted to sound without any electrical components. 
            Focus on the reproducer assembly and horn design. Explain the acoustic principles at 
            work and how the designers maximized sound quality within the technological constraints. 
            Propose modifications that could improve sound quality while maintaining the purely 
            mechanical nature of the device.
            """,
            difficulty="Intermediate",
            model_url="https://sketchfab.com/3d-models/edison-standard-phonograph-replica-a5f903b93a5c4964b113295fcbc456c8"
        ),
        VintageMachine(
            id="mechanical-calculator-1940",
            name="Curta Type I Mechanical Calculator",
            era="Mid 20th Century",
            category="Computing",
            manufacturer="Contina AG Mauren",
            year=1940,
            description="""
            The Curta calculator is a remarkable mechanical calculator designed by Curt Herzstark. 
            Often called the "pepper grinder" due to its cylindrical shape and hand-crank operation, 
            it's considered one of the most elegant mechanical calculators ever created. The device 
            performs addition, subtraction, multiplication, division, and even square roots through 
            purely mechanical means. Its compact size (fitting in the palm of a hand) and precision 
            engineering made it the portable calculator of choice before electronic calculators.
            """,
            technical_specs={
                "dimensions": "2.75\" height, 2.2\" diameter",
                "weight": "8 oz",
                "capacity": "11-digit results, 8-digit input",
                "operations": "Addition, subtraction, multiplication, division",
                "materials": "Metal alloys, over 600 precision parts",
                "accuracy": "Exact to 11 digits",
                "production_period": "1947-1972"
            },
            components=[
                {
                    "name": "Input Setting Pins",
                    "function": "Allow user to input numbers for calculation",
                    "materials": "Steel pins with numbered sleeves",
                    "engineering_principle": "Vertical positioning encoding numeric values"
                },
                {
                    "name": "Crank Mechanism",
                    "function": "Initiates calculation process",
                    "materials": "Steel shaft and handle",
                    "engineering_principle": "Rotational input converted to mathematical operations"
                },
                {
                    "name": "Step Counter",
                    "function": "Counts iterations for multiplication/division",
                    "materials": "Precision gears and numeric display",
                    "engineering_principle": "Mechanical counting through gear rotation"
                },
                {
                    "name": "Result Counter",
                    "function": "Displays calculation results",
                    "materials": "Numbered drums and display windows",
                    "engineering_principle": "Digital numeric representation through physical positioning"
                },
                {
                    "name": "Tens-Carry Mechanism",
                    "function": "Handles carrying of digits during calculation",
                    "materials": "Complex gear train and carry pins",
                    "engineering_principle": "Cascading mechanical state transfer"
                },
                {
                    "name": "Complementary Number System",
                    "function": "Enables subtraction operations",
                    "materials": "Reversing gears and mechanisms",
                    "engineering_principle": "Mechanical implementation of 9's complement arithmetic"
                }
            ],
            challenge_description="""
            Reverse engineer the tens-carry mechanism of the Curta calculator. This sophisticated 
            component allows the calculator to properly "carry the one" during addition operations 
            when a column sum exceeds 9. Analyze how this mechanical system works without electronic 
            components. Explain the sequence of operations that occur during a simple addition that 
            requires carrying. Compare this approach to how modern electronic calculators handle 
            the same operation, and propose how the mechanical design could be improved with modern 
            manufacturing techniques or materials.
            """,
            difficulty="Advanced",
            model_url="https://sketchfab.com/3d-models/curta-calculator-type-i-842b9c0735c64567b34be40e0a573a6f"
        ),
        VintageMachine(
            id="water-pump-cast-iron-1890",
            name="Cast Iron Hand Water Pump",
            era="Victorian Era",
            category="Utilities",
            manufacturer="Various Local Foundries",
            year=1890,
            description="""
            Cast iron hand pumps were widespread in the late 19th century for drawing groundwater 
            from shallow wells. These simple yet reliable machines provided water for households 
            and farms before modern plumbing. The pump operates on the principle of creating a 
            vacuum to draw water upward through a pipe, then uses simple check valves to prevent 
            the water from flowing back down. The user provides power by operating the lever handle, 
            which drives an internal piston.
            """,
            technical_specs={
                "maximum_lift": "25-30 feet",
                "flow_rate": "5-10 gallons per minute with regular pumping",
                "materials": "Cast iron body, leather seals, brass fittings",
                "mounting": "Typically bolted to wooden platform over well",
                "capacity": "Varies based on water table depth and operator effort",
                "height": "30-36 inches above mounting surface",
                "weight": "40-60 lbs"
            },
            components=[
                {
                    "name": "Pump Handle",
                    "function": "Provides leverage for operating the pump",
                    "materials": "Cast iron",
                    "engineering_principle": "Class 2 lever mechanical advantage"
                },
                {
                    "name": "Pump Cylinder",
                    "function": "Contains the piston and creates suction",
                    "materials": "Cast iron, machined smooth interior",
                    "engineering_principle": "Airtight seal creates vacuum"
                },
                {
                    "name": "Piston Assembly",
                    "function": "Creates vacuum to draw water upward",
                    "materials": "Leather cup seal, metal piston",
                    "engineering_principle": "Reciprocating motion creates pressure differential"
                },
                {
                    "name": "Foot Valve",
                    "function": "One-way valve that prevents water from flowing back down",
                    "materials": "Brass or iron with leather flap",
                    "engineering_principle": "Passive one-way flow control"
                },
                {
                    "name": "Spout",
                    "function": "Directs water out of the pump for collection",
                    "materials": "Cast iron",
                    "engineering_principle": "Gravitational flow"
                },
                {
                    "name": "Connecting Rod",
                    "function": "Connects handle to piston",
                    "materials": "Wrought iron",
                    "engineering_principle": "Converts rotational motion to linear motion"
                }
            ],
            challenge_description="""
            Reverse engineer the valve and piston system of the cast iron hand pump. Explain 
            the precise sequence of events that occur during both the up and down strokes of 
            the pump handle. Analyze why this design was so effective and long-lasting despite 
            its simplicity. Consider limitations in its maximum lift capacity and explain the 
            physical principles that impose this limit. Propose modifications that could improve 
            efficiency or reduce operator effort while maintaining the non-powered mechanical nature.
            """,
            difficulty="Beginner",
            model_url="https://sketchfab.com/3d-models/old-water-pump-low-poly-game-ready-0e8ff766277241e6aa66025d426aa831"
        )
    ]


def get_sample_user_submissions() -> List[UserSubmission]:
    """Get sample user submissions."""
    return [
        UserSubmission(
            user_id="user123",
            machine_id="typewriter-royal-1920",
            submission_date=datetime.datetime(2023, 4, 15, 14, 30),
            engineering_notes="""
            The Royal 10 typewriter exemplifies early 20th century precision manufacturing. 
            The type bar mechanism uses a clever radial arrangement where each key connects to 
            a curved type bar containing the letter or symbol. When pressed, the type bar swings 
            in an arc to strike the paper against the platen.
            
            The escapement mechanism is particularly ingenious, using a ratchet and pawl system 
            that releases the carriage exactly one space after each keystroke. This design solved 
            the challenge of consistent character spacing without electronic controls.
            """,
            identified_components=[
                {
                    "name": "Type bar",
                    "function": "Carries character die that strikes the paper",
                    "engineering_principle": "Leverage and rotational movement"
                },
                {
                    "name": "Escapement wheel",
                    "function": "Controls carriage movement in precise increments",
                    "engineering_principle": "Ratcheting mechanism with controlled release"
                },
                {
                    "name": "Ribbon advance",
                    "function": "Moves ribbon to provide fresh ink surface",
                    "engineering_principle": "Unidirectional gear system with auto-reverse"
                }
            ],
            workflow_analysis="""
            The typewriter's workflow is remarkably efficient given its mechanical constraints:
            
            1. Key press initiates movement of the type bar mechanism
            2. Type bar swings in an arc toward the platen
            3. Just before impact, the escapement is triggered
            4. Character strikes ribbon against paper
            5. Escapement releases carriage to move one space
            6. Carriage spring provides return force for next character
            
            This sequence happens nearly instantaneously, allowing skilled typists to achieve 
            significant speeds. The mechanical linkages are precisely calibrated to require minimal 
            force while ensuring consistent character impression.
            """,
            modernization_proposal="""
            While maintaining the mechanical nature of the Royal typewriter, several improvements 
            could be made with modern materials and manufacturing:
            
            1. Replace cast iron frame with aircraft-grade aluminum alloy to reduce weight while 
               maintaining structural integrity
            
            2. Implement carbon fiber type bars with titanium pivots to reduce inertia and increase 
               typing speed potential
            
            3. Replace leather and felt dampers with modern synthetic polymers for longer life and 
               consistent performance across temperature ranges
            
            4. Use modern precision bearings in the carriage mechanism to reduce friction and operator effort
            
            5. Introduce a modular ribbon cartridge system for cleaner replacement while maintaining 
               the original mechanical advance mechanism
            
            These improvements would preserve the fully mechanical operation while enhancing durability, 
            reducing weight, and improving user experience.
            """,
            score=92.5,
            feedback="Excellent analysis of the escapement mechanism with thoughtful modernization proposals that respect the original design principles."
        )
    ]


def fetch_sketchfab_model_info(model_url):
    """Fetch model information from Sketchfab API."""
    # Extract model ID from URL
    try:
        model_id = model_url.split('/')[-1]
        
        # For demonstration, we're returning sample data
        # In a real implementation, this would make an actual API call
        return {
            "title": "3D Model",
            "description": "Interactive 3D model available on Sketchfab",
            "thumbnail_url": "https://static.sketchfab.com/models/42caf7f9fb4c41c1862c87d44d1887d6/thumbnails/d29e03a47add416f9af844a79e7e5c28/ce5f887e11584e1a99ade6d5fe4a488e.jpeg",
            "viewer_url": f"https://sketchfab.com/models/{model_id}/embed"
        }
    except:
        return {
            "title": "Model Information Unavailable",
            "description": "Could not retrieve model information",
            "thumbnail_url": "",
            "viewer_url": ""
        }


# ------ UI Components ------

def run_retrofix_header():
    """Display the header for RetroFix Garage module."""
    st.markdown(
        """
        <div style="background-color:#5D4037; padding:10px; border-radius:10px; margin-bottom:10px">
            <h1 style="color:white; text-align:center">
                <span style="font-size:1.5em">⚙️</span> RetroFix Garage <span style="font-size:1.5em">⚙️</span>
            </h1>
            <h3 style="color:#D7CCC8; text-align:center">Vintage Machine Reverse Engineering Portal</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_machine_card(machine: VintageMachine, expanded: bool = False):
    """Render a vintage machine card."""
    with st.container():
        # Get model info from Sketchfab
        model_info = fetch_sketchfab_model_info(machine.model_url)
        
        # Create a two-column layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if model_info.get("thumbnail_url"):
                st.image(model_info.get("thumbnail_url"), use_column_width=True)
            st.button("Explore in 3D", key=f"3d_{machine.id}")
        
        with col2:
            st.markdown(f"## {machine.name}")
            st.markdown(f"**Manufacturer:** {machine.manufacturer}")
            st.markdown(f"**Year:** {machine.year}")
            st.markdown(f"**Category:** {machine.category}")
            st.markdown(f"**Era:** {machine.era}")
            st.markdown(f"**Difficulty:** {machine.difficulty}")
            
            # View details button
            view_details = st.button("View Details", key=f"details_{machine.id}")
            if view_details:
                st.session_state.selected_machine = machine
                st.rerun()


def generate_3d_machine_model(machine_type="engine"):
    """Generate 3D model data for different machine types"""
    t = np.linspace(0, 10, 50)
    x = np.cos(t)
    y = np.sin(t)
    z = t/10

    if machine_type == "engine":
        # Create animated engine components
        cylinder = go.Cylinder(
            x=[0, 0],
            y=[0, 0],
            z=[-1, 1],
            radius=0.5,
            colorscale='Viridis',
            showscale=False
        )

        piston = go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines+markers',
            line=dict(color='red', width=4),
            marker=dict(size=8)
        )

        return [cylinder, piston]

    return []

def render_3d_model_viewer(machine: VintageMachine):
    """Render a 3D model viewer."""
    #model_info = fetch_sketchfab_model_info(machine.model_url)
    
    #if model_info.get("viewer_url"):
    #    st.markdown(f"### 3D Model: {machine.name}")
    #    st.markdown(
    #        f"""
    #        <div style="width:100%; height:500px; overflow:hidden; border-radius:10px;">
    #            <iframe src="{model_info.get('viewer_url')}" 
    #            width="100%" height="500" frameborder="0" allowfullscreen mozallowfullscreen="true" 
    #            webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" 
    #            xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share></iframe>
    #        </div>
    #        """,
    #        unsafe_allow_html=True
    #    )
    #else:
    #    st.error("3D model viewer is not available for this machine.")

    st.subheader("Interactive 3D Model")

    fig = go.Figure(data=generate_3d_machine_model("engine"))
    fig.update_layout(
        scene=dict(
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            aspectmode='data'
        ),
        width=800,
        height=600,
        showlegend=False
    )

    # Add animation
    frames = []
    for t in np.linspace(0, 2*np.pi, 20):
        frame = go.Frame(
            data=[
                go.Cylinder(
                    x=[0, 0],
                    y=[0, 0],
                    z=[-1, 1],
                    radius=0.5,
                    colorscale='Viridis',
                    showscale=False
                ),
                go.Scatter3d(
                    x=np.cos(t + np.linspace(0, 10, 50)),
                    y=np.sin(t + np.linspace(0, 10, 50)),
                    z=np.linspace(0, 1, 50),
                    mode='lines+markers',
                    line=dict(color='red', width=4),
                    marker=dict(size=8)
                )
            ]
        )
        frames.append(frame)

    fig.frames = frames

    # Add animation controls
    fig.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": True}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "type": "buttons"
        }]
    )

    st.plotly_chart(fig, use_container_width=True)

    # Interactive controls
    st.sidebar.subheader("Model Controls")
    rotation = st.sidebar.slider("Rotation", 0, 360, 180)
    zoom = st.sidebar.slider("Zoom", 0.5, 2.0, 1.0)

    # Update view based on controls
    fig.update_layout(
        scene_camera=dict(
            eye=dict(
                x=zoom * np.cos(np.radians(rotation)),
                y=zoom * np.sin(np.radians(rotation)),
                z=zoom
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)



def render_component_diagram(machine: VintageMachine):
    """Render an interactive component diagram."""
    st.markdown("### Component Diagram")
    
    # Create nodes for components
    nodes = []
    for i, component in enumerate(machine.components):
        nodes.append({
            "id": i,
            "label": component["name"],
            "title": component["function"],
            "group": i
        })
    
    # Create edges between related components
    edges = []
    for i in range(len(machine.components) - 1):
        edges.append({
            "from": i,
            "to": i + 1,
        })
    # Add one edge from last to first to create a loop
    edges.append({
        "from": len(machine.components) - 1,
        "to": 0,
    })
    
    # Create a visualization using plotly
    # We'll create a simplified visualization with plotly
    fig = go.Figure()
    
    # Add nodes as scatter points
    x_coords = [0, 1, 2, 1, 0, -1]
    y_coords = [1, 2, 1, 0, -1, 0]
    
    for i, component in enumerate(machine.components[:6]):  # Limit to 6 components for visualization
        idx = i % len(x_coords)
        fig.add_trace(go.Scatter(
            x=[x_coords[idx]],
            y=[y_coords[idx]],
            mode='markers+text',
            marker=dict(size=30, color=f'rgb({50 + i * 30}, {100 + i * 20}, {150 - i * 10})'),
            text=[component["name"]],
            textposition="bottom center",
            hoverinfo='text',
            hovertext=[f"{component['name']}: {component['function']}<br>Material: {component['materials']}<br>Principle: {component['engineering_principle']}"]
        ))
    
    # Add edges as lines
    for i in range(len(machine.components[:6]) - 1):
        idx1 = i % len(x_coords)
        idx2 = (i + 1) % len(x_coords)
        fig.add_trace(go.Scatter(
            x=[x_coords[idx1], x_coords[idx2]],
            y=[y_coords[idx1], y_coords[idx2]],
            mode='lines',
            line=dict(width=2, color='gray'),
            hoverinfo='none'
        ))
    
    # Add final edge to close the loop
    fig.add_trace(go.Scatter(
        x=[x_coords[(len(machine.components[:6]) - 1) % len(x_coords)], x_coords[0]],
        y=[y_coords[(len(machine.components[:6]) - 1) % len(x_coords)], y_coords[0]],
        mode='lines',
        line=dict(width=2, color='gray'),
        hoverinfo='none'
    ))
    
    # Update layout
    fig.update_layout(
        title="Machine Components Relationship",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        width=700
    )
    
    st.plotly_chart(fig)


def render_exploded_view(machine: VintageMachine):
    """Render an exploded view of the machine."""
    st.markdown("### Exploded View")
    
    # This would typically show an exploded view diagram
    # For our demo, we'll show a sample image and description
    
    st.markdown(f"""
    The {machine.name} consists of {len(machine.components)} main components:
    """)
    
    for i, component in enumerate(machine.components):
        with st.expander(f"{i+1}. {component['name']}"):
            st.markdown(f"**Function:** {component['function']}")
            st.markdown(f"**Materials:** {component['materials']}")
            st.markdown(f"**Engineering Principle:** {component['engineering_principle']}")


def render_technical_specifications(machine: VintageMachine):
    """Render technical specifications."""
    st.markdown("### Technical Specifications")
    
    specs_data = []
    for key, value in machine.technical_specs.items():
        specs_data.append({
            "Specification": key.replace("_", " ").title(),
            "Value": value
        })
    
    st.table(pd.DataFrame(specs_data))


def render_engineering_challenge(machine: VintageMachine):
    """Render engineering challenge."""
    st.markdown("### Engineering Challenge")
    
    st.markdown(machine.challenge_description)
    
    difficulty_color = {
        "Beginner": "#4CAF50",      # Green
        "Intermediate": "#FFC107",  # Yellow
        "Advanced": "#F44336"       # Red
    }.get(machine.difficulty, "#2196F3")  # Blue as default
    
    st.markdown(
        f"""
        <div style="background-color:{difficulty_color}; padding:5px; border-radius:5px; display:inline-block;">
            <span style="color:white; font-weight:bold;">{machine.difficulty} Difficulty</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_submission_form(machine: VintageMachine):
    """Display the challenge submission form."""
    st.markdown("## Challenge Submission")
    
    st.write(f"""
    Fill out this form to submit your reverse engineering analysis of the {machine.name}. 
    Your submission will be reviewed and feedback will be provided.
    """)
    
    # Engineering notes
    st.markdown("### Engineering Notes")
    st.write("Document your observations about the machine's design and functionality.")
    engineering_notes = st.text_area(
        "Engineering Notes",
        height=150,
        help="Describe your general observations about the machine's design, materials, and engineering principles."
    )
    
    # Component identification
    st.markdown("### Component Identification")
    st.write("Identify and describe key components you've analyzed.")
    
    component_cols = st.columns(3)
    
    component_list = []
    for i in range(3):  # Allow identifying 3 components
        with component_cols[i]:
            st.markdown(f"**Component {i+1}**")
            name = st.text_input("Name", key=f"comp_name_{i}")
            function = st.text_input("Function", key=f"comp_func_{i}")
            principle = st.text_input("Engineering Principle", key=f"comp_princ_{i}")
            
            if name and function:
                component_list.append({
                    "name": name,
                    "function": function,
                    "engineering_principle": principle
                })
    
    # Workflow analysis
    st.markdown("### Workflow Analysis")
    st.write("Describe how the machine operates step-by-step.")
    workflow_analysis = st.text_area(
        "Workflow Analysis",
        height=150,
        help="Provide a detailed analysis of how the machine works and the sequence of operations."
    )
    
    # Modernization proposal
    st.markdown("### Modernization Proposal")
    st.write("Propose improvements using modern materials or techniques.")
    modernization_proposal = st.text_area(
        "Modernization Proposal",
        height=150,
        help="Suggest how the machine could be improved while respecting its original design principles."
    )
    
    # Submit button
    submit = st.button("Submit Challenge", type="primary")
    
    if submit:
        if not engineering_notes or not component_list or not workflow_analysis or not modernization_proposal:
            st.error("Please complete all sections of the form before submitting.")
        else:
            # Create submission object
            submission = UserSubmission(
                user_id="current_user",  # In a real app, this would be the actual user ID
                machine_id=machine.id,
                submission_date=datetime.datetime.now(),
                engineering_notes=engineering_notes,
                identified_components=component_list,
                workflow_analysis=workflow_analysis,
                modernization_proposal=modernization_proposal,
                score=None,  # To be assigned after review
                feedback=None  # To be provided after review
            )
            
            # In a real app, this would save to a database
            # For our demo, we'll just show a success message
            st.success("Your submission has been received! It will be reviewed by our engineering team.")
            
            # Add a simulated delay to make it feel like processing
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Show a sample auto-feedback
            st.markdown("### Preliminary Automated Feedback")
            
            feedback_score = random.randint(80, 95)
            
            st.metric("Submission Score", f"{feedback_score}%")
            
            feedback_points = [
                "Good identification of core mechanical principles",
                "Well-structured analysis of component relationships",
                "Creative modernization proposals that respect original design",
                "Consider further analysis of material properties and stress factors"
            ]
            
            for point in feedback_points:
                st.markdown(f"- {point}")
            
            # Option to view other submissions
            st.markdown("### Compare with Other Submissions")
            if st.button("View Sample Submissions"):
                st.session_state.view_sample_submissions = True
                st.rerun()


def display_sample_submissions(machine_id: str):
    """Display sample submissions for a machine."""
    st.markdown("## Sample Submissions")
    
    sample_submissions = [s for s in get_sample_user_submissions() if s.machine_id == machine_id]
    
    if not sample_submissions:
        st.info("No sample submissions available for this machine yet.")
        return
    
    for submission in sample_submissions:
        st.markdown(f"### Submission by User (Score: {submission.score}%)")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Engineering Notes", 
            "Component Identification",
            "Workflow Analysis",
            "Modernization Proposal"
        ])
        
        with tab1:
            st.markdown(submission.engineering_notes)
        
        with tab2:
            for component in submission.identified_components:
                st.markdown(f"**{component['name']}**")
                st.markdown(f"Function: {component['function']}")
                st.markdown(f"Engineering Principle: {component['engineering_principle']}")
                st.markdown("---")
        
        with tab3:
            st.markdown(submission.workflow_analysis)
        
        with tab4:
            st.markdown(submission.modernization_proposal)
        
        # Feedback
        if submission.feedback:
            st.markdown("### Instructor Feedback")
            st.info(submission.feedback)


def display_learning_resources():
    """Display learning resources."""
    st.markdown("## Learning Resources")
    
    # Create tabs for different resource types
    tab1, tab2, tab3 = st.tabs([
        "Engineering Principles", 
        "Historical Context", 
        "Reverse Engineering Methods"
    ])
    
    with tab1:
        st.markdown("### Core Engineering Principles")
        
        principles = [
            {
                "principle": "Mechanical Advantage",
                "description": "The amplification of force achieved by using a device like a lever or pulley system.",
                "application": "Found in typewriter key mechanisms, pump handles, and many vintage tools."
            },
            {
                "principle": "Gear Systems",
                "description": "Transmitting rotational motion while changing speed, direction, or torque.",
                "application": "Clocks, mechanical calculators, and early automobiles all rely on precision gear systems."
            },
            {
                "principle": "Escapement Mechanisms",
                "description": "Controlling periodic motion by regulating the release of energy stored in a spring or weight.",
                "application": "Clocks, typewriters, and mechanical calculators use different forms of escapement."
            },
            {
                "principle": "Fluid Dynamics",
                "description": "The behavior of liquids and gases in motion, crucial for understanding pumps and engines.",
                "application": "Hit-and-miss engines, water pumps, and hydraulic systems all apply these principles."
            },
            {
                "principle": "Material Properties",
                "description": "Understanding strength, elasticity, hardness, and thermal properties of materials.",
                "application": "Every vintage machine represents choices about materials based on available technology and required properties."
            }
        ]
        
        for principle in principles:
            with st.expander(principle["principle"]):
                st.markdown(f"**Description:** {principle['description']}")
                st.markdown(f"**Application:** {principle['application']}")
    
    with tab2:
        st.markdown("### Historical Context of Vintage Machines")
        
        periods = [
            {
                "era": "Industrial Revolution (1760-1840)",
                "description": """
                The transition to new manufacturing processes using steam power and machine tools.
                This period saw the mechanization of textile production and the rise of factory systems.
                Early machine designs from this era often feature cast iron construction and steam power.
                """
            },
            {
                "era": "Age of Steam and Railways (1830-1900)",
                "description": """
                Expansion of steam technologies and the development of railway networks.
                Precision manufacturing improved, allowing for more complex mechanical systems.
                Standardization of parts began to emerge, though mass interchangeability was still limited.
                """
            },
            {
                "era": "Second Industrial Revolution (1870-1914)",
                "description": """
                Introduction of new energy sources (electricity, petroleum), new materials (steel, aluminum), and new communication technologies.
                Mass production techniques enabled more affordable and reliable mechanical devices.
                This era saw typewriters, phonographs, calculators, and other precision office machines gain popularity.
                """
            },
            {
                "era": "Interwar Period (1918-1939)",
                "description": """
                Refinement of mass production techniques and continued mechanization.
                Office machines reached maturity with high reliability and standardized designs.
                Art Deco and Streamline Moderne design aesthetics influenced machine appearance.
                """
            },
            {
                "era": "Early Electronic Era (1940-1970)",
                "description": """
                The last great era of mechanical machines before electronic technologies took over.
                Mechanical designs reached peak efficiency and sophistication.
                Many devices from this period represent the final refinement of purely mechanical solutions before electronic replacements.
                """
            }
        ]
        
        for period in periods:
            with st.expander(period["era"]):
                st.markdown(period["description"])
    
    with tab3:
        st.markdown("### Reverse Engineering Methodologies")
        
        methods = [
            {
                "method": "Functional Decomposition",
                "description": """
                Breaking down a complex system into functional subsystems and analyzing how they work together.
                
                **Steps:**
                1. Identify the primary function of the device
                2. Divide into subsystems that perform specific functions
                3. Analyze how subsystems interact
                4. Document the flow of energy, motion, or information between components
                """
            },
            {
                "method": "Motion Analysis",
                "description": """
                Studying the movement and mechanical transfers within a system.
                
                **Techniques:**
                1. Create motion diagrams showing trajectories
                2. Identify linkages and constraint mechanisms
                3. Analyze conversion between rotational and linear motion
                4. Calculate mechanical advantage at different points
                """
            },
            {
                "method": "Materials Investigation",
                "description": """
                Examining material choices to understand design decisions.
                
                **Considerations:**
                1. Why specific materials were chosen for components
                2. How material limitations influenced design
                3. How material properties relate to component function
                4. How modern materials could improve performance
                """
            },
            {
                "method": "Patent and Literature Research",
                "description": """
                Using historical documentation to understand the original design.
                
                **Resources:**
                1. Original patents often contain detailed diagrams and explanations
                2. Period literature like catalogs and user manuals
                3. Technical articles from engineering journals
                4. Repair guides and parts diagrams
                """
            },
            {
                "method": "3D Modeling and Simulation",
                "description": """
                Creating digital models to understand and test mechanical interactions.
                
                **Process:**
                1. Measure and document all components
                2. Create 3D models of individual parts
                3. Assemble digital model with proper constraints
                4. Simulate operation to visualize motion and stress points
                """
            }
        ]
        
        for method in methods:
            with st.expander(method["method"]):
                st.markdown(method["description"])


def display_machine_catalog():
    """Display the vintage machine catalog."""
    st.subheader("📚 Machine Catalog")
    
    st.write("""
    Explore our collection of vintage machines available for reverse engineering.
    Each machine comes with detailed specifications, interactive 3D models, and engineering challenges.
    """)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get unique categories and eras
        machines = get_sample_machines()
        categories = list(set(m.category for m in machines))
        categories.insert(0, "All Categories")
        
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        eras = list(set(m.era for m in machines))
        eras.insert(0, "All Eras")
        
        selected_era = st.selectbox("Filter by Era", eras)
    
    with col3:
        difficulties = ["All Difficulties", "Beginner", "Intermediate", "Advanced"]
        selected_difficulty = st.selectbox("Filter by Difficulty", difficulties)
    
    # Apply filters
    filtered_machines = machines
    
    if selected_category != "All Categories":
        filtered_machines = [m for m in filtered_machines if m.category == selected_category]
    
    if selected_era != "All Eras":
        filtered_machines = [m for m in filtered_machines if m.era == selected_era]
    
    if selected_difficulty != "All Difficulties":
        filtered_machines = [m for m in filtered_machines if m.difficulty == selected_difficulty]
    
    # Display machines as cards
    if not filtered_machines:
        st.info("No machines match your filter criteria. Please try different filters.")
    else:
        # Show results count
        st.write(f"Showing {len(filtered_machines)} machines")
        
        # Display machines in a grid
        for i in range(0, len(filtered_machines), 2):
            cols = st.columns(2)
            
            for j in range(2):
                if i + j < len(filtered_machines):
                    with cols[j]:
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="border:1px solid #ddd; border-radius:5px; padding:10px; margin-bottom:10px;">
                                    <h3>{filtered_machines[i+j].name} ({filtered_machines[i+j].year})</h3>
                                    <p><strong>Category:</strong> {filtered_machines[i+j].category}</p>
                                    <p><strong>Manufacturer:</strong> {filtered_machines[i+j].manufacturer}</p>
                                    <p><strong>Difficulty:</strong> {filtered_machines[i+j].difficulty}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            if st.button("View Details", key=f"view_{filtered_machines[i+j].id}"):
                                st.session_state.selected_machine = filtered_machines[i+j]
                                st.rerun()


def display_machine_details(machine: VintageMachine):
    """Display detailed information about a vintage machine."""
    st.markdown(f"# {machine.name} ({machine.year})")
    
    st.markdown(f"**Manufacturer:** {machine.manufacturer} | **Category:** {machine.category} | **Era:** {machine.era}")
    
    # Introduction
    st.markdown("## Introduction")
    st.markdown(machine.description)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "3D Model", 
        "Technical Specs", 
        "Component Analysis",
        "Engineering Challenge",
        "Discussions"
    ])
    
    with tab1:
        render_3d_model_viewer(machine)
    
    with tab2:
        render_technical_specifications(machine)
        render_exploded_view(machine)
    
    with tab3:
        render_component_diagram(machine)
    
    with tab4:
        render_engineering_challenge(machine)
        display_submission_form(machine)
        
        # Display sample submissions if requested
        if hasattr(st.session_state, 'view_sample_submissions') and st.session_state.view_sample_submissions:
            display_sample_submissions(machine.id)
    
    with tab5:
        st.markdown("### Discussion Forum")
        st.write("Discuss this machine with other engineers and historians.")
        
        # Sample discussions
        discussions = [
            {
                "author": "EngineeringHistorian",
                "date": "2023-04-10",
                "content": f"The {machine.name} represents a fascinating example of {machine.era} engineering principles. The use of {machine.components[0]['name']} is particularly interesting because it demonstrates how engineers solved complex problems with purely mechanical means."
            },
            {
                "author": "VintageMechanic",
                "date": "2023-04-12",
                "content": f"I've restored several {machine.name}s, and the biggest challenge is always finding replacement parts for the {machine.components[1]['name']}. Does anyone have suggestions for fabricating these with modern materials while maintaining authentic function?"
            }
        ]
        
        for discussion in discussions:
            st.markdown(
                f"""
                <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <div><strong>{discussion['author']}</strong></div>
                        <div style="color:#666;">{discussion['date']}</div>
                    </div>
                    <div>{discussion['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Comment form
        st.markdown("### Add Your Comment")
        comment = st.text_area("Your comment", height=100)
        
        if st.button("Post Comment"):
            if comment:
                st.success("Comment posted successfully!")
            else:
                st.error("Please enter a comment before posting.")
    
    # Back button
    if st.button("Back to Catalog"):
        if hasattr(st.session_state, 'selected_machine'):
            del st.session_state.selected_machine
        if hasattr(st.session_state, 'view_sample_submissions'):
            del st.session_state.view_sample_submissions
        st.rerun()


def display_user_dashboard():
    """Display the user dashboard."""
    st.subheader("👤 Your Dashboard")
    
    # Placeholder for real user data
    user_stats = {
        "challenges_completed": 2,
        "challenges_in_progress": 1,
        "average_score": 87.5,
        "achievements": ["Bronze Restorer", "Mechanical Thinker"]
    }
    
    # Display user stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Challenges Completed", user_stats["challenges_completed"])
    with col2:
        st.metric("Challenges In Progress", user_stats["challenges_in_progress"])
    with col3:
        st.metric("Average Score", f"{user_stats['average_score']}%")
    
    # Achievements
    st.markdown("### Your Achievements")
    
    for achievement in user_stats["achievements"]:
        st.markdown(
            f"""
            <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; margin-bottom:10px;">
                <div style="display:flex; align-items:center;">
                    <div style="width:40px; height:40px; background-color:#5D4037; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">
                        🏆
                    </div>
                    <div>
                        <div><strong>{achievement}</strong></div>
                        <div style="color:#666; font-size:0.9em;">Awarded for successful completion of engineering challenges</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Submissions
    st.markdown("### Your Submissions")
    
    # Sample submission data
    submissions = [
        {
            "machine_name": "Royal 10 Typewriter",
            "submission_date": "2023-04-15",
            "score": 92.5,
            "status": "Reviewed"
        },
        {
            "machine_name": "Hit-and-Miss Engine",
            "submission_date": "2023-04-02",
            "score": 82.5,
            "status": "Reviewed"
        },
        {
            "machine_name": "Curta Type I Mechanical Calculator",
            "submission_date": "2023-04-21",
            "score": None,
            "status": "In Review"
        }
    ]
    
    for submission in submissions:
        status_color = "#4CAF50" if submission["status"] == "Reviewed" else "#FFC107"
        score_display = f"{submission['score']}%" if submission["score"] is not None else "Pending"
        
        st.markdown(
            f"""
            <div style="border:1px solid #ddd; border-radius:5px; padding:10px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <div><strong>{submission['machine_name']}</strong></div>
                    <div style="background-color:{status_color}; color:white; padding:2px 8px; border-radius:12px; font-size:0.8em;">
                        {submission['status']}
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <div>Submitted: {submission['submission_date']}</div>
                    <div>Score: {score_display}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # View submission button
        st.button("View Submission", key=f"view_sub_{submission['machine_name']}")


def display_community_forum():
    """Display the community forum."""
    st.subheader("🌍 Community Forum")
    
    st.write("""
    Connect with other engineers, historians, and enthusiasts in our community forum.
    Share your experiences, ask questions, and collaborate on reverse engineering projects.
    """)
    
    # Forum categories
    categories = [
        {
            "name": "Mechanical Principles",
            "description": "Discuss the fundamental mechanical principles behind vintage machines.",
            "topics": 42,
            "posts": 187
        },
        {
            "name": "Restoration Techniques",
            "description": "Share tips and techniques for restoring vintage machinery.",
            "topics": 56,
            "posts": 324
        },
        {
            "name": "Modernization Projects",
            "description": "Showcase projects that update vintage designs with modern technology.",
            "topics": 28,
            "posts": 143
        },
        {
            "name": "Historical Context",
            "description": "Discuss the historical significance and context of vintage machines.",
            "topics": 35,
            "posts": 198
        },
        {
            "name": "3D Modeling Resources",
            "description": "Share and request 3D models of vintage machines and components.",
            "topics": 19,
            "posts": 87
        }
    ]
    
    # Display categories
    for category in categories:
        st.markdown(
            f"""
            <div style="border:1px solid #ddd; border-radius:5px; padding:10px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <div><strong>{category['name']}</strong></div>
                    <div style="color:#666; font-size:0.9em;">
                        {category['topics']} topics | {category['posts']} posts
                    </div>
                </div>
                <div>{category['description']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # View category button
        st.button("View Discussions", key=f"view_cat_{category['name']}")
    
    # Recent posts
    st.markdown("### Recent Posts")
    
    recent_posts = [
        {
            "title": "Understanding Escapement Mechanisms in Typewriters",
            "author": "MechanicalWizard",
            "date": "2023-04-22",
            "excerpt": "I've been studying the escapement mechanisms in different typewriter models, and I've noticed some fascinating design variations..."
        },
        {
            "title": "3D Printed Replacement Parts for Hit-and-Miss Engines",
            "author": "VintageRestorer",
            "date": "2023-04-20",
            "excerpt": "I've successfully designed and printed replacement governor weights for a 1915 International Harvester engine using modern materials..."
        },
        {
            "title": "Educational Value of Reverse Engineering for Engineering Students",
            "author": "ProfEngineer",
            "date": "2023-04-18",
            "excerpt": "I've been incorporating vintage machine reverse engineering into my mechanical engineering curriculum with excellent results..."
        }
    ]
    
    for post in recent_posts:
        st.markdown(
            f"""
            <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; margin-bottom:10px;">
                <div style="font-size:1.1em; font-weight:bold; margin-bottom:5px;">{post['title']}</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <div>By: {post['author']}</div>
                    <div style="color:#666;">{post['date']}</div>
                </div>
                <div>{post['excerpt']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Read more button
        st.button("Read More", key=f"read_{post['title']}")


# ------ Main Application Function ------

def run_retrofix_garage():
    """Main entry point for the RetroFix Garage application."""
    run_retrofix_header()
    
    # Sidebar with navigation
    st.sidebar.title("RetroFix Navigation")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate to:",
        ["Machine Catalog", "Learning Resources", "Your Dashboard", "Community Forum"]
    )
    
    # Different pages
    if page == "Machine Catalog":
        # Check if a machine is selected
        if hasattr(st.session_state, 'selected_machine'):
            # Display detailed view of the selected machine
            display_machine_details(st.session_state.selected_machine)
        else:
            # Display catalog
            display_machine_catalog()
    
    elif page == "Learning Resources":
        # Display learning resources
        display_learning_resources()
    
    elif page == "Your Dashboard":
        # Display user dashboard
        display_user_dashboard()
    
    elif page == "Community Forum":
        # Display community forum
        display_community_forum()


if __name__ == "__main__":
    run_retrofix_garage()