import React, { useState } from 'react';
import axios from 'axios';

const DataFilter = () => {
    const [filters, setFilters] = useState({ startDate: '', endDate: '' });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [filteredData, setFilteredData] = useState([]);

    const handleFilterChange = (e) => {
        setFilters({ ...filters, [e.target.name]: e.target.value });
    };

    const applyFilters = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.post('/api/filter', filters);
            setFilteredData(response.data);
        } catch (err) {
            setError('Error applying filters');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Filter Data</h2>
            <label>
                Start Date:
                <input
                    type="date"
                    name="startDate"
                    value={filters.startDate}
                    onChange={handleFilterChange}
                />
            </label>
            <label>
                End Date:
                <input
                    type="date"
                    name="endDate"
                    value={filters.endDate}
                    onChange={handleFilterChange}
                />
            </label>
            <button onClick={applyFilters} disabled={loading}>
                {loading ? 'Applying filters...' : 'Apply Filters'}
            </button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div>
                {/* Render the filtered data */}
                {filteredData.length > 0 && (
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredData.map((item) => (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    <td>{item.name}</td>
                                    <td>{item.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default DataFilter;
