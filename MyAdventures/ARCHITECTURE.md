# Minecraft Agent System - Architecture & Game Loop

## Overview
Asynchronous game loop with concurrent agents controlled by a central DataBroker that manages message routing and schema validation.

## Core Components

### 1. DataBroker
**Responsibilities:**
- Poll messages from external chat/input
- Validate message schema
- Route messages to appropriate agents
- Collect messages from agents for broadcasting
- Maintain message queue(s)

**Interface:**
```
- async poll_chat() → Message
- async enqueue_message(agent_id, message) → bool
- async broadcast_message(message) → None
- validate_message(message) → bool
```

### 2. Agents
**Responsibilities:**
- Maintain internal state (IDLE, EXECUTING, PAUSED, etc.)
- Execute perception → decision → action cycle
- Respond to commands from DataBroker
- Send messages to DataBroker for routing

**State Machine:**
```
IDLE ←→ EXECUTING
  ↓         ↓
PAUSED    PAUSED
  ↓         ↓
 (resume) ──→
```

## Game Loop Architecture

### Event-Driven Async Loop (Recommended)

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN EVENT LOOP                          │
│                 (asyncio.gather/TaskGroup)                  │
└─────────────────────────────────────────────────────────────┘
          │
          ├─────────────────┬──────────────────┬────────────────┐
          │                 │                  │                │
      [BROKER]         [AGENT 1]           [AGENT 2]       [AGENT N]
      (Coroutine)      (Coroutine)         (Coroutine)     (Coroutine)
          │                 │                  │                │
          └─────────────────┴──────────────────┴────────────────┘
                          (Message Queue)
```

### Pseudocode - Main Loop

```python
async def game_loop():
    broker = DataBroker()
    agents = [Agent(id=i) for i in range(N)]
    
    # Run all components concurrently
    tasks = [
        broker.run(),           # Handles chat polling & routing
        *[agent.run() for agent in agents]  # Each agent's cycle
    ]
    
    await asyncio.gather(*tasks)  # Run until cancellation/error
```

---

## Message Flow Sequence

### Scenario 1: Chat Command → Agent Execution

```
TIME  │  CHAT INPUT  │  BROKER         │  AGENT          │  RESULT
──────┼──────────────┼─────────────────┼─────────────────┼─────────
T0    │ "build_x"    │                 │                 │
T1    │              │ validate()      │                 │
T2    │              │ route()         │ receive msg     │
T3    │              │                 │ state: IDLE→EXE │
T4    │              │                 │ execute task    │
T5    │              │                 │ decide action   │
T6    │              │                 │ act()           │
T7    │              │ collect_updates │ state: EXECUT...│
T8    │              │ broadcast()     │                 │
```

### Scenario 2: Agent Sends Message to Agent

```
[AGENT A] → enqueue(msg) → [BROKER] → validate → route → [AGENT B]
                           (async queue)
```

---

## Agent State Machine & Transitions

```
┌──────────┐
│   IDLE   │  ← Agent waiting for commands or tasks
└────┬─────┘
     │ receive_command(new_strategy/task)
     │ signal: EXECUTE
     ↓
┌──────────────┐
│  EXECUTING   │  ← Active perception-decide-act cycle
└────┬─────────┘
     │ (during execution)
     ├─→ receive_command(pause) → goto PAUSED
     │
     ├─→ task_complete() → goto IDLE
     │
     └─→ task_failed() → goto IDLE (+ error log)

┌────────────┐
│  PAUSED    │  ← Suspended mid-task
└─────┬──────┘
      │ receive_command(resume)
      │ or
      │ receive_command(stop) → cleanup
      ↓
   (back to appropriate state)
```

---

## Concurrency Pattern: asyncio

### Key Components

```python
# DataBroker structure
class DataBroker:
    def __init__(self):
        self.message_queue = asyncio.Queue()  # Thread-safe queue
        self.agent_messages = {}  # {agent_id: Queue}
    
    async def run(self):
        while True:
            # Concurrently handle multiple operations
            await asyncio.gather(
                self._poll_chat(),
                self._route_messages(),
                self._collect_agent_outputs()
            )
    
    async def _poll_chat(self):
        msg = await chat_service.poll()
        if msg and self.validate_message(msg):
            await self.message_queue.put(msg)
    
    async def _route_messages(self):
        try:
            msg = self.message_queue.get_nowait()
            agent_id = msg.target_agent
            await self.agent_messages[agent_id].put(msg)
        except asyncio.QueueEmpty:
            pass

# Agent structure
class Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.state = AgentState.IDLE
        self.message_queue = asyncio.Queue()
    
    async def run(self):
        while True:
            match self.state:
                case AgentState.IDLE:
                    await self._handle_idle()
                case AgentState.EXECUTING:
                    await self._execute_cycle()
                case AgentState.PAUSED:
                    await self._handle_paused()
    
    async def _execute_cycle(self):
        # Non-blocking perception-decide-act
        perception = await self._perceive()
        decision = await self._decide(perception)
        await self._act(decision)
        
        # Check for incoming commands
        try:
            cmd = self.message_queue.get_nowait()
            self._process_command(cmd)
        except asyncio.QueueEmpty:
            pass
```

---

## Critical Design Decisions

### 1. **Message Queue Strategy**
- **Per-Agent Queue**: Each agent has its own `asyncio.Queue` for targeted messages
- **Broadcast Queue**: Separate queue for system-wide broadcasts
- **Priority Levels**: Different queues for urgent vs normal messages?

### 2. **State Transition Events**
Consider these triggers:
- **External**: Commands from chat (PAUSE, RESUME, STOP, UPDATE)
- **Internal**: Task completion, error detection, goal achieved
- **Time-based**: Timeouts, periodic state checks
- **Data-driven**: Inventory changes, environment changes detected

### 3. **Synchronization Points**
Where DataBroker ensures consistency:
```
[Perception phase]  ← Broker sends environment data
[Decision phase]    ← Agent thinks (isolated)
[Action phase]      ← Agent requests actions
[Broker validates]  ← Safety check + broadcasting
```

### 4. **Error Handling & Recovery**
```
Agent error/crash → Broker detects missing heartbeat
                 → Mark agent as FAILED
                 → Notify other agents
                 → Restart or cleanup
```

---

## Loop Timing & Concurrency Model

### Option A: Tick-Based (Fixed Timestep)
```
Every 100ms:
  ├─ Broker: poll + route
  ├─ Agent 1: percieve-decide-act cycle
  ├─ Agent 2: percieve-decide-act cycle
  └─ Broker: collect outputs
  
Benefits: Deterministic, synchronized
Drawbacks: Less responsive to urgent events
```

### Option B: Event-Driven (Recommended)
```
Whenever message arrives:
  ├─ Broker validates & routes
  ├─ Target agent wakes up
  ├─ Agent processes message while executing
  └─ Async doesn't block other agents

Benefits: Responsive, efficient, naturally asynchronous
Drawbacks: Requires careful synchronization
```

### Option C: Hybrid (Best of Both)
```
Main loop:
  ├─ Event handlers: respond immediately to chat/messages
  ├─ Agent cycles: run concurrently, update every tick
  └─ Broker: coordinates between both
```

---

## Sequence: Complete Example

```
T=0ms
├─ Chat: "Agent1, build structure"
└─ DataBroker.poll_chat() receives

T=1ms  
├─ DataBroker validates schema ✓
├─ DataBroker routes to Agent1.message_queue
└─ Agent1 receives WHILE in IDLE state

T=2ms
├─ Agent1.state = EXECUTING
├─ Agent1 begins perception phase
│  └─ Query environment (non-blocking)
└─ DataBroker polls for next chat input

T=5ms
├─ Agent1._perceive() completes
├─ Agent1._decide() evaluates options
└─ DataBroker collects any agent status updates

T=10ms
├─ Agent1._act() sends action request
├─ DataBroker validates action
├─ DataBroker broadcasts result to other agents
└─ Agent2 receives environment update via broadcast queue

T=15ms
├─ Agent1 loops back (if EXECUTING)
└─ Cycle repeats every ~15ms per agent
```

---

## Implementation Checklist

- [ ] Define `AgentState` enum with all possible states
- [ ] Implement `Message` dataclass with schema validation
- [ ] Create base `Agent` abstract class with perception-decide-act structure
- [ ] Implement `DataBroker` with concurrent queue handling
- [ ] Define state transition logic (conditions triggering state changes)
- [ ] Add heartbeat/watchdog for agent health
- [ ] Implement command handlers (PAUSE, RESUME, STOP, etc.)
- [ ] Add logging at key transition points
- [ ] Handle cancellation & graceful shutdown
- [ ] Test with asyncio.TaskGroup for structured concurrency

---

## Recommended File Structure for Implementation

```
src/
├─ agents/
│  ├─ base_agent.py       (abstract Agent class)
│  ├─ builder_bot.py      (concrete agent implementation)
│  └─ explorerbot.py
├─ communication/
│  ├─ broker.py           (DataBroker implementation)
│  ├─ message.py          (Message class + validators)
│  └─ queue_manager.py    (Queue coordination)
├─ reflection/
│  ├─ message_types.py    (already exists)
│  ├─ states.py           (AgentState enum)
│  └─ events.py           (Event definitions - NEW)
└─ game_loop.py           (main entry point)
```
