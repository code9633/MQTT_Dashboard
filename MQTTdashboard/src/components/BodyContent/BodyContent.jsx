// eslint-disable-next-line no-unused-vars
import React, { useState, useEffect } from "react";
import "./BodyContent.css";
import { TbCircuitVoltmeter } from "react-icons/tb";
import mqtt from "mqtt";

// eslint-disable-next-line no-unused-vars
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  Rectangle,
} from "recharts";

export default function BodyContent() {
  const [historicalChartData, setHistoricalChartData] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState(
    "Waiting for connection..."
  );

  const [forcastVoltage, setForcastVoltage] = useState('0.0')
  const [currentVoltage, setCurrentVoltage] = useState ('0.0')

  const [message, setMessage] = useState("");

  useEffect(() => {
    const client = mqtt.connect("ws://broker.emqx.io:8083/mqtt");

    client.on("connect", (err) => {
      console.log("Connected to MQTT broker");
      setConnectionStatus("Connected");
      client.subscribe("test/topic", { qos: 0 });
    });

    client.on("message", (topic, payload) => {
      console.log("Received message:", JSON.parse(payload.toString()));
      var data = JSON.parse(payload.toString())
      setMessage(data);
      setForcastVoltage(data.ForcastVoltage);
      setCurrentVoltage(data.CurrentVoltage)
      
    });

    client.on("error", (error) => {
      console.log("Connection Failed", error);
      setConnectionStatus("Connection Failed");
    });

    return () => {
      client.end();
    };
  }, []);

  return (
    <div className="bodyContainer">
      <div className="connectionStatus">
        <p>Connection Status: </p>
        <p id="status">{connectionStatus}</p>
      </div>
      <div className="mainCards">
        <div className="cardInner cardOne">
          <div className="cardData">
            <TbCircuitVoltmeter className="bicon" />
            <h3>Current Voltage</h3>
          </div>
          <span id="preUnit">{currentVoltage} V</span>
        </div>

        <div className="cardInner cardTwo">
          <div className="cardData">
            <TbCircuitVoltmeter className="bicon" />
            <h3>Predicted Voltage</h3>
          </div>
          <span id="currUnit">{forcastVoltage} V</span>
        </div>
      </div>

      <div className="historicalCharts">
        <h3>Historical Charts</h3>
        <div className="charts">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              width={500}
              height={300}
              data={historicalChartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="ForcastVoltage"
                stroke="#8884d8"
                activeDot={{ r: 8 }}
              />
              <Line type="monotone" dataKey="CurrentVoltage" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>

          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              width={500}
              height={300}
              data={historicalChartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar
                dataKey="ForcastVoltage"
                fill="#8884d8"
                activeBar={<Rectangle fill="pink" stroke="blue" />}
              />
              <Bar
                dataKey="CurrentVoltage"
                fill="#82ca9d"
                activeBar={<Rectangle fill="gold" stroke="purple" />}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
