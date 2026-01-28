from command_pattern import CommandPattern, AgentCommandSet
from MyAdventures.src.command_related.command_registry import AgentNames

EXPLORER_COMMANDS = AgentCommandSet(
    agent_name=AgentNames.EXPLORER,
    agent_class_name="ExplorerBot",
    commands=[
        CommandPattern(
            command_name="set_range",
            description="Set exploration range",
            args_schema={
                "range": {"type": "integer", "optional": False}
            },
            example="explorer set_range 50"
        ),
        CommandPattern(
            command_name="start",
            description="Start exploration",
            args_schema={
                "x": {"type": "integer", "optional": True},
                "z": {"type": "integer", "optional": True},
                "range": {"type": "integer", "optional": True}
            },
            example="explorer start x=100 z=200 range=50"
        ),
        CommandPattern(
            command_name="pause",
            description="Pause exploration",
            args_schema={},
            example="explorer pause"
        ),
        CommandPattern(
            command_name="resume",
            description="Resume exploration",
            args_schema={},
            example="explorer resume"
        ),
        CommandPattern(
            command_name="stop",
            description="Stop exploration",
            args_schema={},
            example="explorer stop"
        ),
        CommandPattern(
            command_name="status",
            description="Request exploration report",
            args_schema={},
            example="explorer status"   
        )
    ]
)

BUILDER_COMMANDS = AgentCommandSet(
    agent_name=AgentNames.BUILDER,
    agent_class_name="BuilderBot",
    commands=[
        CommandPattern(
            command_name="set_plan",
            description="Set building plan",
            args_schema={
                "plan_name": {"type": "string", "optional": False, "enum": ["house", "bridge", "tower"]},
            },
            example="builder set_plan house"
        ),
            CommandPattern(
            command_name="plan_list",
            description="List available building plans",
            args_schema={},
            example="builder plan_list"
        ),
        CommandPattern(
            command_name="build",
            description="Start building",
            args_schema={},
            example="builder build"
        ),
        CommandPattern(
            command_name="bom",
            description="Request Bill of Materials",
            args_schema={},
            example="builder bom"
        ),
        CommandPattern(
            command_name="pause",
            description="Pause building",
            args_schema={},
            example="builder pause"
        ),
        CommandPattern(
            command_name="resume",
            description="Resume building",
            args_schema={},
            example="builder resume"
        ),
        CommandPattern(
            command_name="stop",
            description="Stop building",
            args_schema={},
            example="builder stop"
        ),
        CommandPattern(
            command_name="status",
            description="Request building report",
            args_schema={},
            example="builder status"   
        )
    ]
)

MINER_COMMANDS = AgentCommandSet(
    agent_name=AgentNames.MINER,
    agent_class_name="MinerBot",
    commands=[
        CommandPattern(
            command_name="set_strategy",
            description="Set mining strategy",
            args_schema={
                "strategy": {"type": "string", "optional": False, "enum": ["vertical_mining", "grid_mining"]},
            },
            example="miner set_strategy vertical_mining"
        ),
        CommandPattern(
            command_name="start",
            description="Start mining operation",
            args_schema={
                "x": {"type": "int", "optional": True},
                "z": {"type": "int", "optional": True},
                "y": {"type": "int", "optional": True}
            },
            example="miner start x=0 y=0 z=0"
        ),
        CommandPattern(
            command_name="pause",
            description="Pause mining",
            args_schema={},
            example="miner pause"
        ),
        CommandPattern(
            command_name="resume",
            description="Resume mining",
            args_schema={},
            example="miner resume"
        ),
        CommandPattern(
            command_name="stop",
            description="Stop mining",
            args_schema={},
            example="miner stop"
        ),
        CommandPattern(
            command_name="status",
            description="Request mining report",
            args_schema={},
            example="miner status"   
        )
    ]
)
