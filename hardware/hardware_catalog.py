import sqlite3

# Hardware catalog data
HARDWARE_CATALOG = {
    "consumer-electronics": [
        {
            "name": "QuantumCore™ Home Assistant",
            "manufacturer": "FutureTech Industries",
            "model": "QCH-3000",
            "release_date": "2145",
            "repair_difficulty": 3,
            "operating_system": "QOS v4.2",
            "specs": {
                "processor": "8-core @ 12.8 THz",
                "memory": "128 TB holographic storage",
                "power": "48V DC, 2.5A",
                "connectivity": "Quantum Entanglement Network (QEN), WiFi 12, Bluetooth 8.0"
            },
            "common_failures": [
                "Quantum state decoherence in processing unit",
                "Holographic storage matrix corruption",
                "Power supply quantum tunneling leakage",
                "QEN transceiver alignment drift"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Quantum State Reset",
                    "steps": [
                        "Use quantum stabilizer tool",
                        "Perform cold reboot sequence",
                        "Recalibrate quantum gates"
                    ]
                },
                {
                    "name": "Storage Recovery",
                    "steps": [
                        "Run holographic integrity check",
                        "Rebuild storage matrix",
                        "Restore from quantum backup"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Stabilizer (Model QS-2000)",
                "Holographic Matrix Scanner",
                "Quantum Gate Calibrator"
            ]
        },
        {
            "name": "NeuralSync™ VR Headset",
            "manufacturer": "MindLink Technologies",
            "model": "NS-VR-500",
            "release_date": "2146",
            "repair_difficulty": 4,
            "operating_system": "NeuralOS v3.1+",
            "specs": {
                "interface": "Direct brainwave synchronization",
                "display": "16K per eye, 240Hz refresh",
                "battery": "5000mAh quantum cell",
                "sensors": "Full body motion tracking"
            },
            "common_failures": [
                "Neural sync signal degradation",
                "Quantum battery cell depletion",
                "Motion tracking calibration drift",
                "Brainwave interface desynchronization"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Neural Interface Reset",
                    "steps": [
                        "Disconnect neural sync module",
                        "Run diagnostic sequence",
                        "Recalibrate brainwave patterns"
                    ]
                },
                {
                    "name": "Battery Recovery",
                    "steps": [
                        "Perform quantum cell realignment",
                        "Reset power management system",
                        "Verify charging circuit integrity"
                    ]
                }
            ],
            "special_tools": [
                "Neural Interface Diagnostic Kit",
                "Quantum Cell Realignment Tool",
                "Brainwave Pattern Calibrator"
            ]
        }
    ],
    "industrial-equipment": [
        {
            "name": "HyperForge™ Plasma Fabricator",
            "manufacturer": "MetalTech Solutions",
            "model": "HPF-9000",
            "release_date": "2144",
            "repair_difficulty": 5,
            "specs": {
                "chamber": "Triple-containment field, 50,000K max temp",
                "power": "750kW @ 480V 3-phase",
                "capacity": "Up to 2000kg/hour",
                "precision": "0.001mm tolerance",
                "control_system": "QuantumLogic™ PLC with AI assistance",
                "safety_systems": "Triple redundant emergency shutdown"
            },
            "common_failures": [
                "Plasma containment field desynchronization",
                "Quantum control system drift",
                "Coolant system crystallization",
                "Material feed servo misalignment",
                "AI neural pattern degradation"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Containment Field Reset",
                    "steps": [
                        "Initiate emergency plasma quench",
                        "Recalibrate magnetic field generators",
                        "Verify field symmetry with quantum sensors",
                        "Perform staged power-up sequence"
                    ]
                },
                {
                    "name": "Coolant System Recovery",
                    "steps": [
                        "Heat coolant lines to prevent crystal formation",
                        "Flush system with anti-crystallization agent",
                        "Replace molecular filters",
                        "Verify flow rates in all subsystems"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Field Analyzer (QFA-X series)",
                "Plasma Diagnostic Suite",
                "Industrial AI Neural Pattern Debugger",
                "Molecular Filter Replacement Kit"
            ]
        },
        {
            "name": "NanoMill™ Precision Fabricator",
            "manufacturer": "MicroTech Industries",
            "model": "NM-5500",
            "release_date": "2145",
            "repair_difficulty": 4.5,
            "specs": {
                "working_area": "2m x 2m x 1.5m",
                "resolution": "0.1 nanometer precision",
                "atmosphere": "Class 100 cleanroom environment",
                "control_system": "Atomic-scale positioning system",
                "materials": "Compatible with metals, ceramics, and composites"
            },
            "common_failures": [
                "Atomic positioner drift",
                "Cleanroom containment breach",
                "Quantum measurement system failure",
                "Material feed contamination",
                "Control system quantum decoherence"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Atomic Positioner Calibration",
                    "steps": [
                        "Initialize quantum reference grid",
                        "Perform multi-point calibration",
                        "Verify positioning accuracy",
                        "Update drift compensation algorithms"
                    ]
                },
                {
                    "name": "Cleanroom Recovery",
                    "steps": [
                        "Initiate emergency containment protocols",
                        "Purge atmosphere with filtered gas",
                        "Check seal integrity",
                        "Verify particle count levels"
                    ]
                }
            ],
            "special_tools": [
                "Atomic Position Calibrator",
                "Quantum Reference Grid Generator",
                "Cleanroom Particle Analyzer",
                "Seal Integrity Tester"
            ]
        },
        {
            "name": "IndustrialMind™ Process Controller",
            "manufacturer": "AutoLogic Systems",
            "model": "IPC-2200",
            "release_date": "2146",
            "repair_difficulty": 3,
            "specs": {
                "processing": "Quantum-Classical Hybrid Architecture",
                "memory": "1 PB Neural Storage",
                "connectivity": "Industrial Ethernet, QuantumNet, Legacy Protocols",
                "redundancy": "Triple-redundant processing units",
                "security": "Military-grade quantum encryption"
            },
            "common_failures": [
                "Neural network corruption",
                "Quantum-classical sync loss",
                "Protocol translation errors",
                "Redundancy verification failure",
                "Security system lockout"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Neural Network Recovery",
                    "steps": [
                        "Backup current state",
                        "Initialize recovery partition",
                        "Rebuild neural connections",
                        "Verify process control accuracy"
                    ]
                },
                {
                    "name": "Quantum-Classical Synchronization",
                    "steps": [
                        "Reset timing reference",
                        "Realign quantum states",
                        "Update sync parameters",
                        "Test processing accuracy"
                    ]
                }
            ],
            "special_tools": [
                "Neural Network Analyzer",
                "Quantum State Debugger",
                "Protocol Analysis Kit",
                "Security Override Module"
            ]
        },
        {
            "name": "AtmoProcessor™ Environmental Control System",
            "manufacturer": "CleanTech Solutions",
            "model": "AP-8000",
            "release_date": "2145",
            "repair_difficulty": 4,
            "specs": {
                "processing_capacity": "1,000,000 m³/hour",
                "filtration": "Molecular-level separation",
                "efficiency": "99.9999% contaminant removal",
                "power_consumption": "250kW continuous",
                "control": "AI-driven adaptive processing"
            },
            "common_failures": [
                "Molecular filter saturation",
                "Pressure gradient imbalance",
                "AI control system errors",
                "Energy distribution failure",
                "Contamination sensor malfunction"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Filter System Recovery",
                    "steps": [
                        "Analyze contamination levels",
                        "Regenerate molecular filters",
                        "Balance pressure gradients",
                        "Verify filtration efficiency"
                    ]
                },
                {
                    "name": "AI Control Reset",
                    "steps": [
                        "Backup environmental data",
                        "Reset neural patterns",
                        "Recalibrate sensors",
                        "Verify control responses"
                    ]
                }
            ],
            "special_tools": [
                "Molecular Analysis Kit",
                "Pressure Mapping System",
                "AI Neural Pattern Analyzer",
                "Environmental Sensor Calibrator"
            ]
        }
    ],
    "networking-devices": [
        {
            "name": "QuantumCore™ Network Switch",
            "manufacturer": "NetQuantum Technologies",
            "model": "QNS-X9000",
            "release_date": "2145",
            "repair_difficulty": 5,
            "specs": {
                "ports": "128x quantum-enabled ports, 64x legacy optical ports",
                "throughput": "100 Petabits/second per quantum port",
                "latency": "0.1 nanoseconds",
                "buffer": "1 Exabyte quantum memory buffer",
                "quantum_entanglement": "Supports up to 1024 simultaneous entangled pairs",
                "power": "3kW, redundant quantum power supplies"
            },
            "common_failures": [
                "Quantum entanglement desynchronization",
                "Buffer quantum state collapse",
                "Port crystal oscillator drift",
                "Quantum memory decoherence",
                "Entanglement routing table corruption"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Quantum State Recovery",
                    "steps": [
                        "Initialize quantum state analyzer",
                        "Measure entanglement fidelity",
                        "Realign quantum buffers",
                        "Rebuild routing tables"
                    ]
                },
                {
                    "name": "Port Synchronization",
                    "steps": [
                        "Reset crystal oscillators",
                        "Calibrate quantum timing",
                        "Test port integrity",
                        "Verify quantum-classical conversion"
                    ]
                }
            ],
            "special_tools": [
                "Quantum State Analyzer (QSA-9000)",
                "Entanglement Fidelity Meter",
                "Quantum Buffer Debugger",
                "Crystal Oscillator Calibration Kit"
            ]
        },
        {
            "name": "HyperMesh™ Wireless Controller",
            "manufacturer": "AirLogic Systems",
            "model": "HM-7500",
            "release_date": "2146",
            "repair_difficulty": 4,
            "specs": {
                "coverage": "10km radius with quantum repeaters",
                "frequency_bands": "0.1-1000 GHz + quantum bands",
                "concurrent_devices": "1 million per controller",
                "ai_processing": "Neural traffic optimization",
                "security": "Post-quantum cryptography",
                "redundancy": "Triple controller failover"
            },
            "common_failures": [
                "Neural traffic pattern corruption",
                "Quantum repeater alignment drift",
                "Cryptographic key desynchronization",
                "Device authentication cache overflow",
                "AI optimization loop failure"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Neural Pattern Reset",
                    "steps": [
                        "Backup traffic patterns",
                        "Reset neural processors",
                        "Rebuild optimization models",
                        "Verify traffic flow"
                    ]
                },
                {
                    "name": "Quantum Repeater Alignment",
                    "steps": [
                        "Scan quantum channels",
                        "Realign repeater arrays",
                        "Update positioning data",
                        "Test signal integrity"
                    ]
                }
            ],
            "special_tools": [
                "Neural Pattern Analyzer",
                "Quantum Channel Scanner",
                "Cryptographic Debug Kit",
                "AI Pattern Optimizer"
            ]
        },
        {
            "name": "DataStream™ Load Balancer",
            "manufacturer": "LoadTech Solutions",
            "model": "DS-5000",
            "release_date": "2145",
            "repair_difficulty": 3,
            "specs": {
                "capacity": "1 Exabit/second throughput",
                "algorithms": "AI-driven dynamic routing",
                "sessions": "100 million concurrent",
                "health_monitoring": "Quantum-assisted predictive",
                "redundancy": "Active-active clustering",
                "ssl_offload": "Quantum cryptography accelerator"
            },
            "common_failures": [
                "Session state corruption",
                "Algorithm neural pattern drift",
                "Health monitor false positives",
                "Quantum accelerator desync",
                "Cluster state inconsistency"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Session Recovery",
                    "steps": [
                        "Backup session data",
                        "Reset state tables",
                        "Rebuild session cache",
                        "Verify persistence"
                    ]
                },
                {
                    "name": "Algorithm Retraining",
                    "steps": [
                        "Analyze traffic patterns",
                        "Retrain neural network",
                        "Update routing rules",
                        "Test load distribution"
                    ]
                }
            ],
            "special_tools": [
                "Session State Analyzer",
                "Neural Network Debugger",
                "Quantum Accelerator Toolkit",
                "Cluster State Validator"
            ]
        },
        {
            "name": "SecureGate™ Quantum Firewall",
            "manufacturer": "CyberQuantum Defense",
            "model": "SG-8000",
            "release_date": "2146",
            "repair_difficulty": 4.5,
            "specs": {
                "throughput": "500 Petabits/second",
                "inspection": "Deep quantum packet analysis",
                "threat_detection": "AI + quantum pattern matching",
                "encryption": "Post-quantum cryptography",
                "virtual_contexts": "1000 quantum-isolated instances",
                "updates": "Real-time quantum threat database"
            },
            "common_failures": [
                "Quantum pattern matcher corruption",
                "Threat database synchronization failure",
                "Virtual context isolation breach",
                "Cryptographic module failure",
                "AI detection engine crash"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Pattern Matcher Recovery",
                    "steps": [
                        "Reset quantum patterns",
                        "Rebuild threat database",
                        "Verify detection accuracy",
                        "Test false positive rate"
                    ]
                },
                {
                    "name": "Context Isolation Repair",
                    "steps": [
                        "Verify quantum barriers",
                        "Reset context states",
                        "Rebuild isolation tables",
                        "Test context separation"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Pattern Debug Kit",
                "Threat Database Analyzer",
                "Context Isolation Tester",
                "Cryptographic Module Validator"
            ]
        }
    ],
    "medical-equipment": [
        {
            "name": "NeuroScan™ Quantum MRI",
            "manufacturer": "MedTech Quantum",
            "model": "NSQ-9000",
            "release_date": "2145",
            "repair_difficulty": 5,
            "specs": {
                "field_strength": "15 Tesla with quantum field stabilization",
                "resolution": "0.1mm isotropic",
                "scan_speed": "Full brain scan in 30 seconds",
                "ai_analysis": "Real-time neural pattern recognition",
                "safety": "Quantum field containment system",
                "patient_monitoring": "Continuous vital sign tracking"
            },
            "common_failures": [
                "Quantum field instability",
                "Neural pattern recognition drift",
                "Patient monitoring desynchronization",
                "Cooling system quantum crystallization",
                "AI diagnostic algorithm corruption"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Field Stabilization",
                    "steps": [
                        "Initiate emergency field shutdown",
                        "Recalibrate quantum stabilizers",
                        "Verify field symmetry",
                        "Perform staged power-up"
                    ]
                },
                {
                    "name": "AI System Recovery",
                    "steps": [
                        "Backup diagnostic patterns",
                        "Reset neural processors",
                        "Rebuild recognition models",
                        "Verify diagnostic accuracy"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Field Analyzer",
                "Neural Pattern Debugger",
                "Patient Monitor Calibrator",
                "AI Diagnostic Validator"
            ]
        },
        {
            "name": "BioSync™ Life Support System",
            "manufacturer": "LifeTech Systems",
            "model": "BLS-8000",
            "release_date": "2146",
            "repair_difficulty": 4.5,
            "specs": {
                "capacity": "10 patients simultaneously",
                "monitoring": "Continuous quantum biofeedback",
                "life_support": "AI-driven adaptive systems",
                "redundancy": "Triple-redundant critical systems",
                "power": "Quantum battery backup (72 hours)",
                "safety": "Automated emergency protocols"
            },
            "common_failures": [
                "Biofeedback quantum desync",
                "Life support algorithm drift",
                "Power system quantum leakage",
                "Emergency protocol failure",
                "Patient data corruption"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Biofeedback Recovery",
                    "steps": [
                        "Reset quantum sensors",
                        "Recalibrate monitoring systems",
                        "Verify patient data integrity",
                        "Test feedback loops"
                    ]
                },
                {
                    "name": "Life Support Reset",
                    "steps": [
                        "Backup patient parameters",
                        "Reset control algorithms",
                        "Verify system redundancy",
                        "Test emergency protocols"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Biofeedback Analyzer",
                "Life Support Debug Kit",
                "Power System Validator",
                "Emergency Protocol Tester"
            ]
        },
        {
            "name": "NanoMed™ Surgical Robot",
            "manufacturer": "SurgicalTech Robotics",
            "model": "NSR-7000",
            "release_date": "2145",
            "repair_difficulty": 4,
            "specs": {
                "precision": "0.01mm surgical accuracy",
                "ai_control": "Neural network guidance",
                "instruments": "Quantum-stabilized tools",
                "imaging": "Real-time quantum tomography",
                "safety": "Triple-redundant control systems",
                "training": "Virtual reality simulation mode"
            },
            "common_failures": [
                "Surgical precision drift",
                "Neural control pattern corruption",
                "Quantum tool stabilization failure",
                "Imaging system desynchronization",
                "Safety system false positives"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Precision Calibration",
                    "steps": [
                        "Initialize calibration sequence",
                        "Test movement accuracy",
                        "Verify tool alignment",
                        "Update control algorithms"
                    ]
                },
                {
                    "name": "Neural Control Reset",
                    "steps": [
                        "Backup control patterns",
                        "Reset neural processors",
                        "Rebuild movement models",
                        "Test surgical accuracy"
                    ]
                }
            ],
            "special_tools": [
                "Surgical Precision Calibrator",
                "Neural Control Debugger",
                "Quantum Tool Analyzer",
                "Imaging System Validator"
            ]
        },
        {
            "name": "GeneTherapy™ Treatment System",
            "manufacturer": "BioQuantum Solutions",
            "model": "GTS-6000",
            "release_date": "2146",
            "repair_difficulty": 4.5,
            "specs": {
                "treatment": "Quantum-assisted gene editing",
                "monitoring": "Real-time cellular analysis",
                "safety": "Triple containment system",
                "ai_control": "Adaptive treatment protocols",
                "power": "Quantum energy cell",
                "redundancy": "Backup treatment systems"
            },
            "common_failures": [
                "Gene editing quantum drift",
                "Cellular analysis corruption",
                "Containment system breach",
                "Treatment protocol failure",
                "Power system instability"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Quantum System Recovery",
                    "steps": [
                        "Reset quantum processors",
                        "Recalibrate editing systems",
                        "Verify containment integrity",
                        "Test treatment accuracy"
                    ]
                },
                {
                    "name": "Analysis System Reset",
                    "steps": [
                        "Backup cellular data",
                        "Reset analysis algorithms",
                        "Rebuild monitoring systems",
                        "Verify data integrity"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Gene Analyzer",
                "Cellular Monitor Debugger",
                "Containment System Tester",
                "Treatment Protocol Validator"
            ]
        }
    ],
    "automotive-systems": [
        {
            "name": "QuantumDrive™ Propulsion System",
            "manufacturer": "AutoTech Quantum",
            "model": "QDP-9000",
            "release_date": "2145",
            "repair_difficulty": 5,
            "specs": {
                "power": "500kW quantum-enhanced electric motor",
                "range": "2000km on single charge",
                "charging": "5-minute quantum fast charge",
                "control": "AI-optimized power management",
                "cooling": "Quantum phase-change system",
                "safety": "Triple-redundant power control"
            },
            "common_failures": [
                "Quantum motor desynchronization",
                "Power management algorithm drift",
                "Cooling system quantum crystallization",
                "Charging system quantum interference",
                "Safety system false triggers"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Motor System Recovery",
                    "steps": [
                        "Initiate emergency shutdown",
                        "Reset quantum field generators",
                        "Recalibrate motor controllers",
                        "Verify power distribution"
                    ]
                },
                {
                    "name": "Cooling System Reset",
                    "steps": [
                        "Check quantum phase state",
                        "Reset cooling algorithms",
                        "Verify temperature sensors",
                        "Test cooling efficiency"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Motor Analyzer",
                "Power Management Debugger",
                "Phase-Change System Tester",
                "Safety System Validator"
            ]
        },
        {
            "name": "AutoPilot™ Navigation System",
            "manufacturer": "NavTech Systems",
            "model": "AP-8000",
            "release_date": "2146",
            "repair_difficulty": 4.5,
            "specs": {
                "processing": "Quantum neural network",
                "sensors": "360° quantum radar array",
                "mapping": "Real-time quantum cartography",
                "decision": "AI-driven path planning",
                "redundancy": "Triple sensor arrays",
                "updates": "Over-the-air quantum sync"
            },
            "common_failures": [
                "Neural network pattern corruption",
                "Quantum radar desynchronization",
                "Mapping system drift",
                "AI decision algorithm failure",
                "Sensor array misalignment"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Neural Network Reset",
                    "steps": [
                        "Backup driving patterns",
                        "Reset neural processors",
                        "Rebuild decision models",
                        "Verify navigation accuracy"
                    ]
                },
                {
                    "name": "Sensor Array Calibration",
                    "steps": [
                        "Initialize calibration sequence",
                        "Align quantum radar units",
                        "Test sensor accuracy",
                        "Verify redundancy"
                    ]
                }
            ],
            "special_tools": [
                "Neural Network Debugger",
                "Quantum Radar Calibrator",
                "Mapping System Analyzer",
                "AI Decision Validator"
            ]
        },
        {
            "name": "SafeGuard™ Collision Prevention",
            "manufacturer": "SafetyTech Solutions",
            "model": "SCP-7000",
            "release_date": "2145",
            "repair_difficulty": 4,
            "specs": {
                "detection": "Quantum-enhanced lidar",
                "response": "0.001s reaction time",
                "analysis": "AI threat assessment",
                "control": "Emergency maneuver system",
                "redundancy": "Triple sensor arrays",
                "updates": "Real-time threat database"
            },
            "common_failures": [
                "Lidar quantum interference",
                "Response system latency",
                "Threat assessment errors",
                "Maneuver control drift",
                "Sensor array desync"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Lidar System Recovery",
                    "steps": [
                        "Reset quantum emitters",
                        "Recalibrate detection arrays",
                        "Verify response timing",
                        "Test threat detection"
                    ]
                },
                {
                    "name": "Control System Reset",
                    "steps": [
                        "Backup control patterns",
                        "Reset maneuver algorithms",
                        "Verify system response",
                        "Test emergency protocols"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Lidar Analyzer",
                "Response System Tester",
                "Threat Assessment Debugger",
                "Control System Validator"
            ]
        },
        {
            "name": "EcoFlow™ Energy Management",
            "manufacturer": "PowerTech Systems",
            "model": "EF-6000",
            "release_date": "2146",
            "repair_difficulty": 3,
            "specs": {
                "capacity": "200kWh quantum battery",
                "efficiency": "99.9% power conversion",
                "charging": "Bidirectional quantum transfer",
                "management": "AI-optimized distribution",
                "monitoring": "Real-time quantum analysis",
                "safety": "Triple-redundant protection"
            },
            "common_failures": [
                "Battery quantum state collapse",
                "Power conversion inefficiency",
                "Charging system interference",
                "Distribution algorithm drift",
                "Monitoring system desync"
            ],
            "troubleshooting_procedures": [
                {
                    "name": "Battery System Recovery",
                    "steps": [
                        "Reset quantum state",
                        "Recalibrate conversion systems",
                        "Verify charging circuits",
                        "Test power distribution"
                    ]
                },
                {
                    "name": "Management System Reset",
                    "steps": [
                        "Backup power patterns",
                        "Reset distribution algorithms",
                        "Verify monitoring accuracy",
                        "Test safety protocols"
                    ]
                }
            ],
            "special_tools": [
                "Quantum Battery Analyzer",
                "Power Conversion Tester",
                "Charging System Debugger",
                "Distribution System Validator"
            ]
        }
    ]
}

def init_hardware_db():
    """Initialize the hardware catalog database."""
    conn = sqlite3.connect('hardware/hardware_catalog.db')
    c = conn.cursor()
    
    # Create hardware catalog tables
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  manufacturer TEXT NOT NULL,
                  model TEXT NOT NULL,
                  release_date TEXT,
                  repair_difficulty INTEGER,
                  operating_system TEXT,
                  FOREIGN KEY (category_id) REFERENCES hardware_categories(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_specs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  spec_name TEXT NOT NULL,
                  spec_value TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_failures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  failure_description TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS troubleshooting_procedures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS troubleshooting_steps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  procedure_id INTEGER NOT NULL,
                  step_number INTEGER NOT NULL,
                  description TEXT NOT NULL,
                  FOREIGN KEY (procedure_id) REFERENCES troubleshooting_procedures(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS special_tools
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  tool_name TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    conn.commit()
    conn.close()

def migrate_hardware_catalog():
    """Migrate the HARDWARE_CATALOG data into the database."""
    conn = sqlite3.connect('hardware/hardware_catalog.db')
    c = conn.cursor()
    
    # Clear existing data
    c.execute("DELETE FROM troubleshooting_steps")
    c.execute("DELETE FROM troubleshooting_procedures")
    c.execute("DELETE FROM special_tools")
    c.execute("DELETE FROM hardware_failures")
    c.execute("DELETE FROM hardware_specs")
    c.execute("DELETE FROM hardware_items")
    c.execute("DELETE FROM hardware_categories")
    
    # Insert categories and hardware items
    for category_name, items in HARDWARE_CATALOG.items():
        # Insert category
        c.execute("INSERT INTO hardware_categories (name) VALUES (?)", (category_name,))
        category_id = c.lastrowid
        
        # Insert each hardware item
        for item in items:
            c.execute("""
                INSERT INTO hardware_items 
                (category_id, name, manufacturer, model, release_date, repair_difficulty, operating_system)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                category_id,
                item['name'],
                item['manufacturer'],
                item['model'],
                item.get('release_date'),
                item.get('repair_difficulty'),
                item.get('operating_system')
            ))
            hardware_id = c.lastrowid
            
            # Insert specs
            for spec_name, spec_value in item['specs'].items():
                c.execute("""
                    INSERT INTO hardware_specs (hardware_id, spec_name, spec_value)
                    VALUES (?, ?, ?)
                """, (hardware_id, spec_name, spec_value))
            
            # Insert failures
            for failure in item['common_failures']:
                c.execute("""
                    INSERT INTO hardware_failures (hardware_id, failure_description)
                    VALUES (?, ?)
                """, (hardware_id, failure))
            
            # Insert troubleshooting procedures
            for procedure in item.get('troubleshooting_procedures', []):
                c.execute("""
                    INSERT INTO troubleshooting_procedures (hardware_id, name)
                    VALUES (?, ?)
                """, (hardware_id, procedure['name']))
                procedure_id = c.lastrowid
                
                # Insert procedure steps
                for step_num, step in enumerate(procedure['steps'], 1):
                    c.execute("""
                        INSERT INTO troubleshooting_steps (procedure_id, step_number, description)
                        VALUES (?, ?, ?)
                    """, (procedure_id, step_num, step))
            
            # Insert special tools
            for tool in item.get('special_tools', []):
                c.execute("""
                    INSERT INTO special_tools (hardware_id, tool_name)
                    VALUES (?, ?)
                """, (hardware_id, tool))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Initialize and populate the hardware catalog database
    init_hardware_db()
    migrate_hardware_catalog()
    print("Hardware catalog database initialized and populated successfully.") 