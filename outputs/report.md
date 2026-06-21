# Research Navigator Report

研究主题：无人机导航

## 0. 检索策略与反馈

### 0.1 Source Weights

| Source | Weight |
|---|---:|
| openalex | 0.65 |
| arxiv | 0.2 |
| venue_boost | 0.15 |

### 0.2 Subdomain Routing

| Subdomain | Weight | Preferred Venues |
|---|---:|---|
| Multi-sensor Localization & Sensor Fusion | 0.25 | ICRA, IROS, RSS, IEEE Transactions on Robotics, IEEE Transactions on Aerospace and Electronic Systems |
| Real-time Reactive Path Planning & Obstacle Avoidance | 0.25 | ICRA, IROS, RSS, Conference on Robot Learning (CoRL), IEEE Transactions on Intelligent Transportation Systems |
| Visual Navigation & Appearance-Invariant Perception | 0.2 | CVPR, ICCV, ECCV, ICRA, IROS, IEEE Transactions on Pattern Analysis and Machine Intelligence |
| SLAM & Mapping for Autonomous Flight | 0.15 | ICRA, IROS, RSS, 3DV, IEEE Transactions on Robotics, Autonomous Robots |
| Certifiable Autonomy & Safety-Critical Navigation | 0.15 | ICRA, IROS, IEEE International Conference on Safety, Security and Rescue Robotics (SSRR), IEEE Transactions on Dependable and Secure Computing, AIAA SciTech Forum |

### 0.3 Global Queries

- drone navigation
- UAV navigation
- autonomous drone localization
- drone path planning
- visual-inertial navigation system
- UAV SLAM
- obstacle avoidance drone

### 0.4 Source Feedback

| Source | Retrieved | Top Selected | Avg Score |
|---|---:|---:|---:|
| openalex | 508 | 30 | 0.5879 |
| arxiv | 47 | 0 | 0.2755 |

### 0.5 Subdomain Feedback

| Subdomain | Retrieved | Top Selected | Avg Score | Venue Hit Rate |
|---|---:|---:|---:|---:|
| SLAM & Mapping for Autonomous Flight | 60 | 6 | 0.6113 | 0.0 |
| Multi-sensor Localization & Sensor Fusion | 79 | 7 | 0.5907 | 0.038 |
| global | 215 | 6 | 0.5228 | 0.0 |
| Visual Navigation & Appearance-Invariant Perception | 53 | 7 | 0.618 | 0.0 |
| Certifiable Autonomy & Safety-Critical Navigation | 78 | 3 | 0.5276 | 0.0 |
| Real-time Reactive Path Planning & Obstacle Avoidance | 70 | 1 | 0.5991 | 0.0286 |

### 0.6 Feedback Suggestions

- openalex 平均质量分较高，建议保留或略微提高权重。
- arxiv 返回了 47 篇，但 Top30 中没有入选，建议降低该 source 权重。
- SLAM & Mapping for Autonomous Flight 的 preferred venue 命中率较低，建议检查 venue 列表或调整 source。
- Multi-sensor Localization & Sensor Fusion 的 preferred venue 命中率较低，建议检查 venue 列表或调整 source。
- Visual Navigation & Appearance-Invariant Perception 的 preferred venue 命中率较低，建议检查 venue 列表或调整 source。
- Certifiable Autonomy & Safety-Critical Navigation 的 preferred venue 命中率较低，建议检查 venue 列表或调整 source。
- Real-time Reactive Path Planning & Obstacle Avoidance 的 preferred venue 命中率较低，建议检查 venue 列表或调整 source。

## 1. 术语发现

- 无人机定位
- 路径规划
- 避障算法
- 视觉导航
- 惯性导航
- GPS辅助导航
- SLAM
- 自主飞行

## 2. 领域结构 / 研究方向聚类

### Integrated Sensing, Communication, and Networked UAV Systems

Research focused on the convergence of wireless communication infrastructure (e.g., 5G/6G) and sensing capabilities for UAVs and aerial networks—enabling perceptive, cellular-connected, and spectrum-efficient drone operations, including UAV-assisted communications, ISAC (Integrated Sensing and Communications), and edge-AI-enabled networked services.

相关论文：
- Integrated Sensing and Communications: Toward Dual-Functional Wireless Networks for 6G and Beyond
- What Will the Future of UAV Cellular Communications Be? A Flight From 5G to 6G
- A Survey on the Convergence of Edge Computing and AI for UAVs: Opportunities and Challenges
- UAV Computing-Assisted Search and Rescue Mission Framework for Disaster and Harsh Environment Mitigation

### Multi-Sensor Fusion and Robust State Estimation for UAVs and Swarms

Advances in tightly coupled, decentralized, or IMU-centric fusion of visual, inertial, GNSS, LiDAR, UWB, and other modalities to achieve drift-free, globally consistent, and real-time pose estimation—especially under GPS-denied, dynamic, or perceptually degraded conditions for single UAVs and aerial swarms.

相关论文：
- GVINS: Tightly Coupled GNSS–Visual–Inertial Fusion for Smooth and Consistent State Estimation
- ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM
- Omni-Swarm: A Decentralized Omnidirectional Visual–Inertial–UWB State Estimation System for Aerial Swarms
- Super Odometry: IMU-centric LiDAR-Visual-Inertial Estimator for Challenging Environments
- LiDAR odometry survey: recent advancements and remaining challenges
- An Overview on Visual SLAM: From Tradition to Semantic

### Vision-Based Perception and Object Detection for UAV Applications

Development and adaptation of deep learning–based vision models (especially YOLO variants) for robust, resource-efficient detection and recognition of small, occluded, or appearance-varying targets in aerial imagery—targeting applications such as precision agriculture, plant disease monitoring, apple harvesting, landing spot identification, and SAR support.

相关论文：
- UAV-YOLOv8: A Small-Object-Detection Model Based on Improved YOLOv8 for UAV Aerial Photography Scenarios
- A Modified YOLOv8 Detection Network for UAV Aerial Image Recognition
- Comparing YOLOv3, YOLOv4 and YOLOv5 for Autonomous Landing Spot Detection in Faulty UAVs
- A Real-Time Apple Targets Detection Method for Picking Robot Based on Improved YOLOv5
- Drones in Plant Disease Assessment, Efficient Monitoring, and Detection: A Way Forward to Smart Agriculture
- A Comprehensive Survey of the Recent Studies with UAV for Precision Agriculture in Open Fields and Greenhouses
- Vision-Based Semantic Segmentation in Scene Understanding for Autonomous Driving: Recent Achievements, Challenges, and Outlooks

### Autonomous Navigation, Path Planning, and Obstacle Avoidance

Algorithms and frameworks for safe, reactive, and socially aware navigation—including geometric path planners (e.g., A*, Bug), neural and bio-inspired methods, collision avoidance schemes, and real-time trajectory generation—applied to UAVs, AGVs, and multi-robot systems operating in cluttered, dynamic, or human-populated environments.

相关论文：
- Obstacle Avoidance and Path Planning Methods for Autonomous Navigation of Mobile Robot
- Comprehensive Review of Drones Collision Avoidance Schemes: Challenges and Open Issues
- Geometric A-Star Algorithm: An Improved A-Star Algorithm for AGV Path Planning in a Port Environment
- A survey on socially aware robot navigation: Taxonomy and future challenges
- Champion-level drone racing using deep reinforcement learning

### SLAM, Mapping, and Semantic Scene Understanding for Autonomous Flight

Foundational and applied research on simultaneous localization and mapping—spanning monocular/stereo/RGB-D/visual-inertial/multimap SLAM, semantic extensions, and long-term robustness—specifically tailored for autonomous UAV flight, environmental monitoring, disaster response, and agricultural mapping in complex indoor–outdoor or natural settings.

相关论文：
- ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM
- An Overview on Visual SLAM: From Tradition to Semantic
- UAV swarms: research, challenges, and future directions
- Collaborative Multi-Robot Search and Rescue: Planning, Coordination, Perception, and Active Vision
- Drones in Plant Disease Assessment, Efficient Monitoring, and Detection: A Way Forward to Smart Agriculture
- A Real-Time Apple Targets Detection Method for Picking Robot Based on Improved YOLOv5
- A Comprehensive Survey of the Recent Studies with UAV for Precision Agriculture in Open Fields and Greenhouses

### Swarm Intelligence and Collaborative Autonomy for Aerial Robotics

Design and deployment of decentralized, coordinated, and scalable aerial swarm systems—addressing challenges in formation control, task allocation, inter-robot perception, collective navigation in unstructured environments (e.g., forests), and emergent behaviors—enabled by novel planning, estimation, and communication architectures.

相关论文：
- Swarm of micro flying robots in the wild
- Omni-Swarm: A Decentralized Omnidirectional Visual–Inertial–UWB State Estimation System for Aerial Swarms
- UAV swarms: research, challenges, and future directions
- Collaborative Multi-Robot Search and Rescue: Planning, Coordination, Perception, and Active Vision


## 3. 必读论文

### ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM

- Year: 2021
- Citations: 3816
- Source: openalex
- Venue: IEEE Transactions on Robotics
- Subdomain: global
- Query: visual-inertial navigation system
- Final Score: 0.698
- URL: https://doi.org/10.1109/tro.2021.3075644
- Abstract: This article presents ORB-SLAM3, the first system able to perform visual, visual-inertial and multimap SLAM with monocular, stereo and RGB-D cameras, using pin-hole and fisheye lens models. The first main novelty is a tightly integrated visual-inertial SLAM system that fully relies on maximum <italic xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">a posteriori</i> (MAP) estimation, even during IMU initialization, resulting in real-time robust operation in small and large, indoor and outdoor environments, being two to ten times more accurate than previo...

### Integrated Sensing and Communications: Toward Dual-Functional Wireless Networks for 6G and Beyond

- Year: 2022
- Citations: 3051
- Source: openalex
- Venue: IEEE Journal on Selected Areas in Communications
- Subdomain: SLAM & Mapping for Autonomous Flight
- Query: event-camera SLAM UAV
- Final Score: 0.725
- URL: https://doi.org/10.1109/jsac.2022.3156632
- Abstract: As the standardization of 5G solidifies, researchers are speculating what 6G will be. The integration of sensing functionality is emerging as a key feature of the 6G Radio Access Network (RAN), allowing for the exploitation of dense cell infrastructures to construct a perceptive network. In this IEEE Journal on Selected Areas in Communications (JSAC) Special Issue overview, we provide a comprehensive review on the background, range of key applications and state-of-the-art approaches of Integrated Sensing and Communications (ISAC). We commence by discussing the interplay between sensing and com...

### UAV-YOLOv8: A Small-Object-Detection Model Based on Improved YOLOv8 for UAV Aerial Photography Scenarios

- Year: 2023
- Citations: 854
- Source: openalex
- Venue: Sensors
- Subdomain: Multi-sensor Localization & Sensor Fusion
- Query: UAV sensor fusion localization
- Final Score: 0.72
- URL: https://doi.org/10.3390/s23167190
- Abstract: Unmanned aerial vehicle (UAV) object detection plays a crucial role in civil, commercial, and military domains. However, the high proportion of small objects in UAV images and the limited platform resources lead to the low accuracy of most of the existing detection models embedded in UAVs, and it is difficult to strike a good balance between detection performance and resource consumption. To alleviate the above problems, we optimize YOLOv8 and propose an object detection model based on UAV aerial photography scenarios, called UAV-YOLOv8. Firstly, Wise-IoU (WIoU) v3 is used as a bounding box re...

### Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning

- Year: 2022
- Citations: 660
- Source: openalex
- Venue: Annual Review of Control Robotics and Autonomous Systems
- Subdomain: Certifiable Autonomy & Safety-Critical Navigation
- Query: certified drone navigation
- Final Score: 0.6693
- URL: https://doi.org/10.1146/annurev-control-042920-020211
- Abstract: The last half decade has seen a steep rise in the number of contributions on safe learning methods for real-world robotic deployments from both the control and reinforcement learning communities. This article provides a concise but holistic review of the recent advances made in using machine learning to achieve safe decision-making under uncertainties, with a focus on unifying the language and frameworks used in control theory and reinforcement learning research. It includes learning-based control approaches that safely improve performance by learning the uncertain dynamics, reinforcement lear...

### Champion-level drone racing using deep reinforcement learning

- Year: 2023
- Citations: 572
- Source: openalex
- Venue: Nature
- Subdomain: global
- Query: autonomous drone localization
- Final Score: 0.7072
- URL: https://doi.org/10.1038/s41586-023-06419-4
- Abstract: Abstract First-person view (FPV) drone racing is a televised sport in which professional competitors pilot high-speed aircraft through a 3D circuit. Each pilot sees the environment from the perspective of their drone by means of video streamed from an onboard camera. Reaching the level of professional pilots with an autonomous drone is challenging because the robot needs to fly at its physical limits while estimating its speed and location in the circuit exclusively from onboard sensors 1 . Here we introduce Swift, an autonomous system that can race physical vehicles at the level of the human ...

### A Real-Time Apple Targets Detection Method for Picking Robot Based on Improved YOLOv5

- Year: 2021
- Citations: 565
- Source: openalex
- Venue: Remote Sensing
- Subdomain: SLAM & Mapping for Autonomous Flight
- Query: drone real-time dense mapping
- Final Score: 0.6798
- URL: https://doi.org/10.3390/rs13091619
- Abstract: The apple target recognition algorithm is one of the core technologies of the apple picking robot. However, most of the existing apple detection algorithms cannot distinguish between the apples that are occluded by tree branches and occluded by other apples. The apples, grasping end-effector and mechanical picking arm of the robot are very likely to be damaged if the algorithm is directly applied to the picking robot. Based on this practical problem, in order to automatically recognize the graspable and ungraspable apples in an apple tree image, a light-weight apple targets detection method wa...

### Swarm of micro flying robots in the wild

- Year: 2022
- Citations: 544
- Source: openalex
- Venue: Science Robotics
- Subdomain: global
- Query: autonomous drone localization
- Final Score: 0.7056
- URL: https://doi.org/10.1126/scirobotics.abm5954
- Abstract: Aerial robots are widely deployed, but highly cluttered environments such as dense forests remain inaccessible to drones and even more so to swarms of drones. In these scenarios, previously unknown surroundings and narrow corridors combined with requirements of swarm coordination can create challenges. To enable swarm navigation in the wild, we develop miniature but fully autonomous drones with a trajectory planner that can function in a timely and accurate manner based on limited information from onboard sensors. The planning problem satisfies various task requirements including flight effici...

### Collaborative Multi-Robot Search and Rescue: Planning, Coordination, Perception, and Active Vision

- Year: 2020
- Citations: 491
- Source: openalex
- Venue: IEEE Access
- Subdomain: SLAM & Mapping for Autonomous Flight
- Query: multi-drone collaborative SLAM
- Final Score: 0.6754
- URL: https://doi.org/10.1109/access.2020.3030190
- Abstract: Search and rescue (SAR) operations can take significant advantage from supporting autonomous or teleoperated robots and multi-robot systems. These can aid in mapping and situational assessment, monitoring and surveillance, establishing communication networks, or searching for victims. This paper provides a review of multi-robot systems supporting SAR operations, with system-level considerations and focusing on the algorithmic perspectives for multi-robot coordination and perception. This is, to the best of our knowledge, the first survey paper to cover (i) heterogeneous SAR robots in different...


## 4. 前沿论文

### UAV swarms: research, challenges, and future directions

- Year: 2025
- Citations: 131
- Source: openalex
- Venue: Journal of Engineering and Applied Science
- Subdomain: SLAM & Mapping for Autonomous Flight
- Query: UAV SLAM lightweight
- Final Score: 0.6875
- URL: https://doi.org/10.1186/s44147-025-00582-3
- Abstract: Abstract Unmanned Aerial Vehicle (UAV) swarms represent a transformative advancement in aerial robotics, leveraging collaborative autonomy to enhance operational capabilities. This paper provides a comprehensive exploration of UAV swarm infrastructure, recent research advancements, and diverse applications. Key areas such as coordinated path planning, task assignment, formation control, and security considerations are examined, highlighting how Artificial Intelligence (AI) and Machine Learning (ML) are integrated to improve decision-making and adaptability. Applications span civilian sectors, ...

### Obstacle Avoidance and Path Planning Methods for Autonomous Navigation of Mobile Robot

- Year: 2024
- Citations: 113
- Source: openalex
- Venue: Sensors
- Subdomain: Real-time Reactive Path Planning & Obstacle Avoidance
- Query: real-time drone obstacle avoidance
- Final Score: 0.6828
- URL: https://doi.org/10.3390/s24113573
- Abstract: Path planning creates the shortest path from the source to the destination based on sensory information obtained from the environment. Within path planning, obstacle avoidance is a crucial task in robotics, as the autonomous operation of robots needs to reach their destination without collisions. Obstacle avoidance algorithms play a key role in robotics and autonomous vehicles. These algorithms enable robots to navigate their environment efficiently, minimizing the risk of collisions and safely avoiding obstacles. This article provides an overview of key obstacle avoidance algorithms, includin...

### LiDAR odometry survey: recent advancements and remaining challenges

- Year: 2024
- Citations: 110
- Source: openalex
- Venue: Intelligent Service Robotics
- Subdomain: Multi-sensor Localization & Sensor Fusion
- Query: drone visual-inertial odometry
- Final Score: 0.682
- URL: https://doi.org/10.1007/s11370-024-00515-8
- Abstract: Abstract Odometry is crucial for robot navigation, particularly in situations where global positioning methods like global positioning system are unavailable. The main goal of odometry is to predict the robot’s motion and accurately determine its current location. Various sensors, such as wheel encoder, inertial measurement unit (IMU), camera, radar, and Light Detection and Ranging (LiDAR), are used for odometry in robotics. LiDAR, in particular, has gained attention for its ability to provide rich three-dimensional (3D) data and immunity to light variations. This survey aims to examine advanc...

### Comprehensive Review of Drones Collision Avoidance Schemes: Challenges and Open Issues

- Year: 2024
- Citations: 108
- Source: openalex
- Venue: IEEE Transactions on Intelligent Transportation Systems
- Subdomain: global
- Query: obstacle avoidance drone
- Final Score: 0.6814
- URL: https://doi.org/10.1109/tits.2024.3375893
- Abstract: In the contemporary landscape, the escalating deployment of drones across diverse industries has ushered in a consequential concern, including ensuring the security of drone operations. This concern extends to a spectrum of challenges, encompassing collisions with stationary and mobile obstacles and encounters with other drones. Moreover, the inherent limitations of drones, namely constraints on energy consumption, data storage capacity, and processing power, present formidable obstacles in developing collision avoidance algorithms. This review paper explores the challenges of ensuring safe dr...

### A survey on socially aware robot navigation: Taxonomy and future challenges

- Year: 2024
- Citations: 81
- Source: openalex
- Venue: The International Journal of Robotics Research
- Subdomain: Visual Navigation & Appearance-Invariant Perception
- Query: semantic visual navigation drone
- Final Score: 0.6723
- URL: https://doi.org/10.1177/02783649241230562
- Abstract: Socially aware robot navigation is gaining popularity with the increase in delivery and assistive robots. The research is further fueled by a need for socially aware navigation skills in autonomous vehicles to move safely and appropriately in spaces shared with humans. Although most of these are ground robots, drones are also entering the field. In this paper, we present a literature survey of the works on socially aware robot navigation in the past 10 years. We propose four different faceted taxonomies to navigate the literature and examine the field from four different perspectives. Through ...

### Autonomous UAV Navigation with Adaptive Control Based on Deep Reinforcement Learning

- Year: 2024
- Citations: 70
- Source: openalex
- Venue: Electronics
- Subdomain: global
- Query: UAV navigation
- Final Score: 0.6677
- URL: https://doi.org/10.3390/electronics13132432
- Abstract: Unmanned aerial vehicle (UAV) navigation plays a crucial role in its ability to perform autonomous missions in complex environments. Most of the existing reinforcement learning methods to solve the UAV navigation problem fix the flight altitude and velocity, which largely reduces the difficulty of the algorithm. But the methods without adaptive control are not suitable in low-altitude environments with complex situations, generally suffering from weak obstacle avoidance. Some UAV navigation studies with adaptive flight only have weak obstacle avoidance capabilities. To address the problem of U...

### UAV-YOLOv8: A Small-Object-Detection Model Based on Improved YOLOv8 for UAV Aerial Photography Scenarios

- Year: 2023
- Citations: 854
- Source: openalex
- Venue: Sensors
- Subdomain: Multi-sensor Localization & Sensor Fusion
- Query: UAV sensor fusion localization
- Final Score: 0.72
- URL: https://doi.org/10.3390/s23167190
- Abstract: Unmanned aerial vehicle (UAV) object detection plays a crucial role in civil, commercial, and military domains. However, the high proportion of small objects in UAV images and the limited platform resources lead to the low accuracy of most of the existing detection models embedded in UAVs, and it is difficult to strike a good balance between detection performance and resource consumption. To alleviate the above problems, we optimize YOLOv8 and propose an object detection model based on UAV aerial photography scenarios, called UAV-YOLOv8. Firstly, Wise-IoU (WIoU) v3 is used as a bounding box re...

### Champion-level drone racing using deep reinforcement learning

- Year: 2023
- Citations: 572
- Source: openalex
- Venue: Nature
- Subdomain: global
- Query: autonomous drone localization
- Final Score: 0.7072
- URL: https://doi.org/10.1038/s41586-023-06419-4
- Abstract: Abstract First-person view (FPV) drone racing is a televised sport in which professional competitors pilot high-speed aircraft through a 3D circuit. Each pilot sees the environment from the perspective of their drone by means of video streamed from an onboard camera. Reaching the level of professional pilots with an autonomous drone is challenging because the robot needs to fly at its physical limits while estimating its speed and location in the circuit exclusively from onboard sensors 1 . Here we introduce Swift, an autonomous system that can race physical vehicles at the level of the human ...


## 5. 新手学习路径

### 阶段 1: 基础认知与系统概览

- 目标：建立无人机导航的完整知识框架，理解各核心模块的功能、边界与协同关系
- 概念：无人机导航系统组成, 定位、感知、规划、控制四层架构, GNSS/INS/Vision/LiDAR等传感器原理与适用场景, 自主飞行的基本定义与分级（如SAE J3016类比）
- 阅读建议：Autonomous Navigation, Path Planning, and Obstacle Avoidance

### 阶段 2: 定位与状态估计基础

- 目标：掌握无人机在不同环境下的位姿估计方法，理解多源信息融合的必要性与基本范式
- 概念：无人机定位, 惯性导航, GPS辅助导航, 视觉导航, SLAM基本原理（前端特征匹配、后端优化、地图表示）, IMU预积分, 滤波与优化基础（EKF、因子图）
- 阅读建议：Multi-Sensor Fusion and Robust State Estimation for UAVs and Swarms

### 阶段 3: 环境感知与语义理解

- 目标：从几何感知进阶到语义感知，理解视觉与多模态数据如何支撑高层导航决策
- 概念：视觉导航, SLAM, 语义SLAM, 小目标检测挑战, 无人机视角图像特性（尺度、畸变、运动模糊）, 轻量化模型设计动机
- 阅读建议：Vision-Based Perception and Object Detection for UAV Applications

### 阶段 4: 路径规划与避障决策

- 目标：掌握从全局路径生成到局部实时避障的典型算法体系，理解其在动态、受限空间中的适应性限制
- 概念：路径规划, 避障算法, 几何规划（A*, RRT, Dijkstra）, 基于优化的轨迹生成（MPC、Polynomial Trajectory）, 反应式避障（VFH, APF, Learning-based）, 安全约束建模（动力学可行性、视野遮挡）
- 阅读建议：Autonomous Navigation, Path Planning, and Obstacle Avoidance

### 阶段 5: 系统集成与鲁棒自主飞行

- 目标：理解真实场景中各模块耦合带来的挑战，学习提升端到端导航鲁棒性与适应性的系统级思路
- 概念：自主飞行, GPS-denied导航, 多传感器紧耦合, 漂移抑制与重定位, 计算资源约束（边缘部署）, 长时运行一致性, 仿真-实机迁移（Gazebo, AirSim, ROS2）
- 阅读建议：SLAM, Mapping, and Semantic Scene Understanding for Autonomous Flight

### 阶段 6: 前沿拓展：协同与智能演进

- 目标：了解单机能力向群体智能与通信感知一体化演进的趋势，建立跨领域技术整合视角
- 概念：Swarm Intelligence and Collaborative Autonomy for Aerial Robotics, Integrated Sensing, Communication, and Networked UAV Systems, 分布式状态估计, 空地协同导航, ISAC（感知-通信一体化）, 边缘AI与网络化决策
- 阅读建议：Integrated Sensing, Communication, and Networked UAV Systems


## 6. 推荐 Github 检索词

- 无人机定位
- 路径规划
- 避障算法
- 视觉导航
- 惯性导航
- GPS辅助导航
- SLAM
- 自主飞行
- Integrated Sensing, Communication, and Networked UAV Systems
- Multi-Sensor Fusion and Robust State Estimation for UAVs and Swarms
- Vision-Based Perception and Object Detection for UAV Applications
- Autonomous Navigation, Path Planning, and Obstacle Avoidance
- SLAM, Mapping, and Semantic Scene Understanding for Autonomous Flight
- Swarm Intelligence and Collaborative Autonomy for Aerial Robotics

## 7. Top Papers with Source Trace

| Rank | Title | Year | Source | Subdomain | Score |
|---:|---|---:|---|---|---:|
| 1 | Integrated Sensing and Communications: Toward Dual-Functional Wireless Networks for 6G and Beyond | 2022 | openalex | SLAM & Mapping for Autonomous Flight | 0.725 |
| 2 | GVINS: Tightly Coupled GNSS–Visual–Inertial Fusion for Smooth and Consistent State Estimation | 2022 | openalex | Multi-sensor Localization & Sensor Fusion | 0.7216 |
| 3 | UAV-YOLOv8: A Small-Object-Detection Model Based on Improved YOLOv8 for UAV Aerial Photography Scenarios | 2023 | openalex | Multi-sensor Localization & Sensor Fusion | 0.72 |
| 4 | Champion-level drone racing using deep reinforcement learning | 2023 | openalex | global | 0.7072 |
| 5 | Swarm of micro flying robots in the wild | 2022 | openalex | global | 0.7056 |
| 6 | What Will the Future of UAV Cellular Communications Be? A Flight From 5G to 6G | 2022 | openalex | Visual Navigation & Appearance-Invariant Perception | 0.7017 |
| 7 | A Survey on the Convergence of Edge Computing and AI for UAVs: Opportunities and Challenges | 2022 | openalex | Multi-sensor Localization & Sensor Fusion | 0.6982 |
| 8 | ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM | 2021 | openalex | global | 0.698 |
| 9 | A Modified YOLOv8 Detection Network for UAV Aerial Image Recognition | 2023 | openalex | Visual Navigation & Appearance-Invariant Perception | 0.6958 |
| 10 | Comparing YOLOv3, YOLOv4 and YOLOv5 for Autonomous Landing Spot Detection in Faulty UAVs | 2022 | openalex | Certifiable Autonomy & Safety-Critical Navigation | 0.6936 |
| 11 | Omni-Swarm: A Decentralized Omnidirectional Visual–Inertial–UWB State Estimation System for Aerial Swarms | 2022 | openalex | Multi-sensor Localization & Sensor Fusion | 0.6924 |
| 12 | UAV swarms: research, challenges, and future directions | 2025 | openalex | SLAM & Mapping for Autonomous Flight | 0.6875 |
| 13 | Obstacle Avoidance and Path Planning Methods for Autonomous Navigation of Mobile Robot | 2024 | openalex | Real-time Reactive Path Planning & Obstacle Avoidance | 0.6828 |
| 14 | LiDAR odometry survey: recent advancements and remaining challenges | 2024 | openalex | Multi-sensor Localization & Sensor Fusion | 0.682 |
| 15 | Comprehensive Review of Drones Collision Avoidance Schemes: Challenges and Open Issues | 2024 | openalex | global | 0.6814 |
| 16 | A Real-Time Apple Targets Detection Method for Picking Robot Based on Improved YOLOv5 | 2021 | openalex | SLAM & Mapping for Autonomous Flight | 0.6798 |
| 17 | UAV Computing-Assisted Search and Rescue Mission Framework for Disaster and Harsh Environment Mitigation | 2022 | openalex | Visual Navigation & Appearance-Invariant Perception | 0.679 |
| 18 | A Comprehensive Survey of the Recent Studies with UAV for Precision Agriculture in Open Fields and Greenhouses | 2022 | openalex | Visual Navigation & Appearance-Invariant Perception | 0.677 |
| 19 | Drones in Plant Disease Assessment, Efficient Monitoring, and Detection: A Way Forward to Smart Agriculture | 2023 | openalex | SLAM & Mapping for Autonomous Flight | 0.6769 |
| 20 | Collaborative Multi-Robot Search and Rescue: Planning, Coordination, Perception, and Active Vision | 2020 | openalex | SLAM & Mapping for Autonomous Flight | 0.6754 |
