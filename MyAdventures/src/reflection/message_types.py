from enum import Enum

"""
    [AGENT] -> [AGENT] internal commands
"""
class InnerCommand(Enum):
    MAP_INFO = "map"  
    BOM_REQUEST = "materials.requirements"
    INVENTORY_UPDATE = "inventory"

"""
    [USER] -> [AGENT] external that change STATE
"""
class StatusCommand(Enum):
    PAUSE_AGENT = "pause"  
    RESUME_AGENT = "resume"
    STOP_AGENT = "stop"
    UPDATE_AGENT = "update"

"""
    [USER] -> [AGENT] external that change ATRIBUTES or BEHAVIOR
"""
class PassiveCommand(Enum):
    SET_NEW_RANGE = "new_range"
    SET_NEW_STRATEGY = "new_strategy"
    SET_NEW_TEMPLATE = "new_template"

    FULFILL_BOM = "fulfill_pending_bom_materials"
    START_MAIN_ACTION = "start_main_action"

 
