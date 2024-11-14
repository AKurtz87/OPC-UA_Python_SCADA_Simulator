# OPC-UA_Python_SCADA_Simulator

### **Introduction**

The proposed project aims to develop an advanced industrial simulator based on the **OPC-UA** (Open Platform Communications Unified Architecture) protocol, leveraging dedicated Python libraries and technologies for process visualization and automation. The project seeks to combine simulation, data analysis, and real-time management within a virtual industrial ecosystem. This innovative approach offers extensive potential for research, training, and technological development within the Industry 4.0 paradigm.

---

<img width="1403" alt="Screenshot 2024-11-14 at 08 39 31" src="https://github.com/user-attachments/assets/dd380cce-aa17-4e80-aba7-fe69acebaf4e">


---

### **Project Objectives**

1. **Simulation of a Complete Industrial System**  
   Development of an OPC-UA server to simulate an industrial plant and manage communication interfaces with system components.

2. **Implementation of a SCADA (Supervisory Control and Data Acquisition) Dashboard**  
   Creation of a web interface for process supervision and automation, integrated with the OPC-UA server via Flask.

3. **Development of Debugging and Testing Tools**  
   Design of tools for analysis and control, including OPC-UA server scanners, node enumeration, and data traffic monitoring.

4. **Advanced Data Analysis**  
   Development of a unique semantics for OPC-UA nodes, enabling predictive and contextual analysis of system variables to enhance operational awareness.

---

### **Methodology**

1. **Configuration and Simulation**
   - Utilize the Python library [python-opcua](https://pypi.org/project/opcua/) to implement the OPC-UA server.
   - Declare nodes with a parent-child structure (e.g., ReactorA.Temperature, ReactorA.Level) to reflect the system’s semantic architecture.

2. **SCADA Dashboard**
   - Create a SCADA dashboard based on Flask for process management and supervision.
   - Integrate the dashboard with the OPC-UA server for real-time data exchange.

3. **Testing and Debugging Tools**
   - Develop a scanner to identify OPC-UA servers on the local network.
   - Implement node enumeration for detailed analysis of the server’s structure.
   - Create tools to analyze OPC-UA traffic, providing structured output for further analysis using LLMs.

4. **Data Analysis and Visualization**
   - Use advanced semantics to identify nodes and link them to the operational context.
   - Prepare data for real-time visualization and predictive analysis.

---

### **Innovation and Research Potential**

- **Academic Context**: The platform can be used for interdisciplinary research projects involving automation, data science, and industrial protocol development.
- **Industrial Sector**: Provides a safe environment to test new automation models and communication protocols without impacting real production systems.
- **Training**: A teaching tool for training students and professionals on SCADA and OPC-UA technologies.
- **Predictive and Optimization Capabilities**: The system not only represents the current state but also enables predictive and contextualized insights, supporting more informed operational decisions.

---

### **Features**

#### Backend (Python)
- **OPC UA Server**: Implements the OPC UA protocol to handle real-time data exchange between the simulation and the HMI.
- **Process Simulation**: Models chemical plant equipment like reactors with parameters such as:
  - Temperature
  - Pressure
  - Level
  - Valve states (e.g., input/output valves)
  - Agitator status and speed
  - Heating system status.
- **Control Mechanisms**: Enables control over actuators such as valves, agitators, and heating systems.

#### Frontend (HTML HMI Dashboard)
- **Real-Time Monitoring**:
  - Displays process parameters such as temperature, pressure, and levels in reactors.
  - Highlights operational states (e.g., agitator active, heating on) with visual cues.
- **Interactive Controls**:
  - Start/stop actuators (e.g., agitator, heating).
  - Open/close valves.
  - Adjust agitator speed using input fields.
- **Responsive Design**:
  - Built for various screen sizes.
  - Auto-refreshes every 5 seconds to keep data up-to-date.

---

### **Expected Results**

- Development of a fully operational industrial simulator based on the OPC-UA protocol.
- Creation of innovative tools for analyzing and managing industrial systems.
- Enhanced understanding and adoption of the OPC-UA protocol in academic and industrial domains.
- Production of structured and contextualized data for advanced analysis and decision-making support.

---

### **How to Run**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the OPC UA Server**:
   ```bash
   python serverB.py
   ```

4. **Start the HMI Dashboard**:
   ```bash
   python hmi_server_autoB.py
   ```

5. **Access the HMI**:
   - Open a web browser and navigate to `http://localhost:5000`.

---

### **File Structure**

1. **`serverB.py`**: Implements the OPC UA server for the SCADA simulation.
   - Handles data modeling and real-time updates.
   - Simulates process dynamics of the chemical plant.

2. **`hmi_server_autoB.py`**: Python script for hosting the HMI dashboard.
   - Provides endpoints for the HTML interface to interact with the OPC UA server.
   - Manages user interactions like control updates.

3. **`dashboard.html`**: The HMI interface.
   - A dynamic, interactive HTML page styled with CSS for visualizing and controlling the SCADA system.

---

### **Conclusion**

This project represents a bridge between academic research and industrial application, laying the foundation for broader adoption of OPC-UA technologies in the Industry 4.0 context. Project funding and contributions would enable the development of a versatile and innovative platform, with positive impacts on both scientific and technological fronts.

---
⚠️⚠️⚠️
Warning: Currently, it is not possible to send manual commands through the dashboard due to conflicts between automatic and manual operation. This issue is being actively addressed and will be resolved soon to ensure seamless functionality.

Feel free to contribute or provide feedback by submitting an issue or pull request!
