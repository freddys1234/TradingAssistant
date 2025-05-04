
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function App() {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetch('https://your-api-url.com/chart-data/1')  // replace with actual backend route
      .then(res => res.json())
      .then(data => setChartData(data));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>📊 Trading Performance</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="price" stroke="#8884d8" name="Price" />
          <Line type="monotone" dataKey="equity" stroke="#82ca9d" name="Equity" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
