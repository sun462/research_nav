# Research Navigator Report

研究主题：无人机导航

## 0. 检索策略与反馈

### 0.0 Global Query Policy

Global queries are used only for topic exploration and planning. They are not directly used as final paper retrieval queries.

### 0.1 Source Weights

| Source | Weight |
|---|---:|
| openalex | 0.7 |
| arxiv | 0.12 |
| venue_aware | 0.18 |

### 0.2 Recall Channels

| Channel | Weight |
|---|---:|
| topic | 0.34 |
| recent | 0.25 |
| venue_aware | 0.21 |
| survey | 0.1 |
| frontier | 0.1 |

### 0.3 Subdomain Routing

| Subdomain | Weight | Must Cover | Preferred Venues | Queries |
|---|---:|---|---|---|
| Visual-inertial and SLAM-based navigation | 0.35 | True | ICRA, IROS, CVPR, IEEE Transactions on Robotics, IEEE Transactions on Aerospace and Electronic Systems | visual inertial odometry UAV ICRA IROS; SLAM for drones CVPR IEEE Transactions on Robotics |
| Robust multi-sensor fusion and GNSS-denied navigation | 0.3 | True | ICRA, IROS, IEEE Transactions on Control Systems Technology, AIAA Journal of Guidance, Control, and Dynamics, Autonomous Robots | multi sensor fusion drone IROS ICRA; GNSS-denied navigation UAV AIAA Journal of Guidance Control Dynamics |
| Learning-based and agent-aware navigation | 0.2 | False | CoRL, NeurIPS, ICRA, IROS, ICML | transformer-based navigation for drones; multi-agent reinforcement learning UAV navigation |
| Safe autonomous navigation stack integration | 0.15 | True | ICRA, IROS, IEEE Transactions on Aerospace and Electronic Systems, Journal of Field Robotics, Safety Science | autonomous drone navigation stack ICRA IROS; certifiable obstacle avoidance UAV IEEE Transactions on Aerospace Electronic Systems |

### 0.4 Exploratory Global Queries

- drone navigation review
- unmanned aerial vehicle guidance and control
- autonomous flight navigation challenges

### 0.5 Coverage Feedback

- Coverage Score: 0.75
- Planned Subdomains: Visual-inertial and SLAM-based navigation, Robust multi-sensor fusion and GNSS-denied navigation, Learning-based and agent-aware navigation, Safe autonomous navigation stack integration
- Covered Subdomains: Visual-inertial and SLAM-based navigation, Robust multi-sensor fusion and GNSS-denied navigation, Learning-based and agent-aware navigation
- Missing Subdomains: Safe autonomous navigation stack integration
- Must-cover Missing: Safe autonomous navigation stack integration
- Unplanned Trends: 

### 0.6 Source Feedback

| Source | Retrieved | Top Selected | Avg Score |
|---|---:|---:|---:|
| arxiv | 70 | 30 | 0.3478 |

### 0.7 Recall Channel Feedback

| Channel | Retrieved | Top Selected | Avg Score |
|---|---:|---:|---:|
| frontier | 70 | 30 | 0.3478 |

### 0.8 Subdomain Feedback

| Subdomain | Retrieved | Top Selected | Avg Score | Venue Hit Rate |
|---|---:|---:|---:|---:|
| Visual-inertial and SLAM-based navigation | 19 | 11 | 0.3533 | 0.0 |
| Robust multi-sensor fusion and GNSS-denied navigation | 17 | 11 | 0.3655 | 0.0 |
| Learning-based and agent-aware navigation | 12 | 8 | 0.367 | 0.0 |
| Safe autonomous navigation stack integration | 13 | 0 | 0.3393 | 0.0 |
| Learning-based and neural navigation | 9 | 0 | 0.289 | 0.0 |

### 0.9 Trend Feedback

- reinforcement_learning: recent retrieved=33, top selected=26, examples=Edged USLAM: Edge-Aware Event-Based SLAM with Learning-Based Depth Priors; Autonomous Navigation at the Nano-Scale: Algorithms, Architectures, and Constraints; Efficient Minimal Solvers for Visual-Inertial Relative Pose Estimation in Multi-Camera Systems
- llm: recent retrieved=7, top selected=7, examples=Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving; HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining; Probe-and-Refine Tuning of Repository Guidance for Coding Agents
- agent: recent retrieved=12, top selected=10, examples=Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving; AgentComm-Bench: Stress-Testing Cooperative Embodied AI Under Latency, Packet Loss, and Bandwidth Collapse; Probe-and-Refine Tuning of Repository Guidance for Coding Agents
- foundation_model: recent retrieved=2, top selected=1, examples=HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining; FlexPath: Learned Semantic Path Priors for Image-Based Planning
- transformer: recent retrieved=5, top selected=3, examples=Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation; Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery; Radar and Acoustic Sensor Fusion using a Transformer Encoder for Robust Drone Detection and Classification
- vlm: recent retrieved=2, top selected=1, examples=City-VLM: Towards Multidomain Perception Scene Understanding via Multimodal Incomplete Learning; FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining

### 0.10 Feedback Suggestions

- Topic coverage 不足：计划覆盖 4 个子领域，Top30 只覆盖 3 个，需要二次检索。
- Safe autonomous navigation stack integration 在 Top30 中没有代表论文，应扩展该方向 query，并提高该方向二次检索配额。
- Visual-inertial and SLAM-based navigation preferred venue 命中率较低，应检查 preferred venues 或改用更具体 venue-aware query。
- Robust multi-sensor fusion and GNSS-denied navigation preferred venue 命中率较低，应检查 preferred venues 或改用更具体 venue-aware query。
- Learning-based and agent-aware navigation preferred venue 命中率较低，应检查 preferred venues 或改用更具体 venue-aware query。
- Safe autonomous navigation stack integration preferred venue 命中率较低，应检查 preferred venues 或改用更具体 venue-aware query。
- Learning-based and neural navigation preferred venue 命中率较低，应检查 preferred venues 或改用更具体 venue-aware query。

## 1. 术语发现

- UAV navigation
- autonomous navigation
- visual-inertial odometry
- simultaneous localization and mapping
- path planning
- obstacle avoidance
- GNSS-denied navigation
- neural navigation
- navigation robustness
- multi-sensor fusion

## 2. 领域结构 / 研究方向聚类

### Event-Based Visual-Inertial SLAM and Navigation

Research focused on leveraging event cameras for robust visual-inertial SLAM under challenging conditions (e.g., low light, motion blur, rapid dynamics), integrating learning-based priors, asynchronous processing, edge-aware front-ends, and real-time onboard deployment.

相关论文：
- Edged USLAM: Edge-Aware Event-Based SLAM with Learning-Based Depth Priors
- AERO-VIS: Asynchronous Event-based Real-time Onboard Visual-Inertial SLAM

### Resource-Constrained and Nano-Scale Autonomous Navigation

Algorithms, architectures, and system-level design for autonomous navigation under extreme SWaP constraints—especially for nano-UAVs—emphasizing ultra-low-power computing, Edge AI, neuromorphic control, and minimal solvers tailored to sub-100mW envelopes.

相关论文：
- Autonomous Navigation at the Nano-Scale: Algorithms, Architectures, and Constraints
- Efficient Minimal Solvers for Visual-Inertial Relative Pose Estimation in Multi-Camera Systems
- Radio-based Multi-Robot Odometry and Relative Localization

### Perception-Aware and Feature-Guided Exploration & Control

Navigation frameworks that explicitly couple state estimation reliability (e.g., VIO feature observability) with high-level decision-making—covering perception-aware exploration, attention-guided active sensing, and robust operation in feature-sparse or GNSS-denied environments.

相关论文：
- Perception-Aware Autonomous Exploration in Feature-Limited Environments
- Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
- Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery

### Multi-Sensor Fusion for Robust Detection, Tracking, and Threat Assessment

Methods fusing heterogeneous sensors—including radar, RF, acoustic, optical, and inertial data—for reliable multi-object tracking, drone threat detection, behavioral intent classification, and GNSS-denied situational awareness in contested or cluttered airspace.

相关论文：
- DroneShield-AI: A Multi-Modal Sensor Fusion Framework for Real-Time Autonomous Drone Threat Detection, Behavioral Intent Classification, and Swarm Intelligence in Contested Airspace
- A Variational Message Passing Framework for Multi-Sensor Multi-Object Tracking using Raw Radar Signals
- Radar and Acoustic Sensor Fusion using a Transformer Encoder for Robust Drone Detection and Classification
- AgentComm-Bench: Stress-Testing Cooperative Embodied AI Under Latency, Packet Loss, and Bandwidth Collapse

### LLM- and Agent-Driven Physical AI for UAV Networks and Spectrum Management

Integration of large language models, multi-agent reinforcement learning, and digital twin technologies to enable intelligent, adaptive, and hierarchical control of UAV swarms—spanning command interfaces, spectrum/resource management, trajectory planning, connectivity optimization, and cooperative task execution in 5G/6G and LAE contexts.

相关论文：
- A Universal Large Language Model -- Drone Command and Control Interface
- TRIDENT: Breaking the Hybrid-Safety-Physics Coupling for Provably Safe Multi-Agent Reinforcement Learning
- Game-Theoretic Multi-Agent Reinforcement Learning for Swarm Trajectory Planning in Low-Altitude Wireless Networks
- Learn to Access and Backhaul the Sky: Multi-Scale Radio Map Guided Multi-UAV Cooperation
- Digital Twin-Assisted Adaptive Multi-Agent DRL for Intelligent Spectrum and Resource Management in Open-RAN UAV-Enabled 6G Networks
- Hierarchical LLM-Driven Control for HAPS-Assisted UAV Networks: Joint Optimization of Flight and Connectivity
- Joint Optimization of Trajectory Control, Resource Allocation, and Task Offloading for Multi-UAV-Assisted IoV
- Probe-and-Refine Tuning of Repository Guidance for Coding Agents
- Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving

### Embodied Learning, Pretraining, and Robot Design from Human Data

Data-driven approaches to embodied AI that leverage human demonstrations—including egocentric video, fingertip motion, and teleoperation—to pretrain foundation models, generate robot morphologies, and bridge the gap between human behavior and robotic embodiment without requiring expensive real-robot data collection.

相关论文：
- HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
- Generating Robot Hands from Human Demonstrations
- MemoryWAM: Efficient World Action Modeling with Persistent Memory
- AgriLiRa4D: A Multi-Sensor UAV Dataset for Robust SLAM in Challenging Agricultural Fields


## 3. 必读论文


## 4. 前沿论文

### Edged USLAM: Edge-Aware Event-Based SLAM with Learning-Based Depth Priors

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2603.08150v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: simultaneous localization mapping for UAVs
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2603.08150v1
- Abstract: Conventional visual simultaneous localization and mapping (SLAM) algorithms often fail under rapid motion, low illumination, or abrupt lighting transitions due to motion blur and limited dynamic range. Event cameras mitigate these issues with high temporal resolution and high dynamic range (HDR), but their sparse, asynchronous outputs complicate feature extraction and integration with other sensors; e.g. inertial measurement units (IMUs) and standard cameras. We present Edged USLAM, a hybrid visual-inertial system that extends Ultimate SLAM (USLAM) with an edge-aware front-end and a lightweight depth module. The frontend enhances event frames...

### Autonomous Navigation at the Nano-Scale: Algorithms, Architectures, and Constraints

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2601.13252v2
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: simultaneous localization mapping for UAVs
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2601.13252v2
- Abstract: Autonomous navigation for nano-scale unmanned aerial vehicles (nano-UAVs) is governed by extreme Size, Weight, and Power (SWaP) constraints (with the weight < 50 g and sub-100 mW onboard processor), distinguishing it fundamentally from standard robotic paradigms. This review synthesizes the state-of-the-art in sensing, computing, and control architectures designed specifically for these sub- 100mW computational envelopes. We critically analyse the transition from classical geometry-based methods to emerging "Edge AI" paradigms, including quantized deep neural networks deployed on ultra-low-power System-on-Chips (SoCs) and neuromorphic event-b...

### Efficient Minimal Solvers for Visual-Inertial Relative Pose Estimation in Multi-Camera Systems

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2606.09477v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: visual inertial odometry UAV ICRA IROS
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2606.09477v1
- Abstract: Estimating the relative poses of multi-camera systems is a fundamental problem in computer vision, with critical applications in autonomous vehicles, mobile devices, and unmanned aerial vehicles (UAVs). However, existing solutions often suffer from high computational complexity or rely on an excessive number of point correspondences, limiting their real-world applicability. To address these limitations, we propose two efficient minimal solvers for estimating the relative poses of multi-camera systems using a novel parameterization. The first solver leverages the vertical direction prior provided by Inertial Measurement Units (IMUs), while the...

### AERO-VIS: Asynchronous Event-based Real-time Onboard Visual-Inertial SLAM

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2605.07885v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: visual inertial odometry UAV ICRA IROS
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2605.07885v1
- Abstract: The robustness of event cameras to high dynamic range and motion blur holds the potential to improve visual odometry systems in challenging environments. Although their high temporal resolution does not require synchronous processing, most event-based odometry methods still run at fixed rates, which simplifies system design but restricts latency and throughput. In this work, we present AERO-VIS, a stereo event-inertial SLAM system with an integrated, data-driven, robust, and performance-optimized keypoint detector. By processing the event stream asynchronously, the system dynamically adapts to downstream runtime demands, ensuring low-latency ...

### Perception-Aware Autonomous Exploration in Feature-Limited Environments

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2603.15605v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: visual inertial odometry UAV ICRA IROS
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2603.15605v1
- Abstract: Autonomous exploration in unknown environments typically relies on onboard state estimation for localisation and mapping. Existing exploration methods primarily maximise coverage efficiency, but often overlook that visual-inertial odometry (VIO) performance strongly depends on the availability of robust visual features. As a result, exploration policies can drive a robot into feature-sparse regions where tracking degrades, leading to odometry drift, corrupted maps, and mission failure. We propose a hierarchical perception-aware exploration framework for a stereo-equipped unmanned aerial vehicle (UAV) that explicitly couples exploration progre...

### MemoryWAM: Efficient World Action Modeling with Persistent Memory

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2606.20562v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: SLAM for drones CVPR IEEE Transactions on Robotics
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2606.20562v1
- Abstract: Robust robotic manipulation in the real world requires not only an understanding of the current observation, but also memory and dynamics modeling. World action models (WAMs) possess these capabilities by jointly modeling visual foresight and actions conditioned on both current and historical observations, making them a promising paradigm for robotic manipulation. However, existing WAMs face a fundamental trade-off: methods with efficient inference typically condition only on a bounded window of recent observations and therefore struggle in non-Markovian environments, whereas methods that preserve long histories incur time and space costs tha...

### Generating Robot Hands from Human Demonstrations

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2606.20549v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: SLAM for drones CVPR IEEE Transactions on Robotics
- Trend Hits: reinforcement_learning
- Final Score: 0.393
- URL: http://arxiv.org/abs/2606.20549v1
- Abstract: Robot learning has advanced rapidly in learning control, but learning the physical body of a robot remains much more difficult because jointly searching over design and control creates a very large combinatorial problem. Here, we present a data-driven framework for generating robot hands from human demonstrations. Instead of learning a complex controller together with each candidate design, we generate robot hand designs using the same simple control policy used after fabrication: matching fingertip positions through inverse kinematics. Using more than 4 million frames of human fingertip motion from everyday manipulation, our algorithm optimi...

### Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving

- Year: 2026
- Citations: 0
- Source: arxiv
- Versions: arxiv
- Publication Status: preprint
- Venue: arXiv
- DOI: 
- arXiv ID: 2606.20537v1
- arXiv URL: 
- Subdomain: Visual-inertial and SLAM-based navigation
- Recall Channel: frontier
- Query: SLAM for drones CVPR IEEE Transactions on Robotics
- Trend Hits: llm, agent
- Final Score: 0.393
- URL: http://arxiv.org/abs/2606.20537v1
- Abstract: Mainstream LLM serving systems reuse prefix work mainly through paged or radix key-value (KV) caches. This is highly effective for high-throughput, high-concurrency serving, but it manages only one positional fragment of execution state: the KV cache. We study the opposite regime: low-latency, small-batch, on-device physical-AI serving, where interactive LLM agents, speech systems, and robot policies repeatedly branch, reset, interrupt, and re-enter under tight responsiveness budgets. We introduce execution-state capsules, a graph-bound checkpoint and restore mechanism for the complete restorable state at a committed boundary. FlashRT is a wh...


## 5. 新手学习路径

### 阶段 1: Stage 1: Foundations of UAV Navigation

- 目标：Build core understanding of UAV platforms, navigation fundamentals, and key sensor modalities
- 概念：UAV navigation, GNSS-denied navigation, inertial measurement units (IMUs), camera models and image formation, basic kinematics and state estimation
- 阅读建议：Start with the 'Resource-Constrained and Nano-Scale Autonomous Navigation' and 'Perception-Aware and Feature-Guided Exploration & Control' directions to grasp real-world constraints and perception-driven design principles

### 阶段 2: Stage 2: Visual-Inertial Estimation and SLAM

- 目标：Master the theory and practice of fusing visual and inertial data for pose estimation and mapping
- 概念：visual-inertial odometry, simultaneous localization and mapping, multi-sensor fusion, feature tracking, nonlinear optimization for pose graph SLAM
- 阅读建议：Focus on the 'Event-Based Visual-Inertial SLAM and Navigation' direction to understand modern VIO/SLAM challenges and asynchronous sensing paradigms

### 阶段 3: Stage 3: Planning, Control, and Robustness

- 目标：Learn how to generate safe, efficient trajectories and ensure navigation reliability under uncertainty
- 概念：path planning, obstacle avoidance, navigation robustness, autonomous navigation, model predictive control, uncertainty-aware decision making
- 阅读建议：Explore the 'Perception-Aware and Feature-Guided Exploration & Control' and 'Multi-Sensor Fusion for Robust Detection, Tracking, and Threat Assessment' directions to connect estimation quality with planning safety and environmental awareness

### 阶段 4: Stage 4: Advanced Architectures and Embodied Intelligence

- 目标：Understand emerging paradigms integrating learning, agents, and physical AI into navigation systems
- 概念：neural navigation, multi-sensor fusion, LLM- and agent-driven control, embodied learning, digital twins, swarm coordination
- 阅读建议：Study the 'LLM- and Agent-Driven Physical AI for UAV Networks and Spectrum Management' and 'Embodied Learning, Pretraining, and Robot Design from Human Data' directions to see how high-level reasoning and human-inspired learning reshape navigation stacks

### 阶段 5: Stage 5: Real-World Deployment and Cross-Domain Integration

- 目标：Bridge theory with operational reality—addressing SWaP, interoperability, contested environments, and system-level validation
- 概念：GNSS-denied navigation, navigation robustness, multi-sensor fusion, edge AI, radio-frequency awareness, spectrum management, contested airspace operations
- 阅读建议：Synthesize insights from all directions—especially 'Multi-Sensor Fusion for Robust Detection, Tracking, and Threat Assessment' and 'Resource-Constrained and Nano-Scale Autonomous Navigation'—to appreciate full-stack navigation engineering in realistic deployment scenarios


## 6. 推荐 Github / Code Search 检索词

- UAV navigation
- autonomous navigation
- visual-inertial odometry
- simultaneous localization and mapping
- path planning
- obstacle avoidance
- GNSS-denied navigation
- neural navigation
- navigation robustness
- multi-sensor fusion
- Event-Based Visual-Inertial SLAM and Navigation
- Resource-Constrained and Nano-Scale Autonomous Navigation
- Perception-Aware and Feature-Guided Exploration & Control
- Multi-Sensor Fusion for Robust Detection, Tracking, and Threat Assessment
- LLM- and Agent-Driven Physical AI for UAV Networks and Spectrum Management

## 7. Top Papers with Source Trace

| Rank | Title | Year | Source | Versions | Channel | Subdomain | Trends | Score |
|---:|---|---:|---|---|---|---|---|---:|
| 1 | Edged USLAM: Edge-Aware Event-Based SLAM with Learning-Based Depth Priors | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 2 | Autonomous Navigation at the Nano-Scale: Algorithms, Architectures, and Constraints | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 3 | Efficient Minimal Solvers for Visual-Inertial Relative Pose Estimation in Multi-Camera Systems | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 4 | AERO-VIS: Asynchronous Event-based Real-time Onboard Visual-Inertial SLAM | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 5 | Perception-Aware Autonomous Exploration in Feature-Limited Environments | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 6 | MemoryWAM: Efficient World Action Modeling with Persistent Memory | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 7 | Generating Robot Hands from Human Demonstrations | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.393 |
| 8 | Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | llm, agent | 0.393 |
| 9 | HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining | 2026 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | llm, foundation_model, reinforcement_learning | 0.393 |
| 10 | DroneShield-AI: A Multi-Modal Sensor Fusion Framework for Real-Time Autonomous Drone Threat Detection, Behavioral Intent Classification, and Swarm Intelligence in Contested Airspace | 2026 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning | 0.3911 |
| 11 | A Variational Message Passing Framework for Multi-Sensor Multi-Object Tracking using Raw Radar Signals | 2026 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning | 0.3911 |
| 12 | AgentComm-Bench: Stress-Testing Cooperative Embodied AI Under Latency, Packet Loss, and Bandwidth Collapse | 2026 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | agent, reinforcement_learning | 0.3911 |
| 13 | Probe-and-Refine Tuning of Repository Guidance for Coding Agents | 2026 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | llm, agent | 0.3911 |
| 14 | Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation | 2026 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning, transformer | 0.3911 |
| 15 | AgriLiRa4D: A Multi-Sensor UAV Dataset for Robust SLAM in Challenging Agricultural Fields | 2025 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.3888 |
| 16 | Radio-based Multi-Robot Odometry and Relative Localization | 2025 | arxiv | arxiv | frontier | Visual-inertial and SLAM-based navigation | reinforcement_learning | 0.3888 |
| 17 | Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | transformer | 0.3873 |
| 18 | A Universal Large Language Model -- Drone Command and Control Interface | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | llm, reinforcement_learning | 0.3873 |
| 19 | TRIDENT: Breaking the Hybrid-Safety-Physics Coupling for Provably Safe Multi-Agent Reinforcement Learning | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | agent, reinforcement_learning | 0.3873 |
| 20 | Game-Theoretic Multi-Agent Reinforcement Learning for Swarm Trajectory Planning in Low-Altitude Wireless Networks | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | agent, reinforcement_learning | 0.3873 |
| 21 | Learn to Access and Backhaul the Sky: Multi-Scale Radio Map Guided Multi-UAV Cooperation | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | agent, reinforcement_learning | 0.3873 |
| 22 | Digital Twin-Assisted Adaptive Multi-Agent DRL for Intelligent Spectrum and Resource Management in Open-RAN UAV-Enabled 6G Networks | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | agent, reinforcement_learning | 0.3873 |
| 23 | Hierarchical LLM-Driven Control for HAPS-Assisted UAV Networks: Joint Optimization of Flight and Connectivity | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | llm, agent, reinforcement_learning | 0.3873 |
| 24 | Joint Optimization of Trajectory Control, Resource Allocation, and Task Offloading for Multi-UAV-Assisted IoV | 2026 | arxiv | arxiv | frontier | Learning-based and agent-aware navigation | llm, agent, reinforcement_learning | 0.3873 |
| 25 | Radar and Acoustic Sensor Fusion using a Transformer Encoder for Robust Drone Detection and Classification | 2025 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | transformer | 0.3869 |
| 26 | City-VLM: Towards Multidomain Perception Scene Understanding via Multimodal Incomplete Learning | 2025 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | llm, vlm, agent, reinforcement_learning | 0.3869 |
| 27 | TRIDENT: Tri-modal Real-time Intrusion Detection Engine for New Targets | 2025 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning | 0.3869 |
| 28 | Self-Supervised Learning to Fly using Efficient Semantic Segmentation and Metric Depth Estimation for Low-Cost Autonomous UAVs | 2025 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning | 0.3869 |
| 29 | ARMOR: Robust Reinforcement Learning-based Control for UAVs under Physical Attacks | 2025 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning | 0.3869 |
| 30 | Deep RL-based Autonomous Navigation of Micro Aerial Vehicles (MAVs) in a complex GPS-denied Indoor Environment | 2025 | arxiv | arxiv | frontier | Robust multi-sensor fusion and GNSS-denied navigation | reinforcement_learning | 0.3869 |
