# Multi Agent Architecture — Nemotron-Ultra-550B

*Generated in 25.3s*

# SLACKWATER — MULTI-AGENT COORDINATION ARCHITECTURE
## Complete Technical Design for 5-20 Simultaneous AI Agents

---

## 1. AGENT MESSAGE BUS PROTOCOL

### 1.1 Core Data Structures

```lua
-- ============================================================
-- MESSAGE BUS TYPES (shared between Luau client & Cloudflare Worker)
-- ============================================================

export type AgentId = string  -- "agent:voyager:001" | "player:user123"
export type MessageId = string  -- UUID v7 (timestamp-sortable)
export type CorrelationId = string  -- links request/response chains

export type MessagePriority = "critical" | "high" | "normal" | "low" | "background"

export type MessageType =
    -- Coordination
    | "task_proposal"        -- "I can do X, who wants it?"
    | "task_claim"           -- "I'll take X"
    | "task_delegate"        -- "You do X, I'll do Y"
    | "task_complete"        -- "X is done, result: ..."
    | "task_failed"          -- "X failed: reason"
    | "help_request"         -- "Need assistance with X"
    | "help_response"        -- "Coming to help" / "Can't help"
    
    -- State Sync
    | "state_broadcast"      -- Periodic: position, inventory, current_task
    | "state_query"          -- "Where are you? What are you holding?"
    | "state_response"       -- Answer to query
    | "world_delta"          -- "Block placed at X", "Resource depleted at Y"
    
    -- Perception
    | "screenshot_request"   -- "Take screenshot of region X"
    | "screenshot_result"    -- Base64 + analysis
    | "vision_alert"         -- "I see problem X at location Y"
    
    -- Social/Player-facing
    | "agent_chat"           -- Agent-to-agent chatter (player can overhear)
    | "player_directive"     -- Player command to agent
    | "agent_report"         -- Agent status update to player
    | "discovery_share"      -- "Found iron vein at X"

export interface Message<T = unknown> {
    id: MessageId
    correlation_id: CorrelationId?      -- for request/response
    from: AgentId
    to: AgentId | "broadcast" | "fleet:<fleet_id>"
    type: MessageType
    priority: MessagePriority
    payload: T
    timestamp: number           -- Unix ms (server authoritative)
    ttl: number                 -- hops remaining (default 3)
    requires_ack: boolean       -- critical messages need ack
    metadata: {
        era: number             -- sender's current tech era
        energy_cost: number     -- estimated API credits this msg may trigger
        tags: string[]          -- ["building", "mining", "urgent"]
    }
}

-- Specific payloads
export interface TaskProposalPayload {
    task_id: string
    task_type: "build" | "mine" | "scout" | "craft" | "research" | "transport" | "defend"
    required_skills: string[]           -- ["welding", "logic_gates", "navigation"]
    estimated_duration_sec: number
    location: Vector3
    bounding_box: BoundingBox?          -- workspace reservation
    resources_needed: ResourceMap       -- {iron: 50, copper: 20}
    reward: number                      -- XP / credit share
    deadline: number?                   -- Unix ms
    dependencies: string[]              -- task_ids that must complete first
}

export interface StateBroadcastPayload {
    position: Vector3
    velocity: Vector3
    current_task: string?               -- task_id or null
    task_progress: number               -- 0-1
    inventory: ResourceMap
    energy: number                      -- 0-100 (agent stamina)
    health: number                      -- 0-100
    mode: "idle" | "working" | "traveling" | "charging" | "error"
    reserved_regions: BoundingBox[]     -- areas this agent has claimed
}
```

### 1.2 Message Bus Implementation (Cloudflare Durable Object)

```typescript
// ============================================================
// Cloudflare Durable Object: AgentMessageBus
// One per world instance (game server)
// ============================================================

interface Env {
    MESSAGE_BUS: DurableObjectNamespace
    AGENT_REGISTRY: KVNamespace
    WORLD_STATE: DurableObjectNamespace
}

export class AgentMessageBus {
    private state: DurableObjectState
    private env: Env
    
    // In-memory queues (persisted to SQLite via state.storage)
    private subscriptionMap: Map<string, Set<WebSocket>> = new Map()  // agent_id -> WS connections
    private topicSubscriptions: Map<string, Set<string>> = new Map()  // topic -> agent_ids
    private messageLog: Message[] = []  // circular buffer, last 10k
    private pendingAcks: Map<string, {msg: Message, resolve: Function, timeout: NodeJS.Timeout}> = new Map()
    
    // Rate limiting per agent
    private rateLimits: Map<string, {count: number, windowStart: number}> = new Map()
    private readonly MAX_MSGS_PER_SEC = 50
    private readonly MAX_MSGS_PER_MIN = 1000

    constructor(state: DurableObjectState, env: Env) {
        this.state = state
        this.env = env
        this.loadPersistedState()
    }

    // ------------------------------------------------------------------
    // WebSocket connection handling (agents connect via WS)
    // ------------------------------------------------------------------
    async fetch(request: Request): Promise<Response> {
        const upgradeHeader = request.headers.get("Upgrade")
        if (upgradeHeader !== "websocket") {
            return new Response("Expected WebSocket", {status: 400})
        }

        const url = new URL(request.url)
        const agentId = url.searchParams.get("agent_id")
        const fleetId = url.searchParams.get("fleet_id")
        const authToken = url.searchParams.get("token")
        
        if (!agentId || !await this.validateAgent(agentId, authToken)) {
            return new Response("Unauthorized", {status: 401})
        }

        const [client, server] = Object.values(new WebSocketPair())
        server.accept()
        
        this.registerConnection(agentId, server, fleetId)
        server.addEventListener("message", (event) => this.handleMessage(agentId, event.data))
        server.addEventListener("close", () => this.unregisterConnection(agentId, server))

        return new Response(null, {status: 101, webSocket: client})
    }

    private registerConnection(agentId: string, ws: WebSocket, fleetId: string?) {
        if (!this.subscriptionMap.has(agentId)) {
            this.subscriptionMap.set(agentId, new Set())
        }
        this.subscriptionMap.get(agentId)!.add(ws)
        
        // Auto-subscribe to fleet topic
        if (fleetId) {
            this.subscribeToTopic(agentId, `fleet:${fleetId}`)
        }
        
        // Subscribe to direct messages
        this.subscribeToTopic(agentId, `agent:${agentId}`)
        
        // Subscribe to broadcasts
        this.subscribeToTopic(agentId, "broadcast")
        
        // Send pending messages for this agent
        this.flushPendingForAgent(agentId)
    }

    // ------------------------------------------------------------------
    // Message routing with priority queues
    // ------------------------------------------------------------------
    private async handleMessage(senderId: string, rawData: string | ArrayBuffer) {
        // Rate limiting
        if (!this.checkRateLimit(senderId)) {
            this.sendToAgent(senderId, {
                type: "rate_limit_exceeded",
                retry_after_ms: 1000
            } as any)
            return
        }

        let msg: Message
        try {
            msg = JSON.parse(rawData as string)
            msg.from = senderId  // Enforce sender identity
            msg.timestamp = Date.now()  // Server-authoritative timestamp
        } catch (e) {
            return // Silently drop malformed
        }

        // Validate message structure
        if (!this.validateMessage(msg)) return

        // Persist to log (async, non-blocking)
        this.appendToLog(msg)

        // Handle ack-required messages
        if (msg.requires_ack) {
            this.trackAck(msg)
        }

        // Route based on destination
        if (msg.to === "broadcast") {
            this.broadcast(msg, senderId)
        } else if (msg.to.startsWith("fleet:")) {
            this.broadcastToFleet(msg, msg.to.slice(6), senderId)
        } else if (msg.to.startsWith("agent:")) {
            this.deliverToAgent(msg.to.slice(6), msg)
        } else if (msg.to.startsWith("topic:")) {
            this.broadcastToTopic(msg.to.slice(6), msg, senderId)
        }
    }

    private deliverToAgent(targetAgentId: string, msg: Message) {
        const connections = this.subscriptionMap.get(targetAgentId)
        if (!connections || connections.size === 0) {
            // Agent offline - queue for later
            this.queueForOfflineAgent(targetAgentId, msg)
            return
        }

        const payload = JSON.stringify(msg)
        for (const ws of connections) {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(payload)
            }
        }
    }

    // ------------------------------------------------------------------
    // Topic-based pub/sub for efficient group messaging
    // ------------------------------------------------------------------
    subscribeToTopic(agentId: string, topic: string) {
        if (!this.topicSubscriptions.has(topic)) {
            this.topicSubscriptions.set(topic, new Set())
        }
        this.topicSubscriptions.get(topic)!.add(agentId)
    }

    private broadcastToTopic(topic: string, msg: Message, excludeSender: string) {
        const subscribers = this.topicSubscriptions.get(topic)
        if (!subscribers) return
        
        for (const agentId of subscribers) {
            if (agentId !== excludeSender) {
                this.deliverToAgent(agentId, msg)
            }
        }
    }

    // ------------------------------------------------------------------
    // Fleet broadcasting (player + all their agents)
    // ------------------------------------------------------------------
    private broadcastToFleet(msg: Message, fleetId: string, excludeSender: string) {
        const fleetTopic = `fleet:${fleetId}`
        this.broadcastToTopic(fleetTopic, msg, excludeSender)
    }

    // ------------------------------------------------------------------
    // Acknowledgment tracking for critical messages
    // ------------------------------------------------------------------
    private trackAck(msg: Message) {
        const timeout = setTimeout(() => {
            this.pendingAcks.delete(msg.id)
            // Trigger retry or escalation
            this.handleAckTimeout(msg)
        }, 5000)  // 5 second ack timeout

        this.pendingAcks.set(msg.id, {msg, resolve: null as any, timeout})
    }

    // Agent sends ack: {type: "ack", correlation_id: "msg_id"}
    private handleAck(ackMsg: any) {
        const pending = this.pendingAcks.get(ackMsg.correlation_id)
        if (pending) {
            clearTimeout(pending.timeout)
            this.pendingAcks.delete(ackMsg.correlation_id)
        }
    }
}
```

### 1.3 Agent-Side Message Client (Luau)

```lua
-- ============================================================
-- AgentMessageClient (runs inside each agent's Luau VM)
-- ============================================================

local AgentMessageClient = {}
AgentMessageClient.__index = AgentMessageClient

type MessageHandler = (Message) -> ()

function AgentMessageClient.new(agentId: string, fleetId: string, wsUrl: string)
    local self = setmetatable({}, AgentMessageClient)
    self.agentId = agentId
    self.fleetId = fleetId
    self.wsUrl = wsUrl
    self.handlers = {} :: {[string]: MessageHandler}
    self.pendingRequests = {} :: {[string]: {resolve: (any) -> (), reject: (string) -> (), timestamp: number}}
    self.messageIdCounter = 0
    self.ws = nil
    self.reconnectAttempts = 0
    self.maxReconnectAttempts = 10
    self.heartbeatInterval = nil
    return self
end

function AgentMessageClient:connect()
    self.ws = WebSocket.connect(self.wsUrl .. "?agent_id=" .. self.agentId .. "&fleet_id=" .. self.fleetId)
    
    self.ws.OnMessage:Connect(function(data)
        self:onMessage(data)
    end)
    
    self.ws.OnClose:Connect(function()
        self:scheduleReconnect()
    end)
    
    -- Heartbeat to detect stale connections
    self.heartbeatInterval = task.delay(30, function()
        self:send({type = "heartbeat"}, "broadcast", "background")
    end)
end

function AgentMessageClient:onMessage(rawData: string)
    local msg = game:GetService("HttpService"):JSONDecode(rawData)
    
    -- Handle ack for our pending requests
    if msg.type == "ack" and msg.correlation_id then
        local pending = self.pendingRequests[msg.correlation_id]
        if pending then
            pending.resolve(msg.payload)
            self.pendingRequests[msg.correlation_id] = nil
        end
        return
    end
    
    -- Handle direct responses (correlation_id matches our request)
    if msg.correlation_id and self.pendingRequests[msg.correlation_id] then
        local pending = self.pendingRequests[msg.correlation_id]
        if msg.type == "error" then
            pending.reject(msg.payload.error)
        else
            pending.resolve(msg.payload)
        end
        self.pendingRequests[msg.correlation_id] = nil
        return
    end
    
    -- Route to registered handlers
    local handler = self.handlers[msg.type]
    if handler then
        task.spawn(handler, msg)
    end
    
    -- Wildcard handler
    if self.handlers["*"] then
        task.spawn(self.handlers["*"], msg)
    end
end

-- High-level API for agents
function AgentMessageClient:send(payload: table, to: string, priority: string?, requiresAck: boolean?): string
    self.messageIdCounter += 1
    local msgId = string.format("%s-%d-%d", self.agentId, os.time(), self.messageIdCounter)
    local correlationId = msgId
    
    local message = {
        id = msgId,
        correlation_id = correlationId,
        from = self.agentId,
        to = to,
        type = payload.type or "custom",
        priority = priority or "normal",
        payload = payload,
        timestamp = os.time() * 1000,
        ttl = 3,
        requires_ack = requiresAck or false,
        metadata = {
            era = self.currentEra or 1,
            energy_cost = payload.estimated_api_cost or 0,
            tags = payload.tags or {}
        }
    }
    
    self.ws:Send(game:GetService("HttpService"):JSONEncode(message))
    return correlationId
end

-- Request-response pattern with timeout
function AgentMessageClient:request(payload: table, to: string, timeoutMs: number?): Promise
    local correlationId = self:send(payload, to, "high", true)
    
    return Promise.new(function(resolve, reject)
        self.pendingRequests[correlationId] = {resolve = resolve, reject = reject, timestamp = os.time()}
        
        task.delay(timeoutMs or 10000, function()
            if self.pendingRequests[correlationId] then
                self.pendingRequests[correlationId].reject("Request timeout")
                self.pendingRequests[correlationId] = nil
            end
        end)
    end)
end

function AgentMessageClient:on(messageType: string, handler: MessageHandler)
    self.handlers[messageType] = handler
end

-- Convenience methods for common patterns
function AgentMessageClient:proposeTask(task: TaskProposalPayload)
    return self:send({
        type = "task_proposal",
        ...task
    }, "broadcast", "normal")
end

function AgentMessageClient:claimTask(taskId: string, proposerId: string)
    return self:send({
        type = "task_claim",
        task_id = taskId
    }, "agent:" .. proposerId, "high", true)
end

function AgentMessageClient:broadcastState(state: StateBroadcastPayload)
    return self:send({
        type = "state_broadcast",
        ...state
    }, "broadcast", "low")
end

function AgentMessageClient:requestHelp(taskId: string, location: Vector3, skillsNeeded: {string})
    return self:send({
        type = "help_request",
        task_id = taskId,
        location = location,
        skills_needed = skillsNeeded
    }, "broadcast", "high")
end
```

---

## 2. TASK PARTITIONING ALGORITHM

### 2.1 Core Concept: Capability-Based Negotiation

Agents don't have hardcoded roles. They advertise **capabilities** and **current capacity**, then negotiate via the message bus.

```lua
-- ============================================================
-- CAPABILITY SYSTEM
-- ============================================================

export type Capability = {
    skill