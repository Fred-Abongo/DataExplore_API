import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

const ChartVisualization = () => {
    const [chartType, setChartType] = useState('line');
    const [chartData, setChartData] = useState([]);
    const [layout, setLayout] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchChartData = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.post('/api/visualize', { chart_type: chartType });
            const { data, layout } = response.data;
            setChartData(data);
            setLayout(layout);
        } catch (err) {
            setError('Error fetching chart data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchChartData();
    }, [chartType]);

    return (
        <div>
            <h2>Visualization Interface</h2>
            <label>
                Select Chart Type:
                <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
                    <option value="line">Line Chart</option>
                    <option value="bar">Bar Chart</option>
                    <option value="scatter">Scatter Plot</option>
                    <option value="pie">Pie Chart</option>
                </select>
            </label>
            {loading && <p>Loading chart...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {!loading && chartData.length > 0 && (
                <Plot data={chartData} layout={layout} style={{ width: "100%", height: "400px" }} />
            )}
        </div>
    );
};

export default ChartVisualization;
