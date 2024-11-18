# **OPC-UA_Python_SCADA_Simulator**

### **Introduction**

This project presents an advanced industrial simulator built on the **OPC-UA** (Open Platform Communications Unified Architecture) protocol. Leveraging Python libraries and modern web technologies, the simulator combines real-time data exchange, process automation, and visualization. This tool serves as an innovative platform for research, training, and development within the **Industry 4.0** paradigm.

---

### **Key Features**

1. **OPC-UA Server-Based Simulation**  
   A comprehensive server simulates an industrial plant with chemical reactors, allowing real-time data exchange and process control.

2. **Interactive SCADA Dashboard**  
   A web-based HMI (Human-Machine Interface) for monitoring and controlling process parameters and actuators.

3. **API-Based Real-Time Updates**  
   The dashboard dynamically retrieves updated process data via API calls, eliminating the need for page reloads.

4. **Automatic and Manual Operation Modes**  
   Users can switch between automatic and manual operation modes for reactors. Manual interventions are allowed even in automatic mode.

5. **Extensive Control Options**  
   Real-time control of actuators (valves, agitators, heaters) and parameters (e.g., agitator speed) directly through the dashboard.

6. **Responsive Design**  
   Optimized for devices of all sizes, the dashboard ensures accessibility on desktops, tablets, and mobile devices.

---

### **Project Objectives**

1. Simulate an industrial plant using an OPC-UA server to handle real-time data exchange and process control.
2. Build a SCADA dashboard for process supervision, automation, and manual intervention.
3. Integrate API-based updates for seamless real-time visualization of process data.
4. Enable dynamic toggling between automatic and manual operation modes.
5. Provide tools for debugging, data analysis, and traffic monitoring.

---

### **Technologies Used**

- **Backend**:
  - `python-opcua`: Implements the OPC-UA server for simulation and real-time communication.
  - `Flask`: Hosts the SCADA dashboard and API endpoints.
- **Frontend**:
  - HTML/CSS/JavaScript: Builds the dynamic and interactive dashboard.
  - Fetch API: Periodically updates dashboard data without reloading.
- **Additional Tools**:
  - Tools for OPC-UA node scanning, enumeration, and traffic monitoring.

---

### **Implementation Details**

1. **OPC-UA Server (`serverB.py`)**
   - Simulates the behavior of chemical plant reactors.
   - Models process parameters and actuator states:
     - Temperature, pressure, level.
     - Actuator states: valves, agitators, heaters.
   - Exposes real-time data via OPC-UA nodes.

2. **SCADA Dashboard (`dashboard.html`, `hmi_server_autoB_api.py`)**
   - Interactive HMI for monitoring and controlling the plant.
   - Displays real-time process variables (e.g., temperature, pressure).
   - Provides control options for actuators and toggling between operating modes.
   - Uses an API (`/api/reattori`) for real-time updates.

3. **Operation Modes**
   - **Automatic Mode**: Reactors operate autonomously based on predefined cycles.
   - **Manual Mode**: Operators can override automatic controls and directly intervene in process parameters and actuators.

---

### **Screenshots**

<img width="1403" alt="Screenshot 2024-11-14 at 08 39 31" src="https://github.com/user-attachments/assets/dd380cce-aa17-4e80-aba7-fe69acebaf4e">

---

### **Setup and Running Instructions**

#### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

#### **2. Install Dependencies**
Install Python dependencies using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```

#### **3. Start the OPC-UA Server**
Run the OPC-UA server simulation:
```bash
python serverB.py
```

#### **4. Start the SCADA Dashboard**
Launch the Flask-based SCADA dashboard:
```bash
python hmi_server_autoB_api.py
```

#### **5. Access the Dashboard**
Open a web browser and navigate to:
```
http://localhost:5000
```

---

### **How It Works**

1. **Real-Time Monitoring**  
   The dashboard fetches updated process data every 2 seconds from the `/api/reattori` endpoint, displaying key parameters and actuator states.

2. **Automatic and Manual Modes**  
   - Automatic mode executes pre-defined cycles.
   - Manual mode allows operators to intervene and override controls.

3. **Actuator Control**  
   - Start/stop actuators such as valves, agitators, and heaters.
   - Adjust parameters like agitator speed (10–300 RPM).
   - Toggle actuator states and operating modes via intuitive controls.

4. **Dynamic Styling**  
   The dashboard visually highlights operational states (e.g., active agitators or heating systems) using dynamic CSS.

---

### **File Structure**

#### **Backend**
- **`serverB.py`**: Implements the OPC-UA server. Handles simulation of reactors and real-time updates.
- **`hmi_server_autoB_api.py`**: Hosts the Flask server for the SCADA dashboard and provides API endpoints.

#### **Frontend**
- **`dashboard.html`**: The SCADA dashboard interface. Integrates with backend APIs for real-time updates and process control.
  
---

### **Network Traffic Analysis with Wireshark**

This simulator provides an excellent opportunity to analyze OPC-UA protocol traffic in detail. By capturing network packets on the `localhost` interface using tools like **Wireshark**, users can study the OPC-UA communication process. 

To facilitate this analysis, the OPC-UA server in this project is configured with **Security Policy set to None**, allowing all communication to occur in **clear text**. This enables researchers and students to:
- Examine the structure of OPC-UA requests and responses.
- Explore the details of the data exchange, including node attributes and variable values.
- Gain a better understanding of how the OPC-UA protocol operates in real-time applications.

This configuration is particularly useful for educational purposes, as it simplifies the process of decoding messages and analyzing protocol behavior without the additional complexity of encryption. 

To perform the analysis:
1. Start the OPC-UA server and dashboard as described in the setup instructions.
2. Open Wireshark, select the `lo` interface (localhost), and start capturing.
3. Apply filters such as `opcua` or `tcp.port==4840` to focus on OPC-UA traffic.
4. Observe and decode the clear-text messages to explore the protocol's operations in depth.

---

### **Project Objectives**

1. Simulate an industrial plant using an OPC-UA server to handle real-time data exchange and process control.
2. Build a SCADA dashboard for process supervision, automation, and manual intervention.
3. Integrate API-based updates for seamless real-time visualization of process data.
4. Enable dynamic toggling between automatic and manual operation modes.
5. Provide tools for debugging, data analysis, and traffic monitoring.
---

### **Future Enhancements**

1. **Advanced Analytics**  
   Add predictive analytics and machine learning models for anomaly detection and optimization.

2. **Expanded Process Simulation**  
   Simulate additional equipment and process scenarios for greater flexibility.

3. **Data Logging and Visualization**  
   Enable historical data logging and provide advanced visualization tools.

4. **Multi-User Support**  
   Implement user roles and authentication for collaborative monitoring and control.

---

### **Conclusion**

This project bridges the gap between academia and industry, providing a robust tool for understanding OPC-UA technologies and SCADA systems. Its flexibility and extensibility make it ideal for research, training, and development in the Industry 4.0 era.




