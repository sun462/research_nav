# Research Navigator Report

研究主题：无人机导航

## 1. 术语发现

- 无人机定位
- 路径规划
- 自主导航
- 视觉导航
- 惯性导航
- GPS辅助导航
- 避障算法
- SLAM
- 飞行控制
- 导航系统

## 2. 领域结构 / 研究方向聚类

### SLAM-Based Autonomous Navigation in GPS-Denied Environments

Research focused on visual, acoustic, or multi-sensor SLAM systems enabling precise localization and mapping for drones operating indoors, underground, or in other GPS-denied settings; emphasizes real-time performance, resource constraints, and integration with inertial or depth sensors.

相关论文：
- 3D TDOA-AOA Quaternion Based Acoustic SLAM for Drone Localization and Source Mapping
- Fully Onboard SLAM for Distributed Mapping With a Swarm of Nano-Drones
- Implementation of a Monocular ORB SLAM for an Indoor Agricultural Drone
- Visual SLAM for Indoor Livestock and Farming Using a Small Drone with a Monocular Camera: A Feasibility Study
- ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM
- DAGmap: Multi-Drone SLAM via a DAG-Based Distributed Ledger

### AI-Driven End-to-End Navigation and Control

Approaches using deep learning (CNNs, RNNs) and deep reinforcement learning (DRL) to directly map raw sensor inputs (e.g., images) to navigation outputs (e.g., steering, velocity, obstacle avoidance actions), often targeting lightweight deployment, generalization across environments, and operation without explicit mapping or hand-crafted features.

相关论文：
- End-to-End Nano-Drone Obstacle Avoidance for Indoor Exploration
- Drone Navigation Using Region and Edge Exploitation-Based Deep CNN
- An Optimization Framework for Efficient Vision-Based Autonomous Drone Navigation
- Deep convolutional neural network based autonomous drone navigation
- Vision Based Drone Obstacle Avoidance by Deep Reinforcement Learning
- Drone Deep Reinforcement Learning: A Review
- Flying Free: A Research Overview of Deep Learning in Drone Navigation Autonomy

### Swarm and Distributed Drone Navigation

Methods addressing collaborative perception, decentralized mapping, communication-efficient coordination, and task allocation among multiple UAVs—especially nano- or resource-constrained drones—emphasizing scalability, robustness, infrastructure independence, and emergent collective behavior.

相关论文：
- Fully Onboard SLAM for Distributed Mapping With a Swarm of Nano-Drones
- DAGmap: Multi-Drone SLAM via a DAG-Based Distributed Ledger
- A Clustering-Based Coverage Path Planning Method for Autonomous Heterogeneous UAVs

### Path Planning and Optimization Algorithms

Computational techniques—including metaheuristics (e.g., PSO variants), mathematical programming, and clustering-based strategies—for generating safe, efficient, and coverage-optimized flight paths under constraints such as heterogeneity, NP-hard complexity, dynamic obstacles, or mission-specific objectives (e.g., search, inspection, delivery).

相关论文：
- A Novel Hybrid Particle Swarm Optimization Algorithm for Path Planning of UAVs
- A Clustering-Based Coverage Path Planning Method for Autonomous Heterogeneous UAVs
- An Optimization Framework for Efficient Vision-Based Autonomous Drone Navigation

### Multi-Sensor Fusion and Alternative Localization for GPS-Denied Operation

Systems leveraging non-GPS modalities—including radar, acoustic (TDOA/AOA), inertial measurement units (IMUs), and edge-computed vision—to achieve robust state estimation, velocity/height measurement, or navigation resilience in signal-deprived or structurally challenging environments.

相关论文：
- 3D TDOA-AOA Quaternion Based Acoustic SLAM for Drone Localization and Source Mapping
- Radar-Aided Navigation System for Small Drones in GPS-Denied Environments
- Edge Computing in 5G for Drone Navigation: What to Offload?
- A review of UAV autonomous navigation in GPS-denied environments

### Application-Specific Drone Navigation Systems

Domain-tailored navigation frameworks addressing unique operational requirements and constraints in high-stakes or specialized contexts—such as emergency rescue, agriculture, livestock monitoring, and industrial inspection—where environmental complexity, payload limits, safety, and mission semantics drive architectural choices.

相关论文：
- A Review of Electric UAV Visual Detection and Navigation Technologies for Emergency Rescue Missions
- Implementation of a Monocular ORB SLAM for an Indoor Agricultural Drone
- Visual SLAM for Indoor Livestock and Farming Using a Small Drone with a Monocular Camera: A Feasibility Study
- Artificial Intelligence Approaches for UAV Navigation: Recent Advances and Future Challenges


## 3. 必读论文

### ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM

- Year: 2021
- Citations: 3805
- URL: https://doi.org/10.1109/tro.2021.3075644
- Abstract: This article presents ORB-SLAM3, the first system able to perform visual, visual-inertial and multimap SLAM with monocular, stereo and RGB-D cameras, using pin-hole and fisheye lens models. The first main novelty is a tightly integrated visual-inertial SLAM system that fully relies on maximum <italic xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">a posteriori</i> (MAP) estimation, even during IMU initialization, resulting in real-time robust operation in small and large, indoor and outdoor environments, being two to ten times more accurate than previo...

### A Clustering-Based Coverage Path Planning Method for Autonomous Heterogeneous UAVs

- Year: 2021
- Citations: 332
- URL: https://doi.org/10.1109/tits.2021.3066240
- Abstract: Unmanned aerial vehicles (UAVs) have been widely applied in civilian and military applications due to their high autonomy and strong adaptability. Although UAVs can achieve effective cost reduction and flexibility enhancement in the development of large-scale systems, they result in a serious path planning and task allocation problem. Coverage path planning, which tries to seek flight paths to cover all of regions of interest, is one of the key technologies in achieving autonomous driving of UAVs and difficult to obtain optimal solutions because of its NP-Hard computational complexity. In this...

### A Novel Hybrid Particle Swarm Optimization Algorithm for Path Planning of UAVs

- Year: 2022
- Citations: 321
- URL: https://doi.org/10.1109/jiot.2022.3182798
- Abstract: Automatic path planning problem is essential for efficient mission execution by unmanned aerial vehicles (UAVs), which needs to access the optimal path rapidly in the complicated field. To address this problem, a novel hybrid particle swarm optimization (PSO) algorithm, namely, SDPSO, is proposed in this article. The proposed algorithm improves the update strategy of the global optimal solution in the PSO algorithm by merging the simulated annealing algorithm, which enhances the optimization ability and avoids falling into local convergence; each particle integrates the beneficial information ...

### Drone Deep Reinforcement Learning: A Review

- Year: 2021
- Citations: 299
- URL: https://doi.org/10.3390/electronics10090999
- Abstract: Unmanned Aerial Vehicles (UAVs) are increasingly being used in many challenging and diversified applications. These applications belong to the civilian and the military fields. To name a few; infrastructure inspection, traffic patrolling, remote sensing, mapping, surveillance, rescuing humans and animals, environment monitoring, and Intelligence, Surveillance, Target Acquisition, and Reconnaissance (ISTAR) operations. However, the use of UAVs in these applications needs a substantial level of autonomy. In other words, UAVs should have the ability to accomplish planned missions in unexpected si...

### Artificial Intelligence Approaches for UAV Navigation: Recent Advances and Future Challenges

- Year: 2022
- Citations: 161
- URL: https://doi.org/10.1109/access.2022.3157626
- Abstract: Unmanned aerial vehicles (UAVs) applications have increased in popularity in recent years because of their ability to incorporate a wide variety of sensors while retaining cheap operating costs, easy deployment, and excellent mobility. However, controlling UAVs remotely in complex environments limits the capability of the UAVs and decreases the efficiency of the whole system. Therefore, many researchers are working on autonomous UAV navigation where UAVs can move and perform the assigned tasks based on their surroundings. With recent technological advancements, the application of artificial in...

### A review of UAV autonomous navigation in GPS-denied environments

- Year: 2023
- Citations: 129
- URL: https://doi.org/10.1016/j.robot.2023.104533
- Abstract: Unmanned aerial vehicles (UAVs) have drawn increased research interest in recent years, leading to a vast number of applications, such as, terrain exploration, disaster assistance and industrial inspection. Unlike UAV navigation in outdoor environments that rely on GPS (Global Positioning System) for localization, indoor navigation can not rely on GPS due to the poor quality or lack of signal. Although some reviewing papers particularly summarized indoor navigation strategies (e.g., Visual-based Navigation) or their specific sub-components (e.g., localization and path planning) in detail, ther...

### Flying Free: A Research Overview of Deep Learning in Drone Navigation Autonomy

- Year: 2021
- Citations: 87
- URL: https://doi.org/10.3390/drones5020052
- Abstract: With the rise of Deep Learning approaches in computer vision applications, significant strides have been made towards vehicular autonomy. Research activity in autonomous drone navigation has increased rapidly in the past five years, and drones are moving fast towards the ultimate goal of near-complete autonomy. However, while much work in the area focuses on specific tasks in drone navigation, the contribution to the overall goal of autonomy is often not assessed, and a comprehensive overview is needed. In this work, a taxonomy of drone navigation autonomy is established by mapping the definit...

### Visual SLAM for Indoor Livestock and Farming Using a Small Drone with a Monocular Camera: A Feasibility Study

- Year: 2021
- Citations: 78
- URL: https://doi.org/10.3390/drones5020041
- Abstract: Real-time data collection and decision making with drones will play an important role in precision livestock and farming. Drones are already being used in precision agriculture. Nevertheless, this is not the case for indoor livestock and farming environments due to several challenges and constraints. These indoor environments are limited in physical space and there is the localization problem, due to GPS unavailability. Therefore, this work aims to give a step toward the usage of drones for indoor farming and livestock management. To investigate on the drone positioning in these workspaces, tw...


## 4. 前沿论文

### 3D TDOA-AOA Quaternion Based Acoustic SLAM for Drone Localization and Source Mapping

- Year: 2025
- Citations: 3
- URL: https://doi.org/10.1109/icassp49660.2025.10888106
- Abstract: This paper focuses on improving 3D sound mapping using acoustic simultaneous localization and mapping (SLAM), angle of arrival (AOA), and time difference of arrival (TDOA). We use quaternion for orientation tracking. Through simulations involving a drone equipped with microphone arrays and an inertial measurement unit (IMU), the paper shows the effective localization of a drone moving in a room and mapping multiple stationary sources in a dynamic environment....

### A Review of Electric UAV Visual Detection and Navigation Technologies for Emergency Rescue Missions

- Year: 2024
- Citations: 48
- URL: https://doi.org/10.3390/su16052105
- Abstract: Sudden disasters often result in significant losses of human lives and property, and emergency rescue is a necessary response to disasters. In recent years, with the development of electric unmanned aerial vehicles (UAVs) and artificial intelligence technology, the combination of these technologies has been gradually applied to emergency rescue missions. However, in the face of the complex working conditions of emergency rescue missions, the application of electric UAV visual detection still faces great challenges, particularly in relation to a lack of GPS positioning signal in closed emergenc...

### Fully Onboard SLAM for Distributed Mapping With a Swarm of Nano-Drones

- Year: 2024
- Citations: 23
- URL: https://doi.org/10.1109/jiot.2024.3367451
- Abstract: The use of Unmanned Aerial Vehicles (UAVs) is rapidly increasing in applications ranging from surveillance and first-aid missions to industrial automation involving cooperation with other machines or humans. To maximize area coverage and reduce mission latency, swarms of collaborating drones have become a significant research direction. However, this approach requires open challenges in positioning, mapping, and communications to be addressed. This work describes a distributed mapping system based on a swarm of nano-UAVs, characterized by a limited payload of 35 g and tightly constrained onboa...

### End-to-End Nano-Drone Obstacle Avoidance for Indoor Exploration

- Year: 2024
- Citations: 16
- URL: https://doi.org/10.3390/drones8020033
- Abstract: Autonomous navigation of drones using computer vision has achieved promising performance. Nano-sized drones based on edge computing platforms are lightweight, flexible, and cheap; thus, they are suitable for exploring narrow spaces. However, due to their extremely limited computing power and storage, vision algorithms designed for high-performance GPU platforms cannot be used for nano-drones. To address this issue, this paper presents a lightweight CNN depth estimation network deployed on nano-drones for obstacle avoidance. Inspired by knowledge distillation (KD), a Channel-Aware Distillation ...

### A review of UAV autonomous navigation in GPS-denied environments

- Year: 2023
- Citations: 129
- URL: https://doi.org/10.1016/j.robot.2023.104533
- Abstract: Unmanned aerial vehicles (UAVs) have drawn increased research interest in recent years, leading to a vast number of applications, such as, terrain exploration, disaster assistance and industrial inspection. Unlike UAV navigation in outdoor environments that rely on GPS (Global Positioning System) for localization, indoor navigation can not rely on GPS due to the poor quality or lack of signal. Although some reviewing papers particularly summarized indoor navigation strategies (e.g., Visual-based Navigation) or their specific sub-components (e.g., localization and path planning) in detail, ther...

### Implementation of a Monocular ORB SLAM for an Indoor Agricultural Drone

- Year: 2023
- Citations: 14
- URL: https://doi.org/10.1109/ica-symp56348.2023.10044953
- Abstract: Drones are increasingly being used in almost every major industry, including agriculture. Intelligent drone systems could enable precise agricultural. One of the critical uses of agricultural drone is to use in an automatic plant monitoring and inspecting. A drone must be tiny enough to fly between plants in order to capture images of plant trees or fruits in an indoor environment. Therefore, drone's payload is crucial because it limited onboard sensors weight. SLAM is necessary for autonomous navigation because it could provide all necessary information of drone navigation system without coll...

### A Novel Hybrid Particle Swarm Optimization Algorithm for Path Planning of UAVs

- Year: 2022
- Citations: 321
- URL: https://doi.org/10.1109/jiot.2022.3182798
- Abstract: Automatic path planning problem is essential for efficient mission execution by unmanned aerial vehicles (UAVs), which needs to access the optimal path rapidly in the complicated field. To address this problem, a novel hybrid particle swarm optimization (PSO) algorithm, namely, SDPSO, is proposed in this article. The proposed algorithm improves the update strategy of the global optimal solution in the PSO algorithm by merging the simulated annealing algorithm, which enhances the optimization ability and avoids falling into local convergence; each particle integrates the beneficial information ...

### Artificial Intelligence Approaches for UAV Navigation: Recent Advances and Future Challenges

- Year: 2022
- Citations: 161
- URL: https://doi.org/10.1109/access.2022.3157626
- Abstract: Unmanned aerial vehicles (UAVs) applications have increased in popularity in recent years because of their ability to incorporate a wide variety of sensors while retaining cheap operating costs, easy deployment, and excellent mobility. However, controlling UAVs remotely in complex environments limits the capability of the UAVs and decreases the efficiency of the whole system. Therefore, many researchers are working on autonomous UAV navigation where UAVs can move and perform the assigned tasks based on their surroundings. With recent technological advancements, the application of artificial in...


## 5. 新手学习路径

### 阶段 1: 基础认知与系统框架

- 目标：建立无人机导航的整体认知，理解核心模块及其协同关系，掌握基本术语和典型系统架构。
- 概念：无人机定位, 飞行控制, 自主导航, 导航系统, GPS辅助导航, 惯性导航
- 阅读建议：从综述类文献入手，如《A review of UAV autonomous navigation in GPS-denied environments》和《Artificial Intelligence Approaches for UAV Navigation: Recent Advances and Future Challenges》，结合入门教材（如《Small Unmanned Aircraft: Theory and Practice》第1–4章）构建系统观。

### 阶段 2: 传感器原理与状态估计

- 目标：掌握无人机常用传感器的工作原理、误差特性及融合方法，能理解并实现基础定位与姿态估计。
- 概念：惯性导航, GPS辅助导航, 视觉导航, SLAM, 多传感器融合
- 阅读建议：精读《ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual–Inertial, and Multimap SLAM》引言与架构设计；学习卡尔曼滤波/ESKF基础，配合实践（如ROS+PX4的VIO示例）；参考《Radar-Aided Navigation System for Small Drones in GPS-Denied Environments》对比非GNSS模态。

### 阶段 3: 环境感知与实时避障

- 目标：理解无人机如何感知动态/结构化环境，实现鲁棒避障与局部路径调整，区分反应式与规划式策略。
- 概念：避障算法, 视觉导航, SLAM, 无人机定位
- 阅读建议：聚焦《End-to-End Nano-Drone Obstacle Avoidance for Indoor Exploration》和《Vision Based Drone Obstacle Avoidance by Deep Reinforcement Learning》，对比传统几何法（如APF、DWA）与学习型方法；动手复现简单Gazebo+PX4避障仿真。

### 阶段 4: 全局路径规划与任务优化

- 目标：掌握面向实际任务（覆盖、搜索、巡检）的路径生成方法，理解算法复杂度、约束建模与实时性权衡。
- 概念：路径规划, 避障算法, 无人机定位, 应用-specific drone navigation systems
- 阅读建议：研读《A Clustering-Based Coverage Path Planning Method for Autonomous Heterogeneous UAVs》和《A Novel Hybrid Particle Swarm Optimization Algorithm for Path Planning of UAVs》，结合Python实现RRT*/PSO等经典算法，并在2D/3D仿真中验证其在障碍物与能耗约束下的表现。

### 阶段 5: 前沿方向深化：SLAM与AI驱动导航

- 目标：深入SLAM在资源受限平台的轻量化实现，以及端到端学习导航的范式演进、泛化性与部署挑战。
- 概念：SLAM, 视觉导航, AI-Driven End-to-End Navigation and Control, SLAM-Based Autonomous Navigation in GPS-Denied Environments
- 阅读建议：精读《Fully Onboard SLAM for Distributed Mapping With a Swarm of Nano-Drones》与《Flying Free: A Research Overview of Deep Learning in Drone Navigation Autonomy》，分析计算/内存瓶颈；尝试在Nano-Drone仿真平台（如CrazyS）部署轻量ORB-SLAM2或训练简化CNN避障模型。

### 阶段 6: 领域落地与系统集成

- 目标：将技术链整合至特定应用场景（如农业、应急），理解需求驱动的设计取舍、安全验证与真实环境鲁棒性工程。
- 概念：应用-Specific Drone Navigation Systems, Swarm and Distributed Drone Navigation, Multi-Sensor Fusion and Alternative Localization for GPS-Denied Operation
- 阅读建议：以《Implementation of a Monocular ORB SLAM for an Indoor Agricultural Drone》和《A Review of Electric UAV Visual Detection and Navigation Technologies for Emergency Rescue Missions》为案例，开展场景建模→传感器选型→算法适配→仿真验证全流程项目实践，并对比不同研究方向聚类中的解决方案差异。


## 6. 推荐 Github 检索词

- 无人机定位
- 路径规划
- 自主导航
- 视觉导航
- 惯性导航
- GPS辅助导航
- 避障算法
- SLAM
- 飞行控制
- 导航系统
- SLAM-Based Autonomous Navigation in GPS-Denied Environments
- AI-Driven End-to-End Navigation and Control
- Swarm and Distributed Drone Navigation
- Path Planning and Optimization Algorithms
- Multi-Sensor Fusion and Alternative Localization for GPS-Denied Operation
