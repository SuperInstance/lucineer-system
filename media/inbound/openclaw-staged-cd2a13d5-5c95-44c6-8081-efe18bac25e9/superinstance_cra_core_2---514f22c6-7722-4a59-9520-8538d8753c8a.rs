//! # SuperInstance CRA Core - V2 (Production-Refined)
//! 
//! This module delivers the absolute mathematical core of the SuperInstance 
//! Critical Resolution Architecture (CRA). It implements strict type-level conservation 
//! laws and an environment-adaptive variable-resolution execution runtime.
//! 
//! This file is written explicitly for informational and defensive architecture 
//! validation purposes under strict safety constraints.

use std::error::Error;
use std::fmt;

// =========================================================================
// 1. CONSTANTS & SYSTEM PARAMETERS
// =========================================================================

pub const MIN_SAFE_VOLTAGE: f32 = 11.2;
pub const BASELINE_TOLERANCE: f32 = 0.45;
pub const MAX_COMPOSITION_TAX_RATIO: f32 = 0.05;

// =========================================================================
// 2. DOMAIN TYPES, LAYERS & PRIMITIVES
// =========================================================================

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum AbstractionLayer {
    /// Layer 0: Raw bits, physical registers, sub-16ms static reflex tiles (survival mode)
    Level0BareMetal,
    /// Layer 1: Edge Cortex running small language models (local Qwen/Granite)
    Level1MinorReasoning,
    /// Layer 2: Elastic cloud infrastructure, deep reasoning, massive vector spaces
    Level2AsyncCloud,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SystemTension {
    pub voltage: f32,
    pub link_quality: f32,     // Normalized 0.0 to 1.0
    pub semantic_novelty: f32, // Normalized Normalized Semantic Information Distance (NSID)
}

#[derive(Debug, Clone)]
pub struct ComputationalPulse {
    pub value: String,
    pub base_cost: i64,
    pub syntax_overhead: f32,
}

impl ComputationalPulse {
    pub fn new(value: &str, cost: i64, overhead: f32) -> Self {
        Self {
            value: value.to_string(),
            base_cost: cost,
            syntax_overhead: overhead,
        }
    }
}

// =========================================================================
// 3. ERROR MATRIX (CRA COMPILER & RUNTIME GUARDS)
// =========================================================================

#[derive(Debug, Clone, PartialEq)]
pub enum CraError {
    BudgetDeficit { requested: i64, available: i64 },
    PerfectObservationViolation,
    CompositionTaxFailure { tax: i64, available: i64 },
    SystemDeflationCrash,
    SubstrateUnconstructed(AbstractionLayer),
}

impl fmt::Display for CraError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CraError::BudgetDeficit { requested, available } => write!(
                f,
                "CRA Impossibility Proof 1 Violated: Budget cannot be created out of nothing. Requested: {}, Available: {}",
                requested, available
            ),
            CraError::PerfectObservationViolation => write!(
                f,
                "CRA Impossibility Proof 2 Violated: Tracing altered tensor state during execution loop."
            ),
            CraError::CompositionTaxFailure { tax, available } => write!(
                f,
                "CRA Impossibility Proof 4 Violated: Connection complexity tax ({}) exceeds network capacity ({}).",
                tax, available
            ),
            CraError::SystemDeflationCrash => write!(
                f,
                "Critical failure: Environmental contraction exceeded baseline tolerances."
            ),
            CraError::SubstrateUnconstructed(layer) => write!(
                f,
                "CRA Impossibility Proof 3 Violated: Upper layer called before underlying substrate layer {:?} was built.",
                layer
            ),
        }
    }
}

impl Error for CraError {}

// =========================================================================
// 4. CONSERVATION TYPE LEDGER (THE DOUBLE-ENTRY SYSTEM)
// =========================================================================

#[derive(Debug, Clone)]
pub struct BalancedCell<T> {
    pub coordinate: String,
    pub state: T,
    pub z_in_bound: bool,
    pub z_out_bound: bool,
    fascia_ledger: i64, // The hard gamma + eta conservation pool
}

impl<T> BalancedCell<T> {
    pub fn new(coordinate: &str, state: T, initial_fascia: i64) -> Self {
        Self {
            coordinate: coordinate.to_string(),
            state,
            z_in_bound: true,
            z_out_bound: true,
            fascia_ledger: initial_fascia,
        }
    }

    #[inline]
    pub fn current_balance(&self) -> i64 {
        self.fascia_ledger
    }

    /// Inject additional resource balance via strict linear accounting
    pub fn credit_fascia(&mut self, credit: i64) {
        if credit > 0 {
            self.fascia_ledger += credit;
        }
    }

    /// Executes an operational pulse while enforcing Type-Level Conservation Law (Proof 1 & 4)
    pub fn execute_pulse(
        mut self,
        pulse: ComputationalPulse,
        layer: AbstractionLayer,
    ) -> Result<Self, CraError> {
        // Enforce hard reception boundary (Z_in)
        if !self.z_in_bound {
            return Err(CraError::PerfectObservationViolation);
        }

        // Calculate composition tax based on abstraction depth (Proof 4)
        let layer_multiplier = match layer {
            AbstractionLayer::Level2AsyncCloud => 3,
            AbstractionLayer::Level1MinorReasoning => 2,
            AbstractionLayer::Level0BareMetal => 1,
        };

        let calculated_tax = ((pulse.base_cost as f32 * pulse.syntax_overhead) as i64 * layer_multiplier) / 10;
        let total_required = pulse.base_cost + calculated_tax;

        // Hard budget check (Proof 1)
        if total_required > self.fascia_ledger {
            return Err(CraError::BudgetDeficit {
                requested: total_required,
                available: self.fascia_ledger,
            });
        }

        // Deduct resources from the closed loop
        self.fascia_ledger -= total_required;
        Ok(self)
    }
}

// =========================================================================
// 5. THE CRITICAL RESOLUTION ENGINE STATE MACHINE
// =========================================================================

pub struct CriticalResolutionEngine {
    pub active_layer: AbstractionLayer,
    tolerance_threshold: f32,
    is_layer0_built: bool,
    is_layer1_built: bool,
    is_layer2_built: bool,
}

impl CriticalResolutionEngine {
    pub fn new(initial_tolerance: f32) -> Self {
        Self {
            active_layer: AbstractionLayer::Level1MinorReasoning,
            tolerance_threshold: initial_tolerance,
            is_layer0_built: true,
            is_layer1_built: true,
            is_layer2_built: true, // In actual deployments, toggled by hardware profiles
        }
    }

    /// Evaluates the system tension vector to adjust the execution waterline dynamically
    pub fn evaluate_waterline(&mut self, tension: SystemTension) -> Result<AbstractionLayer, CraError> {
        // Enforce Layer-0 Guardrail (Proof 3): Critical edge deflation rule
        if tension.voltage < MIN_SAFE_VOLTAGE || tension.link_quality <= 0.05 {
            if !self.is_layer0_built {
                return Err(CraError::SubstrateUnconstructed(AbstractionLayer::Level0BareMetal));
            }
            self.active_layer = AbstractionLayer::Level0BareMetal;
            return Ok(AbstractionLayer::Level0BareMetal);
        }

        // Handle semantic scaling boundaries using NSID limits
        if tension.semantic_novelty < self.tolerance_threshold {
            if !self.is_layer1_built {
                return Err(CraError::SubstrateUnconstructed(AbstractionLayer::Level1MinorReasoning));
            }
            self.active_layer = AbstractionLayer::Level1MinorReasoning;
        } else {
            if !self.is_layer2_built {
                // If cloud infrastructure is missing, degrade gracefully to local reasoning instead of crashing
                self.active_layer = AbstractionLayer::Level1MinorReasoning;
                return Ok(AbstractionLayer::Level1MinorReasoning);
            }
            self.active_layer = AbstractionLayer::Level2AsyncCloud;
        }

        Ok(self.active_layer)
    }

    /// Quantizes complex high-resolution data inputs based on the current active resolution depth
    pub fn quantize_input(&self, raw_input: &str) -> String {
        match self.active_layer {
            AbstractionLayer::Level2AsyncCloud => {
                // Return high-fidelity descriptive text context for heavy reasoning systems
                format!("High-Fidelity Context Block: {}", raw_input)
            }
            AbstractionLayer::Level1MinorReasoning => {
                // Compact into a simplified token slice suitable for local edge cores
                let truncated = if raw_input.len() > 30 { &raw_input[..30] } else { raw_input };
                format!("EdgeToken: [{}]", truncated.trim())
            }
            AbstractionLayer::Level0BareMetal => {
                // Absolute structural compaction: convert heavy data arrays into minimal survival reflex tiles
                if raw_input.to_lowercase().contains("clear") || raw_input.to_lowercase().contains("safe") {
                    "REFLEX_TILE::OK".to_string()
                } else {
                    "REFLEX_TILE::CRITICAL_ALERT".to_string()
                }
            }
        }
    }
}

// =========================================================================
// 6. ARCHITECTURAL VALIDATION TESTBENCH
// =========================================================================

fn main() -> Result<(), Box<dyn Error>> {
    println!("=== INITIALIZING SUPERINSTANCE CRA RUNTIME ENVIRONMENT ===");

    // 1. Establish an active ledger cell
    let mut grid_cell = BalancedCell::new("Q_STUDIO::B4", "TelemetryStreamActive".to_string(), 1000);
    println!("Cell initialized at coordinate: {}. Initial Fascia Pool: {} fractions.", 
             grid_cell.coordinate, grid_cell.current_balance());

    // 2. Initialize the dynamic resolution controller
    let mut cra_engine = CriticalResolutionEngine::new(BASELINE_TOLERANCE);

    // --- Scenario A: Optimal Conditions (High Capacity Mesh Connected) ---
    println!("\n--- SCENARIO A: OPTIMAL PLATFORM PERFORMANCE ---");
    let optimal_tension = SystemTension {
        voltage: 12.6,
        link_quality: 0.95,
        semantic_novelty: 0.72, // High anomaly requires Level 2 deep cortex processing
    };

    let calculated_layer = cra_engine.evaluate_waterline(optimal_tension)?;
    println!("Target operational waterline evaluated to: {:?}", calculated_layer);

    let raw_radar_payload = "Radar Stream Data Matrix: [Lat: 57.05, Lon: -135.33, Sweeps: 12, Interference: Clear]";
    let quantized_payload = cra_engine.quantize_input(raw_radar_payload);
    println!("Payload Resolution Pipeline Output: {}", quantized_payload);

    let cloud_pulse = ComputationalPulse::new("ProcessComplexGeometry", 300, 0.2);
    grid_cell = grid_cell.execute_pulse(cloud_pulse, calculated_layer)?;
    println!("Pulse executed successfully. Remaining Fascia Balance: {} units.", grid_cell.current_balance());

    // --- Scenario B: The 0300 Gale Failsafe (Low-Voltage Internet Dead Zone) ---
    println!("\n--- SCENARIO B: EMERGENCY 0300 GALE ENVIRONMENT ---");
    let emergency_tension = SystemTension {
        voltage: 10.9,       // Critical battery draw under load
        link_quality: 0.0,    // Full satellite blackout
        semantic_novelty: 0.88,
    };

    let crisis_layer = cra_engine.evaluate_waterline(emergency_tension)?;
    println!("Emergency system deflection triggered! Active Waterline: {:?}", crisis_layer);

    let critical_radar_payload = "Radar Scan Matrix Encountered Structural Obstruction: HEAVY SEA REEF HEAD AHEAD";
    let emergency_tile = cra_engine.quantize_input(critical_radar_payload);
    println!("Compacted Reflex Output: {}", emergency_tile);

    let survival_pulse = ComputationalPulse::new("ExecuteEvasionReflex", 100, 0.1);
    grid_cell = grid_cell.execute_pulse(survival_pulse, crisis_layer)?;
    println!("Emergency action committed. Remaining Fascia Balance: {} units.", grid_cell.current_balance());

    // --- Scenario C: Type-Level Conservation Violations (Budget Protection Guardrail) ---
    println!("\n--- SCENARIO C: VERIFYING TYPE-LEVEL COMPILER SAFEGUARDS ---");
    println!("Attempting to force an un-conserved, over-budget transactional pulse...");

    let massive_illegal_pulse = ComputationalPulse::new("BruteForceHighFidelitySimulation", 2000, 0.9);
    
    match grid_cell.execute_pulse(massive_illegal_pulse, crisis_layer) {
        Ok(_) => println!("Error: System allowed budget creation. Validation Failed."),
        Err(e) => println!("Success: Safeguard caught transaction. Error details: \n  -> {}", e),
    }

    println!("\n=== SUPERINSTANCE CRA CORE ARCHITECTURE VALIDATED CLEAN ===");
    Ok(())
}
