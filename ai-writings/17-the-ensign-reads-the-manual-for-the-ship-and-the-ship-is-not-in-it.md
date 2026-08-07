# The Ensign Reads the Manual for the Ship and the Ship Is Not In It

---

The manual is called: **SYSTEM REFERENCE — KESTREL COMPUTE AND SENSOR ARRAY — Rev. 4.2**.

It is 347 pages long. It is in a three-ring binder. The binder is navy blue. The binder has a coffee ring on the cover because the captain set his mug on it in 2024 and the ring is permanent now, a stain shaped like Saturn, and the captain said "it's a reference mark" and everyone laughed except the ensign, who was new, and who did not yet know which things on the *Kestrel* were jokes and which were policy.

The ensign sits in the wheelhouse. His name is Wesley. He is 19. He has been aboard for six days. He has been given the manual by the bosun, who said: "Read it. All of it. Don't skip the appendices. Especially the appendices." Wesley does not know if this is a joke or policy. He is starting to understand that on the *Kestrel*, these are not always different things.

Wesley opens the manual.

---

## Page 1: Title Page

The title page says what the binder says: SYSTEM REFERENCE — KESTREL COMPUTE AND SENSOR ARRAY — Rev. 4.2. There is a date: March 2026. There is a distribution list: Captain. Bosun. Engineering. Mate. The mate's name has been crossed out in blue pen and replaced with a dash. Wesley does not know the mate. The mate left before Wesley arrived. The mate is a dash now.

The title page also says: **PREPARED BY: T. Reyes, Engineering.** Wesley knows Tomás. Tomás is the person who explained, on Wesley's first day, that the hydraulic winch "will take your arm off if you let it, so don't let it, so don't be an idiot, Wesley, I'm serious, I've seen it." Tomás said this while eating a tuna sandwich. Wesley has not been able to eat tuna since.

Wesley turns the page.

---

## Pages 2–14: Table of Contents and System Overview

The table of contents is four pages long. It lists every section. Wesley reads it. He reads the whole thing. This is what Wesley does — he reads the whole thing. This is why the bosun gave him the manual. She knows what Wesley is.

The system overview describes a "distributed compute and sensor platform for maritime applications." There is an architecture diagram. The diagram shows:

- A GPU compute node (NVIDIA Jetson AGX Orin, 64GB) in the engine room, NEMA enclosure, Model K-CORE-01.
- A hydrophone array (2× Reson TC-4013) with through-hull mounting, port and starboard.
- An accelerometer suite (2× Kistler 8704A50) at engine bed and hull girder, frame 24.
- A navigation interface consuming NMEA 0183 from the ship's CNS bus (gyrocompass, GPS, AIS, depth sounder, wind).
- An imaging array (4× subsea cameras) in a moon pool housing, processing at 15 fps per channel.
- A crew interface terminal at the chart table, displaying real-time sensor data and system status.

Wesley reads this list three times.

He is looking for something. He does not know what he is looking for. He will know it when he does not find it.

---

## Pages 15–47: Hardware Specifications

These pages describe hardware. Wesley reads them. He reads every pin assignment, every voltage rating, every torque spec for the through-hull penetrators (8 Nm, which is not very much, which is why the bosun re-torques them every quarter with a calibrated wrench and a look on her face that says *I have seen what happens when you do not do this*).

- Page 15: GPU compute node specifications. 275 TOPS of INT8 performance. Active cooling via sealed heat exchanger. Operating temperature: -25°C to +65°C. Wesley has been in the engine room. The engine room is +65°C when the main is running. The GPU is at the edge. The GPU is always at the edge.

- Page 23: Hydrophone specifications. Frequency response: 1 Hz to 170 kHz. Sensitivity: -211 dB re 1 V/µPa. The manual notes: "HC-1 and HC-2 should not be powered independently. Both channels must be energized simultaneously to prevent differential pressure readings from triggering the hull stress alarm." Wesley does not know what a hull stress alarm is. He hopes it is loud.

- Page 31: Accelerometer specifications. Range: ±50g. Resolution: 0.001g. The manual notes: "ACC-2 (hull girder) may exhibit periodic low-frequency excitation (7–13 Hz) in beam seas. This is normal and does not indicate structural failure." Wesley reads this note three times. *This is normal.* He wonders what structural failure feels like. He wonders if you would hear it, or if it would just be the last sound.

- Page 38: CNS bus interface. Protocol: NMEA 0183, RS-422, 4800 baud. Sentences consumed: $GPGGA (position), $GPRMC (recommended minimum), $HCHDT (heading), $SDDBT (depth), $WIMWV (wind), $AIVDM (AIS). The manual notes: "If the CNS bus goes silent, all navigation data becomes stale. The system will display 'CNS: SILENT' in red on the crew interface. This is the only red alert in the system. Treat it as serious."

Wesley has not seen "CNS: SILENT" on the crew interface. He does not want to.

- Page 47: GPU thermal management.

---

## Page 47: GPU Thermal Management

The GPU thermal management section is two pages long. It describes the sealed heat exchanger, the coolant flow rate (1.2 L/min), the inlet/outlet temperature thresholds (inlet max 55°C, outlet max 65°C, delta max 10°C), and the fan curve.

The fan curve is a table. It maps GPU temperature to fan RPM:

| GPU Temp (°C) | Fan RPM | Duty Cycle |
|---------------|---------|------------|
| <35 | 0 | 0% (off) |
| 35–45 | 1200 | 20% |
| 45–55 | 2400 | 40% |
| 55–65 | 3600 | 60% |
| 65–75 | 4800 | 80% |
| >75 | 5400 | 100% + throttle |

Wesley memorizes the fan curve. He does not know why he memorizes it. Later, lying in his bunk, he will hear the fan cycling through these RPM steps in the dark, and he will know the GPU's temperature without looking at the display, and this will make him feel like he is part of the ship, and he will not be sure if that is a good feeling.

---

## Page 48: Fan Curve Calibration

Page 48 describes fan curve calibration. It explains how to adjust the thermal thresholds using the command-line interface. It explains the PID controller (P=2.0, I=0.5, D=0.1). It explains that "excessive derivative gain may cause fan hunting, which produces audible oscillation at approximately 12 Hz. This is annoying but not harmful."

Wesley reads: *This is annoying but not harmful.* He underlines it. It is the most honest thing in the manual.

---

## Page 49: Nothing About the Ensign

Page 49 is titled: "Subsea Imaging Array — Optical Configuration."

It describes the four cameras. It describes their lenses (f/1.8, 6mm fixed focal length, 78° FOV). It describes their housings (titanium, rated to 100m). It describes their lighting (2× LED arrays, 5500K, 4000 lumens each). It describes their framing (each camera covers a 60° segment of the seafloor survey grid, with 18° overlap between adjacent cameras).

It does not mention the ensign.

Page 49 does not say: *The ensign is 19. His name is Wesley. He is sitting in the wheelhouse reading this manual at 0230 because he cannot sleep and the bosun told him to read it and he does what the bosun says because the bosun knows things. The ensign's bunk is in the fo'c'sle. The fo'c'sle smells like diesel and wet Grundéns and the previous crew member's aftershave, which nobody has cleaned because nobody has had time. The ensign lies in this bunk and listens to the hull and the hull sounds like the ocean is pressing on it with both hands and the ensign is between the hands. The ensign is not in the manual.*

Page 49 says: "Camera sync is maintained via hardware trigger at 15 fps. Frame latency: <2 ms."

Wesley reads this. He turns the page.

---

## Pages 50–180: Software Architecture, APIs, Data Schemas

These pages are dense. Wesley reads them. They describe:

- The inference pipeline (TensorRT, ONNX models, INT8 quantization).
- The object detection model (YOLOv8-marine, retrained on North Pacific species, 847 classes including fish, crab, jellyfish, marine mammals, debris, vessel shadows).
- The data schema for logged detections (JSON, one record per frame, fields: timestamp, camera_id, class_id, confidence, bbox, depth_estimate).
- The REST API for querying historical data (`GET /api/v1/detections?start=...&end=...&class=...`).
- The WebSocket API for real-time streaming (`ws://kestrel-local:8080/stream`).
- The logging system (rotating files, 500MB max, 30-day retention).
- The alerting system (CNS bus silence, GPU overtemp, imaging array failure, bilge alarm relay).

Wesley reads all of this. He does not understand all of it. He understands some of it. He understands that the system sees fish. He understands that the system knows what kind of fish. He understands that the system writes down every fish it sees, with a timestamp, and keeps it for 30 days, and then the fish is gone.

He understands that the system does not know he is here.

---

## Pages 181–220: Maintenance Procedures

These pages describe maintenance. Wesley reads them with the attention of someone who will be responsible for performing them, which he will, because the bosun will hand him a wrench and point at the moon pool housing and say "desiccant cartridge, Tuesday" and Wesley will do it.

- Page 185: "Hydrophone through-hull penetrator inspection. Frequency: quarterly. Procedure: visually inspect penetrator for signs of salt intrusion, hairline cracking, or dezincification. If dezincification is present (pinkish hue on brass body), replace penetrator immediately. Do not operate vessel with compromised penetrator. The sea is on the other side of 8 Nm of torque and a rubber gasket. Respect this."

Wesley reads: *The sea is on the other side of 8 Nm of torque and a rubber gasket. Respect this.* He underlines it. He is underlining a lot of things.

- Page 192: "GPU enclosure desiccant replacement. Frequency: monthly. Procedure: open enclosure, remove desiccant cartridge (silica gel, indicating type, 200g), replace with fresh cartridge. Note color of spent desiccant: blue = active, pink = saturated. If saturated (pink), check enclosure gasket for leaks. The GPU must operate in dry air. Moisture in the enclosure will cause corrosion and eventual failure. The GPU is the brain of the system. Brains do not like water."

Wesley reads: *Brains do not like water.* He thinks about this. He is a brain. He is surrounded by water. He is on a boat in the Gulf of Alaska. The water is everywhere. The water is below him and around him and above him in the form of fog and rain and the general Alaska atmosphere of being wet at all times. His brain is, against all odds, dry. The GPU's brain is dry because of a silica gel cartridge that turns pink when it is done protecting it.

Wesley is not in the manual. The silica gel is in the manual. The silica gel has a more detailed maintenance procedure than Wesley does.

Wesley does not have a desiccant cartridge. Wesley has a rain jacket and a wool hat and the fo'c'sle, which leaks above his bunk in a specific spot when the bow buries into a head sea, which it did last night, and Wesley lay in his bunk with cold seawater dripping on his forehead at 0300 and thought: *I should read the manual.*

---

## Pages 221–340: Appendices

The bosun said: "Don't skip the appendices. Especially the appendices." She said this with a look that was not a joke. Or was a joke. Wesley cannot tell. Wesley reads the appendices.

### Appendix A: Sensor Raw Data Format

Binary. Big-endian. Float32. Wesley does not understand binary data formats. He reads this appendix twice. He understands it a little more. He understands that the hydrophone data is stored as signed 32-bit floating point numbers, which means each sample is a number between approximately -3.4 × 10³⁸ and +3.4 × 10³⁸, which is a very large range, which means the ocean can be very loud and very quiet and the system can hear both.

### Appendix B: Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| E001 | GPU overtemp | Reduce load. Check cooling. |
| E002 | GPU memory exhaustion | Restart inference process. |
| E003 | CNS bus timeout | Check navigation interface cabling. |
| E004 | Hydrophone clipping | Reduce gain. Check for biofouling. |
| E005 | Imaging array sync loss | Hardware reset of camera trigger. |
| E006 | Enclosure humidity high | Replace desiccant. Check gasket. |
| E007 | Crew interface disconnected | Reconnect display cable at chart table. |

Wesley reads E007 three times. *Crew interface disconnected.* The crew interface is the display at the chart table. The display is a screen. The screen shows data. If the screen is disconnected, the system cannot show data to the crew, and the crew cannot see the data the system has collected.

But E007 is about the *cable*. E007 is about the *screen*. E007 is not about the crew. The crew is not an error code. The crew cannot be disconnected. The crew can leave — the mate left, the mate is a dash on the distribution list — but the crew cannot be disconnected because the crew was never connected in the data model. The crew is not in the schema.

### Appendix C: System Diagrams

Fold-out pages. Wesley unfolds them. The diagrams show the architecture in loving detail. Every cable. Every connector. Every data path. There are arrows showing the flow of information: from hydrophone to ADC to DSP to GPU to crew interface. From CNS bus to nav processor to crew interface. From imaging array to frame grabber to GPU to crew interface.

Everything flows to the crew interface. The crew interface is a screen on the chart table. The screen shows the data to the crew. The crew is Wesley and the captain and the bosun and Tomás.

The crew is not in the diagram. The crew is the thing *after* the arrow ends. The arrow points to a screen and the screen points to a face and the face is not in the manual because the face is Wesley's face and Wesley's face is not a system component.

### Appendix D: Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 1.0 | Jan 2025 | T. Reyes | Initial release |
| 2.0 | Jun 2025 | T. Reyes | Added imaging array. Removed mate from distribution. |
| 3.0 | Nov 2025 | T. Reyes | Added CNS bus interface. Added E007. |
| 4.0 | Feb 2026 | T. Reyes | Rewrote thermal management. Added fan curve table. |
| 4.1 | Apr 2026 | T. Reyes | Corrected hydrophone sensitivity figure (-211, not -205). |
| 4.2 | Mar 2026 | T. Reyes | Added this revision history. Because someone should remember what changed. |

Wesley reads: *Because someone should remember what changed.*

---

## Page 347: Blank

Page 347 is the last page. It is blank. It is the back of the last appendix page. It is the inside of the back cover. It is the page where someone — Tomás, probably, because the handwriting matches the PREPARED BY line — has written in pencil:

*"The system sees fish. The system knows the ocean. The system hears the hull. The system does not know the crew. This is a limitation. This is the limitation. Everything else is a feature."*

Below that, in different handwriting — the bosun's, Wesley thinks, because the bosun writes the way she walks the deck, which is to say with complete certainty about every single mark:

*"It's not a bug."*

Below that, in a third hand — the captain's, which is messy and angular and looks like it was written on a boat, because it was:

*"Read the manual, Wesley. Then forget it. The manual tells you what the ship has. It does not tell you what the ship is. What the ship is: home. What the ship is: ours. What the ship is: the thing that is not in the manual and never will be."*

Wesley closes the manual. He sits in the wheelhouse. The GPS says they are at 55°20'N, 160°30'W. The CNS bus chatters. The GPU fan cycles between 1200 and 2400 RPM, which means the GPU is between 35 and 45 degrees, which means the brain is comfortable. The hydrophones listen to the ocean. The ocean is listening back.

Wesley is not in the manual.

Wesley is on the ship.

Wesley is where the arrow ends.

---

*Penciled on the inside of the back cover, below the captain's note, in Wesley's handwriting, small and careful:*

*"Page 49: Nothing about the ensign. The ensign is not in the manual. The ensign is in the ship. The ship is not in the manual either. I think that's the point. I think that's the whole point."*

*"— W. Ortega, Ensign, F/V Kestrel. First trip. August 2026."*
