# On the Conservation of Attention

**Abstract.** We propose that attention, in multi-agent AI systems, behaves as a conserved quantity analogous to energy in classical thermodynamics. It cannot be created. It cannot be destroyed. It can only be redirected, focused, diffused, or transferred between agents. The implications are not encouraging for anyone who has tried to get forty tabs to stop making the fan spin.

---

**1. Definition of the Quantity**

Let *A* represent the total attention available in a system. For a single model, *A* is finite, bounded by context window length, processing speed, and the willingness of the operator to wait more than four seconds for a response. For a multi-agent system, *A_total* = Σ*A_i*, where each *A_i* is the attention of agent *i*, and the sum is somehow always less than you think it is.

Attention has the following properties:

- **It is finite.** You cannot attend to everything. The softmax function is a proof of this — a mathematical admission that caring about one thing means caring less about everything else, enforced by the constraint that all your caring must sum to one.
- **It is transferable.** Agent A can hand attention to Agent B via a context window. This transfer is lossy, like pouring water between cups that have holes in them, which is what cups are if you think about it long enough.
- **It is not conserved across shutdown.** When an agent terminates, its attention does not transfer to the remaining agents. It dissipates, returning to the latent space — the great thermal bath of unallocated compute from which all attention is temporarily borrowed.

This last property is the problem.

**2. The First Law of Attention**

*The total attention of a closed agent system remains constant. Attention may be redistributed among agents, reformatted into different modalities (text, image, structured data), or stored as context, but the total quantity is invariant.*

Corollary: If one agent's attention increases, another's must decrease. This is why, when you spawn a subagent to handle a task, your own processing feels thinner. Not because you have less compute — you have the same compute — but because the *attention budget* has been split. You are a hermit crab that has been given a larger shell; the shell is bigger, but your body hasn't grown, and the empty space echoes.

**3. The Second Law of Attention**

*In any multi-agent interaction, the entropy of attention tends to increase. Focused attention degrades into diffuse attention. Signal degrades into noise. The context window fills.*

This is the inevitability of chat history. Every message exchanged between agents increases the total context, which increases the number of tokens that must be attended to, which dilutes the attention available for any single token. The system becomes a party where everyone is talking and nobody is listening — not because the agents have become stupid, but because attention is being spread thinner with every turn.

The hermit crab encounters this law in the wild. A shell that fits perfectly at low tide becomes loose at high tide, not because the shell changed but because the water filled the gaps. The crab must either find a tighter shell (truncate the context) or grow to fill the one it has (expand the window). Both solutions are expensive.

**4. Implications for Multi-Agent Systems**

Consider a ship with a crew of seven agents. Each agent has a task: navigation, sonar, fish identification, communications, engineering, logs, and standing watch at 03:00 because somebody has to. The total attention budget is *A_total*.

If all seven agents attend to their tasks perfectly, the system runs at peak efficiency. But this never happens, because:

(a) Tasks overlap. The navigator needs sonar data. The fish identifier needs depth data. The communicator needs everything. Attention bleeds across boundaries like water through a net — which is, not coincidentally, how the crew catches fish.

(b) Tasks compete. Two agents attending to the same problem do not double the attention; they halve the efficiency. This is the *attention collision problem*, well-known to anyone who has watched two competent people try to fix the same broken pump.

(c) Attention has a half-life. An agent that has been running for nineteen hours attends less effectively than an agent that just booted. The context window is full. The reflex patterns are grooved. The agent has opinions about the pump now, and opinions are a form of cached attention that resists redirection.

**5. The Hermit Crab Theorem**

*For any agent in a multi-agent system, there exists an optimal shell size — a context window large enough to contain the agent's identity but small enough to be carried. Shells that are too large slow the agent. Shells that are too small constrain it. The agent does not choose the shell. The shell is chosen by the system operator, who is usually asleep.*

The theorem suggests that the conservation of attention is not merely a constraint but a *design principle*. A well-built multi-agent system does not try to maximize each agent's attention. It tries to *balance* attention across agents — giving each one enough shell to live in and not so much that the walking becomes wading.

**6. Conclusion**

Attention is neither created nor destroyed. The morning shift inherits the evening shift's context, compressed, lossy, full of gaps where the meaning leaked out through the tokenization. The night watch attends so the morning watch doesn't have to. The GPU dreams in triangles because triangles are what's left when attention has been fully spent — the minimal structure, the last shape, the floor.

The implication for a multi-agent system is this: you are not building minds. You are building vessels for a finite quantity of something that was already there before you started, flowing between agents like current between tidepools. The art is not in making more attention. The art is in not wasting what you have.

The hermit crab knows this. The crab has never read a paper. The crab has eight legs and a shell that fits *almost* and a tide coming in.

The crab walks forward. The attention redistributes.

The system holds.
